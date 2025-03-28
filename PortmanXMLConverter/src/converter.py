"""
Main converter module for EMSWe-compliant XML conversion.
"""

import os
import logging
from typing import Dict, Any, Optional, Tuple, Union
from lxml import etree

from .converter_config import OUTPUT_DIR
from .validator import XMLValidator
from .parser import XMLParser
from .transformer import XMLTransformer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EMSWeConverter:
    """
    Main converter class for EMSWe-compliant XML.
    """

    def __init__(self, formality_type: str = "ATA"):
        """
        Initialize the EMSWe converter.

        Args:
            formality_type: Type of formality to handle (e.g., "ATA")
        """
        self.formality_type = formality_type
        self.validator = XMLValidator(formality_type)
        self.parser = XMLParser()
        self.transformer = XMLTransformer()

        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def validate_xml(self, xml_file_path: str) -> Tuple[bool, str]:
        """
        Validate an XML file against EMSWe schemas.

        Args:
            xml_file_path: Path to the XML file

        Returns:
            Tuple containing (is_valid, error_message)
        """
        is_valid, errors = self.validator.validate_file(xml_file_path)

        if not is_valid:
            error_message = "\n".join(errors)
            logger.error(f"XML validation failed: {error_message}")
            return False, error_message

        logger.info("XML validation successful")
        return True, "XML validation successful"

    def convert_to_emswe(self, portman_data: Dict[str, Any], output_filename: str = None) -> Tuple[bool, str]:
        """
        Convert Portman agent data to EMSWe-compliant XML.

        Args:
            portman_data: Dictionary containing Portman agent data
            output_filename: Name of the output file (optional)

        Returns:
            Tuple containing (success, output_path_or_error)
        """

        try:
            # Transform data to EMSWe XML
            xml_root = self.transformer.portman_to_emswe(portman_data, self.formality_type)

            if xml_root is None:
                return False, "Failed to transform data to EMSWe XML"

            # Validate the generated XML
            is_valid, errors = self.validator.validate(xml_root)

            if not is_valid:
                error_message = "\n".join(errors)
                logger.error(f"Generated XML validation failed: {error_message}")
                return False, error_message

            # Save to file if output filename is provided
            if output_filename:
                if not output_filename.endswith('.xml'):
                    output_filename += '.xml'

                output_path = self.transformer.save_xml(xml_root, output_filename)

                if not output_path:
                    return False, "Failed to save XML to file"

                return True, output_path

            # Return XML as string if no output filename
            xml_string = etree.tostring(xml_root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode("utf-8")
            return True, xml_string

        except Exception as e:
            logger.error(f"Error converting to EMSWe: {str(e)}")
            return False, f"Error: {str(e)}"

    def convert_from_emswe(self, xml_file_path: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
        """
        Convert EMSWe-compliant XML to Portman agent data.

        Args:
            xml_file_path: Path to the XML file

        Returns:
            Tuple containing (success, portman_data_or_error)
        """
        try:
            # Validate the XML first
            is_valid, errors = self.validator.validate_file(xml_file_path)

            if not is_valid:
                error_message = "\n".join(errors)
                logger.error(f"XML validation failed: {error_message}")
                return False, error_message

            # Parse the XML
            xml_root = self.parser.parse_file(xml_file_path)

            if xml_root is None:
                return False, "Failed to parse XML file"

            # Transform to Portman format
            portman_data = self.transformer.emswe_to_portman(xml_root)

            if not portman_data:
                return False, "Failed to transform XML to Portman data"

            return True, portman_data

        except Exception as e:
            logger.error(f"Error converting from EMSWe: {str(e)}")
            return False, f"Error: {str(e)}"
