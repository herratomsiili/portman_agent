describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('should show login form', () => {
    cy.get('form').should('exist')
    cy.get('input[name="username"]').should('exist')
    cy.get('input[name="password"]').should('exist')
    cy.get('button[type="submit"]').should('exist')
  })

  it('should show error with invalid credentials', () => {
    cy.get('input[name="username"]').type('invalid')
    cy.get('input[name="password"]').type('invalid')
    cy.get('button[type="submit"]').click()
    cy.get('.error-message').should('be.visible')
  })

  it('should login with valid credentials', () => {
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin')
    cy.get('button[type="submit"]').click()
    cy.url().should('not.include', '/login')
  })
}) 