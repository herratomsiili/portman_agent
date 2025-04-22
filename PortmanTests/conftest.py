# test that conf is loading

import pytest
import pg8000
import os

@pytest.fixture(scope="session")
def test_db_connection():
    """Create test database connection."""
    conn = pg8000.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
        database="portman"
    )
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def test_db_cursor(test_db_connection):
    """Create test database cursor."""
    cursor = test_db_connection.cursor()
    yield cursor
    cursor.close()

@pytest.fixture(scope="function")
def setup_test_tables(test_db_cursor):
    """Create test tables."""
    # Create voyages table
    test_db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS voyages (
            portCallId INTEGER PRIMARY KEY,
            imoLloyds INTEGER,
            vesselTypeCode TEXT,
            vesselName TEXT,
            prevPort TEXT,
            portToVisit TEXT,
            nextPort TEXT,
            agentName TEXT,
            shippingCompany TEXT,
            eta TIMESTAMP NULL,
            ata TIMESTAMP NULL,
            portAreaCode TEXT,
            portAreaName TEXT,
            berthCode TEXT,
            berthName TEXT,
            etd TIMESTAMP NULL,
            atd TIMESTAMP NULL,
            passengersOnArrival INTEGER DEFAULT 0,
            passengersOnDeparture INTEGER DEFAULT 0,
            crewOnArrival INTEGER DEFAULT 0,
            crewOnDeparture INTEGER DEFAULT 0,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create arrivals table
    test_db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS arrivals (
            id SERIAL PRIMARY KEY,
            portCallId INTEGER,
            eta TIMESTAMP NULL,
            old_ata TIMESTAMP NULL,
            ata TIMESTAMP NOT NULL,
            vesselName TEXT,
            portAreaName TEXT,
            berthName TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    yield

    # Clean up tables after tests
    test_db_cursor.execute("DROP TABLE IF EXISTS voyages")
    test_db_cursor.execute("DROP TABLE IF EXISTS arrivals")

@pytest.fixture
def sample_port_call_data():
    """Sample port call data for testing."""
    return {
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