"""
Example test case for database testing utilities.

This module demonstrates how to use the database testing utilities
of the Portman testing package.
"""

import unittest
import psycopg2
from datetime import datetime, timedelta

from portman_testing.db.mock_postgres import MockPostgresDB


class TestDatabaseUtilities(unittest.TestCase):
    """Test cases for database testing utilities."""

    def setUp(self):
        """Set up test environment."""
        # Create mock database
        self.db = MockPostgresDB()
        self.test_db_name = self.db.setup_test_db()

    def tearDown(self):
        """Clean up test environment."""
        # Drop test database
        self.db.teardown_test_db()

    def test_database_creation(self):
        """Test database creation."""
        # Verify connection to test database
        with self.db.get_connection(self.test_db_name) as conn:
            with conn.cursor() as cur:
                # Check if voyages table exists
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'voyages'
                    );
                """)
                voyages_exists = cur.fetchone()[0]

                # Check if arrivals table exists
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'arrivals'
                    );
                """)
                arrivals_exists = cur.fetchone()[0]

        # Verify tables exist
        self.assertTrue(voyages_exists)
        self.assertTrue(arrivals_exists)

    def test_load_test_data(self):
        """Test loading test data."""
        # Load test data for specific IMO numbers
        test_imo_numbers = ["9123456", "9234567"]
        self.db.load_test_data(test_imo_numbers)

        # Query voyages table
        voyages = self.db.execute_query(
            "SELECT DISTINCT vessel_imo FROM voyages"
        )

        # Verify IMO numbers in voyages table
        imo_numbers_in_db = set(voyage["vessel_imo"] for voyage in voyages)
        self.assertEqual(imo_numbers_in_db, set(test_imo_numbers))

    def test_execute_query(self):
        """Test executing queries."""
        # Insert test data
        self.db.execute_query("""
            INSERT INTO voyages (
                vessel_name, vessel_imo, port_locode, port_name,
                eta, etd, port_call_id
            ) VALUES (
                'Test Vessel', '9123456', 'FIHEL', 'Helsinki',
                '2025-03-18T08:00:00Z', '2025-03-18T16:00:00Z',
                'PORT-123456'
            );
        """)

        # Query inserted data
        results = self.db.execute_query(
            "SELECT * FROM voyages WHERE vessel_imo = %s",
            ('9123456',)
        )

        # Verify query results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["vessel_name"], "Test Vessel")
        self.assertEqual(results[0]["port_locode"], "FIHEL")

    def test_get_voyage_by_imo(self):
        """Test getting voyages by IMO number."""
        # Insert test data
        self.db.execute_query("""
            INSERT INTO voyages (
                vessel_name, vessel_imo, port_locode, port_name,
                eta, etd, port_call_id
            ) VALUES (
                'Test Vessel 1', '9123456', 'FIHEL', 'Helsinki',
                '2025-03-18T08:00:00Z', '2025-03-18T16:00:00Z',
                'PORT-123456'
            ), (
                'Test Vessel 1', '9123456', 'FITUR', 'Turku',
                '2025-03-19T08:00:00Z', '2025-03-19T16:00:00Z',
                'PORT-123457'
            );
        """)

        # Get voyages by IMO
        voyages = self.db.get_voyage_by_imo('9123456')

        # Verify voyages
        self.assertEqual(len(voyages), 2)
        self.assertEqual(voyages[0]["port_locode"], "FIHEL")
        self.assertEqual(voyages[1]["port_locode"], "FITUR")

    def test_insert_voyage(self):
        """Test inserting voyage data."""
        # Create voyage data
        voyage_data = {
            "vessel_name": "Test Vessel",
            "vessel_imo": "9123456",
            "port_locode": "FIHEL",
            "port_name": "Helsinki",
            "eta": datetime.now().isoformat(),
            "etd": (datetime.now() + timedelta(hours=8)).isoformat(),
            "port_call_id": "PORT-123456"
        }

        # Insert voyage
        self.db.insert_voyage(voyage_data)

        # Verify insertion
        voyages = self.db.get_voyage_by_imo('9123456')
        self.assertEqual(len(voyages), 1)
        self.assertEqual(voyages[0]["vessel_name"], "Test Vessel")
        self.assertEqual(voyages[0]["port_locode"], "FIHEL")


if __name__ == "__main__":
    unittest.main()
