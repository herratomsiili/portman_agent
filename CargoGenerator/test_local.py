import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()

# Configuration
FUNCTION_URL = os.getenv("FUNCTION_URL", "http://localhost:7071/api/cargo-generator")

def test_cargo_generator():
    """Test the cargo generator function with a sample vessel"""
    
    # Test data - sample vessel IMO
    test_data = {
        "imo": "9311581",        # Maersk vessel (example)
        "portToVisit": "NLRTM",  # Rotterdam
        "prevPort": "USMIA"      # Miami
    }
    
    # Send request to the function
    response = requests.post(
        FUNCTION_URL,
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Print the results
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        cargo_data = response.json()
        print(json.dumps(cargo_data, indent=2))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_cargo_generator() 