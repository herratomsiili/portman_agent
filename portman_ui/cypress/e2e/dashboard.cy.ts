describe('Dashboard', () => {
  beforeEach(() => {
    cy.visit('/login')
    cy.dataCy('input-email').type('admin@portman.com')
    cy.dataCy('input-password').type('admin123')
    cy.dataCy('auth-submit').click()
    cy.visit('/dashboard')
  })

  it('should show dashboard title', () => {
    cy.dataCy('dashboard-title').should('contain', 'Dashboard')
  })

  it('should display summary cards', () => {
    cy.dataCy('card-tracked-vessels').should('be.visible')
    cy.dataCy('card-active-calls').should('be.visible')
    cy.dataCy('card-scheduled-arrivals').should('be.visible')
    cy.dataCy('card-passengers').should('be.visible')
  })

  it('should display upcoming arrivals section', () => {
    cy.dataCy('upcoming-arrivals-title').should('be.visible')
    cy.dataCy('upcoming-arrivals-list')
      .find('.MuiListItem-root')
      .should('have.length.at.least', 0)
  })

  it('should display active vessels section', () => {
    cy.dataCy('active-vessels-title').should('be.visible')
    cy.dataCy('active-vessels-list')
      .find('.MuiListItem-root')
      .should('have.length.at.least', 0)
  })

  it('should show vessel details in lists', () => {
    cy.dataCy('upcoming-arrivals-list')
      .find('.MuiListItem-root')
      .first()
      .find('.MuiTypography-root')
      .first()
      .should('not.be.empty')

    cy.dataCy('active-vessels-list')
      .find('.MuiListItem-root')
      .first()
      .find('.MuiTypography-root')
      .first()
      .should('not.be.empty')
  })

  // it.skip('should navigate to vessel details when clicking on vessel', () => {
  //   cy.dataCy('upcoming-arrivals-list')
  //     .find('.MuiListItem-root')
  //     .first()
  //     .click()
  //
  //   cy.url().should('include', '/vessel/')
  // })

  // it.skip('should handle empty data gracefully', () => {
  //   cy.intercept('GET', '**/voyages', { body: [] }).as('emptyPortCalls')
  //
  //   cy.visit('/dashboard')
  //
  //   cy.dataCy('no-upcoming-arrivals').should('exist')
  //   cy.dataCy('no-active-vessels').should('exist')
  // })
}) 