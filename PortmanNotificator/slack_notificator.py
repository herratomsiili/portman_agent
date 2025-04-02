import logging
import os
import json
import requests
import azure.functions as func
import xml.etree.ElementTree as ET

def blob_trigger(blob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob: {blob.name}")
    
    if not os.environ.get("SLACK_WEBHOOK_ENABLED"):
        logging.info("Slack webhook is disabled, skipping notification")
        return

    channel = os.environ.get("SLACK_CHANNEL")
    try:
        # Read the blob content
        blob_content = blob.read().decode('utf-8')
        
        # Parse the XML to extract port call ID and ATA
        port_call_id, ata = extract_info_from_xml(blob_content)
        
        # Send notification to Slack with XML content
        send_slack_notification(blob.name, port_call_id, ata, blob_content, channel)
        
        logging.info(f"Successfully processed and notified about arrival {port_call_id}")
    
    except Exception as e:
        logging.error(f"Error processing blob {blob.name}: {str(e)}")
        # Send error notification to Slack
        send_slack_error(blob.name, str(e), channel)

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

def send_slack_notification(blob_name, port_call_id, ata, xml_content, channel):
    """Send a notification to Slack about the new arrival XML."""
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    
    # Format the XML content nicely (limit to 2500 characters to avoid message size limits)
    formatted_xml = format_xml_for_display(xml_content, max_length=2500)
    
    logging.info(f"Sending Slack notification with webhook url {webhook_url} for {blob_name} with port_call_id {port_call_id} and ata {ata}")

    # Create a message for Slack with XML content
    message = {
        "channel": channel,
        "username": "Portman Bot",
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
                        "text": f"File: `{blob_name}`"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*ATA xml-message:*\n```{formatted_xml}\n```"
                }
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

def send_slack_error(blob_name, error_message, channel):
    """Send an error notification to Slack."""
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    
    message = {
        "channel": channel,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"⚠️ *Error processing arrival XML file: `{blob_name}`*\n\nError message:\n```{error_message}```"
                }
            }
        ]
    }
    
    # Send the error message to Slack
    requests.post(
        webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"}
    )