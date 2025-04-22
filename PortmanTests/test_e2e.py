# e2e tests for the complete flow from API to database

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from PortmanTrigger.portman import (
    process_query,
    save_results_to_db,
    fetch_data_from_api
)

def test_end_to_end_flow(test_db_connection, sample_port_call_data):
    """Test complete flow from API to database."""
    # 1. Fetch data from API (mocked)
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"portCalls": [sample_port_call_data]}
        mock_get.return_value = mock_response
        data = fetch_data_from_api()
        
        assert data is not None
        assert "portCalls" in data
        assert len(data["portCalls"]) == 1

    # 2. Process the data
    results = process_query(data)
    
    assert len(results) == 1
    result = results[0]
    assert result["portCallId"] == sample_port_call_data["portCallId"]
    assert result["vesselName"] == sample_port_call_data["vesselName"]
    assert result["crewOnArrival"] == sample_port_call_data["imoInformation"][0]["numberOfCrew"]

    # 3. Save to database
    save_results_to_db(results)
    
    # 4. Verify database entries
    cursor = test_db_connection.cursor()
    
    # Check voyages table
    cursor.execute("SELECT * FROM voyages WHERE portCallId = %s", (sample_port_call_data["portCallId"],))
    voyage = cursor.fetchone()
    
    assert voyage is not None
    assert voyage[0] == sample_port_call_data["portCallId"]  # portCallId
    assert voyage[2] == sample_port_call_data["vesselTypeCode"]  # vesselTypeCode
    assert voyage[3] == sample_port_call_data["vesselName"]  # vesselName
    
    # Check arrivals table
    cursor.execute("SELECT * FROM arrivals WHERE portCallId = %s", (sample_port_call_data["portCallId"],))
    arrival = cursor.fetchone()
    
    assert arrival is not None
    assert arrival[1] == sample_port_call_data["portCallId"]  # portCallId
    assert arrival[5] == sample_port_call_data["vesselName"]  # vesselName

    cursor.close()

def test_data_consistency(test_db_connection, sample_port_call_data):
    """Test data consistency between tables."""
    # Process and save data
    results = process_query({"portCalls": [sample_port_call_data]})
    save_results_to_db(results)
    
    cursor = test_db_connection.cursor()
    
    # Get data from both tables
    cursor.execute("""
        SELECT v.portCallId, v.vesselName, v.portAreaName, a.ata, a.eta
        FROM voyages v
        JOIN arrivals a ON v.portCallId = a.portCallId
        WHERE v.portCallId = %s
    """, (sample_port_call_data["portCallId"],))
    
    row = cursor.fetchone()
    
    # Verify data consistency
    assert row is not None
    assert row[0] == sample_port_call_data["portCallId"]
    assert row[1] == sample_port_call_data["vesselName"]
    assert row[2] == sample_port_call_data["portAreaDetails"][0]["portAreaName"]
    
    cursor.close()

def test_error_handling(test_db_connection):
    """Test error handling in the flow."""
    # Test with invalid data
    invalid_data = {"portCalls": [{"invalid": "data"}]}
    
    # Should handle invalid data gracefully
    results = process_query(invalid_data)
    assert len(results) == 0
    
    # Test database connection error
    with patch('pg8000.connect', side_effect=Exception("Connection failed")):
        with pytest.raises(Exception) as exc_info:
            save_results_to_db(results)
        assert "Connection failed" in str(exc_info.value) 