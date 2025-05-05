"""
Adapter module for converting Digitraffic port call data to the format expected by the EMSWe converter.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


def adapt_digitraffic_to_portman(digitraffic_data: Dict[str, Any], xml_type=None) -> Dict[str, Any]:
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
        mmsi = digitraffic_data.get("mmsi", "unknown")  # Extract MMSI
        
        # Log original values for debugging
        logger.info(f"Adapting data for port call {port_call_id} - Original vesselName: {vessel_name}, imoLloyds: {imo_lloyds}, mmsi: {mmsi}")

        # Arrival information
        eta = digitraffic_data.get("eta")
        ata = digitraffic_data.get("ata")
        
        # Log original eta value
        logger.info(f"Original ETA value: {eta}")
        
        # Format ETA for XML usage if available
        formatted_eta = None
        if eta:
            try:
                # Handle different datetime formats
                if isinstance(eta, str):
                    # Try to standardize the format for ETA
                    if '+' in eta:
                        # Handle timezone offset format
                        dt_part = eta.split('+')[0]
                        if '.' not in dt_part:
                            dt_part += '.000'
                        formatted_eta = dt_part + 'Z'
                    elif 'Z' in eta:
                        # Already in UTC format
                        dt_part = eta.replace('Z', '')
                        if '.' not in dt_part:
                            dt_part += '.000'
                        formatted_eta = dt_part + 'Z'
                    else:
                        # Add timezone if not present
                        if '.' not in eta:
                            eta += '.000'
                        formatted_eta = eta + 'Z'
                logger.info(f"Formatted ETA: {formatted_eta}")
            except Exception as e:
                logger.warning(f"Could not format ETA: {str(e)}, using original value")
                formatted_eta = eta
        
        port_area_name = digitraffic_data.get("portAreaName", "")
        port_area_code = digitraffic_data.get("portAreaCode", "")
        berth_name = digitraffic_data.get("berthName", "")
        berth_code = digitraffic_data.get("berthCode", "")
        port_to_visit = digitraffic_data.get("portToVisit", "")
        
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

        # Build destination string, excluding unknown or empty values
        destination_parts = [port_to_visit]
        if port_area_name.lower() not in ["unknown", ""]:
            destination_parts.append(port_area_name)
        if berth_name.lower() not in ["unknown", ""]:
            destination_parts.append(berth_name)
        destination = "/".join(destination_parts)

        # Agent information
        agent_name = digitraffic_data.get("agentName", "")
        shipping_company = digitraffic_data.get("shippingCompany", "")

        # Create portman data structure with required fields for EMSWe conversion
        portman_data = {
            "document_id": f"MSGID-{port_call_id}",
            "declaration_id": f"DECL-PT-{port_call_id}",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "call_id": str(port_call_id),
            "remarks": f"{vessel_name} (IMO: {imo_lloyds}) {'port arrival ->' if xml_type == 'ATA' else '->'} {destination}",

            # Required fields for ArrivalTransportEvent
            "arrival_datetime": ata or formatted_eta or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "location": port_to_visit,  # Use validated port code here

            # Required field for CallTransportEvent
            "call_datetime": ata or formatted_eta or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "anchorage_indicator": "0",
            
            # Add original ETA for VID XML
            "eta": formatted_eta or eta,
            
            # Add standardized port and berth codes
            "portToVisit": port_to_visit,
            "portAreaCode": port_area_code,
            "portAreaName": port_area_name,
            "berthCode": berth_code,
            "berthName": berth_name,

            # Add vessel information directly - IMPORTANT for VID schema
            "vesselName": vessel_name,
            "imoLloyds": imo_lloyds,
            "mmsi": mmsi,  # Include MMSI in the output

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
                
        # Log the vessel info we're passing through
        logger.info(f"Adapted Portman data contains vesselName: {portman_data.get('vesselName')}, imoLloyds: {portman_data.get('imoLloyds')}, mmsi: {portman_data.get('mmsi')}, eta: {portman_data.get('eta')}")

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
            "eta": digitraffic_data.get("eta", datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")),
            "portToVisit": "PORTX",
            "portAreaCode": "",  # Allow empty value 
            "portAreaName": "Unknown Area",
            "berthCode": "",  # Allow empty value
            "berthName": "Unknown Berth",
            "vesselName": digitraffic_data.get("vesselName", "Unknown Vessel"),
            "imoLloyds": digitraffic_data.get("imoLloyds", "00000000"),
            "mmsi": digitraffic_data.get("mmsi", "00000000"),  # Include MMSI in fallback
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
