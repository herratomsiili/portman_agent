"""
Example integration test case.

This module demonstrates how to use all components of the Portman testing package
together to test the complete workflow of the Portman Agent.
"""

import unittest
import os
from datetime import datetime, timedelta

from portman_testing.api.mock_digitraffic import MockDigitraffic
from portman_testing.db.mock_postgres import MockPostgresDB
from portman_testing.fixtures.vessel_data import VesselFixtures
from portman_testing.fixtures.port_call_data import PortCallFixtures
from portman_testing.helpers.azure_function import MockHttpTrigger, mock_context
from portman_testing.helpers.config import PortmanConfig, set_env_var


class TestIntegration(unittest.TestCase):
    """Integration test for the Portman Agent testing package."""

    def setUp(self):
        """Set up test environment."""
        # Create mock API
        self.mock_api = MockDigitraffic()

        # Create mock database
        self.db = MockPostgresDB()
        self.test_db_name = self.db.setup_test_db()

        # Set up test vessels
        self.test_vessels = VesselFixtures.get_predefined_vessels()
        self.test_imo_numbers = [vessel["imo"] for vessel in self.test_vessels]

        # Set up environment variables
        set_env_var("DB_HOST", "localhost")
        set_env_var("DB_PORT", "5432")
        set_env_var("DB_NAME", self.test_db_name)
        set_env_var("DB_USER", "postgres")
        set_env_var("DB_PASSWORD", "postgres")
        set_env_var("API_URL", "https://meri.digitraffic.fi/api/port-call/v1")

    def tearDown(self):
        """Clean up test environment."""
        # Drop test database
        self.db.teardown_test_db()

    def test_complete_workflow(self):
        """Test complete workflow from API to database."""
        # This test simulates the complete workflow of the Portman Agent:
        # 1. HTTP trigger receives request with IMO numbers
        # 2. Agent fetches port call data from API
        # 3. Agent processes data and stores in database
        # 4. Agent returns response with status

        # Step 1: Create HTTP trigger with IMO numbers
        imo_param = ",".join(self.test_imo_numbers[:2])  # Use first two IMO numbers
        http_trigger = MockHttpTrigger(
            method="GET",
            route="portman",
            params={
                "code": "test_function_code",
                "imo": imo_param
            }
        )
        context = mock_context("PortmanFunction")

        # Step 2: Simulate API response (normally this would be done by the function)
        # In a real test, you would patch the API call in the function to return this mock data
        port_calls = []
        for vessel in self.test_vessels[:2]:  # Use first two vessels
            # Generate port calls for this vessel
            vessel_calls = PortCallFixtures.generate_port_calls(
                [vessel],
                count_per_vessel=2
            )
            port_calls.extend(vessel_calls)

        # Step 3: Process data and store in database (normally done by the function)
        # In a real test, you would call the actual function and it would do this processing
        for port_call in port_calls:
            # Extract vessel data
            vessel = port_call["vessel"]

            # Extract port data
            port = port_call["port"]

            # Extract berth data
            berth = port_call["berthDetails"]

            # Extract timestamps
            eta = port_call["etaTimestamp"]
            etd = port_call["etdTimestamp"]
            ata = port_call.get("ataTimestamp")
            atd = port_call.get("atdTimestamp")

            # Extract previous and next ports
            prev_port = port_call.get("prevPort", {})
            next_port = port_call.get("nextPort", {})

            # Create voyage record
            voyage_data = {
                "vessel_name": vessel["name"],
                "vessel_imo": vessel["imo"],
                "vessel_mmsi": vessel.get("mmsi", ""),
                "port_locode": port["locode"],
                "port_name": port["name"],
                "berth_code": berth["berthCode"],
                "berth_name": berth["berthName"],
                "eta": eta,
                "etd": etd,
                "ata": ata,
                "atd": atd,
                "passenger_count": port_call.get("passengerCount"),
                "crew_count": port_call.get("crewCount"),
                "prev_port_locode": prev_port.get("locode"),
                "prev_port_name": prev_port.get("name"),
                "next_port_locode": next_port.get("locode"),
                "next_port_name": next_port.get("name"),
                "port_call_id": port_call["portCallId"],
                "port_call_status": port_call["portCallStatus"],
                "cargo_description": port_call.get("cargoDescription")
            }

            # Insert voyage into database
            self.db.insert_voyage(voyage_data)

            # Generate and insert arrival updates
            arrival_updates = PortCallFixtures.generate_arrival_updates(port_call, count=2)
            for update in arrival_updates:
                self.db.insert_arrival(update)

        # Step 4: Verify data was stored correctly
        # Query voyages table
        voyages = self.db.execute_query(
            "SELECT * FROM voyages WHERE vessel_imo IN %s",
            (tuple(self.test_imo_numbers[:2]),)
        )

        # Verify voyages count (2 vessels * 2 port calls = 4 voyages)
        self.assertEqual(len(voyages), 4)

        # Query arrivals table
        arrivals = self.db.execute_query(
            "SELECT * FROM arrivals WHERE vessel_imo IN %s",
            (tuple(self.test_imo_numbers[:2]),)
        )

        # Verify arrivals count (4 port calls * 2 updates = 8 arrivals)
        self.assertEqual(len(arrivals), 8)

        # In a real test, you would also verify the function's response
        # For this example, we'll just simulate a successful response
        response = {
            "status": "success",
            "processedVessels": 2,
            "totalPortCalls": 4,
            "totalArrivals": 8
        }

        # Verify response
        self.assertEqual(response["processedVessels"], 2)
        self.assertEqual(response["totalPortCalls"], 4)
        self.assertEqual(response["totalArrivals"], 8)


if __name__ == "__main__":
    unittest.main()
