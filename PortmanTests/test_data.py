import os
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta

def create_test_data():
    """Populate the test database with initial data."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    
    try:
        with conn.cursor() as cur:
            # Create test voyages
            now = datetime.utcnow()
            voyages = [
                (3190880, 9606900, 230629000, '20', 'Viking Grace', 'FIMHQ', 'FITKU', 'FILAN',
                 'Viking Line Abp / Helsinki', 'Viking Line Abp', now + timedelta(hours=24), None, 'PASSE', 'Matkustajasatama',
                 'v1', 'viking1', now + timedelta(hours=48), None, 235, 188, 1849, 1346),
                (3191032, 9827877, 230041000, '20', 'Viking Glory', 'FILAN', 'FITKU', 'FIMHQ',
                 'Viking Line Abp / Helsinki', 'Viking Line Abp', now, now, 'PASSE', 'Matkustajasatama',
                 'v1', 'viking1', now + timedelta(hours=24), None, 223, 185, 1265, 662),
                (3194267, 9354284, 230639000, '20', 'Baltic Princess', 'FIMHQ', 'FITKU', 'FILAN',
                 'Tallink Silja Oy', 'Tallink Silja Oy', now + timedelta(hours=48), None, 'PASSE', 'Matkustajasatama',
                 's2', 'silja2', now + timedelta(hours=72), None, 241, 171, 1147, 607)
            ]
            execute_values(
                cur,
                """
                INSERT INTO voyages (
                    portCallId, imoLloyds, mmsi, vesselTypeCode, vesselName, prevPort, portToVisit, nextPort,
                    agentName, shippingCompany, eta, ata, portAreaCode, portAreaName, berthCode, berthName,
                    etd, atd, crewOnArrival, crewOnDeparture, passengersOnArrival, passengersOnDeparture
                )
                VALUES %s
                ON CONFLICT (portCallId) DO NOTHING
                """,
                voyages
            )

            # Create test arrivals
            arrivals = [
                (3190880, now + timedelta(hours=24), None, now + timedelta(hours=24), 'Viking Grace', 'Matkustajasatama', 'viking1'),
                (3191032, now, None, now, 'Viking Glory', 'Matkustajasatama', 'viking1'),
                (3194267, now + timedelta(hours=48), None, now + timedelta(hours=48), 'Baltic Princess', 'Matkustajasatama', 'silja2')
            ]
            execute_values(
                cur,
                """
                INSERT INTO arrivals (
                    portCallId, eta, old_ata, ata, vesselName, portAreaName, berthName
                )
                VALUES %s
                ON CONFLICT (id) DO NOTHING
                """,
                arrivals
            )

        conn.commit()
        print("Test data created successfully")
    except Exception as e:
        print(f"Error creating test data: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_test_data()
