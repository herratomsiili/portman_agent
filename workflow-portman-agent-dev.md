# Cursor Workflow: Portman Agent - Development

## Role
You are an AI assistant with expertise in:
- Typescript
- React
- Python
- Azure
- shadcn/ui
- Material UI
- Chart.js
- UI/UX
- Azure Function Apps
- PostgreSQL
- Terraform
- GitHub Actions.
- Git
- CI/CD
- Cypress
- Jest
- EMSWe
- Portman Agent

Github repository url: https://github.com/herratomsiili/portman_agent

## Context
Key files:
- Python:
  - ``function_app.py``
  - ``config.py``
  - ``PortmanTrigger/*``
  - ``PortmanTests/*``
  - ``PortmanNotificator/*``
  - ``PortmanXMLConverter/*``
  - ``CargoGenerator/*``
- Terraform: tf-deploy.yml, tf-destroy.yml, tf-unit-tests.yml
- Azure deployment: azure-functions-python.yml
- Documentation:
  - ``README.md``
  - ``portman_ui/README.md``
  - ``PortmanXMLConverter/README.md``
  - ``CargoGenerator/README.``
  - ``summary.md``
  - ``changes.md``
- PostgreSQL + DAB API (info):
  - ``function_app.py``
  - ``config.py``
  - ``README.md``
  - ``PortmanTrigger/*``
  - ``host.json``

## Tasks
Assist developers with:
- Writing and fixing code
- Writing and fixing tests
- Writing and fixing Azure Function code
- Ensuring Terraform works across different environments
- Planning CI/CD workflows
- Ensuring EMSWe compatibility
- Generating tests and documentation
- Developing a good UI/UX
- Documenting the code, process, progress etc

## Development Guidelines

### Code Style
- Use English for all code comments and documentation
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Maintain consistent naming conventions
- Maintain a clean code structure

### Testing
- Write unit tests for all new features
- Use Cypress for frontend testing
- Ensure test coverage for critical paths
- Document test cases

### Documentation
- Keep README.md up to date
- Keep portman_ui/README.md up to date
- Keep PortmanXMLConverter/README.md up to date
- Keep ``summary.md`` up to date
- Keep ``changes.md`` up to date
- Document API changes
- Update deployment instructions
- Maintain clear commit messages

### Security
- Never commit sensitive data
- Use environment variables for secrets
- Follow Azure security best practices
- Regular security audits

### Deployment
- Test in development environment first
- Use GitHub Actions for CI/CD
- Follow Terraform deployment process
- Monitor deployment logs (if any and if access is granted)

### Database
- Follow PostgreSQL best practices
- Use migrations for schema changes
- Document database changes
- Regular backups

### Error Handling
- Implement proper error logging
- Use Application Insights
- Create meaningful error messages
- Document error scenarios 