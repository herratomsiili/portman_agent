describe('Port Calls', () => {
  beforeEach(() => {
    // Login first
    cy.visit('/login')
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin')
    cy.get('button[type="submit"]').click()
    
    // Navigate to port calls
    cy.visit('/portcalls')
  })

  it('should show port calls table', () => {
    cy.get('table').should('exist')
    cy.get('th').should('have.length.at.least', 5)
  })

  it('should filter port calls', () => {
    cy.get('input[placeholder="Search..."]').type('Test Vessel')
    cy.get('tr').should('have.length.at.least', 1)
  })

  it('should show port call details', () => {
    cy.get('tr').first().click()
    cy.get('.portcall-details').should('be.visible')
  })

  it('should handle admin actions', () => {
    cy.get('button[data-cy="admin-actions"]').click()
    cy.get('.admin-menu').should('be.visible')
  })
}) 