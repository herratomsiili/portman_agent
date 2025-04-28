// Configuration for API endpoints
export const API_CONFIG = {
  // The base URL for the API
  apiBaseUrl: 'https://therranen-portman-dev-dab-cont--9xa9w7w.thankfulpebble-a521a7c0.swedencentral.azurecontainerapps.io',
  
  // API endpoints
  endpoints: {
    // REST endpoints for data entities
    rest: {
      arrivals: '/api/arrivals',
      voyages: '/api/voyages',
    },
    // GraphQL endpoint
    graphql: '/graphql',
    // Function app endpoints
    functions: {
      cargoGenerator: '/api/cargo-generator',
      vesselDetails: '/api/vessel-details',
    }
  },
  
  // Default request timeout in milliseconds
  requestTimeout: 30000,
}; 