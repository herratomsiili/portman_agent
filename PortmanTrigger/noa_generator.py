import logging
import json
import azure.functions as func
import pg8000
from config import DATABASE_CONFIG, XML_CONVERTER_CONFIG
import requests
import os
from datetime import datetime

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
        logging.error(f"Error connecting to database '{dbName}': {e}")
        return None

def get_voyage_data(portCallId):
    """Get voyage data from the database based on portCallId."""
    try:
        conn = get_db_connection(DATABASE_CONFIG["dbname"])
        if conn is None:
            return None
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                portCallId, imoLloyds, vesselName, eta, portAreaCode, portAreaName, 
                berthCode, berthName, passengersOnArrival, crewOnArrival, 
                portToVisit, prevPort, agentName, shippingCompany
            FROM voyages 
            WHERE portCallId = %s
        """, (portCallId,))
        
        row = cursor.fetchone()
        if not row:
            logging.error(f"No voyage found with portCallId {portCallId}")
            cursor.close()
            conn.close()
            return None
        
        # Map database columns to dictionary
        columns = [
            "portCallId", "imoLloyds", "vesselName", "eta", "portAreaCode", "portAreaName", 
            "berthCode", "berthName", "passengersOnArrival", "crewOnArrival", 
            "portToVisit", "prevPort", "agentName", "shippingCompany"
        ]
        
        # Create dictionary from query results
        voyage_data = {columns[i]: row[i] for i in range(len(columns))}
        
        cursor.close()
        conn.close()
        return voyage_data
    except Exception as e:
        logging.error(f"Error fetching voyage data: {e}")
        return None

def update_noa_xml_url(portCallId, xml_url):
    """Update the NOA XML URL in the voyages table."""
    try:
        conn = get_db_connection(DATABASE_CONFIG["dbname"])
        if conn is None:
            return False
        
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE voyages SET noa_xml_url = %s WHERE portCallId = %s",
            (xml_url, portCallId)
        )
        
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected > 0:
            logging.info(f"NOA XML URL updated for portCallId {portCallId}")
            return True
        else:
            logging.error(f"No rows updated for portCallId {portCallId}")
            return False
    except Exception as e:
        logging.error(f"Error updating NOA XML URL: {e}")
        return False

def noa_generator(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function to generate NOA XML for a specified port call.
    
    Args:
        req: The HTTP request object containing portCallId parameter.
        
    Returns:
        func.HttpResponse: The HTTP response containing operation status and SAS URL if successful.
    """
    logging.info('NOA Generator function processing a request')
    
    # Get portCallId from query parameter or request body
    portCallId = req.params.get('portCallId')
    if not portCallId:
        try:
            req_body = req.get_json()
            portCallId = req_body.get('portCallId')
        except ValueError:
            pass
    
    if not portCallId:
        return func.HttpResponse(
            "Please provide a portCallId parameter",
            status_code=400
        )
    
    # Get voyage data from database
    voyage_data = get_voyage_data(portCallId)
    if not voyage_data:
        return func.HttpResponse(
            f"No voyage found with portCallId {portCallId}",
            status_code=404
        )
    
    # Convert numeric fields to strings to avoid NoneType issues
    for field in ["portCallId", "imoLloyds"]:
        if field in voyage_data and voyage_data[field] is not None:
            voyage_data[field] = str(voyage_data[field])
    
    # Convert datetime fields to ISO format strings to make them JSON serializable
    for field in ["eta", "ata", "etd", "atd"]:
        if field in voyage_data and voyage_data[field] is not None:
            # Check if it's already a string
            if not isinstance(voyage_data[field], str):
                try:
                    voyage_data[field] = voyage_data[field].isoformat()
                except AttributeError:
                    # If it's not a datetime object and not a string, convert to string
                    voyage_data[field] = str(voyage_data[field])
    
    # Ensure string fields have proper values
    for field in ["vesselName", "portAreaName", "portToVisit", "prevPort", "berthName"]:
        if field in voyage_data and voyage_data[field] is None:
            voyage_data[field] = ""  # Replace None with empty string
    
    # Call the XML Storage Function
    xml_converterfunction_url = XML_CONVERTER_CONFIG["function_url"]
    xml_converter_function_key = XML_CONVERTER_CONFIG["function_key"]
    
    # Add the function key to the URL if it exists
    if xml_converter_function_key:
        if "?" in xml_converterfunction_url:
            xml_converterfunction_url += f"&code={xml_converter_function_key}"
        else:
            xml_converterfunction_url += f"?code={xml_converter_function_key}"
    
    logging.info(f"Calling xml-converter for NOA: {xml_converterfunction_url}")
    
    # Send the voyage data to the function for NOA generation
    try:
        # Log the payload for debugging
        logging.info(f"Payload to XML converter: {json.dumps({'portcall_data': voyage_data, 'formality_type': 'NOA'})}")
        
        response = requests.post(
            xml_converterfunction_url,
            json={"portcall_data": voyage_data, "formality_type": "NOA"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            response_data = response.json()
            # Get SAS URL from the response
            sas_url = response_data.get('sasUrl')
            
            if not sas_url:
                return func.HttpResponse(
                    json.dumps({"status": "error", "message": "No URL found in XML converter response"}),
                    mimetype="application/json",
                    status_code=500
                )
            
            # Update the database with the NOA XML URL
            if update_noa_xml_url(portCallId, sas_url):
                return func.HttpResponse(
                    json.dumps({
                        "status": "success", 
                        "message": f"NOA XML generated and URL updated for portCallId {portCallId}",
                        "sasUrl": sas_url
                    }),
                    mimetype="application/json"
                )
            else:
                return func.HttpResponse(
                    json.dumps({
                        "status": "partial", 
                        "message": f"NOA XML generated but URL update failed for portCallId {portCallId}",
                        "sasUrl": sas_url
                    }),
                    mimetype="application/json",
                    status_code=500
                )
        else:
            return func.HttpResponse(
                json.dumps({
                    "status": "error", 
                    "message": f"XML converter failed with status {response.status_code}: {response.text}"
                }),
                mimetype="application/json", 
                status_code=500
            )
    except Exception as e:
        logging.error(f"Error calling XML converter: {str(e)}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            mimetype="application/json", 
            status_code=500
        ) 