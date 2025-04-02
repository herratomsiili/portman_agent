"""
XML validation module for EMSWe-compliant XML documents.
"""

import os
import logging
from lxml import etree
from typing import Dict, List, Optional, Tuple, Union

from .converter_config import SCHEMA_PATHS, NAMESPACES

logger = logging.getLogger(__name__)

class XMLValidator:
    """
    Validates XML documents against EMSWe XSD schemas.
    """

    def __init__(self, formality_type: str = "ATA"):
        """
        Initialize the validator for a specific formality type.

        Args:
            formality_type: The type of formality (e.g., "ATA", "NOA")
        """
        self.formality_type = formality_type
        self.schema_paths = SCHEMA_PATHS.get(formality_type, {})
        self.schema = None
        self._load_schema()

    # Updated _load_schema method
    def _load_schema(self) -> None:
        """
        Load the XSD schema for validation.
        """
        if not self.schema_paths:
            raise ValueError(f"No schema paths defined for formality type: {self.formality_type}")

        try:
            main_schema_path = self.schema_paths.get("main")
            if not main_schema_path or not os.path.exists(main_schema_path):
                # Add debug information
                print(f"DEBUG: Schema file not found at: {main_schema_path}")
                print(f"DEBUG: Current working directory: {os.getcwd()}")
                print(
                    f"DEBUG: Files in schemas directory: {os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schemas')) if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schemas')) else 'schemas directory not found'}")

                raise FileNotFoundError(f"Main schema file not found: {main_schema_path}")

            # Create XML parser with schema resolution
            parser = etree.XMLParser(resolve_entities=False)

            # Load and parse the schema
            schema_doc = etree.parse(main_schema_path, parser)
            self.schema = etree.XMLSchema(schema_doc)

            logger.info(f"Successfully loaded schema for {self.formality_type}")
        except Exception as e:
            logger.error(f"Failed to load schema: {str(e)}")
            raise

    def validate(self, xml_content: Union[str, bytes, etree._Element]) -> Tuple[bool, List[str]]:
        """
        Validate XML content against the loaded schema.

        Args:
            xml_content: XML content as string, bytes, or lxml Element

        Returns:
            Tuple containing (is_valid, error_messages)
        """
        if self.schema is None:
            raise ValueError("Schema not loaded. Call _load_schema() first.")

        errors = []

        try:
            # Parse XML if it's a string or bytes
            if isinstance(xml_content, (str, bytes)):
                parser = etree.XMLParser(remove_blank_text=True)
                xml_doc = etree.fromstring(xml_content, parser)
            else:
                xml_doc = xml_content

            # Validate against schema
            is_valid = self.schema.validate(xml_doc)

            # Collect error messages if validation failed
            if not is_valid:
                for error in self.schema.error_log:
                    errors.append(f"Line {error.line}, Column {error.column}: {error.message}")

            return is_valid, errors

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return False, errors

    def validate_file(self, xml_file_path: str) -> Tuple[bool, List[str]]:
        """
        Validate an XML file against the loaded schema.

        Args:
            xml_file_path: Path to the XML file

        Returns:
            Tuple containing (is_valid, error_messages)
        """
        if not os.path.exists(xml_file_path):
            return False, [f"File not found: {xml_file_path}"]

        try:
            parser = etree.XMLParser(remove_blank_text=True)
            xml_doc = etree.parse(xml_file_path, parser)
            return self.validate(xml_doc)
        except Exception as e:
            return False, [f"Error parsing XML file: {str(e)}"]
