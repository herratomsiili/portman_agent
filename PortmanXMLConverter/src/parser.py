"""
XML parser module for EMSWe-compliant XML documents.
"""

import os
import logging
from lxml import etree
from typing import Dict, Any, Optional, Union

from .converter_config import NAMESPACES

logger = logging.getLogger(__name__)

class XMLParser:
    """
    Parser for EMSWe-compliant XML documents.
    """

    def __init__(self):
        """
        Initialize the XML parser.
        """
        self.namespaces = NAMESPACES

    def parse_file(self, xml_file_path: str) -> Optional[etree._Element]:
        """
        Parse an XML file into an lxml Element.

        Args:
            xml_file_path: Path to the XML file

        Returns:
            Parsed XML as lxml Element or None if parsing fails
        """
        if not os.path.exists(xml_file_path):
            logger.error(f"File not found: {xml_file_path}")
            return None

        try:
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.parse(xml_file_path, parser).getroot()
        except Exception as e:
            logger.error(f"Error parsing XML file: {str(e)}")
            return None

    def parse_string(self, xml_content: Union[str, bytes]) -> Optional[etree._Element]:
        """
        Parse XML content from a string or bytes.

        Args:
            xml_content: XML content as string or bytes

        Returns:
            Parsed XML as lxml Element or None if parsing fails
        """
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.fromstring(xml_content, parser)
        except Exception as e:
            logger.error(f"Error parsing XML string: {str(e)}")
            return None

    def extract_data(self, xml_root: etree._Element) -> Dict[str, Any]:
        """
        Extract relevant data from an EMSWe XML document.

        Args:
            xml_root: Root element of the XML document

        Returns:
            Dictionary containing extracted data
        """
        result = {
            "document_type": None,
            "mai_data": {},
            "formality_data": {}
        }

        try:
            # Determine document type
            for child in xml_root:
                tag = etree.QName(child).localname
                if tag != "MAI":
                    result["document_type"] = tag
                    break

            # Extract MAI data
            mai_element = xml_root.find(".//mai:MAI", namespaces=self.namespaces)
            if mai_element is not None:
                result["mai_data"] = self._extract_mai_data(mai_element)

            # Extract formality-specific data (e.g., ATA)
            if result["document_type"]:
                formality_element = xml_root.find(f".//{result['document_type'].lower()}:{result['document_type']}",
                                                  namespaces=self.namespaces)
                if formality_element is not None:
                    result["formality_data"] = self._extract_formality_data(formality_element, result["document_type"])

            return result
        except Exception as e:
            logger.error(f"Error extracting data from XML: {str(e)}")
            return result

    def _extract_mai_data(self, mai_element: etree._Element) -> Dict[str, Any]:
        """
        Extract data from the MAI element.

        Args:
            mai_element: The MAI element

        Returns:
            Dictionary containing MAI data
        """
        mai_data = {}

        try:
            # Extract document ID
            doc_id = mai_element.find(".//ram:ID", namespaces=self.namespaces)
            if doc_id is not None:
                mai_data["document_id"] = doc_id.text

            # Extract document type code
            type_code = mai_element.find(".//ram:TypeCode", namespaces=self.namespaces)
            if type_code is not None:
                mai_data["type_code"] = type_code.text

            # Extract purpose code
            purpose_code = mai_element.find(".//ram:PurposeCode", namespaces=self.namespaces)
            if purpose_code is not None:
                mai_data["purpose_code"] = purpose_code.text

            # Extract version ID
            version_id = mai_element.find(".//ram:VersionID", namespaces=self.namespaces)
            if version_id is not None:
                mai_data["version_id"] = version_id.text

            # Extract timestamp
            timestamp = mai_element.find(".//udt:DateTimeString", namespaces=self.namespaces)
            if timestamp is not None:
                mai_data["timestamp"] = timestamp.text

            # Extract declaration ID
            decl_id = mai_element.find(".//mai:ExchangedDeclaration/ram:ID", namespaces=self.namespaces)
            if decl_id is not None:
                mai_data["declaration_id"] = decl_id.text

            # Extract declarant info
            declarant = mai_element.find(".//ram:DeclarantTradeParty", namespaces=self.namespaces)
            if declarant is not None:
                mai_data["declarant"] = {
                    "id": self._get_element_text(declarant, ".//ram:ID"),
                    "name": self._get_element_text(declarant, ".//ram:Name"),
                    "role_code": self._get_element_text(declarant, ".//ram:RoleCode"),
                }

                # Extract contact info
                contact = declarant.find(".//ram:DefinedTradeContact", namespaces=self.namespaces)
                if contact is not None:
                    mai_data["declarant"]["contact"] = {
                        "name": self._get_element_text(contact, ".//ram:PersonName"),
                        "phone": self._get_element_text(contact, ".//ram:TelephoneUniversalCommunication/ram:CompleteNumber"),
                        "email": self._get_element_text(contact, ".//ram:EmailURIUniversalCommunication/ram:URIID"),
                    }

                # Extract address
                address = declarant.find(".//ram:PostalTradeAddress", namespaces=self.namespaces)
                if address is not None:
                    mai_data["declarant"]["address"] = {
                        "postcode": self._get_element_text(address, ".//ram:PostcodeCode"),
                        "street": self._get_element_text(address, ".//ram:StreetName"),
                        "city": self._get_element_text(address, ".//ram:CityName"),
                        "country": self._get_element_text(address, ".//ram:CountryID"),
                        "building": self._get_element_text(address, ".//ram:BuildingNumber"),
                    }

            # Extract call ID
            call_event = mai_element.find(".//mai:SpecifiedLogisticsTransportMovement/ram:CallTransportEvent/ram:ID",
                                          namespaces=self.namespaces)
            if call_event is not None:
                mai_data["call_id"] = call_event.text

            return mai_data
        except Exception as e:
            logger.error(f"Error extracting MAI data: {str(e)}")
            return mai_data

    def _extract_formality_data(self, formality_element: etree._Element, formality_type: str) -> Dict[str, Any]:
        """
        Extract data from a formality element (e.g., ATA).

        Args:
            formality_element: The formality element
            formality_type: Type of formality (e.g., "ATA")

        Returns:
            Dictionary containing formality data
        """
        formality_data = {}

        try:
            if formality_type == "ATA":
                # Extract remarks
                remarks = formality_element.find(".//ram:Remarks", namespaces=self.namespaces)
                if remarks is not None:
                    formality_data["remarks"] = remarks.text

                # Extract arrival event data
                arrival_event = formality_element.find(".//ata:SpecifiedLogisticsTransportMovement/ram:ArrivalTransportEvent",
                                                       namespaces=self.namespaces)
                if arrival_event is not None:
                    # Extract arrival date/time
                    arrival_datetime = arrival_event.find(".//qdt:DateTimeString", namespaces=self.namespaces)
                    if arrival_datetime is not None:
                        formality_data["arrival_datetime"] = arrival_datetime.text

                    # Extract location
                    location = arrival_event.find(".//ram:OccurrenceLogisticsLocation/ram:ID", namespaces=self.namespaces)
                    if location is not None:
                        formality_data["location"] = location.text

                # Extract call event data
                call_event = formality_element.find(".//ata:SpecifiedLogisticsTransportMovement/ram:CallTransportEvent",
                                                    namespaces=self.namespaces)
                if call_event is not None:
                    # Extract call arrival date/time
                    call_datetime = call_event.find(".//qdt:DateTimeString", namespaces=self.namespaces)
                    if call_datetime is not None:
                        formality_data["call_datetime"] = call_datetime.text

                    # Extract anchorage indicator
                    anchorage = call_event.find(".//ram:MaritimeAnchorageIndicator", namespaces=self.namespaces)
                    if anchorage is not None:
                        formality_data["anchorage_indicator"] = anchorage.text

            # Add support for other formality types as needed

            return formality_data
        except Exception as e:
            logger.error(f"Error extracting {formality_type} data: {str(e)}")
            return formality_data

    def _get_element_text(self, parent: etree._Element, xpath: str) -> Optional[str]:
        """
        Helper method to get element text using XPath.

        Args:
            parent: Parent element
            xpath: XPath expression

        Returns:
            Element text or None if not found
        """
        element = parent.find(xpath, namespaces=self.namespaces)
        return element.text if element is not None else None
