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
        berth_name = digitraffic_data.get("berthName", "unknown")
        port_to_visit = digitraffic_data.get("portToVisit", "unknown")

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
            "location": berth_name or port_area_name or "Unknown Terminal",

            # Required field for CallTransportEvent
            "call_datetime": ata or eta or datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "anchorage_indicator": "0",

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
            "location": "Unknown Terminal",
            "call_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "anchorage_indicator": "0",
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
