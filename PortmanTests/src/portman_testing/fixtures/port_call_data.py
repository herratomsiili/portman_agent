"""
Test fixtures module for port call data.

This module provides test fixtures and utilities for generating
realistic port call data for testing the Portman Agent.
"""

import random
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta


class PortCallFixtures:
    """
    Test fixtures for port call data.

    This class provides methods for generating realistic port call data
    for testing the Portman Agent.
    """

    # Finnish ports with their locodes
    FINNISH_PORTS = [
        {"locode": "FIHEL", "name": "Helsinki"},
        {"locode": "FITUR", "name": "Turku"},
        {"locode": "FIKTK", "name": "Kotka"},
        {"locode": "FIHKO", "name": "Hanko"},
        {"locode": "FIPOR", "name": "Pori"},
        {"locode": "FIRAU", "name": "Rauma"},
        {"locode": "FIOUL", "name": "Oulu"},
        {"locode": "FIVAA", "name": "Vaasa"},
        {"locode": "FIHMA", "name": "Hamina"},
        {"locode": "FIKKN", "name": "Kokkola"}
    ]

    # Baltic Sea ports with their locodes
    BALTIC_PORTS = [
        {"locode": "SESTU", "name": "Stockholm"},
        {"locode": "EEMUG", "name": "Muuga"},
        {"locode": "EETLL", "name": "Tallinn"},
        {"locode": "LVRIX", "name": "Riga"},
        {"locode": "LVVNT", "name": "Ventspils"},
        {"locode": "LTKLJ", "name": "Klaipeda"},
        {"locode": "PLGDY", "name": "Gdynia"},
        {"locode": "PLGDA", "name": "Gdansk"},
        {"locode": "DEHAM", "name": "Hamburg"},
        {"locode": "DKAAR", "name": "Aarhus"},
        {"locode": "DKCPH", "name": "Copenhagen"},
        {"locode": "RUKGD", "name": "Kaliningrad"},
        {"locode": "RULED", "name": "St. Petersburg"}
    ]

    # Port call types
    PORT_CALL_TYPES = ["STANDARD", "BUNKERING", "CARGO", "PASSENGER", "MAINTENANCE"]

    # Port call statuses
    PORT_CALL_STATUSES = ["ACTIVE", "COMPLETED", "CANCELLED", "PLANNED"]

    # Cargo descriptions
    CARGO_DESCRIPTIONS = [
        "General cargo", "Containers", "Bulk cargo", "Vehicles",
        "Passengers", "Oil products", "Chemicals", "LNG",
        "Forest products", "Metal products", "Agricultural products",
        "Construction materials", "Machinery", "Empty"
    ]

    @staticmethod
    def generate_port_call_id() -> str:
        """
        Generate a random port call ID.

        Returns:
            A port call ID string
        """
        return f"PORT-{random.randint(100000, 999999)}"

    @staticmethod
    def generate_port_call_number() -> str:
        """
        Generate a random port call number.

        Returns:
            A port call number string
        """
        return f"PC{random.randint(10000, 99999)}"

    @classmethod
    def get_random_port(cls, exclude_ports: Optional[List[Dict[str, str]]] = None) -> Dict[str, str]:
        """
        Get a random port from the combined list of Finnish and Baltic ports.

        Args:
            exclude_ports: List of ports to exclude from selection

        Returns:
            Dictionary containing port locode and name
        """
        all_ports = cls.FINNISH_PORTS + cls.BALTIC_PORTS

        if exclude_ports:
            available_ports = [p for p in all_ports if p not in exclude_ports]
        else:
            available_ports = all_ports

        return random.choice(available_ports)

    @classmethod
    def generate_port_call(cls,
                           vessel: Dict[str, Any],
                           base_time: Optional[datetime] = None,
                           port: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generate a random port call for a vessel.

        Args:
            vessel: Vessel data dictionary
            base_time: Base time for the port call (default: current time)
            port: Port data dictionary (default: randomly selected)

        Returns:
            Dictionary containing port call data
        """
        if base_time is None:
            base_time = datetime.now()

        if port is None:
            port = cls.get_random_port()

        # Generate previous and next ports
        prev_port = cls.get_random_port(exclude_ports=[port])
        next_port = cls.get_random_port(exclude_ports=[port, prev_port])

        # Generate timestamps
        eta = base_time - timedelta(hours=random.randint(1, 24))
        etd = base_time + timedelta(hours=random.randint(12, 48))
        ata = base_time
        atd = base_time + timedelta(hours=random.randint(6, 36))

        # Generate berth information
        berth_number = random.randint(1, 9)
        berth_code = f"{port['locode']}-B{berth_number}"
        berth_name = f"Berth {berth_number}"

        # Generate port area details
        port_areas = ["MAIN", "SOUTH", "NORTH", "WEST", "EAST"]
        port_area_code = f"{port['locode']}-{random.choice(port_areas)}"
        port_area_name = f"{port['name']} {random.choice(['Main', 'South', 'North', 'West', 'East'])} Port"

        # Generate passenger and crew counts
        if vessel.get("shipType") == 60:  # Passenger vessel
            passenger_count = random.randint(500, 2500)
            crew_count = random.randint(50, 200)
        else:
            passenger_count = random.randint(0, 20)
            crew_count = random.randint(10, 30)

        # Generate port call details
        port_call_id = cls.generate_port_call_id()
        port_call_number = cls.generate_port_call_number()
        port_call_type = random.choice(cls.PORT_CALL_TYPES)
        port_call_status = random.choice(cls.PORT_CALL_STATUSES)

        # Generate cargo description
        cargo_description = random.choice(cls.CARGO_DESCRIPTIONS)

        # Create port call object
        return {
            "portCallId": port_call_id,
            "portCallTimestamp": base_time.isoformat(),
            "portCallNumber": port_call_number,
            "portCallType": port_call_type,
            "vessel": vessel,
            "port": port,
            "portAreaDetails": {
                "portAreaCode": port_area_code,
                "portAreaName": port_area_name
            },
            "berthDetails": {
                "berthCode": berth_code,
                "berthName": berth_name
            },
            "etaTimestamp": eta.isoformat(),
            "etdTimestamp": etd.isoformat(),
            "ataTimestamp": ata.isoformat(),
            "atdTimestamp": atd.isoformat(),
            "portCallStatus": port_call_status,
            "prevPort": prev_port,
            "nextPort": next_port,
            "cargoDescription": cargo_description,
            "passengerCount": passenger_count,
            "crewCount": crew_count,
            "updateTimestamp": (base_time - timedelta(hours=random.randint(1, 6))).isoformat()
        }

    @classmethod
    def generate_port_calls(cls,
                            vessels: List[Dict[str, Any]],
                            count_per_vessel: int = 3,
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Generate multiple port calls for multiple vessels.

        Args:
            vessels: List of vessel data dictionaries
            count_per_vessel: Number of port calls to generate per vessel
            start_date: Start date for port calls (default: 30 days ago)
            end_date: End date for port calls (default: current time)

        Returns:
            List of dictionaries containing port call data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)

        if end_date is None:
            end_date = datetime.now()

        port_calls = []

        for vessel in vessels:
            # Generate port calls for this vessel
            for i in range(count_per_vessel):
                # Calculate a time for this port call
                days_range = (end_date - start_date).days
                random_days = random.randint(0, days_range)
                event_date = start_date + timedelta(days=random_days)

                # Generate a port call
                port_call = cls.generate_port_call(vessel, event_date)
                port_calls.append(port_call)

        # Sort port calls by timestamp
        port_calls.sort(key=lambda x: x.get('portCallTimestamp', ''))

        return port_calls

    @classmethod
    def generate_arrival_updates(cls,
                                 port_call: Dict[str, Any],
                                 count: int = 3) -> List[Dict[str, Any]]:
        """
        Generate arrival time updates for a port call.

        Args:
            port_call: Port call data dictionary
            count: Number of updates to generate

        Returns:
            List of dictionaries containing arrival update data
        """
        updates = []

        # Parse the ETA timestamp
        eta_str = port_call.get('etaTimestamp', '')
        if not eta_str:
            return updates

        eta = datetime.fromisoformat(eta_str.replace('Z', '+00:00'))

        # Generate updates leading up to the ETA
        for i in range(count):
            # Each update is further back in time
            update_time = eta - timedelta(days=count-i)

            # Previous ETA is different from current
            previous_eta = eta - timedelta(hours=random.randint(1, 6))
            current_eta = eta

            # Calculate change in minutes
            eta_change_minutes = int((current_eta - previous_eta).total_seconds() / 60)

            update = {
                "vessel_imo": port_call['vessel']['imo'],
                "port_call_id": port_call['portCallId'],
                "timestamp": update_time.isoformat(),
                "previous_eta": previous_eta.isoformat(),
                "current_eta": current_eta.isoformat(),
                "eta_change_minutes": eta_change_minutes
            }

            updates.append(update)

        return updates
