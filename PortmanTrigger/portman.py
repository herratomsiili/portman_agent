import sqlite3
import requests
import pg8000
from datetime import datetime
import os
import argparse
import json
import glob
import natsort
import logging

from config import DATABASE_CONFIG, XML_CONVERTER_CONFIG
# Import the blob utilities
try:
    from PortmanTrigger.blob_utils import generate_blob_storage_link
except ImportError:
    try:
        # Try alternative import path
        from blob_utils import generate_blob_storage_link
    except ImportError:
        # Fallback definition if the module can't be imported
        def generate_blob_storage_link(blob_name, connection_string=None):
            log("Warning: generate_blob_storage_link function not available")
            return ""

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PortmanTrigger')

def log(message):
    logger.info(message)

def get_db_connection(dbName):
    """Establish and return a database connection to a specified database."""
    try:
        conn = pg8000.connect(
            database=dbName,
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"]
        )
        return conn
    except Exception as e:
        log(f"Error connecting to database '{dbName}': {e}")
        return None

def get_tracked_vessels():
    """Get IMO numbers to track from environment variables or command-line arguments."""
    parser = argparse.ArgumentParser(description="Portman Tracking Options")
    parser.add_argument("--imo", help="Comma-separated list of IMO numbers to track")
    args = parser.parse_args()

    # Read from command-line argument first
    if args.imo:
        tracked_set = set(map(int, args.imo.split(",")))
        log(f"Tracking vessels from CLI argument: {tracked_set}")
        return tracked_set

    # Fallback to environment variable
    tracked_env = os.getenv("TRACKED_VESSELS")
    if tracked_env:
        tracked_set = set(map(int, tracked_env.split(",")))
        log(f"Tracking vessels from ENV variable: {tracked_set}")
        return tracked_set

    log("No vessel filtering applied. Tracking all vessels.")
    return None  # No filtering if not set


def create_database_and_tables():
    """Create the database and the necessary tables if they don't exist."""
    try:
        log("Checking if database and tables exist...")

        # Connect to PostgreSQL system database to check existence
        conn = get_db_connection("postgres")
        if conn is None:
            return
        conn.autocommit = True
        cursor = conn.cursor()

        # Create database if it doesn't exist
        db_name = DATABASE_CONFIG["dbname"]
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        if not cursor.fetchone():
            log("Database '" +  db_name + "' does not exist. Creating...")
            cursor.execute(f"CREATE DATABASE {db_name};")
        cursor.close()
        conn.close()

        # Connect to the created database
        conn = get_db_connection(db_name)
        if conn is None:
            return
        cursor = conn.cursor()

        # Create the 'voyages' table
        create_voyages_table = """
        CREATE TABLE IF NOT EXISTS voyages (
            portCallId INTEGER PRIMARY KEY,
            imoLloyds INTEGER,
            mmsi INTEGER,
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
        );
        """
        cursor.execute(create_voyages_table)

        # Create the 'arrivals' table
        create_arrivals_table = """
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
        );
        """
        cursor.execute(create_arrivals_table)

        conn.commit()
        cursor.close()
        conn.close()
        log("Database and tables setup complete.")
    except Exception as e:
        log(f"Error setting up database and tables: {e}")

def update_database_schema():
    """Update database schema by adding new columns if they don't exist."""
    try:
        log("Checking for schema updates...")
        conn = get_db_connection(DATABASE_CONFIG["dbname"])
        if conn is None:
            return
        
        cursor = conn.cursor()
        
        # Check and update voyages table schema
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'voyages' AND table_schema = 'public'
        """)
        existing_columns = [row[0].lower() for row in cursor.fetchall()]
        log(f"Current columns in voyages table: {existing_columns}")
        
        # Add new columns to voyages table if they don't exist
        columns_to_add = {
            'noa_xml_url': 'TEXT DEFAULT NULL',
            'ata_xml_url': 'TEXT DEFAULT NULL',
            'vid_xml_url': 'TEXT DEFAULT NULL',
            'mmsi': 'INTEGER DEFAULT NULL'
        }
        
        for column_name, column_def in columns_to_add.items():
            if column_name.lower() not in existing_columns:
                log(f"Adding column '{column_name}' to voyages table")
                cursor.execute(f"ALTER TABLE voyages ADD COLUMN {column_name} {column_def};")
                conn.commit()
                # Verify the column was added successfully
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'voyages' AND column_name = %s AND table_schema = 'public'
                """, (column_name,))
                if cursor.fetchone():
                    log(f"Successfully added column '{column_name}' to voyages table")
                else:
                    log(f"Failed to add column '{column_name}' to voyages table. Will retry.")
                    try:
                        # Try one more time with a different approach
                        cursor.execute(f"ALTER TABLE voyages ADD COLUMN IF NOT EXISTS {column_name} {column_def};")
                        conn.commit()
                        log(f"Second attempt to add column '{column_name}' completed")
                    except Exception as inner_e:
                        log(f"Second attempt to add column '{column_name}' failed: {inner_e}")
        
        # Check and update arrivals table schema
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'arrivals' AND table_schema = 'public'
        """)
        existing_columns = [row[0].lower() for row in cursor.fetchall()]
        log(f"Current columns in arrivals table: {existing_columns}")
        
        # Add new columns to arrivals table if they don't exist
        columns_to_add = {
            'ata_xml_url': 'TEXT DEFAULT NULL'
        }
        
        for column_name, column_def in columns_to_add.items():
            if column_name.lower() not in existing_columns:
                log(f"Adding column '{column_name}' to arrivals table")
                cursor.execute(f"ALTER TABLE arrivals ADD COLUMN {column_name} {column_def};")
                conn.commit()
                # Verify the column was added successfully
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'arrivals' AND column_name = %s AND table_schema = 'public'
                """, (column_name,))
                if cursor.fetchone():
                    log(f"Successfully added column '{column_name}' to arrivals table")
                else:
                    log(f"Failed to add column '{column_name}' to arrivals table. Will retry.")
                    try:
                        # Try one more time with a different approach
                        cursor.execute(f"ALTER TABLE arrivals ADD COLUMN IF NOT EXISTS {column_name} {column_def};")
                        conn.commit()
                        log(f"Second attempt to add column '{column_name}' completed")
                    except Exception as inner_e:
                        log(f"Second attempt to add column '{column_name}' failed: {inner_e}")
        
        cursor.close()
        conn.close()
        log("Schema updates complete.")
    except Exception as e:
        log(f"Error updating database schema: {e}")

