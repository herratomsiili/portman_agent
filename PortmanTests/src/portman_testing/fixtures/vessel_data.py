"""
Test fixtures module for vessel data.

This module provides test fixtures and utilities for generating
realistic vessel data for testing the Portman Agent.
"""

import random
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta


class VesselFixtures:
    """
    Test fixtures for vessel data.

    This class provides methods for generating realistic vessel data
    for testing the Portman Agent.
    """

    # Common vessel types with their codes
    VESSEL_TYPES = {
        60: "Passenger",
        70: "Cargo",
        80: "Tanker",
        30: "Fishing",
        31: "Tug",
        32: "Towing",
        33: "Dredger",
        34: "Diving",
        35: "Military",
        36: "Sailing",
        37: "Pleasure Craft"
    }

    # Sample vessel names by type
    VESSEL_NAMES = {
        "Passenger": [
            "Viking Grace", "Silja Symphony", "Gabriella", "Amorella", "Baltic Princess",
            "Finlandia", "Mariella", "Galaxy", "Viking XPRS", "Cinderella"
        ],
        "Cargo": [
            "Finnmaster", "Baltic Carrier", "Nordic Trader", "Aurora", "Polaris",
            "Midas", "Orion", "Pegasus", "Hercules", "Poseidon"
        ],
        "Tanker": [
            "Nordic Breeze", "Baltic Explorer", "Aurora Borealis", "Polar Star", "Arctic Voyager",
            "Northern Light", "Frost", "Ice Queen", "Snow Crystal", "Winter Wind"
        ]
    }

    @staticmethod
    def generate_imo_number() -> str:
        """
        Generate a random IMO number.

        IMO numbers are 7 digits, starting with 9.

        Returns:
            A valid IMO number as string
        """
        return f"9{random.randint(100000, 999999)}"

    @staticmethod
    def generate_mmsi_number() -> str:
        """
        Generate a random MMSI number.

        MMSI numbers are 9 digits, often starting with country code.
        Finnish vessels often start with 230.

        Returns:
            A valid MMSI number as string
        """
        country_codes = ["230", "231", "232", "265", "266", "276", "277"]
        country_code = random.choice(country_codes)
        suffix = random.randint(100000, 999999)
        return f"{country_code}{suffix}"

    @staticmethod
    def generate_call_sign() -> str:
        """
        Generate a random call sign.

        Finnish vessels often have call signs starting with OF or OG.

        Returns:
            A valid call sign as string
        """
        prefixes = ["OFA", "OFB", "OFC", "OFD", "OFE", "OFF", "OFG", "OFH", "OFI", "OFJ"]
        suffix = random.randint(1000, 9999)
        return f"{random.choice(prefixes)}{suffix}"

    @classmethod
    def generate_vessel(cls, vessel_type: Optional[int] = None, imo: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a random vessel with realistic data.

        Args:
            vessel_type: Vessel type code (default: None, randomly selected)
            imo: IMO number (default: None, randomly generated)

        Returns:
            Dictionary containing vessel data
        """
        # Select vessel type if not provided
        if vessel_type is None:
            vessel_type = random.choice(list(cls.VESSEL_TYPES.keys()))

        vessel_type_name = cls.VESSEL_TYPES.get(vessel_type, "Unknown")

        # Generate IMO if not provided
        if imo is None:
            imo = cls.generate_imo_number()

        # Generate vessel name based on type
        if vessel_type_name in cls.VESSEL_NAMES:
            vessel_name = random.choice(cls.VESSEL_NAMES[vessel_type_name])
        else:
            vessel_name = f"Test Vessel {imo[-4:]}"

        # Generate other vessel details
        mmsi = cls.generate_mmsi_number()
        call_sign = cls.generate_call_sign()

        # Generate vessel dimensions based on type
        if vessel_type == 60:  # Passenger
            length = random.randint(150, 300)
            width = random.randint(25, 40)
            draught = random.randint(60, 90) / 10  # 6.0 - 9.0 meters
        elif vessel_type == 70:  # Cargo
            length = random.randint(100, 250)
            width = random.randint(20, 35)
            draught = random.randint(70, 120) / 10  # 7.0 - 12.0 meters
        elif vessel_type == 80:  # Tanker
            length = random.randint(120, 280)
            width = random.randint(22, 38)
            draught = random.randint(80, 140) / 10  # 8.0 - 14.0 meters
        else:
            length = random.randint(50, 150)
            width = random.randint(10, 25)
            draught = random.randint(30, 70) / 10  # 3.0 - 7.0 meters

        return {
            "name": vessel_name,
            "imo": imo,
            "mmsi": mmsi,
            "callSign": call_sign,
            "shipType": vessel_type,
            "shipTypeName": vessel_type_name,
            "draught": draught,
            "overallLength": length,
            "maxWidth": width
        }

    @classmethod
    def generate_vessels(cls, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate multiple random vessels.

        Args:
            count: Number of vessels to generate

        Returns:
            List of dictionaries containing vessel data
        """
        return [cls.generate_vessel() for _ in range(count)]

    @classmethod
    def get_predefined_vessels(cls) -> List[Dict[str, Any]]:
        """
        Get a list of predefined vessels with fixed IMO numbers.

        These vessels can be used for consistent testing.

        Returns:
            List of dictionaries containing vessel data
        """
        predefined_vessels = [
            cls.generate_vessel(vessel_type=60, imo="9123456"),  # Passenger
            cls.generate_vessel(vessel_type=70, imo="9234567"),  # Cargo
            cls.generate_vessel(vessel_type=80, imo="9345678"),  # Tanker
            cls.generate_vessel(vessel_type=31, imo="9456789"),  # Tug
            cls.generate_vessel(vessel_type=36, imo="9567890")   # Sailing
        ]

        # Override names for predefined vessels
        predefined_vessels[0]["name"] = "Test Passenger"
        predefined_vessels[1]["name"] = "Test Cargo"
        predefined_vessels[2]["name"] = "Test Tanker"
        predefined_vessels[3]["name"] = "Test Tug"
        predefined_vessels[4]["name"] = "Test Sailing"

        return predefined_vessels
