"""
Test module for the complete EMSWe converter solution.
"""

import os
import json
import pytest
import tempfile
from PortmanXMLConverter.src.converter import EMSWeConverter

# Test data paths
EXAMPLE_XML_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "PortmanXMLConverter",
    "xml_templates",
    "ATA_Envelope.xml"
)

def test_converter_initialization():
    """Test that the converter initializes correctly."""
    converter = EMSWeConverter(formality_type="ATA")
    assert converter is not None
    assert converter.formality_type == "ATA"
    assert converter.validator is not None
    assert converter.parser is not None
    assert converter.transformer is not None

def test_validate_xml():
    """Test XML validation functionality."""
    converter = EMSWeConverter(formality_type="ATA")
    # Skip validation if template file doesn't exist or is empty
    if not os.path.exists(EXAMPLE_XML_PATH) or os.path.getsize(EXAMPLE_XML_PATH) == 0:
        pytest.skip(f"XML template file not found or empty: {EXAMPLE_XML_PATH}")
    is_valid, message = converter.validate_xml(EXAMPLE_XML_PATH)
    assert is_valid
    assert "successful" in message

def test_convert_from_emswe():
    """Test conversion from EMSWe XML to Portman data."""
    converter = EMSWeConverter(formality_type="ATA")
    # Skip test if template file doesn't exist or is empty
    if not os.path.exists(EXAMPLE_XML_PATH) or os.path.getsize(EXAMPLE_XML_PATH) == 0:
        pytest.skip(f"XML template file not found or empty: {EXAMPLE_XML_PATH}")
    success, result = converter.convert_from_emswe(EXAMPLE_XML_PATH)

    assert success
    assert isinstance(result, dict)
    assert "document_type" in result
    assert result["document_type"] == "ATA"
    assert "document_id" in result
    assert result["document_id"] == "MSGID1617779134129"
    assert "arrival_datetime" in result
    assert result["arrival_datetime"] == "2024-05-25T13:25:00.000+00:00"

def test_convert_to_emswe():
    """Test conversion from Portman data to EMSWe XML."""
    # Create sample Portman data
    portman_data = {
        "document_id": "MSGID_TEST_123",
        "declaration_id": "DECL-TEST-001",
        "timestamp": "2024-03-26T10:00:00Z",
        "call_id": "TEST-20240326-001",
        "remarks": "Test remarks",
        "arrival_datetime": "2024-03-26T09:30:00Z",
        "location": "Test Terminal",
        "call_datetime": "2024-03-26T09:30:00Z",
        "anchorage_indicator": "0",
        "declarant": {
            "id": "TEST123456789",
            "name": "Test Shipping Ltd.",
            "role_code": "AG",
            "contact": {
                "name": "Test Person",
                "phone": "123-456-7890",
                "email": "test@example.com"
            },
            "address": {
                "postcode": "12345",
                "street": "Test Street",
                "city": "Test City",
                "country": "IT",
                "building": "123"
            }
        }
    }

    # Create temporary file for output
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Convert to EMSWe XML
        converter = EMSWeConverter(formality_type="ATA")
        success, result = converter.convert_to_emswe(portman_data, os.path.basename(temp_path))

        assert success
        assert os.path.exists(result)

        # Validate the generated XML
        is_valid, message = converter.validate_xml(result)
        assert is_valid
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_round_trip_conversion():
    """Test round-trip conversion (EMSWe -> Portman -> EMSWe)."""
    converter = EMSWeConverter(formality_type="ATA")
    
    # Skip test if template file doesn't exist or is empty
    if not os.path.exists(EXAMPLE_XML_PATH) or os.path.getsize(EXAMPLE_XML_PATH) == 0:
        pytest.skip(f"XML template file not found or empty: {EXAMPLE_XML_PATH}")

    # First convert from EMSWe to Portman
    success1, portman_data = converter.convert_from_emswe(EXAMPLE_XML_PATH)
    assert success1

    # Then convert back to EMSWe
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        success2, xml_path = converter.convert_to_emswe(portman_data, os.path.basename(temp_path))
        assert success2
        assert os.path.exists(xml_path)

        # Validate the generated XML
        is_valid, message = converter.validate_xml(xml_path)
        assert is_valid

        # Convert the generated XML back to Portman
        success3, portman_data2 = converter.convert_from_emswe(xml_path)
        assert success3

        # Check that key fields are preserved
        assert portman_data["document_id"] == portman_data2["document_id"]
        assert portman_data["document_type"] == portman_data2["document_type"]
        assert portman_data["arrival_datetime"] == portman_data2["arrival_datetime"]
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    # Run tests manually
    test_converter_initialization()
    test_validate_xml()
    test_convert_from_emswe()
    test_convert_to_emswe()
    test_round_trip_conversion()
    print("All converter tests passed!")
