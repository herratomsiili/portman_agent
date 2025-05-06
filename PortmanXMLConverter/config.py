"""
Configuration settings for the PortmanXMLConverter package.
This is a fallback configuration for command-line usage.
"""

import os

# Azure Storage configuration
AZURE_STORAGE_CONFIG = {
    "connection_string": os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
    "container_name": os.environ.get("AZURE_STORAGE_CONTAINER_NAME", "xml-documents")
}

# XML schema configuration
XML_SCHEMA_CONFIG = {
    "ATA": {
        "schema_path": "schemas/ATA/",
        "root_schema": "ATA_Envelope_1p0.xsd"
    },
    "NOA": {
        "schema_path": "schemas/NOA/",
        "root_schema": "NOA_Envelope_1p0.xsd"
    },
    "VID": {
        "schema_path": "schemas/VID/",
        "root_schema": "VID_Envelope_1p0.xsd"
    }
} 