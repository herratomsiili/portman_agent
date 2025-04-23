# Portman UI Testing Guide

## Overview
This document outlines the testing strategy and setup for the Portman UI application. We use:
- **Jest + React Testing Library** for unit and component testing
- **Cypress** for end-to-end testing

## Dependencies

### Testing Libraries
- **Jest** (`jest@29.7.0`) - Test runner
- **React Testing Library** (`@testing-library/react@16.2.0`) - Component testing
- **Jest DOM** (`@testing-library/jest-dom@6.6.3`) - DOM testing utilities
- **User Event** (`@testing-library/user-event@13.5.0`) - User interaction testing
- **Cypress** (`cypress@13.6.4`) - E2E testing
- **Jest Environment JSDOM** (`jest-environment-jsdom@29.7.0`) - Browser environment for Jest
- **TS Jest** (`ts-jest@29.3.1`) - TypeScript support for Jest

## Test Structure
- `cypress/e2e/` - End-to-end tests
- `cypress/support/` - Test support files
- `src/__tests__/` - Unit and component tests
- `.github/workflows/tests.yml` - CI/CD test workflow

## Test Types

### Unit & Component Tests (Jest + React Testing Library)
Used for:
- Testing individual components
- Testing hooks and utilities
- Testing component state and props
- Testing user interactions at component level

Example:
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { PortCallCard } from '../components/PortCallCard';

describe('PortCallCard', () => {
  it('renders port call details correctly', () => {
    const mockPortCall = {
      portCallId: 123,
      vesselName: 'Test Vessel',
      eta: '2024-03-20T10:00:00Z'
    };

    render(<PortCallCard portCall={mockPortCall} />);
    
    expect(screen.getByText('Test Vessel')).toBeInTheDocument();
    expect(screen.getByText('ETA: 20.03.2024 10:00')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const mockOnClick = jest.fn();
    render(<PortCallCard portCall={mockPortCall} onClick={mockOnClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(mockOnClick).toHaveBeenCalled();
  });
});
```

### End-to-End Tests (Cypress)
Used for:
- Testing complete user flows
- Testing integration with backend
- Testing responsive design
- Testing error scenarios

Key endpoints mocked:
- `/api/voyages` - Port calls list
- `/api/port-calls/:id` - Individual port call details
- `/api/arrivals` - Arrival updates
- `/api/vessels/tracked` - Tracked vessels
- `/api/auth/*` - Authentication endpoints
- `/api/settings` - User settings
- AIS API - Vessel location data

### Test Support Files

#### `e2e.ts`
- Sets up global test configuration
- Initializes mock API before each test
- Imports custom commands

#### `commands.ts`
- Defines custom Cypress commands
- Currently includes:
  - `dataCy`: Selects elements by data-cy attribute
  - Example: `cy.dataCy('submit-button')` instead of `cy.get('[data-cy=submit-button]')`

#### `mock-api.ts`
- Defines mock API responses for tests
- Intercepts HTTP requests
- Provides consistent test data

### CI/CD Workflow (`tests.yml`)
The GitHub Actions workflow:
1. Sets up test environment
   - Node.js dependencies
   - Environment variables
2. Creates test data
   - Mock API responses
3. Runs tests
   - Jest unit tests
   - Cypress E2E tests
4. Uploads test artifacts
   - Screenshots
   - Videos
   - Coverage reports

## Running Tests

### Available Scripts
```bash
# Run Jest tests
npm test

# Run Jest tests in watch mode
npm run test:watch

# Run Jest tests with coverage
npm run test:coverage

# Run Cypress tests
npm run test:e2e

# Open Cypress Test Runner
npm run test:e2e:open

# Run Cypress tests in dev mode (with dev server)
npm run test:e2e:dev

# Run all tests (Jest + Cypress)
npm run test:all
```

### CI/CD
Tests run automatically on:
- Push to main/develop branches
- Pull requests to main/develop

## Test Data
Test data is managed in:
- `cypress/support/mock-api.ts` - API mock responses
- `src/__tests__/mocks/` - Jest mock data

## Best Practices
1. Use data-cy attributes for Cypress tests
2. Use data-testid for Jest tests
3. Keep mock data consistent with UI expectations
4. Test both success and error scenarios
5. Maintain test isolation
6. Use meaningful test descriptions
7. Follow the testing pyramid:
   - More unit tests than component tests
   - More component tests than E2E tests

## Test Organization

### Unit & Component Tests
- `src/__tests__/components/` - Component tests
- `src/__tests__/hooks/` - Custom hooks tests
- `src/__tests__/utils/` - Utility function tests
- `src/__tests__/mocks/` - Mock data and functions

### E2E Tests
- `auth.cy.ts` - Authentication flows
- `dashboard.cy.ts` - Dashboard functionality
- `portcalls.cy.ts` - Port calls management

### Test Data Structure
Each test file should:
1. Set up required mock data
2. Test user interactions
3. Verify expected outcomes
4. Clean up after tests

## Troubleshooting

### Common Issues
1. **Test Timeouts**
   - Check mock API responses
   - Verify network intercepts
   - Adjust timeouts in `cypress.config.ts`

2. **Failed Assertions**
   - Verify data-cy attributes
   - Check mock data structure
   - Review component state

3. **CI/CD Failures**
   - Check environment variables
   - Verify test setup
   - Review test artifacts

4. **Jest Test Failures**
   - Check component props
   - Verify mock implementations
   - Review test setup and teardown

## Contributing
When adding new tests:
1. Follow existing patterns
2. Use appropriate test types
3. Use data-cy/data-testid attributes
4. Update mock data as needed
5. Document new test cases 