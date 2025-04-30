"""
Configuration settings for the EMSWe XML converter.
"""
import os

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Paths to schema files
SCHEMA_PATHS = {
    "ATA": {
        "main": os.path.join(PROJECT_ROOT, "schemas", "ATA", "ATA_Envelope.xsd"),
        "ata": os.path.join(PROJECT_ROOT, "schemas", "ATA", "ATA_Envelope_ATA_MMTPluspD22B.xsd"),
        "mai": os.path.join(PROJECT_ROOT, "schemas", "ATA", "ATA_Envelope_MAI_MMTPluspD22B.xsd"),
        "qdt": os.path.join(PROJECT_ROOT, "schemas", "ATA", "ATA_Envelope_QualifiedDataType_30p0.xsd"),
        "ram": os.path.join(PROJECT_ROOT, "schemas", "ATA", "ATA_Envelope_ReusableAggregateBusinessInformationEntity_30p0.xsd"),
        "udt": os.path.join(PROJECT_ROOT, "schemas", "ATA", "ATA_Envelope_UnqualifiedDataType_100pD22B.xsd"),
    },
    "NOA": {
        "main": os.path.join(PROJECT_ROOT, "schemas", "NOA", "NOA_Envelope.xsd"),
        "noa": os.path.join(PROJECT_ROOT, "schemas", "NOA", "NOA_Envelope_NOA_MMTPluspD22B.xsd"),
        "mai": os.path.join(PROJECT_ROOT, "schemas", "NOA", "NOA_Envelope_MAI_MMTPluspD22B.xsd"),
        "qdt": os.path.join(PROJECT_ROOT, "schemas", "NOA", "NOA_Envelope_QualifiedDataType_30p0.xsd"),
        "ram": os.path.join(PROJECT_ROOT, "schemas", "NOA", "NOA_Envelope_ReusableAggregateBusinessInformationEntity_30p0.xsd"),
        "udt": os.path.join(PROJECT_ROOT, "schemas", "NOA", "NOA_Envelope_UnqualifiedDataType_100pD22B.xsd"),
    }
}

# XML namespaces used in EMSWe documents
NAMESPACES = {
    "mai": "urn:un:unece:uncefact:data:standard:MAI:MMTPlus",
    "ata": "urn:un:unece:uncefact:data:standard:ATA:MMTPlus",
    "noa": "urn:un:unece:uncefact:data:standard:NOA:MMTPlus",
    "qdt": "urn:un:unece:uncefact:data:Standard:QualifiedDataType:30",
    "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:30",
    "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
}

# Default output directory for generated files
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