def parse_arguments():
    """Parse command-line arguments and environment variables."""
    parser = argparse.ArgumentParser(description="Portman JSON Input Options")
    parser.add_argument("--input-file", help="Path to a JSON input file")
    parser.add_argument("--input-dir", help="Directory containing JSON files (portnet*.json)")
    parser.add_argument("--imo", help="Comma-separated list of IMO numbers to track")
    args = parser.parse_args()

    return {
        "input_file": args.input_file or os.getenv("INPUT_FILE"),
        "input_dir": args.input_dir or os.getenv("INPUT_DIR"),
        "tracked_vessels": set(map(int, args.imo.split(","))) if args.imo else set(map(int, os.getenv("TRACKED_VESSELS", "").split(","))) if os.getenv("TRACKED_VESSELS") else None
    }

def get_json_source(input_file, input_dir, tracked_vessels):
    """Determine JSON data source: single file or directory of files."""
    if input_file:
        log(f"Reading JSON from file: {input_file}")
        return read_json_from_file(input_file)

    elif input_dir:
        log(f"Reading JSON files from directory: {input_dir}")
        read_json_from_directory(input_dir, tracked_vessels)  # Now processes files one by one
        return None  # Processing is already handled

    log("No input file or directory specified. Fetching from API instead.")
    return None  # Fallback to API fetching

