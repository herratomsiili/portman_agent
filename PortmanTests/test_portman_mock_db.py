import unittest
from unittest.mock import patch, MagicMock
from PortmanTrigger.portman import (
    process_query,
    save_results_to_db,
    fetch_data_from_api,
    get_db_connection
)

class TestPortmanMockDb(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Test data
        self.sample_port_call = {
            "portCallId": 12345,
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
                "eta": "2024-03-13T10:00:00Z",
                "ata": "2024-03-13T10:15:00Z",
                "portAreaCode": "FI-TKU",
                "portAreaName": "Turku",
                "berthCode": "TKU1",
                "berthName": "Terminal 1",
                "etd": "2024-03-13T20:00:00Z",
                "atd": "2024-03-13T20:15:00Z"
            }]
        }

    def test_process_query(self):
        """Test JSON data processing."""
        # Test data processing
        results = process_query({"portCalls": [self.sample_port_call]})
        
        # Verify results
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["portCallId"], 12345)
        self.assertEqual(result["vesselName"], "Test Vessel")
        self.assertEqual(result["crewOnArrival"], 10)
        self.assertEqual(result["crewOnDeparture"], 10)

    @patch('requests.get')
    def test_fetch_data_from_api(self, mock_get):
        """Test API data fetching."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"portCalls": [self.sample_port_call]}
        mock_get.return_value = mock_response

        # Test API call
        data = fetch_data_from_api()
        
        # Verify results
        self.assertIsNotNone(data)
        self.assertIn("portCalls", data)
        self.assertEqual(len(data["portCalls"]), 1)

    @patch('pg8000.connect')
    def test_save_results_to_db(self, mock_connect):
        """Test database operations."""
        # Mock database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Test data
        results = process_query({"portCalls": [self.sample_port_call]})
        
        # Test database save
        save_results_to_db(results)
        
        # Verify database operations
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()

    def test_get_db_connection(self):
        """Test database connection."""
        # using mock db
        with patch('pg8000.connect') as mock_connect:
            # Test successful connection
            mock_connect.return_value = MagicMock()
            conn = get_db_connection("test_db")
            self.assertIsNotNone(conn)
            
            # Test connection failure
            mock_connect.side_effect = Exception("Connection failed")
            conn = get_db_connection("test_db")
            self.assertIsNone(conn)

if __name__ == '__main__':
    unittest.main() 