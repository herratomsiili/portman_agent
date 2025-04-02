"""
Transformer module for converting between Portman agent data and EMSWe-compliant XML.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Union
from lxml import etree

from .converter_config import NAMESPACES, OUTPUT_DIR
from .parser import XMLParser

logger = logging.getLogger(__name__)

class XMLTransformer:
    """
    Transforms data between Portman agent format and EMSWe-compliant XML.
    """

    def __init__(self):
        """
        Initialize the XML transformer.
        """
        self.namespaces = NAMESPACES
        self.parser = XMLParser()

        # Ensure output directory exists
        #os.makedirs(OUTPUT_DIR, exist_ok=True)

    def portman_to_emswe(self, portman_data: Dict[str, Any], formality_type: str = "ATA") -> Optional[etree._Element]:
        """
        Transform Portman agent data to EMSWe-compliant XML.

        Args:
            portman_data: Dictionary containing Portman agent data
            formality_type: Type of formality to generate (e.g., "ATA")

        Returns:
            Root element of the generated XML document or None if transformation fails
        """
        try:
            # Create root element with namespaces
            root = etree.Element("Envelope", nsmap={
                None: "",  # Default namespace
                "mai": self.namespaces["mai"],
                "ata": self.namespaces["ata"],
                "qdt": self.namespaces["qdt"],
                "ram": self.namespaces["ram"],
                "udt": self.namespaces["udt"]
            })

            # Generate MAI element
            mai_element = self._generate_mai_element(portman_data)
            root.append(mai_element)

            # Generate formality-specific element (e.g., ATA)
            if formality_type == "ATA":
                ata_element = self._generate_ata_element(portman_data)
                root.append(ata_element)
            # Add support for other formality types as needed

            return root
        except Exception as e:
            logger.error(f"Error transforming Portman data to EMSWe: {str(e)}")
            return None

    def emswe_to_portman(self, xml_root: etree._Element) -> Dict[str, Any]:
        """
        Transform EMSWe-compliant XML to Portman agent data.

        Args:
            xml_root: Root element of the EMSWe XML document

        Returns:
            Dictionary containing Portman agent data
        """
        try:
            # Extract data from XML using the parser
            extracted_data = self.parser.extract_data(xml_root)

            # Transform to Portman format
            portman_data = self._transform_to_portman_format(extracted_data)

            return portman_data
        except Exception as e:
            logger.error(f"Error transforming EMSWe to Portman data: {str(e)}")
            return {}

    def save_xml(self, xml_root: etree._Element, filename: str) -> str:
        """
        Save XML document to file.

        Args:
            xml_root: Root element of the XML document
            filename: Name of the output file

        Returns:
            Path to the saved file
        """
        # Normalize path to handle both forward and backslashes
        norm_path = os.path.normpath(filename)
        output_path = os.path.join(OUTPUT_DIR, norm_path) if not os.path.isabs(norm_path) else norm_path

        try:
            # Ensure the directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # Create XML tree
            tree = etree.ElementTree(xml_root)

            # Write to file with pretty formatting
            tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

            logger.info(f"XML saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving XML to file: {str(e)}")
            return ""

    def _generate_mai_element(self, portman_data: Dict[str, Any]) -> etree._Element:
        """
        Generate the MAI element from Portman data.

        Args:
            portman_data: Dictionary containing Portman agent data

        Returns:
            MAI element
        """
        # Create MAI element
        mai_element = etree.Element(f"{{{self.namespaces['mai']}}}MAI")

        # Create ExchangedDocument element
        exchanged_doc = etree.SubElement(mai_element, f"{{{self.namespaces['mai']}}}ExchangedDocument")

        # Add document ID
        doc_id = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}ID")
        doc_id.text = portman_data.get("document_id", f"MSGID{int(datetime.now().timestamp())}")

        # Add document type code
        type_code = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}TypeCode")
        type_code.text = "ATA"  # For ATA formality

        # Add purpose code
        purpose_code = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}PurposeCode")
        purpose_code.text = "9"  # Original

        # Add version ID
        version_id = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}VersionID")
        version_id.text = "1.0"

        # Add authentication with timestamp
        auth = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}FirstSignatoryDocumentAuthentication")
        auth_dt = etree.SubElement(auth, f"{{{self.namespaces['ram']}}}ActualDateTime")
        dt_string = etree.SubElement(auth_dt, f"{{{self.namespaces['udt']}}}DateTimeString")
        dt_string.text = portman_data.get("timestamp", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

        # Create ExchangedDeclaration element
        exchanged_decl = etree.SubElement(mai_element, f"{{{self.namespaces['mai']}}}ExchangedDeclaration")

        # Add declaration ID
        decl_id = etree.SubElement(exchanged_decl, f"{{{self.namespaces['ram']}}}ID")
        decl_id.text = portman_data.get("declaration_id", f"DECL-PT-{datetime.now().strftime('%y-%m%d%H%M')}")

        # Add declarant information if available
        if "declarant" in portman_data:
            declarant = portman_data["declarant"]
            declarant_element = etree.SubElement(exchanged_decl, f"{{{self.namespaces['ram']}}}DeclarantTradeParty")

            # Add declarant ID
            if "id" in declarant:
                decl_id_elem = etree.SubElement(declarant_element, f"{{{self.namespaces['ram']}}}ID")
                decl_id_elem.text = declarant["id"]

            # Add declarant name
            if "name" in declarant:
                decl_name = etree.SubElement(declarant_element, f"{{{self.namespaces['ram']}}}Name")
                decl_name.text = declarant["name"]

            # Add role code
            if "role_code" in declarant:
                role_code = etree.SubElement(declarant_element, f"{{{self.namespaces['ram']}}}RoleCode")
                role_code.text = declarant["role_code"]

            # Add contact information if available
            if "contact" in declarant:
                contact = declarant["contact"]
                contact_element = etree.SubElement(declarant_element, f"{{{self.namespaces['ram']}}}DefinedTradeContact")

                # Add person name
                if "name" in contact:
                    person_name = etree.SubElement(contact_element, f"{{{self.namespaces['ram']}}}PersonName")
                    person_name.text = contact["name"]

                # Add phone
                if "phone" in contact:
                    phone_element = etree.SubElement(contact_element, f"{{{self.namespaces['ram']}}}TelephoneUniversalCommunication")
                    phone_number = etree.SubElement(phone_element, f"{{{self.namespaces['ram']}}}CompleteNumber")
                    phone_number.text = contact["phone"]

                # Add email
                if "email" in contact:
                    email_element = etree.SubElement(contact_element, f"{{{self.namespaces['ram']}}}EmailURIUniversalCommunication")
                    email_uri = etree.SubElement(email_element, f"{{{self.namespaces['ram']}}}URIID")
                    email_uri.text = contact["email"]

            # Add address information if available
            if "address" in declarant:
                address = declarant["address"]
                address_element = etree.SubElement(declarant_element, f"{{{self.namespaces['ram']}}}PostalTradeAddress")

                # Add postcode
                if "postcode" in address:
                    postcode = etree.SubElement(address_element, f"{{{self.namespaces['ram']}}}PostcodeCode")
                    postcode.text = address["postcode"]

                # Add street
                if "street" in address:
                    street = etree.SubElement(address_element, f"{{{self.namespaces['ram']}}}StreetName")
                    street.text = address["street"]

                # Add city
                if "city" in address:
                    city = etree.SubElement(address_element, f"{{{self.namespaces['ram']}}}CityName")
                    city.text = address["city"]

                # Add country
                if "country" in address:
                    country = etree.SubElement(address_element, f"{{{self.namespaces['ram']}}}CountryID")
                    country.text = address["country"]

                # Add building number
                if "building" in address:
                    building = etree.SubElement(address_element, f"{{{self.namespaces['ram']}}}BuildingNumber")
                    building.text = address["building"]

        # Add transport movement with call ID if available
        if "call_id" in portman_data:
            transport = etree.SubElement(mai_element, f"{{{self.namespaces['mai']}}}SpecifiedLogisticsTransportMovement")
            call_event = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CallTransportEvent")
            call_id = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}ID")
            call_id.text = portman_data["call_id"]

        return mai_element

    def _generate_ata_element(self, portman_data: Dict[str, Any]) -> etree._Element:
        """
        Generate the ATA element from Portman data.

        Args:
            portman_data: Dictionary containing Portman agent data

        Returns:
            ATA element
        """
        # Create ATA element
        ata_element = etree.Element(f"{{{self.namespaces['ata']}}}ATA")

        # Create ExchangedDocument element if remarks are available
        if "remarks" in portman_data:
            exchanged_doc = etree.SubElement(ata_element, f"{{{self.namespaces['ata']}}}ExchangedDocument")
            remarks = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}Remarks")
            remarks.text = portman_data["remarks"]

        # Create SpecifiedLogisticsTransportMovement element
        transport = etree.SubElement(ata_element, f"{{{self.namespaces['ata']}}}SpecifiedLogisticsTransportMovement")

        # Add ArrivalTransportEvent if arrival data is available
        if "arrival_datetime" in portman_data or "location" in portman_data:
            arrival_event = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}ArrivalTransportEvent")

            # Add arrival date/time if available
            if "arrival_datetime" in portman_data:
                arrival_dt = etree.SubElement(arrival_event, f"{{{self.namespaces['ram']}}}ActualArrivalRelatedDateTime")
                dt_string = etree.SubElement(arrival_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
                dt_string.text = portman_data["arrival_datetime"]

            # Add location if available
            if "location" in portman_data:
                location_element = etree.SubElement(arrival_event, f"{{{self.namespaces['ram']}}}OccurrenceLogisticsLocation")
                location_id = etree.SubElement(location_element, f"{{{self.namespaces['ram']}}}ID")
                location_id.text = portman_data["location"]

        # Add CallTransportEvent if call data is available
        if "call_datetime" in portman_data or "anchorage_indicator" in portman_data:
            call_event = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CallTransportEvent")

            # Add call date/time if available
            if "call_datetime" in portman_data:
                call_dt = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}ActualArrivalRelatedDateTime")
                dt_string = etree.SubElement(call_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
                dt_string.text = portman_data["call_datetime"]

            # Add anchorage indicator if available
            if "anchorage_indicator" in portman_data:
                anchorage = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}MaritimeAnchorageIndicator")
                anchorage.text = portman_data["anchorage_indicator"]

        return ata_element

    def _transform_to_portman_format(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform extracted XML data to Portman agent format.

        Args:
            extracted_data: Dictionary containing extracted XML data

        Returns:
            Dictionary in Portman agent format
        """
        portman_data = {}

        # Copy document type
        portman_data["document_type"] = extracted_data.get("document_type")

        # Process MAI data
        mai_data = extracted_data.get("mai_data", {})
        if mai_data:
            portman_data["document_id"] = mai_data.get("document_id")
            portman_data["declaration_id"] = mai_data.get("declaration_id")
            portman_data["timestamp"] = mai_data.get("timestamp")
            portman_data["call_id"] = mai_data.get("call_id")

            # Copy declarant information
            if "declarant" in mai_data:
                portman_data["declarant"] = mai_data["declarant"]

        # Process formality-specific data
        formality_data = extracted_data.get("formality_data", {})
        if formality_data:
            # Copy common fields
            for key, value in formality_data.items():
                portman_data[key] = value

            # Map to Portman-specific fields based on formality type
            if portman_data["document_type"] == "ATA":
                # Map arrival information to Portman's port call data
                if "arrival_datetime" in formality_data:
                    portman_data["ata"] = formality_data["arrival_datetime"]

                if "location" in formality_data:
                    portman_data["berth"] = formality_data["location"]

        return portman_data
