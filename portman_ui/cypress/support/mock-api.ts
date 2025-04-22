import { defineConfig } from 'cypress';

export const mockApi = {
  setup() {
    // Mock port calls endpoints
    cy.intercept('GET', '/api/voyages', {
      statusCode: 200,
      body: [
        {
          portCallId: 3190880,
          imoLloyds: 9606900,
          vesselTypeCode: '20',
          vesselName: 'Viking Grace',
          prevPort: 'FIMHQ',
          portToVisit: 'FITKU',
          nextPort: 'FILAN',
          agentName: 'Viking Line Abp / Helsinki',
          shippingCompany: 'Viking Line Abp',
          eta: '2024-03-13T10:00:00Z',
          ata: null,
          portAreaCode: 'PASSE',
          portAreaName: 'Matkustajasatama',
          berthCode: 'v1',
          berthName: 'viking1',
          etd: '2024-03-13T20:00:00Z',
          atd: null,
          passengersOnArrival: 235,
          passengersOnDeparture: 188,
          crewOnArrival: 1849,
          crewOnDeparture: 1346
        }
      ]
    }).as('getPortCalls');

    cy.intercept('GET', '/api/port-calls/3190880', {
      statusCode: 200,
      body: {
        portCallId: 3190880,
        imoLloyds: 9606900,
        vesselTypeCode: '20',
        vesselName: 'Viking Grace',
        prevPort: 'FIMHQ',
        portToVisit: 'FITKU',
        nextPort: 'FILAN',
        agentName: 'Viking Line Abp / Helsinki',
        shippingCompany: 'Viking Line Abp',
        eta: '2024-03-13T10:00:00Z',
        ata: null,
        portAreaCode: 'PASSE',
        portAreaName: 'Matkustajasatama',
        berthCode: 'v1',
        berthName: 'viking1',
        etd: '2024-03-13T20:00:00Z',
        atd: null,
        passengersOnArrival: 235,
        passengersOnDeparture: 188,
        crewOnArrival: 1849,
        crewOnDeparture: 1346
      }
    }).as('getPortCallById');

    // Mock arrivals endpoint
    cy.intercept('GET', '/api/arrivals', {
      statusCode: 200,
      body: [
        {
          id: 1,
          portCallId: 3190880,
          eta: '2024-03-13T10:00:00Z',
          old_ata: null,
          ata: '2024-03-13T10:30:00Z',
          vesselName: 'Viking Grace',
          portAreaName: 'Matkustajasatama',
          berthName: 'viking1'
        }
      ]
    }).as('getArrivals');

    // Mock tracked vessels endpoint
    cy.intercept('GET', '/api/vessels/tracked', {
      statusCode: 200,
      body: {
        vessels: [
          {
            imo: 9606900,
            name: 'Viking Grace',
            type: 'Passenger Ship'
          }
        ]
      }
    }).as('getTrackedVessels');

    // Mock AIS API endpoint
    cy.intercept('GET', 'https://meri.digitraffic.fi/api/ais/v1/locations', {
      statusCode: 200,
      body: {
        features: [
          {
            properties: {
              mmsi: 230123456,
              imo: 9606900,
              name: 'Viking Grace',
              shipType: 70,
              latitude: 60.123,
              longitude: 24.456,
              speed: 12.5,
              course: 90,
              timestamp: '2024-03-13T10:00:00Z'
            }
          }
        ]
      }
    }).as('getVesselLocations');

    // Mock authentication endpoints
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        token: 'test-token',
        user: {
          id: 1,
          username: 'testuser',
          role: 'admin'
        }
      }
    }).as('login');

    cy.intercept('POST', '/api/auth/register', {
      statusCode: 201,
      body: {
        message: 'User registered successfully'
      }
    }).as('register');

    // Mock settings endpoint
    cy.intercept('GET', '/api/settings', {
      statusCode: 200,
      body: {
        apiUrl: 'http://localhost:3000/api',
        refreshInterval: 60,
        defaultView: 'dashboard',
        theme: 'light'
      }
    }).as('getSettings');
  }
}; 