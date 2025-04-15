"""
Main script for the EMSWe XML Converter for Portman Agent.

This script provides a command-line interface for converting between
Portman agent data and EMSWe-compliant XML documents.
"""

import os
import sys
import json
import argparse
import logging
import datetime
from typing import Dict, Any

from PortmanXMLConverter.src.converter import EMSWeConverter
from PortmanXMLConverter.src.digitraffic_adapter import adapt_digitraffic_to_portman
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PortmanXMLConverter')

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="EMSWe XML Converter for Portman Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate an XML file
  python3 main.py validate --xml-file /path/to/file.xml

  # Convert EMSWe XML to Portman JSON
  python3 main.py from-emswe --xml-file /path/to/file.xml --output-file portman_data.json

  # Convert Portman JSON to EMSWe XML
  python3 main.py to-emswe --json-file /path/to/data.json --output-file emswe_output.xml

  # Convert Digitraffic port call data to EMSWe XML
  python3 main.py from-digitraffic --json-file /path/to/portcall.json --output-file emswe_output.xml
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate an EMSWe XML file")
    validate_parser.add_argument("--xml-file", required=True, help="Path to the XML file to validate")
    validate_parser.add_argument("--formality-type", default="ATA", help="Formality type (default: ATA)")

    # From EMSWe command
    from_emswe_parser = subparsers.add_parser("from-emswe", help="Convert EMSWe XML to Portman JSON")
    from_emswe_parser.add_argument("--xml-file", required=True, help="Path to the EMSWe XML file")
    from_emswe_parser.add_argument("--output-file", help="Path to save the output JSON file (default: stdout)")
    from_emswe_parser.add_argument("--formality-type", default="ATA", help="Formality type (default: ATA)")

    # To EMSWe command
    to_emswe_parser = subparsers.add_parser("to-emswe", help="Convert Portman JSON to EMSWe XML")
    to_emswe_parser.add_argument("--json-file", required=True, help="Path to the Portman JSON file")
    to_emswe_parser.add_argument("--output-file", help="Path to save the output XML file (default: stdout)")
    to_emswe_parser.add_argument("--formality-type", default="ATA", help="Formality type (default: ATA)")

    # From Digitraffic command (new)
    from_digitraffic_parser = subparsers.add_parser("from-digitraffic",
                                                    help="Convert Digitraffic port call data to EMSWe XML")
    from_digitraffic_parser.add_argument("--json-file", required=True, help="Path to the Digitraffic JSON file")
    from_digitraffic_parser.add_argument("--output-file", help="Path to save the output XML file (default: stdout)")
    from_digitraffic_parser.add_argument("--formality-type", default="ATA", help="Formality type (default: ATA)")
    from_digitraffic_parser.add_argument("--batch", action="store_true",
                                         help="Process multiple port calls in batch mode")

    return parser.parse_args()


def validate_xml(args):
    """Validate an EMSWe XML file."""
    converter = EMSWeConverter(formality_type=args.formality_type)
    is_valid, message = converter.validate_xml(args.xml_file)

    if is_valid:
        logger.info(f"XML file is valid: {args.xml_file}")
        print(f"XML file is valid: {args.xml_file}")
        return 0
    else:
        logger.error(f"XML file is invalid: {args.xml_file}")
        print(f"XML file is invalid: {args.xml_file}")
        print(f"Errors: {message}")
        return 1


def convert_from_emswe(args):
    """Convert EMSWe XML to Portman JSON."""
    converter = EMSWeConverter(formality_type=args.formality_type)
    success, result = converter.convert_from_emswe(args.xml_file)

    if not success:
        logger.error(f"Conversion failed: {result}")
        print(f"Conversion failed: {result}")
        return 1

    # Convert to JSON
    json_data = json.dumps(result, indent=2)

    # Output to file or stdout
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(json_data)
        logger.info(f"Portman data saved to: {args.output_file}")
        print(f"Portman data saved to: {args.output_file}")
    else:
        print(json_data)

    return 0


