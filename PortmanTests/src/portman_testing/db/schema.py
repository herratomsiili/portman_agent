"""
Database schema definitions for Portman Agent testing.

This module provides SQL statements for creating test database tables
and generating test data for the Portman Agent.
"""

from typing import List, Optional
from datetime import datetime, timedelta
import random
import json

# SQL for creating voyages table
VOYAGES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS voyages (
    id SERIAL PRIMARY KEY,
    vessel_name VARCHAR(255) NOT NULL,
    vessel_imo VARCHAR(20) NOT NULL,
    vessel_mmsi VARCHAR(20),
    port_locode VARCHAR(10) NOT NULL,
    port_name VARCHAR(255) NOT NULL,
    berth_code VARCHAR(20),
    berth_name VARCHAR(255),
    eta TIMESTAMP WITH TIME ZONE,
    etd TIMESTAMP WITH TIME ZONE,
    ata TIMESTAMP WITH TIME ZONE,
    atd TIMESTAMP WITH TIME ZONE,
    passenger_count INTEGER,
    crew_count INTEGER,
    prev_port_locode VARCHAR(10),
    prev_port_name VARCHAR(255),
    next_port_locode VARCHAR(10),
    next_port_name VARCHAR(255),
    port_call_id VARCHAR(50) UNIQUE,
    port_call_status VARCHAR(20),
    cargo_description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_voyages_vessel_imo ON voyages(vessel_imo);
CREATE INDEX IF NOT EXISTS idx_voyages_port_locode ON voyages(port_locode);
CREATE INDEX IF NOT EXISTS idx_voyages_eta ON voyages(eta);
"""

# SQL for creating arrivals table
ARRIVALS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS arrivals (
    id SERIAL PRIMARY KEY,
    vessel_imo VARCHAR(20) NOT NULL,
    port_call_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    previous_eta TIMESTAMP WITH TIME ZONE,
    current_eta TIMESTAMP WITH TIME ZONE,
    eta_change_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_arrivals_vessel_imo ON arrivals(vessel_imo);
CREATE INDEX IF NOT EXISTS idx_arrivals_port_call_id ON arrivals(port_call_id);
"""

def get_vessel_name(imo: str) -> str:
    """
    Generate a realistic vessel name based on IMO number.

    Args:
        imo: IMO number of the vessel

    Returns:
        A vessel name
    """
    # Use last digits of IMO to deterministically generate a name
    vessel_prefixes = ["MS", "MV", "SS", "MT", "MY"]
    vessel_names = [
        "Nordic", "Baltic", "Atlantic", "Pacific", "Arctic",
        "Explorer", "Voyager", "Discovery", "Navigator", "Mariner",
        "Princess", "Queen", "Star", "Sun", "Moon",
        "Horizon", "Aurora", "Borealis", "Polaris", "Orion"
    ]
    vessel_suffixes = ["I", "II", "III", "IV", "V", "", "", "", "", ""]

    # Use IMO to deterministically select name components
    seed = int(imo[-3:])
    random.seed(seed)

    prefix = vessel_prefixes[seed % len(vessel_prefixes)]
    name = vessel_names[seed % len(vessel_names)]
    suffix = vessel_suffixes[seed % len(vessel_suffixes)]

    return f"{prefix} {name} {suffix}".strip()

def get_test_data_sql(imo_numbers: Optional[List[str]] = None) -> str:
    """
    Generate SQL statements to insert test data into the database.

    Args:
        imo_numbers: List of IMO numbers to include in test data

    Returns:
        SQL statements for inserting test data
    """
    if not imo_numbers:
        imo_numbers = [f"9{str(i).zfill(6)}" for i in range(1, 6)]

    # Ports data
    ports = [
        {"locode": "FIHEL", "name": "Helsinki"},
        {"locode": "FITUR", "name": "Turku"},
        {"locode": "FIKTK", "name": "Kotka"},
        {"locode": "FIHKO", "name": "Hanko"},
        {"locode": "FIPOR", "name": "Pori"},
        {"locode": "FIRAU", "name": "Rauma"},
        {"locode": "FIOUL", "name": "Oulu"},
        {"locode": "FIVAA", "name": "Vaasa"},
        {"locode": "SESTU", "name": "Stockholm"},
        {"locode": "EEMUG", "name": "Muuga"},
        {"locode": "LVRIX", "name": "Riga"},
        {"locode": "DEHAM", "name": "Hamburg"},
        {"locode": "PLGDY", "name": "Gdynia"},
        {"locode": "DKAAR", "name": "Aarhus"}
    ]

    # Generate SQL statements
    sql_statements = []

    # For each IMO number, generate voyage and arrival data
    for imo in imo_numbers:
        vessel_name = get_vessel_name(imo)
        mmsi = f"23{imo[2:8]}"

        # Generate 5 voyages per vessel
        for i in range(5):
            # Select random ports
            port_idx = random.randint(0, len(ports) - 1)
            current_port = ports[port_idx]

            prev_port_idx = (port_idx - 1) % len(ports)
            prev_port = ports[prev_port_idx]

            next_port_idx = (port_idx + 1) % len(ports)
            next_port = ports[next_port_idx]

            # Generate timestamps
            base_time = datetime.now() - timedelta(days=30) + timedelta(days=i*7)
            eta = base_time - timedelta(hours=random.randint(1, 24))
            etd = base_time + timedelta(hours=random.randint(12, 48))
            ata = base_time
            atd = base_time + timedelta(hours=random.randint(6, 36))

            # Generate berth information
            berth_number = random.randint(1, 9)
            berth_code = f"{current_port['locode']}-B{berth_number}"
            berth_name = f"Berth {berth_number}"

            # Generate passenger and crew counts
            passenger_count = random.randint(0, 2000)
            crew_count = random.randint(10, 100)

            # Generate port call ID and status
            port_call_id = f"PORT-{random.randint(100000, 999999)}"
            port_call_status = random.choice(["ACTIVE", "COMPLETED", "PLANNED"])

            # Generate cargo description
            cargo_description = random.choice([
                "General cargo", "Containers", "Bulk cargo", "Vehicles",
                "Passengers", "Oil products", "Chemicals", "LNG"
            ])

            # Create SQL for voyage insert
            voyage_sql = f"""
            INSERT INTO voyages (
                vessel_name, vessel_imo, vessel_mmsi, port_locode, port_name,
                berth_code, berth_name, eta, etd, ata, atd,
                passenger_count, crew_count, prev_port_locode, prev_port_name,
                next_port_locode, next_port_name, port_call_id, port_call_status,
                cargo_description
            ) VALUES (
                '{vessel_name}', '{imo}', '{mmsi}', '{current_port['locode']}', '{current_port['name']}',
                '{berth_code}', '{berth_name}', '{eta.isoformat()}', '{etd.isoformat()}', '{ata.isoformat()}', '{atd.isoformat()}',
                {passenger_count}, {crew_count}, '{prev_port['locode']}', '{prev_port['name']}',
                '{next_port['locode']}', '{next_port['name']}', '{port_call_id}', '{port_call_status}',
                '{cargo_description}'
            );
            """
            sql_statements.append(voyage_sql)

            # Generate 2-3 arrival updates per voyage
            num_arrivals = random.randint(2, 3)
            for j in range(num_arrivals):
                # Generate timestamps for arrival updates
                timestamp = eta - timedelta(days=num_arrivals-j)
                previous_eta = eta - timedelta(hours=random.randint(1, 6))
                current_eta = eta
                eta_change_minutes = int((current_eta - previous_eta).total_seconds() / 60)

                # Create SQL for arrival insert
                arrival_sql = f"""
                INSERT INTO arrivals (
                    vessel_imo, port_call_id, timestamp, previous_eta, current_eta, eta_change_minutes
                ) VALUES (
                    '{imo}', '{port_call_id}', '{timestamp.isoformat()}', '{previous_eta.isoformat()}', '{current_eta.isoformat()}', {eta_change_minutes}
                );
                """
                sql_statements.append(arrival_sql)

    return "\n".join(sql_statements)

def get_sample_voyage_data(imo: str) -> dict:
    """
    Generate a sample voyage data dictionary for testing.

    Args:
        imo: IMO number of the vessel

    Returns:
        Dictionary containing sample voyage data
    """
    vessel_name = get_vessel_name(imo)
    mmsi = f"23{imo[2:8]}"

    # Select random port
    ports = [
        {"locode": "FIHEL", "name": "Helsinki"},
        {"locode": "FITUR", "name": "Turku"},
        {"locode": "FIKTK", "name": "Kotka"}
    ]
    current_port = random.choice(ports)
    prev_port = random.choice([p for p in ports if p != current_port])
    next_port = random.choice([p for p in ports if p != current_port and p != prev_port])

    # Generate timestamps
    base_time = datetime.now()
    eta = base_time - timedelta(hours=random.randint(1, 24))
    etd = base_time + timedelta(hours=random.randint(12, 48))
    ata = base_time
    atd = base_time + timedelta(hours=random.randint(6, 36))

    # Generate berth information
    berth_number = random.randint(1, 9)
    berth_code = f"{current_port['locode']}-B{berth_number}"
    berth_name = f"Berth {berth_number}"

    return {
        "vessel_name": vessel_name,
        "vessel_imo": imo,
        "vessel_mmsi": mmsi,
        "port_locode": current_port["locode"],
        "port_name": current_port["name"],
        "berth_code": berth_code,
        "berth_name": berth_name,
        "eta": eta.isoformat(),
        "etd": etd.isoformat(),
        "ata": ata.isoformat(),
        "atd": atd.isoformat(),
        "passenger_count": random.randint(0, 2000),
        "crew_count": random.randint(10, 100),
        "prev_port_locode": prev_port["locode"],
        "prev_port_name": prev_port["name"],
        "next_port_locode": next_port["locode"],
        "next_port_name": next_port["name"],
        "port_call_id": f"PORT-{random.randint(100000, 999999)}",
        "port_call_status": random.choice(["ACTIVE", "COMPLETED", "PLANNED"]),
        "cargo_description": random.choice([
            "General cargo", "Containers", "Bulk cargo", "Vehicles",
            "Passengers", "Oil products", "Chemicals", "LNG"
        ])
    }

def get_sample_arrival_data(imo: str, port_call_id: str) -> dict:
    """
    Generate a sample arrival data dictionary for testing.

    Args:
        imo: IMO number of the vessel
        port_call_id: Port call ID

    Returns:
        Dictionary containing sample arrival data
    """
    # Generate timestamps
    base_time = datetime.now()
    previous_eta = base_time - timedelta(hours=random.randint(1, 6))
    current_eta = base_time
    eta_change_minutes = int((current_eta - previous_eta).total_seconds() / 60)

    return {
        "vessel_imo": imo,
        "port_call_id": port_call_id,
        "timestamp": base_time.isoformat(),
        "previous_eta": previous_eta.isoformat(),
        "current_eta": current_eta.isoformat(),
        "eta_change_minutes": eta_change_minutes
    }
