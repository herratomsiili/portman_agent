# Portman UI Instructions

This document provides information about the Portman UI application, its components, and how to interact with APIs.

## API Endpoints

### Paginated APIs

The application supports paginated API endpoints for data that could return large result sets:

- `/arrivals` - Fetches vessel arrival data with pagination
- `/voyages` - Fetches port call data with pagination

Both endpoints use the same pagination pattern:
- The initial request returns up to 100 items
- If more data is available, a `nextLink` property is included in the response
- The `nextLink` contains a URL with an `$after` parameter that can be used to fetch the next page

## Components

### Tables with Auto-Loading

The following views implement automatic data loading functionality:

- `Arrivals.tsx` - Lists vessel arrival information
- `PortCalls.tsx` - Lists port call information

These components:
1. Automatically fetch all available data recursively
2. Show loading indicators during data retrieval
3. Display the total count of records loaded
4. Implement search functionality to filter the data
5. Allow changing rows per page and navigating between pages

When implementing new tables that need to access large datasets:
1. Create a paginated API method in `api.ts` similar to `getArrivals` or `getPortCallsPaginated`
2. Use the recursive loading pattern seen in these components
3. Include appropriate loading indicators and error handling

## Search Functionality

All table components implement client-side search that filters already loaded data. Search is typically performed on:
- Vessel names
- Port names
- IDs (like portcallid or IMO numbers)

## Status Indicators

- Arrivals use color-coded chips:
  - Green: New Arrival
  - Orange: Updated Arrival
  
- Port Calls use color-coded chips:
  - Green: Arrived (has ATA)
  - Blue: Expected (no ATA yet) 