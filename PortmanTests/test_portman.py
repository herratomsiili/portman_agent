# Test cases for the PortmanTrigger/portman.py module.

import unittest
import json
import pg8000
from datetime import datetime, timezone
from PortmanTrigger.portman import (
    process_query,
    save_results_to_db,
    fetch_data_from_api,
    get_db_connection
)
from config import DATABASE_CONFIG

class TestPortman(unittest.TestCase):
    def setUp(self):
        """Create an actual PostgreSQL database connection and initialize test data."""
        self.conn = pg8000.connect(
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"],
            database=DATABASE_CONFIG["dbname"],
            port=DATABASE_CONFIG["port"]
        )
        self.cursor = self.conn.cursor()

        # Clear test tables before running tests
        # self.cursor.execute("DELETE FROM arrivals;")
        # self.cursor.execute("DELETE FROM voyages;")
        # self.conn.commit()

        # Test data
        self.sample_port_call = {
            "portCallId": 11111,
            "imoLloyds": 9876543,
            "vesselTypeCode": "CARGO",
            "vesselName": "Test Vessel",
            "prevPort": "Helsinki",
            "portToVisit": "Turku",
            "nextPort": "Stockholm",
            "agentInfo": [
                {"role": 1, "name": "Test Agent"},
                {"role": 2, "name": "Test Shipping"}
            ],
            "imoInformation": [
                {
                    "imoGeneralDeclaration": "Arrival",
                    "numberOfPassangers": 0,
                    "numberOfCrew": 10
                },
                {
                    "imoGeneralDeclaration": "Departure",
                    "numberOfPassangers": 0,
                    "numberOfCrew": 10
                }
            ],
            "portAreaDetails": [{
                "eta": "2025-03-13T10:00:00Z",
                "ata": "2025-03-13T10:15:00Z",
                "portAreaCode": "FI-TKU",
                "portAreaName": "Turku",
                "berthCode": "TKU1",
                "berthName": "Terminal 1",
                "etd": "2025-03-13T20:00:00Z",
                "atd": "2025-03-13T20:15:00Z"
            }]
        }

    def tearDown(self):
        """Closes database connection after tests."""
        self.cursor.close()
        self.conn.close()

    def test_process_query(self):
        """Test JSON data processing."""
        results = process_query({"portCalls": [self.sample_port_call]})

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["portCallId"], 12345)
        self.assertEqual(result["vesselName"], "Test Vessel")
        self.assertEqual(result["crewOnArrival"], 10)
        self.assertEqual(result["crewOnDeparture"], 10)

    def test_save_results_to_db(self):
        """Test database storage with a real database."""
        results = process_query({"portCalls": [self.sample_port_call]})
        save_results_to_db(results)

        # Retrieve data from the database and verify storage
        self.cursor.execute("SELECT vessel_name FROM voyages WHERE port_call_id = %s", (12345,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Test Vessel")

    def test_get_db_connection(self):
        """Test database connection to the correct database."""
        conn = get_db_connection(DATABASE_CONFIG["dbname"])
        self.assertIsNotNone(conn)

        # Verify that the connection is working by running a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)

        conn.close()

if __name__ == '__main__':
    unittest.main()
