describe('Vessel Tracking', () => {
    beforeEach(() => {
        // Login first with correct credentials
        cy.visit('/login')
        cy.dataCy('input-email').type('admin@portman.com')
        cy.dataCy('input-password').type('admin123')
        cy.dataCy('auth-submit').click()

        // Navigate to vessel tracking and verify we're on the correct page
        cy.visit('/vessel-tracking')
    })

    it('should show page title and filter fields', () => {
        cy.dataCy('vesseltracking-container').should('be.visible');
        cy.contains('Vessel Tracking').should('be.visible');
        cy.get('#status-filter').should('exist');
        cy.get('#port-filter').should('exist');
    });

    it('should show map and vessel cards', () => {
        cy.get('.leaflet-container').should('exist');
        cy.get('[data-cy=vessel-card]').should('have.length.at.least', 1);
    });

    it('should display vessel information in cards', () => {
        cy.get('[data-cy=vessel-card]').first().within(() => {
            cy.contains('MMSI:').should('exist');
            cy.contains('Position:').should('exist');
            cy.contains('Course:').should('exist');
            cy.contains('Heading:').should('exist');
            cy.contains('Last Update:').should('exist');
        });
    });

    it('should filter vessels by status', () => {
        cy.get('#status-filter').click();
        cy.get('[role="option"]').contains('Active').click();
        cy.get('[data-cy=vessel-card]').should('have.length.at.least', 1);
    });

    it('should filter vessels by port', () => {
        cy.get('#port-filter').click();
        cy.get('[role="option"]').first().click();
        cy.get('[data-cy=vessel-card]').should('have.length.at.least', 1);
    });

    it('should show pagination controls', () => {
        cy.get('.MuiTablePagination-root').should('exist');
        cy.get('.MuiTablePagination-selectRoot').should('exist');
        cy.get('.MuiTablePagination-displayedRows').should('exist');
    });

    it('should change rows per page', () => {
        // Get initial row count
        cy.get('[data-cy=vessel-card]').its('length').then((initialCount) => {
            // Change rows per page to 25
            cy.get('.MuiTablePagination-select').click();
            cy.get('[role="option"]').contains('25').click();

            // Check that rows count is now 25 or less
            cy.get('[data-cy=vessel-card]').should('have.length.at.most', 25);
        });
    });

    it('should show loading state when fetching data', () => {
        // Intercept API calls and delay response
        cy.intercept('GET', '**/vessel-locations', (req) => {
            req.on('response', (res) => {
                res.delay = 2000;
            });
        }).as('getVesselLocations');

        // Reload the page
        cy.visit('/vessel-tracking');

        // Check loading indicator appears
        cy.get('.MuiCircularProgress-root').should('be.visible');

        // Wait for data to load
        cy.wait('@getVesselLocations');

        // Check map and cards appear after loading
        cy.get('.leaflet-container').should('be.visible');
        cy.get('[data-cy=vessel-card]').should('have.length.at.least', 1);
    });
});
