"""
Adapter module for converting Digitraffic port call data to the format expected by the EMSWe converter.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


def adapt_digitraffic_to_portman(digitraffic_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adapt Digitraffic port call data to the Portman format expected by the EMSWe converter.

    Args:
        digitraffic_data: Dictionary containing Digitraffic port call data

    Returns:
        Dictionary in Portman format suitable for EMSWe conversion
    """
    try:
        # Basic port call information
        port_call_id = digitraffic_data.get("portCallId", "unknown")
        vessel_name = digitraffic_data.get("vesselName", "unknown")
        imo_lloyds = digitraffic_data.get("imoLloyds", "unknown")

        # Arrival information
        eta = digitraffic_data.get("eta")
        ata = digitraffic_data.get("ata")
        port_area_name = digitraffic_data.get("portAreaName", "unknown")
        port_area_code = digitraffic_data.get("portAreaCode", "PORT1")
        berth_name = digitraffic_data.get("berthName", "unknown")
        berth_code = digitraffic_data.get("berthCode", "BRTH1")
        port_to_visit = digitraffic_data.get("portToVisit", "unknown")
        
        # Ensure port codes are exactly 5 characters (required by schema)
        # Process port_to_visit
        if port_to_visit:
            if len(port_to_visit) > 5:
                port_to_visit = port_to_visit[:5]
                logger.info(f"Truncated portToVisit to 5 characters: {port_to_visit}")
            elif len(port_to_visit) < 5:
                port_to_visit = port_to_visit.ljust(5, 'X')
                logger.info(f"Padded portToVisit to 5 characters: {port_to_visit}")
        else:
            port_to_visit = "PORTX"  # Default 5-character code
            
        # Process port_area_code
        if port_area_code:
            if len(port_area_code) > 5:
                port_area_code = port_area_code[:5]
                logger.info(f"Truncated portAreaCode to 5 characters: {port_area_code}")
            elif len(port_area_code) < 5:
                port_area_code = port_area_code.ljust(5, 'X')
                logger.info(f"Padded portAreaCode to 5 characters: {port_area_code}")
        else:
            port_area_code = "AREAX"  # Default 5-character code
            
        # Process berth_code
        if berth_code:
            if len(berth_code) > 5:
                berth_code = berth_code[:5]
                logger.info(f"Truncated berthCode to 5 characters: {berth_code}")
            elif len(berth_code) < 5:
                berth_code = berth_code.ljust(5, 'X')
                logger.info(f"Padded berthCode to 5 characters: {berth_code}")
        else:
            berth_code = "BRTHX"  # Default 5-character code

        # Passenger and crew information - ensure they're integers or None
        # We use None to indicate "not provided" rather than 0 (which means "zero passengers/crew")
        passengers_on_arrival = digitraffic_data.get("passengersOnArrival")
        crew_on_arrival = digitraffic_data.get("crewOnArrival")

        # Ensure we have valid integer values or None
        if passengers_on_arrival is not None:
            try:
                passengers_on_arrival = int(passengers_on_arrival)
            except (ValueError, TypeError):
                # If conversion fails, set to None to indicate missing data
                passengers_on_arrival = None
        
        if crew_on_arrival is not None:
            try:
                crew_on_arrival = int(crew_on_arrival)
            except (ValueError, TypeError):
                # If conversion fails, set to None to indicate missing data
                crew_on_arrival = None

        # Log passenger and crew counts for debugging
        logger.info(f"Adapting port call {port_call_id} with passengers: {passengers_on_arrival}, crew: {crew_on_arrival}")

        # Build destination string, excluding unknown or "ei tiedossa" values
        destination_parts = [port_to_visit]
        if port_area_name.lower() not in ["unknown", "ei tiedossa"]:
            destination_parts.append(port_area_name)
        if berth_name.lower() not in ["unknown", "ei tiedossa"]:
            destination_parts.append(berth_name)
        destination = "/".join(destination_parts)

        # Agent information
        agent_name = digitraffic_data.get("agentName", "unknown")
        shipping_company = digitraffic_data.get("shippingCompany", "unknown")

        # Create portman data structure with required fields for EMSWe conversion
        portman_data = {
            "document_id": f"MSGID-{port_call_id}",
            "declaration_id": f"DECL-PT-{port_call_id}",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "call_id": str(port_call_id),
            "remarks": f"{vessel_name} (IMO: {imo_lloyds}) port arrival to {destination}",

            # Required fields for ArrivalTransportEvent
            "arrival_datetime": ata or eta or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "location": port_to_visit,  # Use validated port code here

            # Required field for CallTransportEvent
            "call_datetime": ata or eta or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "anchorage_indicator": "0",
            
            # Add standardized port and berth codes
            "portToVisit": port_to_visit,
            "portAreaCode": port_area_code,
            "portAreaName": port_area_name,
            "berthCode": berth_code,
            "berthName": berth_name,

            # Required declarant information
            "declarant": {
                "id": f"FI{imo_lloyds}" if imo_lloyds else "FI123456789012",
                "name": agent_name or shipping_company or "Unknown Agent",
                "role_code": "AG",
                "contact": {
                    "name": agent_name or "Port Agent",
                    "phone": "+358-00-0000000",
                    "email": "contact@example.com"
                },
                "address": {
                    "postcode": "00000",
                    "street": "Port Street",
                    "city": "Port City",
                    "country": "FI",
                    "building": "1"
                }
            }
        }
        
        # Add passenger and crew counts if available (only if they have actual values)
        if passengers_on_arrival is not None:
            portman_data["passengersOnArrival"] = passengers_on_arrival
            
        if crew_on_arrival is not None:
            portman_data["crewOnArrival"] = crew_on_arrival
        
        # Log the standardized codes for debugging
        logger.info(f"Using standardized codes - portToVisit: {port_to_visit} ({len(port_to_visit)} chars), "
                    f"portAreaCode: {port_area_code} ({len(port_area_code)} chars), "
                    f"berthCode: {berth_code} ({len(berth_code)} chars)")

        return portman_data

    except Exception as e:
        logger.error(f"Error adapting Digitraffic data: {str(e)}")
        # Return minimal valid structure
        return {
            "document_id": f"MSGID-{datetime.now().timestamp()}",
            "declaration_id": f"DECL-PT-{datetime.now().strftime('%y%m%d%H%M')}",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "call_id": f"CALL-{datetime.now().strftime('%Y%m%d')}-001",
            "remarks": "Adapted from Digitraffic data",
            "arrival_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "location": "UNKNW",  # Ensure 5 characters
            "call_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "anchorage_indicator": "0",
            "portToVisit": "PORTX",
            "portAreaCode": "AREAX", 
            "portAreaName": "Unknown Area",
            "berthCode": "BRTHX",
            "berthName": "Unknown Berth",
            "declarant": {
                "id": "FI123456789012",
                "name": "Unknown Agent",
                "role_code": "AG",
                "contact": {
                    "name": "Port Agent",
                    "phone": "+358-00-0000000",
                    "email": "contact@example.com"
                },
                "address": {
                    "postcode": "00000",
                    "street": "Port Street",
                    "city": "Port City",
                    "country": "FI",
                    "building": "1"
                }
            }
        }
