# EMSWe XML Converter for Portman Agent

A Python-based converter for transforming Portman agent data format and EMSWe-compliant XML documents.

## Overview

This converter provides functionality to:
- Validate EMSWe-compliant XML documents against XSD schemas
- Parse EMSWe XML documents and extract structured data
- Transform between Portman agent JSON format and EMSWe-compliant XML
- Support bidirectional conversion with data preservation

The implementation complies with the European Maritime Single Window environment (EMSWe) standards as defined in the [EMSWe Message Implementation Guide](https://emsa.europa.eu/emswe-mig/).

### Supported XML Types

The converter currently supports the following EMSWe-compliant XML documents:
- ATA (Notification of actual arrival)
- NOA (Notice of pre arrival)
- VID (Request for Visit ID)

Each document type follows the EMSWe Message Implementation Guide specifications.

## Usage

### Command-line Interface

The converter provides a command-line interface with the following commands:

#### Validate an XML file

```bash
python3 xml_converter.py validate --xml-file /path/to/file.xml --formality-type ATA|NOA|VID
```

#### Convert EMSWe XML to Portman JSON

```bash
python3 xml_converter.py from-emswe --xml-file /path/to/file.xml --output-file portman_data.json --formality-type ATA|NOA|VID
```

#### Convert Portman JSON to EMSWe XML

```bash
python3 xml_converter.py to-emswe --json-file /path/to/data.json --output-file emswe_output.xml --formality-type ATA|NOA|VID
```

#### Convert Digitraffic port call data to EMSWe XML

```bash
python3 xml_converter.py from-digitraffic --json-file /path/to/portcall.json --output-file emswe_output.xml --formality-type ATA|NOA|VID --batch
```

The `--batch` flag can be used to process multiple port calls in batch mode.

### Using as a Library

You can also use the converter as a Python library in your own code:

```python
from src.converter import EMSWeConverter

# Initialize the converter with desired formality type
converter = EMSWeConverter(formality_type="ATA")  # Or "NOA" or "VID"

# Validate an XML file
is_valid, message = converter.validate_xml("/path/to/file.xml")

# Convert from EMSWe XML to Portman data
success, portman_data = converter.convert_from_emswe("/path/to/file.xml")

# Convert from Portman data to EMSWe XML
portman_data = {
    "document_id": "MSGID_TEST_123",
    "declaration_id": "DECL-TEST-001",
    "timestamp": "2024-03-26T10:00:00Z",
    "arrival_datetime": "2024-03-26T09:30:00Z",
    "location": "Terminal B3",
    # ... other fields
}
success, result = converter.convert_to_emswe(portman_data, "output.xml")
```

## Data Format

### EMSWe XML Format

The EMSWe XML format follows the structure defined in the EMSWe Message Implementation Guide, with an Envelope containing:
- MAI (Main message header)
- Document specific element (ATA, NOA, or VID)

Example:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Envelope xmlns:mai="urn:un:unece:uncefact:data:standard:MAI:MMTPlus"
    xmlns:ata="urn:un:unece:uncefact:data:standard:ATA:MMTPlus"
    xmlns:noa="urn:un:unece:uncefact:data:standard:NOA:MMTPlus"
    xmlns:vid="urn:un:unece:uncefact:data:standard:VID:MMTPlus"
    xmlns:qdt="urn:un:unece:uncefact:data:Standard:QualifiedDataType:30"
    xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:30"
    xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">
  <mai:MAI>
    <!-- Main message header information -->
  </mai:MAI>
  <!-- One of the following based on formality type -->
  <ata:ATA>
    <!-- Notification of actual arrival information -->
  </ata:ATA>
  <!-- or -->
  <noa:NOA>
    <!-- Notice of arrival information -->
  </noa:NOA>
  <!-- or -->
  <vid:VID>
    <!-- Vessel Information Data -->
  </vid:VID>
</Envelope>
```

## References

- [EMSWe Message Implementation Guide](https://emsa.europa.eu/emswe-mig/)
- [European Maritime Single Window environment (EMSWe) Regulation (EU) 2019/1239](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R1239)
