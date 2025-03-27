"""
Example test case for test fixtures.

This module demonstrates how to use the test fixtures
of the Portman testing package.
"""

import unittest
from datetime import datetime, timedelta

from portman_testing.fixtures.vessel_data import VesselFixtures
from portman_testing.fixtures.port_call_data import PortCallFixtures


class TestFixtures(unittest.TestCase):
    """Test cases for test fixtures."""

    def setUp(self):
        """Set up test environment."""
        pass

    def test_vessel_fixtures(self):
        """Test vessel fixtures."""
        # Generate a single vessel
        vessel = VesselFixtures.generate_vessel()

        # Verify vessel structure
        self.assertIn("name", vessel)
        self.assertIn("imo", vessel)
        self.assertIn("mmsi", vessel)
        self.assertIn("callSign", vessel)
        self.assertIn("shipType", vessel)

        # Generate vessel with specific type
        passenger_vessel = VesselFixtures.generate_vessel(vessel_type=60)
        self.assertEqual(passenger_vessel["shipType"], 60)

        # Generate vessel with specific IMO
        specific_vessel = VesselFixtures.generate_vessel(imo="9123456")
        self.assertEqual(specific_vessel["imo"], "9123456")

        # Generate multiple vessels
        vessels = VesselFixtures.generate_vessels(count=3)
        self.assertEqual(len(vessels), 3)

        # Get predefined vessels
        predefined_vessels = VesselFixtures.get_predefined_vessels()
        self.assertGreaterEqual(len(predefined_vessels), 5)

    def test_port_call_fixtures(self):
        """Test port call fixtures."""
        # Get a vessel for testing
        vessel = VesselFixtures.generate_vessel()

        # Generate a single port call
        port_call = PortCallFixtures.generate_port_call(vessel)

        # Verify port call structure
        self.assertIn("portCallId", port_call)
        self.assertIn("vessel", port_call)
        self.assertIn("port", port_call)
        self.assertIn("etaTimestamp", port_call)
        self.assertIn("etdTimestamp", port_call)
        self.assertIn("portCallStatus", port_call)

        # Generate port call with specific port
        helsinki_port = {"locode": "FIHEL", "name": "Helsinki"}
        helsinki_call = PortCallFixtures.generate_port_call(vessel, port=helsinki_port)
        self.assertEqual(helsinki_call["port"]["locode"], "FIHEL")

        # Generate port call with specific time
        specific_time = datetime.now()
        timed_call = PortCallFixtures.generate_port_call(vessel, base_time=specific_time)
        self.assertIn(specific_time.isoformat(), timed_call["portCallTimestamp"])

        # Generate multiple port calls
        vessels = VesselFixtures.generate_vessels(count=2)
        port_calls = PortCallFixtures.generate_port_calls(vessels, count_per_vessel=2)
        self.assertEqual(len(port_calls), 4)

        # Generate arrival updates
        arrival_updates = PortCallFixtures.generate_arrival_updates(port_call)
        self.assertGreaterEqual(len(arrival_updates), 1)
        self.assertEqual(arrival_updates[0]["vessel_imo"], vessel["imo"])
        self.assertEqual(arrival_updates[0]["port_call_id"], port_call["portCallId"])


if __name__ == "__main__":
    unittest.main()
