import logging
import os
import json
import requests
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta, UTC
import xml.etree.ElementTree as ET

def blob_trigger(blob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob: {blob.name}")

    if not os.environ.get("SLACK_WEBHOOK_ENABLED"):
        logging.info("Slack webhook is disabled, skipping notification")
        return

    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    channel = os.environ.get("SLACK_CHANNEL")
    username = "Portman Bot"
    try:
        # Read the blob content
        blob_content = blob.read().decode('utf-8')

        # Parse the XML to extract port call ID and ATA
        port_call_id, ata = extract_info_from_xml(blob_content)

        # Generate a URL with SAS token to access the blob directly
        blob_url = generate_blob_storage_link(blob.name)

        # Send notification to Slack with XML content
        send_slack_notification(webhook_url, blob.name, port_call_id, ata, blob_content, channel, username, blob_url)

        logging.info(f"Successfully processed and notified about arrival {port_call_id}")

    except Exception as e:
        logging.error(f"Error processing blob {blob.name}: {str(e)}")
        # Send error notification to Slack
        send_slack_error(webhook_url, blob.name, str(e), channel, username)

def extract_info_from_xml(xml_content):
    """Extract portCallId and ATA from the XML."""
    try:
        # Register namespaces
        namespaces = {
            'mai': 'urn:un:unece:uncefact:data:standard:MAI:MMTPlus',
            'ata': 'urn:un:unece:uncefact:data:standard:ATA:MMTPlus',
            'ram': 'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:30',
            'qdt': 'urn:un:unece:uncefact:data:Standard:QualifiedDataType:30'
        }
        
        root = ET.fromstring(xml_content)
        
        # Extract port call ID from MAI part
        port_call_id_element = root.find('.//mai:SpecifiedLogisticsTransportMovement/ram:CallTransportEvent/ram:ID', namespaces)
        port_call_id = port_call_id_element.text if port_call_id_element is not None else "Unknown"
        
        # Extract ATA from the ATA part - last timestamp in the file
        ata_elements = root.findall('.//qdt:DateTimeString', namespaces)
        ata = ata_elements[-1].text if ata_elements and len(ata_elements) > 0 else "Unknown"
        
        return port_call_id, ata
    
    except Exception as e:
        logging.error(f"Error parsing XML: {str(e)}")
        return "Unknown", "Unknown"

def send_slack_notification(webhook_url, blob_name, port_call_id, ata, xml_content, channel, username, blob_url):
    """Send a notification to Slack about the new arrival XML."""
    # Format the XML content nicely (limit to 2500 characters to avoid message size limits)
    formatted_xml = format_xml_for_display(xml_content, max_length=2500)
    
    logging.info(f"Sending Slack notification with webhook url {webhook_url} for {blob_name} with port_call_id {port_call_id} and ata {ata}")

    # Create a message for Slack with XML content
    message = {
        "channel": channel,
        "username": username,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚢 *New port arrival detected 🚢*\n*VisitID:* {port_call_id}\n*ATA:* {ata}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"File: `{blob_name}`" + (f" | <{blob_url}| Download>" if blob_url else "")
                    }
                ]
            }
        ]
    }

    # Only add channel if it was provided
    if channel:
        message["channel"] = channel
    
    # Send the message to Slack
    response = requests.post(
        webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        logging.error(f"Error sending to Slack: {response.status_code}, {response.text}")

def generate_blob_storage_link(blob_name):
    """Generate a URL with SAS token to access the blob directly."""
    try:
        # Get storage account connection string
        connection_string = os.environ.get("AzureWebJobsStorage")
        if not connection_string:
            logging.warning("AzureWebJobsStorage not set, cannot generate direct link")
            return ""

        container_name = blob_name.split('/')[0]
        blob_path = '/'.join(blob_name.split('/')[1:])

        # Create the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get account name from connection string
        account_name = blob_service_client.account_name

        # Get account key (needed for SAS token generation)
        account_key = connection_string.split('AccountKey=')[1].split(';')[0]

        # Generate SAS token with read permission that expires in 7 days
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_path,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(UTC) + timedelta(days=7)
        )

        # Create the URL with SAS token
        blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_path}?{sas_token}"

        return blob_url
    except Exception as e:
        logging.error(f"Error generating blob storage link: {e}")
        return ""

def format_xml_for_display(xml_content, max_length=2500):
    """Format XML content for better display in Slack message and limit to max_length."""
    try:
        # Try to pretty-print the XML
        from xml.dom import minidom
        parsed_xml = minidom.parseString(xml_content)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")
        
        # Remove empty lines that minidom sometimes adds
        pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])
        
        # If XML is too long, truncate it
        if len(pretty_xml) > max_length:
            return pretty_xml[:max_length] + "\n... (truncated)"
        return pretty_xml
    except Exception as e:
        logging.warning(f"Couldn't pretty-print XML: {e}")
        # If pretty printing fails, just truncate the raw XML
        if len(xml_content) > max_length:
            return xml_content[:max_length] + "\n... (truncated)"
        return xml_content

def send_slack_error(webhook_url, blob_name, error_message, channel, username):
    """Send an error notification to Slack."""

    # Generate a blob link even for errors
    blob_url = generate_blob_storage_link(blob_name)

    message = {
        "username": username,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"⚠️ *Error processing arrival XML file: `{blob_name}`*\n" + (f" | <{blob_url}| Download>" if blob_url else "") + "\n\nError message:\n```{error_message}```"
                }
            }
        ]
    }

    # Only add channel if it was provided
    if channel:
        message["channel"] = channel
    
    # Send the error message to Slack
    requests.post(
        webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"}
    )