# Vessel Details Function

This Azure Function retrieves vessel details from the Digitraffic Port Call API based on an IMO number. It's designed to be used as a microservice for accurate vessel data lookup.

## Implementation

This function is implemented using Azure Functions v2 programming model and registered in function_app.py. It makes an API call to Digitraffic Port Call API to retrieve accurate vessel information.

## Supported APIs

- [Digitraffic Port Call API](https://meri.digitraffic.fi/api/port-call/v1/vessel-details) - Free, no API key required (Finnish Transport Infrastructure Agency)

## Configuration

The function doesn't require any special configuration as the Digitraffic API is free and doesn't require an API key.

## Usage

### HTTP Request

**Endpoint**: `POST /api/vessel-details`

**Body**:
```json
{
  "imo": "9854466"
}
```

Alternatively, you can use a GET request with a query parameter:
```
GET /api/vessel-details?imo=9854466
```

### Response

Success (200 OK):
```json
{
  "name": "Saltstraum",
  "namePrefix": "MT",
  "callSign": "LAJU6",
  "flagState": "NO",
  "vesselType": "Chemical tanker",
  "vesselTypeCode": 83,
  "iceClass": "IA",
  "grossTonnage": 7256,
  "netTonnage": 3225,
  "deadWeight": 10585,
  "mmsi": 0,
  "length": 125.82,
  "overallLength": 129.5,
  "breadth": 19.65,
  "draught": 8.18,
  "portOfRegistry": "Bergen",
  "dataSource": "Portnet",
  "updateTimestamp": "2025-01-15T07:52:22.000+00:00"
}
```

Not Found (404):
```json
{
  "error": "No vessel details found for IMO 9854466"
}
```

## Data Provided

The Digitraffic Port Call API provides comprehensive vessel data including:
- Vessel name and prefix
- Radio call sign
- Flag state (nationality)
- Vessel type and type code
- Ice class
- Tonnage information (gross, net, deadweight)
- MMSI number
- Vessel dimensions (length, breadth, draught)
- Port of registry
- Data source and timestamp

## Integration

This function is designed to be called by the Cargo Generator function to provide accurate vessel details for cargo declarations. The integration is configured through the `FUNCTION_APP_URL` and `VESSEL_DETAILS_FUNCTION_KEY` settings in the Cargo Generator function. 