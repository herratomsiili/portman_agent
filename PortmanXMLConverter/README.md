# EMSWe XML Converter for Portman Agent

A Python-based converter for transforming Portman agent data format and EMSWe-compliant XML documents.  

### Current implemented EMSWe-compliant XML documents:  
- ATA (Notification of actual arrival)

## Overview

This converter provides functionality to:
- Validate EMSWe-compliant XML documents against XSD schemas
- Parse EMSWe XML documents and extract structured data
- Transform between Portman agent JSON format and EMSWe-compliant XML
- Support bidirectional conversion with data preservation

The implementation complies with the European Maritime Single Window environment (EMSWe) standards as defined in the [EMSWe Message Implementation Guide](https://emsa.europa.eu/emswe-mig/).

## Installation

### Requirements

- Python 3.8 or higher
- lxml library

### Setup
Install dependencies:
```bash
pip install -r portman_agent/PortmanXMLConverter/src/requirements.txt
```

## Usage

### Command-line Interface

The converter provides a command-line interface with the following commands:

#### Validate an XML file

```bash
python3 main.py validate --xml-file /path/to/file.xml
```

#### Convert EMSWe XML to Portman JSON

```bash
python3 main.py from-emswe --xml-file /path/to/file.xml --output-file portman_data.json
```

#### Convert Portman JSON to EMSWe XML

```bash
python3 main.py to-emswe --json-file /path/to/data.json --output-file emswe_output.xml
```

### Using as a Library

You can also use the converter as a Python library in your own code:

```python
from src.converter import EMSWeConverter

# Initialize the converter
converter = EMSWeConverter(formality_type="ATA")

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

## Project Structure

- `src/` - Source code directory
    - `__init__.py` - Package initialization
    - `config.py` - Configuration settings
    - `validator.py` - XML validation module
    - `parser.py` - XML parsing module
    - `transformer.py` - Data transformation module
    - `converter.py` - Main converter module
- `main.py` - Command-line interface
- `test_*.py` - Unit tests
- `validation_tests.py` - Comprehensive validation tests

## Data Format

### EMSWe XML Format

The EMSWe XML format follows the structure defined in the EMSWe Message Implementation Guide, with an Envelope containing MAI (Main message header) and ATA (Notification of actual arrival) elements.

Example:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Envelope xmlns:mai="urn:un:unece:uncefact:data:standard:MAI:MMTPlus"
    xmlns:ata="urn:un:unece:uncefact:data:standard:ATA:MMTPlus"
    xmlns:qdt="urn:un:unece:uncefact:data:Standard:QualifiedDataType:30"
    xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:30"
    xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">
  <mai:MAI>
    <!-- Main message header information -->
  </mai:MAI>
  <ata:ATA>
    <!-- Notification of actual arrival information -->
  </ata:ATA>
</Envelope>
```

## Testing

### Running Unit Tests

```bash
python3 -m pytest -v
```

### Running Validation Tests

```bash
python3 validation_tests.py
```

You can also run specific validation tests:

```bash
python3 validation_tests.py --test validate
python3 validation_tests.py --test from-emswe
python3 validation_tests.py --test to-emswe
python3 validation_tests.py --test round-trip
python3 validation_tests.py --test edge-cases
```

## Integration with Portman Agent

This converter is designed to integrate with the Portman Agent project, which tracks vessel port calls. The converter enables the Portman Agent to communicate with Maritime National Single Window (MNSW) systems using EMSWe-compliant XML messages.

To integrate with the Portman Agent:

1. Import the converter module in your Portman Agent code
2. Use the converter to transform between Portman data format and EMSWe XML
3. Send the EMSWe-compliant XML to the MNSW system

## License

[Specify license information]

## References

- [EMSWe Message Implementation Guide](https://emsa.europa.eu/emswe-mig/)
- [European Maritime Single Window environment (EMSWe) Regulation (EU) 2019/1239](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R1239)
