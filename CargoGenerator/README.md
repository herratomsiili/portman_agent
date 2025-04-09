# Cargo Declaration Generator

This Azure Function generates realistic cargo declarations for testing "cargo declaration at arrival" notifications. It uses Azure OpenAI to create realistic cargo data based on vessel IMO number and port of arrival.

## Implementation

This function is implemented using the Azure Functions v2 programming model where the HTTP trigger is registered in function_app.py using the decorator pattern.

The function follows a two-step process:
1. Generate cargo data using Azure OpenAI based on the IMO number and ports
2. Retrieve actual vessel details from the Vessel Details function and add them to the response

## Requirements

- Azure Functions Core Tools
- Python 3.12
- Azure OpenAI service deployment (GPT-4 recommended)

## Configuration

The function requires the following environment variables:

- `OPENAI_API_KEY`: Your Azure OpenAI API key
- `OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `OPENAI_DEPLOYMENT_NAME`: The name of your deployed model (e.g., "cargo-generator")
- `OPENAI_API_VERSION`: The API version to use (e.g., "2023-05-15")
- `FUNCTION_APP_URL`: The base URL of your Azure Functions app (without /api)
- `VESSEL_DETAILS_FUNCTION_KEY`: The Azure function key of your Vessel Details function

Copy `sample.local.settings.json` to `local.settings.json` and fill in your Azure OpenAI credentials.

## Usage

Send a POST request to the function with the following JSON body:

```json
{
  "imo": "9311581",        // Vessel IMO number
  "portToVisit": "NLRTM",  // Port of arrival code
  "prevPort": "USMIA"      // Previous port code (optional)
}
```

The function will return a JSON document containing the generated cargo declaration data following the European Maritime Single Window environment (EMSWe) specification.

## Processing Flow

1. The function receives the IMO number and port data
2. OpenAI generates realistic cargo information without any vessel details
3. The Vessel Details function is called to retrieve actual vessel information
4. The vessel details are added to the final response

This approach ensures accurate vessel data is included while allowing OpenAI to focus on generating realistic cargo information.

## Example Response

```json
{
  "vesselDetails": {
    "name": "MAERSK NEVADA",
    "imo": "9311581",
    "callSign": "DDDA",
    "flagState": "Denmark",
    "vesselType": "Container Ship",
    "grossTonnage": 94724,
    "netTonnage": 59516,
    "mmsi": 219622000
  },
  "transportMovement": {
    "previousPort": "USMIA",
    "portToVisit": "NLRTM",
    "departureDate": "2023-04-01T14:30:00Z",
    "arrivalDate": "2023-04-07T08:30:00Z"
  },
  "cargoItems": [
    {
      "goodsDescription": "Laptops and Electronics",
      "grossWeight": 12500.5,
      "packageCount": 125,
      "packageType": "Pallets"
    },
    // More cargo items...
  ],
  "containers": [
    {
      "containerNumber": "MSCU1234567",
      "type": "22G1",
      "weight": 12500.5,
      "contents": "Electronics"
    },
    // More containers...
  ]
}
```

## Deployment

Deploy the function to Azure using the Azure Functions Core Tools or Azure DevOps pipelines. The function is accessible at the `/api/cargo-generator` endpoint. 