def read_json_from_file(filepath):
    """Read JSON data from a specified file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        log(f"Error reading JSON file {filepath}: {e}")
        return None

def read_json_from_directory(directory, tracked_vessels, conn=None):
    """Read and process each JSON file separately, saving its data to the database."""
    try:
        file_pattern = os.path.join(directory, "portnet*.json")  # Match 'portnet*.json'
        files = glob.glob(file_pattern)
        sorted_files = natsort.natsorted(files)

        log(f"Found {len(sorted_files)} matching JSON files in {directory}: {sorted_files}")

        for filepath in sorted_files:
            try:
                log(f"Processing file: {filepath}")
                with open(filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)

                if "portCalls" in data and isinstance(data["portCalls"], list):
                    results = process_query(data, tracked_vessels)
                    save_results_to_db(results, conn)  # Save after processing each file
                    log(f"Finished processing {filepath}, {len(results)} voyages saved.")
                else:
                    log(f"Skipping file {filepath}: No valid 'portCalls' data found.")

            except Exception as e:
                log(f"Skipping file {filepath} due to error: {e}")

    except Exception as e:
        log(f"Error processing JSON directory {directory}: {e}")


def fetch_data_from_api():
    """Fetch JSON data from the API."""
    url = "https://meri.digitraffic.fi/api/port-call/v1/port-calls"
    log("Fetching data from the API...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        log("Data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        log(f"Error fetching data from API: {e}")
        return None

def process_query(data, tracked_vessels=None):
    """Process the JSON data and prepare results for database insertion."""
    if isinstance(data, dict) and "portCalls" in data:
        data = data["portCalls"]

    if not isinstance(data, list):
        log("Error: Expected a list of port calls in the JSON data.")
        return []

    log(f"Tracking only these vessels: {tracked_vessels}" if tracked_vessels else "Tracking all vessels.")

    results = []
    for entry in data:
        try:
            port_call_id = int(entry.get("portCallId"))  # Ensure it's always an integer
            #imo_number = int(entry.get("imoLloyds"))  # Ensure it's always an integer
        except (TypeError, ValueError):
            #log(f"Skipping entry with invalid portCallId {entry.get('portCallId')} or imoLloyds {entry.get('imoLloyds')}")
            log(f"Skipping entry with invalid portCallId {entry.get('portCallId')}")
            continue  # Skip invalid values

        imo_number = int(entry.get("imoLloyds")) if entry.get("imoLloyds") is not None else None  # Ensure it's always an integer
        mmsi = int(entry.get("mmsi")) if entry.get("mmsi") is not None else None  # Extract mmsi if available
        
        #log(f"Checking vessel {imo_number} with portCallId {port_call_id}...")  # Debugging

        # Skip if filtering is enabled and the IMO number is not in the list
        if tracked_vessels and imo_number not in tracked_vessels:
            #log(f"Skipping vessel {imo_number} (not in tracked list).")
            continue

        if tracked_vessels:
            log(f"Processing vessel {imo_number} with portCallId {port_call_id}...")  # Log vessel is being processed

        # Extract agentName & shippingCompany from agentInfo[]
        agent_name = None
        shipping_company = None
        for agent in entry.get("agentInfo", []):
            if agent.get("role") == 1:
                agent_name = agent.get("name")
            elif agent.get("role") == 2:
                shipping_company = agent.get("name")

        # Extract passengers & crew from imoInformation[]
        passengers_on_arrival = 0
        passengers_on_departure = 0
        crew_on_arrival = 0
        crew_on_departure = 0

        for imo in entry.get("imoInformation", []):
            if imo.get("imoGeneralDeclaration") == "Arrival":
                passengers_on_arrival = imo.get("numberOfPassangers", 0) or 0
                crew_on_arrival = imo.get("numberOfCrew", 0) or 0
            elif imo.get("imoGeneralDeclaration") == "Departure":
                passengers_on_departure = imo.get("numberOfPassangers", 0) or 0
                crew_on_departure = imo.get("numberOfCrew", 0) or 0

        # Extract timestamps & berth info from portAreaDetails[0]
        port_area_details = entry.get("portAreaDetails", [{}])
        first_area = port_area_details[0] if port_area_details else {}

        results.append({
            "portCallId": port_call_id,
            "portCallTimestamp": entry.get("portCallTimestamp"),
            "imoLloyds": imo_number if imo_number else 0,
            "mmsi": mmsi,  # Include mmsi in the results
            "vesselTypeCode": entry.get("vesselTypeCode"),
            "vesselName": entry.get("vesselName"),
            "radioCallSign": entry.get("radioCallSign", ""),  # Include radio call sign
            "prevPort": entry.get("prevPort"),
            "portToVisit": entry.get("portToVisit"),
            "nextPort": entry.get("nextPort"),
            "agentName": agent_name,
            "shippingCompany": shipping_company,
            "eta": first_area.get("eta"),
            "ata": first_area.get("ata"),
            "portAreaCode": first_area.get("portAreaCode"),
            "portAreaName": first_area.get("portAreaName"),
            "berthCode": first_area.get("berthCode"),
            "berthName": first_area.get("berthName"),
            "etd": first_area.get("etd"),
            "atd": first_area.get("atd"),
            "passengersOnArrival": passengers_on_arrival,
            "passengersOnDeparture": passengers_on_departure,
            "crewOnArrival": crew_on_arrival,
            "crewOnDeparture": crew_on_departure
        })
    log(f"Processed {len(results)} records.")
    return results

def createNoaXml(voyage_data):
    """Generate and store Notice of Arrival (NOA) XML document."""
    try:
        # Validate mandatory fields and data types
        required_fields = ["portCallId", "imoLloyds", "vesselName", "eta", "portAreaName"]
        for field in required_fields:
            if field not in voyage_data or voyage_data[field] is None:
                log(f"Cannot generate NOA XML: Missing required field '{field}' for portCallId {voyage_data.get('portCallId', 'unknown')}")
                return None
        
        # Convert numeric fields to strings to avoid NoneType issues
        for field in ["portCallId", "imoLloyds"]:
            if field in voyage_data and voyage_data[field] is not None:
                voyage_data[field] = str(voyage_data[field])
        
        # Store original portCallId for database operations
        original_port_call_id = voyage_data.get("portCallId")
        
        # Ensure string fields have proper values
        for field in ["vesselName", "portAreaName", "portToVisit", "prevPort", "berthName"]:
            if field in voyage_data and voyage_data[field] is None:
                voyage_data[field] = ""  # Replace None with empty string
        
        # Truncate IDs if needed to prevent validation errors (max 17 chars)
        if "portCallId" in voyage_data and len(str(voyage_data["portCallId"])) > 17:
            original_id = voyage_data["portCallId"]
            voyage_data["portCallId"] = str(voyage_data["portCallId"])[-17:]  # Keep the last 17 chars
            log(f"Warning: Truncated portCallId from {original_id} to {voyage_data['portCallId']} for XML compatibility")
            
        # Call the XML Storage Function
        xml_converterfunction_url = XML_CONVERTER_CONFIG["function_url"]
        xml_converter_function_key = XML_CONVERTER_CONFIG["function_key"]
        
        # Add the function key to the URL if it exists
        if xml_converter_function_key:
            if "?" in xml_converterfunction_url:
                xml_converterfunction_url += f"&code={xml_converter_function_key}"
            else:
                xml_converterfunction_url += f"?code={xml_converter_function_key}"
        
        log(f"Calling xml-converter for NOA: {xml_converterfunction_url}")

        # Send the voyage data to the function for NOA generation
        response = requests.post(
            xml_converterfunction_url,
            json={"portcall_data": voyage_data, "formality_type": "NOA"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            response_data = response.json()
            # Get SAS URL from the response (new format uses sasUrl instead of url)
            sas_url = response_data.get('sasUrl')
            
            if not sas_url:
                # Fallback to old response format if sasUrl is not found
                plain_url = response_data.get('url')
                if not plain_url:
                    log(f"No URL found in XML converter response for portCallId {voyage_data.get('portCallId')}")
                    return None
                    
                # Extract the blob name from the URL for SAS token generation
                try:
                    blob_path = plain_url.split('.net/')[1]  # Get container_name/blob_path
                except (IndexError, AttributeError):
                    log(f"Could not parse blob path from URL: {plain_url}")
                    blob_path = plain_url  # Fallback to using the URL as is
                
                # Generate the SAS URL using the shared utility function
                storage_connection_string = os.getenv("AzureWebJobsStorage")
                sas_url = generate_blob_storage_link(blob_path, storage_connection_string)
                
                if not sas_url:
                    log(f"Failed to generate SAS URL for blob: {blob_path}")
                    sas_url = plain_url  # Fallback to plain URL if SAS generation fails
            
            log(f"NOA XML for portCallId {voyage_data.get('portCallId')} successfully generated and stored.")
            
            # Store the XML URL in the voyages table
            try:
                conn = get_db_connection(DATABASE_CONFIG["dbname"])
                if conn is None:
                    log(f"Failed to connect to database when storing NOA XML URL")
                    return None
                
                cursor = conn.cursor()
                
                # Update the record with the NOA XML URL (use SAS URL if available)
                cursor.execute(
                    "UPDATE voyages SET noa_xml_url = %s WHERE portCallId = %s",
                    (sas_url, original_port_call_id)
                )
                
                affected = cursor.rowcount
                if affected > 0:
                    log(f"NOA XML URL (with SAS token) stored in voyages table for portCallId {original_port_call_id}")
                else:
                    log(f"No rows updated for portCallId {original_port_call_id}")
                
                conn.commit()
                cursor.close()
                conn.close()
                return sas_url
            except Exception as e:
                log(f"Error storing NOA XML URL in voyages table: {str(e)}")
        else:
            log(f"Error with NOA XML generation/storage for portCallId {voyage_data.get('portCallId')}: Status {response.status_code}")
            
    except Exception as e:
        log(f"Error triggering NOA XML function for portCallId {voyage_data.get('portCallId', 'unknown')}: {str(e)}")
    
    return None

def createArrivalXml(arrival_data):
    """Generate and store Actual Time of Arrival (ATA) XML document."""
    try:
        # Validate mandatory fields and data types
        required_fields = ["portCallId", "imoLloyds", "vesselName", "ata", "portAreaName"]
        for field in required_fields:
            if field not in arrival_data or arrival_data[field] is None:
                log(f"Cannot generate ATA XML: Missing required field '{field}' for portCallId {arrival_data.get('portCallId', 'unknown')}")
                return None
        
        # Convert numeric fields to strings to avoid NoneType issues
        for field in ["portCallId", "imoLloyds"]:
            if field in arrival_data and arrival_data[field] is not None:
                arrival_data[field] = str(arrival_data[field])
        
        # Ensure string fields have proper values
        for field in ["vesselName", "portAreaName", "portToVisit", "prevPort", "berthName"]:
            if field in arrival_data and arrival_data[field] is None:
                arrival_data[field] = ""  # Replace None with empty string
        
        # Truncate IDs if needed to prevent validation errors (max 17 chars)
        if "portCallId" in arrival_data and len(str(arrival_data["portCallId"])) > 17:
            original_id = arrival_data["portCallId"]
            arrival_data["portCallId"] = str(arrival_data["portCallId"])[-17:]  # Keep the last 17 chars
            log(f"Warning: Truncated portCallId from {original_id} to {arrival_data['portCallId']} for XML compatibility")
            
        # Call the XML Storage Function
        xml_converterfunction_url = XML_CONVERTER_CONFIG["function_url"]
        xml_converter_function_key = XML_CONVERTER_CONFIG["function_key"]
        
        # Add the function key to the URL if it exists
        if xml_converter_function_key:
            if "?" in xml_converterfunction_url:
                xml_converterfunction_url += f"&code={xml_converter_function_key}"
            else:
                xml_converterfunction_url += f"?code={xml_converter_function_key}"
        
        log(f"Calling xml-converter: {xml_converterfunction_url}")

        # Send the arrival data to the function
        response = requests.post(
            xml_converterfunction_url,
            json={"portcall_data": arrival_data, "formality_type": "ATA"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            response_data = response.json()
            # Get SAS URL from the response (new format uses sasUrl instead of url)
            sas_url = response_data.get('sasUrl')
            
            if not sas_url:
                # Fallback to old response format if sasUrl is not found
                plain_url = response_data.get('url')
                if not plain_url:
                    log(f"No URL found in XML converter response for portCallId {arrival_data.get('portCallId')}")
                    return None
                    
                # Extract the blob name from the URL for SAS token generation
                try:
                    blob_path = plain_url.split('.net/')[1]  # Get container_name/blob_path
                except (IndexError, AttributeError):
                    log(f"Could not parse blob path from URL: {plain_url}")
                    blob_path = plain_url  # Fallback to using the URL as is
                
                # Generate the SAS URL using the shared utility function
                storage_connection_string = os.getenv("AzureWebJobsStorage")
                sas_url = generate_blob_storage_link(blob_path, storage_connection_string)
                
                if not sas_url:
                    log(f"Failed to generate SAS URL for blob: {blob_path}")
                    sas_url = plain_url  # Fallback to plain URL if SAS generation fails
            
            log(f"ATA XML for portCallId {arrival_data.get('portCallId')} successfully generated and stored.")
            
            # Store the XML URL in the arrivals table
            try:
                conn = get_db_connection(DATABASE_CONFIG["dbname"])
                if conn is not None:
                    cursor = conn.cursor()
                    
                    # First find the ID of the most recent arrival record for this port call
                    cursor.execute(
                        "SELECT id FROM arrivals WHERE portCallId = %s ORDER BY id DESC LIMIT 1",
                        (arrival_data.get('portCallId'),)
                    )
                    
                    result = cursor.fetchone()
                    if result:
                        arrival_id = result[0]
                        # Then update that specific record with the SAS URL
                        cursor.execute(
                            "UPDATE arrivals SET ata_xml_url = %s WHERE id = %s",
                            (sas_url, arrival_id)
                        )
                        
                        # Also update the voyages table with the ATA XML URL
                        cursor.execute(
                            "UPDATE voyages SET ata_xml_url = %s WHERE portCallId = %s",
                            (sas_url, arrival_data.get('portCallId'))
                        )
                        
                        conn.commit()
                        log(f"XML URL (with SAS token) stored in arrivals and voyages tables for portCallId {arrival_data.get('portCallId')}")
                    else:
                        log(f"No arrival record found for portCallId {arrival_data.get('portCallId')}")
                    
                    cursor.close()
                    conn.close()
                    return sas_url  # Return the XML URL on success
            except Exception as e:
                log(f"Error storing XML URL in arrivals table: {str(e)}")
        else:
            log(f"Error with XML generation/storage for portCallId {arrival_data.get('portCallId')}: Status {response.status_code}")
            
    except Exception as e:
        log(f"Error triggering XML function for portCallId {arrival_data.get('portCallId', 'unknown')}: {str(e)}")
    
    return None  # Return None if unsuccessful

def createVidXml(voyage_data):
    """Generate and store Vessel Information Data (VID) XML document."""
    try:
        # Validate mandatory fields and data types
        required_fields = ["portCallId", "imoLloyds", "vesselName", "eta", "portAreaName"]
        for field in required_fields:
            if field not in voyage_data or voyage_data[field] is None:
                log(f"Cannot generate VID XML: Missing required field '{field}' for portCallId {voyage_data.get('portCallId', 'unknown')}")
                return None
        
        # Convert numeric fields to strings to avoid NoneType issues
        for field in ["portCallId", "imoLloyds", "mmsi"]:
            if field in voyage_data and voyage_data[field] is not None:
                voyage_data[field] = str(voyage_data[field])
        
        # Store original portCallId for database operations
        original_port_call_id = voyage_data.get("portCallId")
        
        # Ensure string fields have proper values
        for field in ["vesselName", "portAreaName", "portToVisit", "prevPort", "berthName", "radioCallSign"]:
            if field in voyage_data and voyage_data[field] is None:
                voyage_data[field] = ""  # Replace None with empty string
        
        # Truncate IDs if needed to prevent validation errors (max 17 chars)
        if "portCallId" in voyage_data and len(str(voyage_data["portCallId"])) > 17:
            original_id = voyage_data["portCallId"]
            voyage_data["portCallId"] = str(voyage_data["portCallId"])[-17:]  # Keep the last 17 chars
            log(f"Warning: Truncated portCallId from {original_id} to {voyage_data['portCallId']} for XML compatibility")
            
        # Call the XML Storage Function
        xml_converterfunction_url = XML_CONVERTER_CONFIG["function_url"]
        xml_converter_function_key = XML_CONVERTER_CONFIG["function_key"]
        
        # Add the function key to the URL if it exists
        if xml_converter_function_key:
            if "?" in xml_converterfunction_url:
                xml_converterfunction_url += f"&code={xml_converter_function_key}"
            else:
                xml_converterfunction_url += f"?code={xml_converter_function_key}"
        
        log(f"Calling xml-converter for VID: {xml_converterfunction_url}")

        # Send the voyage data to the function for VID generation
        response = requests.post(
            xml_converterfunction_url,
            json={"portcall_data": voyage_data, "formality_type": "VID"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            response_data = response.json()
            # Get SAS URL from the response (new format uses sasUrl instead of url)
            sas_url = response_data.get('sasUrl')
            
            if not sas_url:
                # Fallback to old response format if sasUrl is not found
                plain_url = response_data.get('url')
                if not plain_url:
                    log(f"No URL found in XML converter response for portCallId {voyage_data.get('portCallId')}")
                    return None
                    
                # Extract the blob name from the URL for SAS token generation
                try:
                    blob_path = plain_url.split('.net/')[1]  # Get container_name/blob_path
                except (IndexError, AttributeError):
                    log(f"Could not parse blob path from URL: {plain_url}")
                    blob_path = plain_url  # Fallback to using the URL as is
                
                # Generate the SAS URL using the shared utility function
                storage_connection_string = os.getenv("AzureWebJobsStorage")
                sas_url = generate_blob_storage_link(blob_path, storage_connection_string)
                
                if not sas_url:
                    log(f"Failed to generate SAS URL for blob: {blob_path}")
                    sas_url = plain_url  # Fallback to plain URL if SAS generation fails
            
            log(f"VID XML for portCallId {voyage_data.get('portCallId')} successfully generated and stored.")
            
            # Store the XML URL in the voyages table
            try:
                conn = get_db_connection(DATABASE_CONFIG["dbname"])
                if conn is None:
                    log(f"Failed to connect to database when storing VID XML URL")
                    return None
                
                cursor = conn.cursor()
                
                # Update the record with the VID XML URL (use SAS URL if available)
                cursor.execute(
                    "UPDATE voyages SET vid_xml_url = %s WHERE portCallId = %s",
                    (sas_url, original_port_call_id)
                )
                
                affected = cursor.rowcount
                if affected > 0:
                    log(f"VID XML URL (with SAS token) stored in voyages table for portCallId {original_port_call_id}")
                else:
                    log(f"No rows updated for portCallId {original_port_call_id}")
                
                conn.commit()
                cursor.close()
                conn.close()
                return sas_url
            except Exception as e:
                log(f"Error storing VID XML URL in voyages table: {str(e)}")
        else:
            log(f"Error with VID XML generation/storage for portCallId {voyage_data.get('portCallId')}: Status {response.status_code}")
            
    except Exception as e:
        log(f"Error triggering VID XML function for portCallId {voyage_data.get('portCallId', 'unknown')}: {str(e)}")
    
    return None

def diagnose_database_structure():
    """Diagnose database structure to help identify issues with XML URL storage."""
    try:
        log("Diagnosing database structure...")
        conn = get_db_connection(DATABASE_CONFIG["dbname"])
        if conn is None:
            log("Cannot diagnose database - connection failed")
            return
        
        cursor = conn.cursor()
        
        # Check voyages table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'voyages' AND table_schema = 'public'
        """)
        columns = cursor.fetchall()
        
        log("Voyages table structure:")
        for col in columns:
            log(f"  Column: {col[0]}, Type: {col[1]}")
        
        cursor.close()
        conn.close()
        log("Database diagnosis complete.")
    except Exception as e:
        log(f"Error diagnosing database structure: {str(e)}")

