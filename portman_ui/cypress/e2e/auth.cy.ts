describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should show the login form by default', () => {
    cy.dataCy('login-card').should('be.visible');
  });

  it('should handle invalid credentials', () => {
    cy.dataCy('input-email').type('invalid@example.com');
    cy.dataCy('input-password').type('wrongpassword');
    cy.dataCy('auth-submit').click();
    cy.dataCy('auth-error').should('be.visible');
    cy.dataCy('auth-error').should('contain', 'Username or password was incorrect. Please try again.');
  });

  it('should login successfully with valid credentials', () => {
    cy.dataCy('input-email').type('viewer@portman.com');
    cy.dataCy('input-password').type('viewer123');
    cy.dataCy('auth-submit').click();
    cy.dataCy('dashboard-title').should('be.visible', { timeout: 10000 });
    cy.url().should('include', '/dashboard', { timeout: 10000 });
  });

  it('should validate the form inputs', () => {
    cy.dataCy('auth-submit').click();
    cy.dataCy('auth-error').should('be.visible');
    cy.dataCy('auth-error').should('contain', 'Email and password are required');
  });

  it('should toggle to registration form', () => {
    cy.dataCy('auth-toggle-mode').click();
    cy.dataCy('auth-form').should('be.visible');
    cy.dataCy('input-name').should('be.visible');
    cy.dataCy('input-email').should('be.visible');
    cy.dataCy('input-password').should('be.visible');
    cy.dataCy('input-confirm-password').should('be.visible');
    cy.dataCy('select-role').should('be.visible');
    cy.dataCy('select-role').click();
    cy.dataCy('role-admin').should('be.visible');
    cy.dataCy('role-user').should('be.visible');
    cy.dataCy('role-viewer').should('be.visible');
  });

  it('should register a new user', () => {
    cy.dataCy('auth-toggle-mode').click();
    cy.dataCy('input-name').type('New User');
    cy.dataCy('input-email').type('newuser@example.com');
    cy.dataCy('input-password').type('securepassword');
    cy.dataCy('input-confirm-password').type('securepassword');
    cy.dataCy('auth-submit').click();
    cy.dataCy('auth-success').should('be.visible');
  });

  it('should validate registration form', () => {
    cy.dataCy('auth-toggle-mode').click();
    cy.dataCy('auth-submit').click();
    cy.dataCy('auth-error').should('be.visible');
    cy.dataCy('auth-error').should('contain', 'Email and password are required');
  });

  it('should toggle back to login form', () => {
    cy.dataCy('auth-toggle-mode').click();
    cy.dataCy('login-card').should('be.visible');
  });
});
