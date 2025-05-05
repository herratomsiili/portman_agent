"""
Transformer module for converting between Portman agent data and EMSWe-compliant XML.
"""

import os
import logging
from datetime import datetime, timedelta
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
            formality_type: Type of formality to generate (e.g., "ATA", "NOA")

        Returns:
            Root element of the generated XML document or None if transformation fails
        """
        try:
            # Create root element with namespaces
            nsmap = {
                None: "",  # Default namespace
                "mai": self.namespaces["mai"],
                "qdt": self.namespaces["qdt"],
                "ram": self.namespaces["ram"],
                "udt": self.namespaces["udt"]
            }
            
            # Add formality-specific namespace
            if formality_type == "ATA":
                nsmap["ata"] = self.namespaces["ata"]
            elif formality_type == "NOA":
                nsmap["noa"] = self.namespaces["noa"]
            elif formality_type == "VID":
                nsmap["vid"] = self.namespaces["vid"]
                
            root = etree.Element("Envelope", nsmap=nsmap)

            # Generate MAI element
            mai_element = self._generate_mai_element(portman_data, formality_type)
            root.append(mai_element)

            # Generate formality-specific element
            if formality_type == "ATA":
                formality_element = self._generate_ata_element(portman_data)
                root.append(formality_element)
            elif formality_type == "NOA":
                formality_element = self._generate_noa_element(portman_data)
                root.append(formality_element)
            elif formality_type == "VID":
                formality_element = self._generate_vid_element(portman_data)
                root.append(formality_element)

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

    def _generate_mai_element(self, portman_data: Dict[str, Any], formality_type: str = "ATA") -> etree._Element:
        """
        Generate the MAI element from Portman data.

        Args:
            portman_data: Dictionary containing Portman agent data
            formality_type: Type of formality (e.g., "ATA", "NOA")

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
        type_code.text = formality_type  # Use the formality type

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

        # Add transport movement with call ID if available - ONLY for ATA and NOA, NOT for VID
        if "call_id" in portman_data and formality_type != "VID":
            transport = etree.SubElement(mai_element, f"{{{self.namespaces['mai']}}}SpecifiedLogisticsTransportMovement")
            call_event = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CallTransportEvent")
            call_id = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}ID")
            call_id.text = portman_data["call_id"]
            logger.info(f"Added CallTransportEvent with ID {portman_data['call_id']} for {formality_type}")
        elif formality_type == "VID":
            logger.info("Skipping CallTransportEvent/ID in MAI section for VID message")

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

        # Create ExchangedDocument element for remarks
        exchanged_doc = etree.SubElement(ata_element, f"{{{self.namespaces['ata']}}}ExchangedDocument")
        
        # Add remarks if available
        if "remarks" in portman_data:
            remarks = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}Remarks")
            remarks.text = portman_data["remarks"]

        # Create SpecifiedLogisticsTransportMovement element
        transport = etree.SubElement(ata_element, f"{{{self.namespaces['ata']}}}SpecifiedLogisticsTransportMovement")

        # Add arrival information
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

        # Add call information
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
        
    def _generate_noa_element(self, portman_data: Dict[str, Any]) -> etree._Element:
        """
        Generate the NOA (Notice of pre-arrival) element from Portman data.

        Args:
            portman_data: Dictionary containing Portman agent data

        Returns:
            NOA element
        """
        # Create NOA element
        noa_element = etree.Element(f"{{{self.namespaces['noa']}}}NOA")

        # Create ExchangedDocument element for remarks
        exchanged_doc = etree.SubElement(noa_element, f"{{{self.namespaces['noa']}}}ExchangedDocument")
        
        # Add remarks if available
        if "remarks" in portman_data:
            remarks = etree.SubElement(exchanged_doc, f"{{{self.namespaces['ram']}}}Remarks")
            if isinstance(portman_data["remarks"], str):
                remarks.text = portman_data["remarks"]
                remarks.set("languageID", "EN")

        # Create SpecifiedLogisticsTransportMovement element
        transport = etree.SubElement(noa_element, f"{{{self.namespaces['noa']}}}SpecifiedLogisticsTransportMovement")

        # Add mode code - Maritime
        mode_code = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}ModeCode")
        mode_code.text = portman_data.get("mode_code", "1")  # Default to 1 for maritime transport

        # Add voyage ID if available or create one from call ID
        voyage_id = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}ID")
        voyage_id.text = portman_data.get("voyage_id", f"VYG-{portman_data.get('call_id', str(int(datetime.now().timestamp())))}")

        # Get passenger count from passengersOnArrival field - optional element, but value must be >= 1 when included
        passenger_count = None
        if "passengersOnArrival" in portman_data and portman_data["passengersOnArrival"] is not None:
            try:
                # Handle both string and integer inputs
                passenger_value = portman_data["passengersOnArrival"]
                if isinstance(passenger_value, int):
                    passenger_count = passenger_value
                else:
                    passenger_count = int(passenger_value)
                
                # Only add the element if we have a valid value
                if passenger_count > 0:
                    passenger_qty = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}PassengerQuantity")
                    passenger_qty.text = str(passenger_count)
                else:
                    # If zero passengers, don't include the element
                    passenger_count = None
            except (ValueError, TypeError):
                # If conversion fails, don't add the element
                passenger_count = None
            
        # Get crew count from crewOnArrival field - optional element, but value must be >= 1 when included
        crew_count = None
        if "crewOnArrival" in portman_data and portman_data["crewOnArrival"] is not None:
            try:
                # Handle both string and integer inputs
                crew_value = portman_data["crewOnArrival"]
                if isinstance(crew_value, int):
                    crew_count = crew_value
                else:
                    crew_count = int(crew_value)
                
                # Only add the element if we have a valid value
                if crew_count > 0:
                    crew_qty = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CrewQuantity")
                    crew_qty.text = str(crew_count)
                else:
                    # If zero crew, don't include the element
                    crew_count = None
            except (ValueError, TypeError):
                # If conversion fails, don't add the element
                crew_count = None

        # Add cargo description if available (generic if not provided)
        cargo_desc = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CargoDescription")
        cargo_desc.text = portman_data.get("cargo_description", "Standard cargo")
        cargo_desc.set("languageID", "EN")
        
        # Add dangerous goods indicator (default to 0/no)
        dangerous_goods = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}DangerousGoodsIndicator")
        dangerous_goods.text = portman_data.get("dangerous_goods_indicator", "0")
        
        # Add call purpose code (default to 1 - Other)
        call_purpose = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CallPurposeCode")
        call_purpose.text = portman_data.get("call_purpose_code", "1")
        
        # Add regular service indicator
        regular_service = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}RegularServiceIndicator")
        regular_service.text = portman_data.get("regular_service_indicator", "0")
        
        # Add total onboard person quantity (passengers + crew)
        # Schema requires this to be greater than 0
        total_count = 0
        if passenger_count is not None:
            total_count += passenger_count
        if crew_count is not None:
            total_count += crew_count
            
        # Ensure at least 1 person on board to meet schema validation
        total_count = max(1, total_count)
            
        total_onboard = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}TotalOnboardPersonQuantity")
        total_onboard.text = str(total_count)
        
        # Add found stowaway indicator
        stowaway_indicator = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}FoundStowawayIndicator")
        stowaway_indicator.text = portman_data.get("found_stowaway_indicator", "0")
        
        # Debug output to help diagnose issues
        logger.info(f"NOA XML generation - PassengersOnArrival: {portman_data.get('passengersOnArrival')}, CrewOnArrival: {portman_data.get('crewOnArrival')}")
        logger.info(f"Processed values - Passenger count: {passenger_count}, Crew count: {crew_count}, Total count: {total_count}")
        
        # Add vessel information
        if "imoLloyds" in portman_data or "vesselName" in portman_data:
            used_means = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}UsedLogisticsTransportMeans")
            
            # Add vessel type code if available
            if "vesselTypeCode" in portman_data:
                type_code = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}TypeCode")
                type_code.text = str(portman_data["vesselTypeCode"])
            
            # Add IMO number if available
            if "imoLloyds" in portman_data:
                reg_event = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}RegistrationTransportEvent")
                reg_id = etree.SubElement(reg_event, f"{{{self.namespaces['ram']}}}ID")
                reg_id.text = str(portman_data["imoLloyds"])
            
            # Add shipping company if available
            if "shippingCompany" in portman_data:
                ship_company = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}ShipCompanyTradeParty")
                company_name = etree.SubElement(ship_company, f"{{{self.namespaces['ram']}}}Name")
                company_name.text = portman_data["shippingCompany"]
        
        # Add port information
        if "portToVisit" in portman_data or "location" in portman_data:
            itinerary = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}ItineraryTransportRoute")
            stop_event = etree.SubElement(itinerary, f"{{{self.namespaces['ram']}}}ItineraryStopTransportEvent")
            
            # IMPORTANT: Elements must be in the correct order
            # 1. First add ArrivalRelatedDateTime
            arr_dt = etree.SubElement(stop_event, f"{{{self.namespaces['ram']}}}ArrivalRelatedDateTime")
            dt_string = etree.SubElement(arr_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
            dt_string.text = portman_data.get("eta", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
                
            # 2. Add DepartureRelatedDateTime 
            dep_dt = etree.SubElement(stop_event, f"{{{self.namespaces['ram']}}}DepartureRelatedDateTime")
            dt_string = etree.SubElement(dep_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
            dt_string.text = portman_data.get("etd", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
                
            # 3. Add sequence number
            seq_num = etree.SubElement(stop_event, f"{{{self.namespaces['ram']}}}SequenceNumeric")
            seq_num.text = "1"
                
            # 4. Finally add location
            location = etree.SubElement(stop_event, f"{{{self.namespaces['ram']}}}OccurrenceLogisticsLocation")
            loc_id = etree.SubElement(location, f"{{{self.namespaces['ram']}}}ID")
            
            # Get port ID - only portToVisit needs to be standardized as UN/LOCODE (5 chars)
            port_id = portman_data.get("portToVisit", portman_data.get("location", "PORT1"))
            loc_id.text = port_id
        
        # Now add the CallTransportEvent after all required elements
        call_event = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CallTransportEvent")
            
        # Add estimated arrival date/time
        est_arrival_dt = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}EstimatedTransportMeansArrivalOccurrenceDateTime")
        dt_string = etree.SubElement(est_arrival_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
        dt_string.text = portman_data.get("eta", portman_data.get("arrival_datetime", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))
            
        # REQUIRED: Add estimated departure date/time (required by schema)
        est_departure_dt = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}EstimatedTransportMeansDepartureOccurrenceDateTime")
        dt_string = etree.SubElement(est_departure_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
        dt_string.text = portman_data.get("etd", portman_data.get("departure_datetime", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))
        
        # Add berth information if available
        if "berthCode" in portman_data or "berthName" in portman_data:
            location_element = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}ExpectedArrivalPortAreaRelatedLogisticsLocation")
            name = etree.SubElement(location_element, f"{{{self.namespaces['ram']}}}Name")
            name.text = portman_data.get("berthName", portman_data.get("berthCode", ""))
            
        return noa_element

    def _generate_vid_element(self, portman_data: Dict[str, Any]) -> etree._Element:
        """
        Generate the VID (Vessel Information Data) element from Portman data.

        Args:
            portman_data: Dictionary containing Portman agent data

        Returns:
            VID element
        """
        # Create VID element
        vid_element = etree.Element(f"{{{self.namespaces['vid']}}}VID")

        # Create SpecifiedLogisticsTransportMovement element
        transport = etree.SubElement(vid_element, f"{{{self.namespaces['vid']}}}SpecifiedLogisticsTransportMovement")

        # IMPORTANT: The VID schema requires a very specific sequence per EMSWe specification:
        # 1. First must be UsedLogisticsTransportMeans
        used_means = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}UsedLogisticsTransportMeans")
            
        # Add vessel name - REQUIRED by schema
        # Always add this element, even if empty
        name = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}Name")
        name.text = portman_data.get("vesselName", "")
        
        # Add IMONumberIndicator - REQUIRED by schema
        imo_indicator = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}IMONumberIndicator")
        # Set to "1" (yes) if IMO number is present
        imo_indicator.text = "1" if portman_data.get("imoLloyds") else "0"
        
        # Add IMO number if available - conditional on IMONumberIndicator
        # Always add IMO ID when it's available
        if portman_data.get("imoLloyds"):
            imo_id = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}IMOID")
            imo_id.text = str(portman_data["imoLloyds"])
        
        # Add MMSI number if available and valid - using MMSIID as per schema
        # MMSIID must be exactly 9 characters long
        if portman_data.get("mmsi"):
            mmsi_value = str(portman_data["mmsi"]).strip()
            
            # Check if MMSI is valid (exactly 9 numeric characters and not 0)
            mmsi_is_valid = (
                len(mmsi_value) == 9 and 
                mmsi_value.isdigit() and 
                mmsi_value != "000000000"
            )
            
            if mmsi_is_valid:
                mmsi = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}MMSIID")
                mmsi.text = mmsi_value
                logger.info(f"Added MMSI {mmsi_value} to VID XML")
            else:
                logger.warning(f"MMSI value {mmsi_value} is invalid (must be 9 digits). Skipping MMSIID element.")
        
        # Add vessel type code if available
        if "vesselTypeCode" in portman_data:
            type_code = etree.SubElement(used_means, f"{{{self.namespaces['ram']}}}TypeCode")
            type_code.text = str(portman_data["vesselTypeCode"])

        # 2. Second must be CallTransportEvent
        call_event = etree.SubElement(transport, f"{{{self.namespaces['ram']}}}CallTransportEvent")
        
        # Add EstimatedTransportMeansArrivalOccurrenceDateTime - REQUIRED by schema
        # Get the eta from the input data - prioritize standard 'eta' field, then try arrival_datetime
        eta_value = None
        if "eta" in portman_data and portman_data["eta"]:
            eta_value = portman_data["eta"]
        elif "arrival_datetime" in portman_data and portman_data["arrival_datetime"]:
            eta_value = portman_data["arrival_datetime"]
            
        est_arrival_dt = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}EstimatedTransportMeansArrivalOccurrenceDateTime")
        dt_string = etree.SubElement(est_arrival_dt, f"{{{self.namespaces['qdt']}}}DateTimeString")
        
        if eta_value:
            dt_string.text = eta_value
        else:
            # Only use current time + 1 hour as a fallback if no ETA provided
            dt_string.text = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            logger.warning(f"No ETA provided for VID, using generated timestamp: {dt_string.text}")
            
        # Add OccurrenceLogisticsLocation - REQUIRED by schema
        location_element = etree.SubElement(call_event, f"{{{self.namespaces['ram']}}}OccurrenceLogisticsLocation")
        
        # Add location ID (UN/LOCODE) - REQUIRED by schema
        location_id = etree.SubElement(location_element, f"{{{self.namespaces['ram']}}}ID")
        if "portToVisit" in portman_data and portman_data["portToVisit"]:
            location_id.text = portman_data["portToVisit"]
        else:
            # Default fallback to meet schema requirements
            location_id.text = "XXXXX"  
        
        return vid_element

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