def convert_to_emswe(args):
    """Convert Portman JSON to EMSWe XML."""
    # Read JSON file
    try:
        with open(args.json_file, 'r') as f:
            portman_data = json.load(f)
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        print(f"Error reading JSON file: {str(e)}")
        return 1

    # Convert to EMSWe XML
    converter = EMSWeConverter(formality_type=args.formality_type)
    success, result = converter.convert_to_emswe(portman_data, args.output_file)

    if not success:
        logger.error(f"Conversion failed: {result}")
        print(f"Conversion failed: {result}")
        return 1

    # Output to file or stdout
    if args.output_file:
        logger.info(f"EMSWe XML saved to: {result}")
        print(f"EMSWe XML saved to: {result}")
    else:
        print(result)

    return 0


def convert_from_digitraffic(args):
    """Convert Digitraffic port call data to EMSWe XML."""
    # Read JSON file
    try:
        with open(args.json_file, 'r') as f:
            digitraffic_data = json.load(f)
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        print(f"Error reading JSON file: {str(e)}")
        return 1

    # Initialize converter
    converter = EMSWeConverter(formality_type=args.formality_type)

    # Check if we're processing multiple port calls
    if args.batch:
        # Determine if it's a list of port calls or a structure with a portCalls field
        if isinstance(digitraffic_data, dict) and "portCalls" in digitraffic_data:
            port_calls = digitraffic_data["portCalls"]
        elif isinstance(digitraffic_data, list):
            port_calls = digitraffic_data
        else:
            port_calls = [digitraffic_data]  # Treat as single port call

        logger.info(f"Processing {len(port_calls)} port calls in batch mode")

        # Create output directory if needed
        if args.output_file:
            # Normalize path to handle both forward and backslashes
            norm_path = os.path.normpath(args.output_file)
            output_dir = os.path.dirname(norm_path)
            if output_dir:  # If there's a directory part in the path
                os.makedirs(output_dir, exist_ok=True)
                print(f"Created output directory: {output_dir}")
        else:
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created default output directory: {output_dir}")

        # Process each port call
        success_count = 0
        for i, port_call in enumerate(port_calls):
            # Adapt Digitraffic data to Portman format
            portman_data = adapt_digitraffic_to_portman(port_call)

            # Generate output filename
            if args.output_file:
                norm_path = os.path.normpath(args.output_file)
                base_name = os.path.splitext(norm_path)[0]
                ext = os.path.splitext(norm_path)[1] or ".xml"
                output_file = f"{base_name}_{i + 1}{ext}"
                print(f"base_name: {base_name}")
                print(f"ext: {ext}")
                print(f"output_file: {output_file}")
            else:
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"portcall_{i + 1}.xml")

            # Convert to EMSWe XML
            success, result = converter.convert_to_emswe(portman_data, output_file)

            if success:
                logger.info(f"Port call {i + 1} converted successfully: {result}")
                print(f"Port call {i + 1} converted successfully: {result}")
                success_count += 1
            else:
                logger.error(f"Port call {i + 1} conversion failed: {result}")
                print(f"Port call {i + 1} conversion failed: {result}")

        logger.info(
            f"Batch processing complete. {success_count} of {len(port_calls)} port calls converted successfully.")
        print(f"Batch processing complete. {success_count} of {len(port_calls)} port calls converted successfully.")

        return 0 if success_count > 0 else 1
    else:
        # Process single port call (either the whole file or the first port call)
        if isinstance(digitraffic_data, dict) and "portCalls" in digitraffic_data and digitraffic_data["portCalls"]:
            port_call = digitraffic_data["portCalls"][0]
            logger.info(f"Processing first port call from a list of {len(digitraffic_data['portCalls'])} port calls")
            print(f"Processing first port call from a list of {len(digitraffic_data['portCalls'])} port calls")
        else:
            port_call = digitraffic_data

        # Adapt Digitraffic data to Portman format
        portman_data = adapt_digitraffic_to_portman(port_call)

        # Ensure output directory exists if specified
        if args.output_file:
            norm_path = os.path.normpath(args.output_file)
            output_dir = os.path.dirname(norm_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                print(f"Created output directory: {output_dir}")

        # Convert to EMSWe XML
        success, result = converter.convert_to_emswe(portman_data, args.output_file)

        if not success:
            logger.error(f"Conversion failed: {result}")
            print(f"Conversion failed: {result}")
            return 1

        # Output to file or stdout
        if args.output_file:
            logger.info(f"EMSWe XML saved to: {result}")
            print(f"EMSWe XML saved to: {result}")
        else:
            print(result)

        return 0
    
def convert_from_portcall_data(portcall_data, xml_type=None):
    """Convert Digitraffic port call data to EMSWe XML."""
    # Read JSON file
    converter = EMSWeConverter(formality_type=xml_type)

    # Process single port call (either the whole file or the first port call)
    if isinstance(portcall_data, dict) and "portCalls" in portcall_data and portcall_data["portCalls"]:
        port_call = portcall_data["portCalls"][0]
        logger.info(f"Processing first port call from a list of {len(portcall_data['portCalls'])} port calls")
        print(f"Processing first port call from a list of {len(portcall_data['portCalls'])} port calls")
    else:
        port_call = portcall_data

    # Adapt Digitraffic data to Portman format
    portman_data = adapt_digitraffic_to_portman(port_call)

    # Generate a unique filename
    port_call_id = portcall_data.get('portCallId')
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"ATA_{port_call_id}_{timestamp}.xml"

    # Convert to EMSWe XML
    success, result = converter.convert_to_emswe(portman_data)

    if not success:
        logger.error(f"Conversion failed: {result}")
        print(f"Conversion failed: {result}")
        return None

    # Get storage connection string from app settings
    connection_string = AZURE_STORAGE_CONFIG["connection_string"]
    container_name = AZURE_STORAGE_CONFIG["container_name"]
    
    if (not connection_string or not container_name):
        logger.info("Storage connection string or container name not found")
        #logger.info(f"Generated XML file:\n{result}")
        #print("Storage connection string or container name not found")
        logger.info(result)
        #print(f"Generated XML file:\n{result}")
        return None

    # Connect to blob storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    # Create container if it doesn't exist
    if not container_client.exists():
        container_client.create_container()

    #if not container_client.exists():
    #    # Use PublicAccess.Blob to allow anonymous access to blobs but not container listings
    #    from azure.storage.blob import PublicAccess
    #    container_client.create_container(public_access=PublicAccess.Blob)
    #    logger.info(f"Created container '{container_name}' with blob-level public access")
    
    # Upload XML to Blob Storage
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(result, overwrite=True, content_type="application/xml")
    
    # Return success response with the blob URL
    blob_url = blob_client.url

    return blob_url

def xml_converter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Portman XML converter function processing a request')
    try:
        req_body = req.get_json()
            
        if not req_body or 'portcall_data' not in req_body:
            return func.HttpResponse(
                "Please pass portcall_data in the request body",
                status_code=400
            )
        
        portcall_data = req_body.get('portcall_data')
        formality_type = req_body.get('formality_type')
        blob_url = convert_from_portcall_data(portcall_data, formality_type)

        # The condition is reversed - when blob_url is None, (not blob_url) is True
        # So we're correctly entering this block when blob_url is None
        if blob_url is None:
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "XML generated but not stored"}),
                mimetype="application/json",
                status_code=200
            )
        # This else block only executes when blob_url is not None
        else:
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "XML generated and stored successfully", "url": blob_url}),
                mimetype="application/json",
                status_code=200
            )
    except Exception as e:
        logging.error(f"Error processing arrival data: {str(e)}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            mimetype="application/json", 
            status_code=500
        )
