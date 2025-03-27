"""
Response templates for the Digitraffic port call API.

This module provides template functions to generate realistic mock responses
that match the structure of the actual Digitraffic port call API.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


def get_vessel_name(imo: str) -> str:
    """
    Generate a realistic vessel name based on IMO number.

    Args:
        imo: IMO number of the vessel

    Returns:
        A vessel name
    """
    # Use last digits of IMO to deterministically generate a name
    vessel_prefixes = ["MS", "MV", "SS", "MT", "MY"]
    vessel_names = [
        "Nordic", "Baltic", "Atlantic", "Pacific", "Arctic",
        "Explorer", "Voyager", "Discovery", "Navigator", "Mariner",
        "Princess", "Queen", "Star", "Sun", "Moon",
        "Horizon", "Aurora", "Borealis", "Polaris", "Orion"
    ]
    vessel_suffixes = ["I", "II", "III", "IV", "V", "", "", "", "", ""]

    # Use IMO to deterministically select name components
    seed = int(imo[-3:])
    random.seed(seed)

    prefix = vessel_prefixes[seed % len(vessel_prefixes)]
    name = vessel_names[seed % len(vessel_names)]
    suffix = vessel_suffixes[seed % len(vessel_suffixes)]

    return f"{prefix} {name} {suffix}".strip()


def get_port_call_template(imo: str, event_timestamp: str) -> Dict[str, Any]:
    """
    Generate a template for a port call event.

    Args:
        imo: IMO number of the vessel
        event_timestamp: ISO timestamp for the port call

    Returns:
        Dict containing a port call event in the same format as the Digitraffic API
    """
    # Parse the timestamp to generate related times
    dt = datetime.fromisoformat(event_timestamp.replace('Z', '+00:00'))

    # Generate related timestamps
    eta = (dt - timedelta(hours=random.randint(1, 24))).isoformat() + 'Z'
    etd = (dt + timedelta(hours=random.randint(12, 48))).isoformat() + 'Z'
    ata = dt.isoformat() + 'Z'
    atd = (dt + timedelta(hours=random.randint(6, 36))).isoformat() + 'Z'

    # Generate vessel details
    vessel_name = get_vessel_name(imo)
    mmsi = f"23{imo[2:8]}"  # Generate a plausible MMSI from IMO

    # Generate passenger and crew counts
    passenger_count = random.randint(0, 2000)
    crew_count = random.randint(10, 100)

    # Generate port details
    ports = [
        {"locode": "FIHEL", "name": "Helsinki"},
        {"locode": "FITUR", "name": "Turku"},
        {"locode": "FIKTK", "name": "Kotka"},
        {"locode": "FIHKO", "name": "Hanko"},
        {"locode": "FIPOR", "name": "Pori"},
        {"locode": "FIRAU", "name": "Rauma"},
        {"locode": "FIOUL", "name": "Oulu"},
        {"locode": "FIVAA", "name": "Vaasa"},
        {"locode": "SESTU", "name": "Stockholm"},
        {"locode": "EEMUG", "name": "Muuga"},
        {"locode": "LVRIX", "name": "Riga"},
        {"locode": "DEHAM", "name": "Hamburg"},
        {"locode": "PLGDY", "name": "Gdynia"},
        {"locode": "DKAAR", "name": "Aarhus"}
    ]

    # Select current port and previous/next ports
    current_port_idx = random.randint(0, len(ports) - 1)
    current_port = ports[current_port_idx]

    prev_port_idx = (current_port_idx - 1) % len(ports)
    prev_port = ports[prev_port_idx]

    next_port_idx = (current_port_idx + 1) % len(ports)
    next_port = ports[next_port_idx]

    # Generate berth information
    berths = [f"{i}" for i in range(1, 10)]
    berth = random.choice(berths)

    # Create the port call object
    return {
        "portCallId": f"PORT-{random.randint(100000, 999999)}",
        "portCallTimestamp": event_timestamp,
        "portCallNumber": f"PC{random.randint(10000, 99999)}",
        "portCallType": random.choice(["STANDARD", "BUNKERING", "CARGO", "PASSENGER"]),
        "vessel": {
            "name": vessel_name,
            "imo": imo,
            "mmsi": mmsi,
            "callSign": f"{random.choice(['OFK', 'OFZ', 'OFX'])}{random.randint(1000, 9999)}",
            "shipType": random.choice([60, 70, 80]),  # 60=passenger, 70=cargo, 80=tanker
            "draught": random.randint(50, 150) / 10,  # 5.0 - 15.0 meters
            "overallLength": random.randint(100, 300),  # 100 - 300 meters
            "maxWidth": random.randint(15, 40)  # 15 - 40 meters
        },
        "port": {
            "locode": current_port["locode"],
            "name": current_port["name"]
        },
        "portAreaDetails": {
            "portAreaCode": f"{current_port['locode']}-{random.choice(['MAIN', 'SOUTH', 'NORTH', 'WEST', 'EAST'])}",
            "portAreaName": f"{current_port['name']} {random.choice(['Main', 'South', 'North', 'West', 'East'])} Port"
        },
        "berthDetails": {
            "berthCode": f"{current_port['locode']}-B{berth}",
            "berthName": f"Berth {berth}"
        },
        "etaTimestamp": eta,
        "etdTimestamp": etd,
        "ataTimestamp": ata,
        "atdTimestamp": atd,
        "portCallStatus": random.choice(["ACTIVE", "COMPLETED", "CANCELLED", "PLANNED"]),
        "prevPort": {
            "locode": prev_port["locode"],
            "name": prev_port["name"]
        },
        "nextPort": {
            "locode": next_port["locode"],
            "name": next_port["name"]
        },
        "cargoDescription": random.choice([
            "General cargo", "Containers", "Bulk cargo", "Vehicles",
            "Passengers", "Oil products", "Chemicals", "LNG"
        ]),
        "passengerCount": passenger_count,
        "crewCount": crew_count,
        "updateTimestamp": (dt - timedelta(hours=random.randint(1, 6))).isoformat() + 'Z'
    }


def get_empty_response() -> Dict[str, Any]:
    """
    Generate an empty response with no port calls.

    Returns:
        Dict containing an empty response in the same format as the Digitraffic API
    """
    now = datetime.now()
    return {
        "portCalls": [],
        "metadata": {
            "resultCount": 0,
            "from": (now - timedelta(days=30)).isoformat() + 'Z',
            "to": now.isoformat() + 'Z'
        }
    }


def get_error_response(error_code: int = 500, error_message: str = "Internal Server Error") -> Dict[str, Any]:
    """
    Generate an error response.

    Args:
        error_code: HTTP error code
        error_message: Error message

    Returns:
        Dict containing an error response
    """
    return {
        "error": {
            "code": error_code,
            "message": error_message,
            "timestamp": datetime.now().isoformat() + 'Z'
        }
    }
