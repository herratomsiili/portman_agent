# UI Testing Guide

This document explains the UI testing setup and practices used in the Portman UI project.

## Testing Libraries

The project uses two main testing libraries:

1. **Jest** - For unit and component testing
2. **Cypress** - For end-to-end (E2E) testing

### Jest

Jest is used for:
- Unit testing of individual components
- Testing component logic and state
- Testing utility functions
- Fast feedback during development

#### Key Features
- Fast test execution
- Snapshot testing
- Mocking capabilities
- Coverage reporting
- Watch mode for development

#### Usage

```bash
# Run all Jest tests
npm test

# Run tests in watch mode (auto-rerun on changes)
npm run test:watch

# Generate coverage report
npm run test:coverage
```

#### Example Test

```typescript
import { render, screen } from '@testing-library/react';
import { PortCallCard } from './PortCallCard';

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
});
```

### Cypress

Cypress is used for:
- End-to-end testing
- User interaction testing
- Browser automation
- Visual regression testing
- Network request testing

#### Key Features
- Real browser testing
- Time-travel debugging
- Automatic waiting
- Screenshot and video recording
- Network request stubbing

#### Support Files

The `cypress/support/e2e.ts` file is automatically loaded before each end-to-end test. It serves several important purposes:

- **Custom Commands**: Defines reusable commands like `dataCy()` which makes it easier to select elements using `data-cy` attributes
- **TypeScript Support**: Provides type definitions for custom commands
- **Global Setup**: A place to set up global behavior that should apply to all tests
- **Stable Selectors**: Encourages the use of `data-cy` attributes for selecting elements, which makes tests more resilient to changes in CSS or HTML structure

Example usage in tests:
```typescript
// Instead of
cy.get('[data-cy=submit-button]').click()

// You can use
cy.dataCy('submit-button').click()
```

When writing components, add `data-cy` attributes to elements you want to test:
```jsx
<button data-cy="submit-button">Submit</button>
```

This approach helps separate testing concerns from styling or structural concerns, making tests more maintainable.

#### Usage

```bash
# Run all Cypress tests
npm run test:e2e

# Open Cypress Test Runner
npm run test:e2e:open
```

#### Example Test

```typescript
describe('Port Calls Page', () => {
  beforeEach(() => {
    cy.visit('/portcalls');
  });

  it('displays port calls table', () => {
    cy.get('table').should('exist');
    cy.get('tr').should('have.length.at.least', 1);
  });

  it('filters port calls', () => {
    cy.get('input[placeholder="Search..."]').type('Test Vessel');
    cy.get('tr').should('have.length.at.least', 1);
  });
});
```

## Testing Strategy

### Unit Tests (Jest)
- Test individual components in isolation
- Mock external dependencies
- Focus on component logic and state
- Use React Testing Library for component testing
- Aim for high coverage of business logic

### E2E Tests (Cypress)
- Test complete user flows
- Test critical paths
- Test integration with backend
- Test responsive design
- Test error handling

## Best Practices

1. **Test Organization**
   - Keep tests close to the code they test
   - Use descriptive test names
   - Group related tests using `describe` blocks

2. **Component Testing**
   - Test component behavior, not implementation
   - Use `data-testid` attributes for stable selectors
   - Mock external dependencies
   - Test both success and error cases

3. **E2E Testing**
   - Test complete user journeys
   - Use realistic data
   - Test error scenarios
   - Test responsive behavior
   - Use fixtures for consistent data

4. **Performance**
   - Keep tests fast and focused
   - Use appropriate test types for different needs
   - Run Jest tests during development
   - Run Cypress tests before deployment

## Running All Tests

To run both Jest and Cypress tests:

```bash
npm run test:all
```

This will:
1. Run all Jest tests
2. Run all Cypress tests
3. Generate coverage reports
4. Save test artifacts

## CI/CD Integration

Tests are automatically run in CI/CD pipeline:
- Jest tests run on every push
- Cypress tests run on pull requests
- Coverage reports are generated
- Test results are published as artifacts

## Troubleshooting

### Common Issues

1. **Tests are slow**
   - Use appropriate test types
   - Mock heavy operations
   - Run tests in parallel when possible

2. **Flaky tests**
   - Use proper waiting strategies
   - Avoid time-dependent tests
   - Use stable selectors

3. **Coverage issues**
   - Review uncovered code
   - Add missing tests
   - Consider if coverage is needed

### Getting Help

- Check Jest documentation: https://jestjs.io/
- Check Cypress documentation: https://docs.cypress.io/
- Review test examples in the project
- Ask for help in team channels 