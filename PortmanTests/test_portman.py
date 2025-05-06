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

        # Test data
        self.sample_port_call = {
            "portCallId": 3190880,
            "imoLloyds": 9606900,
            "mmsi": 257800000,
            "vesselTypeCode": "20",
            "vesselName": "Viking Grace",
            "prevPort": "FIMHQ",
            "portToVisit": "FITKU",
            "nextPort": "FILAN",
            "agentInfo": [
                {"role": 1, "name": "Viking Line Abp / Helsinki"},
                {"role": 2, "name": "Viking Line Abp"}
            ],
            "imoInformation": [
                {
                    "imoGeneralDeclaration": "Arrival",
                    "numberOfPassangers": 235,
                    "numberOfCrew": 1849
                },
                {
                    "imoGeneralDeclaration": "Departure",
                    "numberOfPassangers": 188,
                    "numberOfCrew": 1346
                }
            ],
            "portAreaDetails": [{
                "eta": "2024-03-13T10:00:00.000+00:00",
                "ata": None,
                "portAreaCode": "PASSE",
                "portAreaName": "Matkustajasatama",
                "berthCode": "v1",
                "berthName": "viking1",
                "etd": "2024-03-13T20:00:00.000+00:00",
                "atd": None
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
        self.assertEqual(result["portCallId"], 3190880)
        self.assertEqual(result["vesselName"], "Viking Grace")
        self.assertEqual(result["crewOnArrival"], 1849)
        self.assertEqual(result["crewOnDeparture"], 1346)

    def test_save_results_to_db(self):
        """Test database storage with a real database."""
        results = process_query({"portCalls": [self.sample_port_call]})
        save_results_to_db(results)

        # Retrieve data from the database and verify storage
        self.cursor.execute("SELECT vesselName FROM voyages WHERE portCallId = %s", (3190880,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Viking Grace")

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