def save_results_to_db(results, conn=None):
    """Save processed results into the 'voyages' table and trigger arrivals only when `ata` is updated at the minute level."""
    try:
        log(f"Saving {len(results)} records to the database...")
        connection_managed_elsewhere = conn is not None

        if conn is None:
            conn = get_db_connection(DATABASE_CONFIG["dbname"])
            if conn is None:
                raise Exception("Failed to connect to database")

        cursor = conn.cursor()

        new_arrival_count = 0   # Track the count of new arrivals
        new_eta_count = 0       # Track the count of new eta timestamps for NOA generation
        new_voyage_count = 0    # Track count of new voyages for VID generation
        updated_voyage_count = 0 # Track count of updated existing voyages

        # Extract unique portCallIds from JSON data
        port_call_ids = list(set(entry["portCallId"] for entry in results))

        # Fetch all old ata values and existing port calls in one query
        old_ata_map = {}
        old_eta_map = {}
        existing_port_calls = set()
        if port_call_ids:
            # Detect if using SQLite
            is_sqlite = isinstance(conn, sqlite3.Connection)
            placeholder = "?" if is_sqlite else "%s"

            # Fetch old ATA, ETA values and port call IDs using proper placeholders
            port_call_ids = list(set(entry["portCallId"] for entry in results))
            query = f"""
                SELECT portCallId, ata, eta FROM voyages WHERE portCallId IN ({','.join([placeholder] * len(port_call_ids))});
            """
            cursor.execute(query, tuple(port_call_ids))

            fetched_data = cursor.fetchall()

            # Populate maps with data
            for row in fetched_data:
                port_call_id, old_ata, old_eta = row
                existing_port_calls.add(int(port_call_id))
                if old_ata:  # Only store valid timestamps
                    old_ata_map[int(port_call_id)] = old_ata.strftime("%Y-%m-%dT%H:%M:00.000Z")  # Normalize to minute level
                if old_eta:  # Store valid ETA timestamps
                    old_eta_map[int(port_call_id)] = old_eta.strftime("%Y-%m-%dT%H:%M:00.000Z")  # Normalize to minute level

        for entry in results:
            port_call_id = int(entry["portCallId"])  # Ensure it's stored as an integer
            imo_number = int(entry["imoLloyds"]) if entry["imoLloyds"] is not None else None  # Ensure it's always an integer
            mmsi = int(entry["mmsi"]) if entry.get("mmsi") is not None else None  # Get mmsi if available
            
            new_ata = entry["ata"]
            if new_ata:
                new_ata = datetime.strptime(new_ata, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%dT%H:%M:00.000Z")  # Normalize

            new_eta = entry["eta"]
            if new_eta:
                new_eta = datetime.strptime(new_eta, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%dT%H:%M:00.000Z")  # Normalize

            # Fetch old values from the maps (default to None)
            old_ata = old_ata_map.get(port_call_id, None)
            old_eta = old_eta_map.get(port_call_id, None)

            # Check if this is a new port call that needs VID
            is_new_port_call = port_call_id not in existing_port_calls

            # Determine operation - new insert or update existing
            if is_new_port_call:
                # For new port calls, use INSERT
                insert_query = f"""
                INSERT INTO voyages (portCallId, imoLloyds, mmsi, vesselTypeCode, vesselName, prevPort,
                    portToVisit, nextPort, agentName, shippingCompany, eta, ata, portAreaCode,
                    portAreaName, berthCode, berthName, etd, atd,
                    passengersOnArrival, passengersOnDeparture, crewOnArrival, crewOnDeparture,
                    modified)
                VALUES ({','.join([placeholder] * 22)}, CURRENT_TIMESTAMP)
                RETURNING portCallId;
                """
                
                cursor.execute(insert_query, (
                    port_call_id, imo_number, mmsi, entry["vesselTypeCode"], entry["vesselName"],
                    entry["prevPort"], entry["portToVisit"], entry["nextPort"], entry["agentName"],
                    entry["shippingCompany"], entry["eta"], new_ata, entry["portAreaCode"], entry["portAreaName"],
                    entry["berthCode"], entry["berthName"], entry["etd"], entry["atd"],
                    entry["passengersOnArrival"], entry["passengersOnDeparture"], entry["crewOnArrival"],
                    entry["crewOnDeparture"]
                ))
                
                new_voyage_count += 1
            else:
                # For existing port calls, use UPDATE
                update_query = f"""
                UPDATE voyages SET
                    imoLloyds = %s,
                    mmsi = %s,
                    vesselTypeCode = %s,
                    vesselName = %s,
                    prevPort = %s,
                    portToVisit = %s,
                    nextPort = %s,
                    agentName = %s,
                    shippingCompany = %s,
                    eta = %s,
                    ata = %s,
                    portAreaCode = %s,
                    portAreaName = %s,
                    berthCode = %s,
                    berthName = %s,
                    etd = %s,
                    atd = %s,
                    passengersOnArrival = %s,
                    passengersOnDeparture = %s,
                    crewOnArrival = %s,
                    crewOnDeparture = %s,
                    modified = CURRENT_TIMESTAMP
                WHERE portCallId = %s
                """
                
                cursor.execute(update_query, (
                    imo_number, mmsi, entry["vesselTypeCode"], entry["vesselName"],
                    entry["prevPort"], entry["portToVisit"], entry["nextPort"], entry["agentName"],
                    entry["shippingCompany"], entry["eta"], new_ata, entry["portAreaCode"], entry["portAreaName"],
                    entry["berthCode"], entry["berthName"], entry["etd"], entry["atd"],
                    entry["passengersOnArrival"], entry["passengersOnDeparture"], entry["crewOnArrival"],
                    entry["crewOnDeparture"], port_call_id
                ))
                
                updated_voyage_count += 1

            # Generate VID XML for new port calls with ETA data
            if is_new_port_call and entry.get("eta"):
                log(f"New port call detected for portCallId {port_call_id}. Generating VID-XML.")
                
                # IMPORTANT: Commit the transaction to ensure the new record is stored
                # before generating the XML
                conn.commit()
                
                # Prepare data for VID XML generation, ensuring no None values
                vid_data = {
                    "portCallId": port_call_id,
                    "imoLloyds": imo_number,
                    "mmsi": mmsi,  # Include mmsi for VID generation
                    "vesselName": entry.get("vesselName") or "",
                    "eta": entry.get("eta") or "",
                    "portAreaCode": entry.get("portAreaCode") or "",
                    "portAreaName": entry.get("portAreaName") or "",
                    "berthCode": entry.get("berthCode") or "", 
                    "berthName": entry.get("berthName") or "",
                    "passengersOnArrival": entry.get("passengersOnArrival") or 0,
                    "crewOnArrival": entry.get("crewOnArrival") or 0,
                    "portToVisit": entry.get("portToVisit") or "",
                    "prevPort": entry.get("prevPort") or "",
                    "agentName": entry.get("agentName") or "",
                    "shippingCompany": entry.get("shippingCompany") or "",
                    "radioCallSign": entry.get("radioCallSign", "")
                }
                
                # Generate and store the VID XML
                createVidXml(vid_data)

            # Generate NOA XML when ETA changes are detected
            if old_eta is not None and old_eta != new_eta and new_eta is not None:
                log(f"ETA change detected for portCallId {port_call_id}. Generating NOA-XML.")
                log(f"Old ETA: {old_eta}, New ETA: {new_eta}")
                
                # Commit to ensure all changes are saved
                conn.commit()
                
                # Prepare data for NOA XML generation
                noa_data = {
                    "portCallId": port_call_id,
                    "imoLloyds": imo_number,
                    "mmsi": mmsi,
                    "vesselName": entry.get("vesselName") or "",
                    "eta": new_eta,
                    "etd": entry.get("etd"),
                    "portAreaCode": entry.get("portAreaCode") or "",
                    "portAreaName": entry.get("portAreaName") or "",
                    "berthCode": entry.get("berthCode") or "", 
                    "berthName": entry.get("berthName") or "",
                    "passengersOnArrival": entry.get("passengersOnArrival") or 0,
                    "crewOnArrival": entry.get("crewOnArrival") or 0,
                    "portToVisit": entry.get("portToVisit") or "",
                    "prevPort": entry.get("prevPort") or "",
                    "agentName": entry.get("agentName") or "",
                    "shippingCompany": entry.get("shippingCompany") or ""
                }
                
                # Generate and store the NOA XML
                noa_url = createNoaXml(noa_data)
                if noa_url:
                    new_eta_count += 1
                    log(f"NOA XML generated for portCallId {port_call_id} due to ETA change")

            # Generate ATA XML for arrivals with updated ATA
            if old_ata != new_ata and new_ata is not None:
                insert_arrival_query = f"""
                INSERT INTO arrivals (portCallId, eta, old_ata, ata, vesselName, portAreaName, berthName, created)
                VALUES ({','.join([placeholder] * 7)}, CURRENT_TIMESTAMP);
                """
                cursor.execute(insert_arrival_query, (
                    port_call_id, entry["eta"], old_ata, new_ata,
                    entry["vesselName"], entry["portAreaName"], entry["berthName"]
                ))
                
                # Commit the arrival record before XML generation
                conn.commit()
                
                new_arrival_count += 1
                print(
                    f"-----------------------------\n"
                    f"Port Call ID: {port_call_id}\n"
                    f"Port Call Time Stamp: {entry['portCallTimestamp']}\n\n"
                    f"Aluksen IMO/nimi: {imo_number}/{entry['vesselName']}\n"
                    f"Aluksen MMSI: {mmsi}\n\n"
                    f"Satamakoodi: {entry['portToVisit']}\n"
                    f"Satama: {entry['portAreaName']}\n"
                    f"Laituri: {entry['berthName']}\n\n"
                    f"Saapuminen\n"
                    f"Arvioitu saapumisaika (UTC): {datetime.strptime(entry['eta'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M') if entry.get('eta') else 'N/A'}\n"
                    f"Toteutunut saapumisaika (UTC): {datetime.strptime(new_ata, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M') if new_ata else 'N/A'}\n"
                    f"Miehistön lukumäärä: {entry['crewOnArrival']}\n"
                    f"Matkustajien lukumäärä: {entry['passengersOnArrival']}\n\n"
                    f"Lähtö\n"
                    f"Arvioitu lähtöaika (UTC): {datetime.strptime(entry['etd'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M') if entry.get('etd') else 'N/A'}\n"
                    f"Toteutunut lähtöaika (UTC): {datetime.strptime(entry['atd'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M') if entry.get('atd') else 'N/A'}\n"
                    f"Miehistön lukumäärä: {entry['crewOnDeparture']}\n"
                    f"Matkustajien lukumäärä: {entry['passengersOnDeparture']}\n"
                )
                
                # Prepare data for ATA XML generation, ensuring no None values
                ata_data = {
                    "portCallId": port_call_id,
                    "imoLloyds": imo_number,
                    "mmsi": mmsi,  # Include mmsi for ATA generation
                    "vesselName": entry.get("vesselName") or "",
                    "eta": entry.get("eta") or "",
                    "ata": new_ata,
                    "portAreaCode": entry.get("portAreaCode") or "",
                    "portAreaName": entry.get("portAreaName") or "",
                    "berthCode": entry.get("berthCode") or "", 
                    "berthName": entry.get("berthName") or "",
                    "passengersOnArrival": entry.get("passengersOnArrival") or 0,
                    "crewOnArrival": entry.get("crewOnArrival") or 0,
                    "portToVisit": entry.get("portToVisit") or "",
                    "prevPort": entry.get("prevPort") or "",
                    "agentName": entry.get("agentName") or "",
                    "shippingCompany": entry.get("shippingCompany") or ""
                }
                
                createArrivalXml(ata_data)

        # Final commit at the end of processing all records
        conn.commit()
        cursor.close()
        if not connection_managed_elsewhere:
            conn.close()
        log(f"{len(results)} records saved/updated in the database.")
        log(f"Total new voyages: {new_voyage_count}, updated voyages: {updated_voyage_count}, new arrivals: {new_arrival_count}, eta updated: {new_eta_count}")

    except Exception as e:
        log(f"Error saving results to the database: {e}")
        raise  # Re-raise the exception to be caught by the test

def main(req=None):
    log("Program started.")
    create_database_and_tables()
    update_database_schema()
    
    # Parse CLI arguments and environment variables
    args = {}
    if req:
        req.params.get("input-file"), req.params.get("input-dir"), req.params.get("imo")
        args = {
            "input_file": req.params.get("input-file"),
            "input_dir": req.params.get("input-dir"),
            "tracked_vessels": set(map(int, req.params.get("imo").split(","))) if req.params.get("imo") else None
        }

    # Process JSON from input file or directory
    data = None
    if args and (args["input_file"] or args["input_dir"]):
        data = get_json_source(args["input_file"], args["input_dir"], args["tracked_vessels"])
    else:
        # If no file/directory is specified, fetch data from API
        log("No input file or directory specified. Fetching from API...")
        data = fetch_data_from_api()

    if data:
        if args:
            results = process_query(data, args["tracked_vessels"])
        else:
            results = process_query(data)
        save_results_to_db(results)
    else:
        log("No data available to process.")

    log("Program completed.")
