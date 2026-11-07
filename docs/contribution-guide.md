 # Contribution Guide
 
 Thank you for considering contributing to RAVEN. This guide outlines the process for contributing to the project.
 
 ## Code of Conduct
 
 By participating in this project, you agree to abide by our Code of Conduct:
 - Be respectful and inclusive
 - Focus on constructive feedback
 - No harassment, discrimination, or offensive behavior
 - Respect intellectual property and licensing
 
 ## Getting Started
 
 1. Fork the repository
 2. Clone your fork locally
 3. Create a feature branch: `git checkout -b feature/your-feature-name`
 4. Make your changes
 5. Run tests and quality checks
 6. Submit a pull request
 
 ## Development Setup
 
 See [Development Guide](development-guide.md) for detailed setup instructions.
 
 Quick start:
 ```bash
 git clone https://github.com/your-username/RAVEN.git
 cd RAVEN
 
 # Windows
 .\setup.ps1
 
 # Linux/macOS
 ./setup.sh
 ```
 
 ## Pull Request Process
 
 ### Before Submitting
 
 - [ ] Tests pass locally (`python -m pytest` and `npm run test`)
 - [ ] Type checking passes (`python -m mypy --strict app` and `npm run typecheck`)
 - [ ] Linting passes (`python -m ruff check app` and `npm run lint`)
 - [ ] Documentation updated if applicable
 - [ ] CHANGELOG.md updated (if user-facing change)
 - [ ] Commit messages follow conventional commits format
 
 ### PR Requirements
 
 1. **Clear title**: Use conventional commits format
    - `feat: add new recon module for DNS enumeration`
    - `fix: resolve policy engine L3 approval bypass`
    - `docs: update API reference for evidence endpoints`
    - `refactor: simplify attack graph path finding`
    - `test: add unit tests for risk engine`
 
 2. **Description**: Explain what changed and why
    - Link related issues
    - Describe testing performed
    - Note any breaking changes
 
 3. **Scope**: Keep PRs focused
    - One feature/fix per PR
    - Small, reviewable changes preferred
    - Large changes should be discussed in an issue first
 
 4. **Review process**:
    - Automated checks must pass
    - At least one maintainer review required
    - Address review comments
    - Maintainer merges after approval
 
 ## Coding Standards
 
 See [Development Guide](development-guide.md#coding-standards) for detailed standards.
 
 Key points:
 - **Python**: Ruff + mypy strict, Google docstrings, async/await
 - **TypeScript**: ESLint + Prettier, strict mode, functional components
 - **Design**: Follow design.md - no gradients, shadows, animations, emojis
 - **Security**: Policy engine gate, secret redaction, evidence integrity
 
 ## Testing Requirements
 
 ### New Features
 
 - Unit tests for all new functions/classes
 - Integration tests for API endpoints
 - Frontend component tests for new UI
 - Minimum 80% coverage for new code
 
 ### Bug Fixes
 
 - Add regression test demonstrating the bug
 - Verify fix resolves the test
 - Add edge case tests if applicable
 
 ### Running Tests
 
 ```bash
 # Backend
 cd backend
 python -m pytest tests/ -v --cov=app
 
 # Frontend
 cd frontend
 npm run test -- --coverage
 npm run test:e2e
 ```
 
 ## Documentation
 
 Update documentation for:
 - New API endpoints (api-reference.md)
 - New configuration options (configuration.md)
 - New modules/features (architecture.md, user-guide.md)
 - Architecture changes (architecture.md)
 - Database schema changes (database-schema.md)
 
 Documentation style:
 - Clear, concise technical writing
 - Code examples for all APIs
 - Screenshots for UI changes (placeholder if not available)
 - Keep in sync with implementation
 
 ## Security Considerations
 
 RAVEN is a security tool. Contributions must maintain security posture:
 
 - **Never** bypass the policy engine
 - **Never** add unrestricted command execution
 - **Never** log secrets or sensitive data
 - **Always** validate scope before action
 - **Always** use evidence integrity hashes
 - **Report** security issues privately (see SECURITY.md)
 
 ### Security Review
 
 Changes to these areas require additional security review:
 - Policy engine
 - Test executor
 - Evidence vault
 - Scope validation
 - Authentication/authorization
 - LLM integration (prompt injection prevention)
 
 ## Issue Reporting
 
 ### Bug Reports
 
 Include:
 - OS, Python/Node versions, Docker version
 - Steps to reproduce
 - Expected vs actual behavior
 - Relevant logs (redact sensitive data)
 - Screenshots if UI-related
 
 ### Feature Requests
 
 Include:
 - Use case and motivation
 - Proposed solution
 - Alternatives considered
 - Impact on existing functionality
 - Security implications
 
 ## Architecture Decisions
 
 Major architectural changes should be documented as Architecture Decision Records (ADRs) in `docs/adr/`:
 
 ```markdown
 # ADR-001: Use FastAPI for Backend
 
 ## Status: Accepted
 
 ## Context
 Need async Python web framework with OpenAPI support.
 
 ## Decision
 Use FastAPI with Pydantic v2.
 
 ## Consequences
 - Automatic OpenAPI generation
 - Async support for high concurrency
 - Pydantic validation built-in
 ```
 
 ## Licensing
 
 By contributing, you agree that your contributions will be licensed under the project's license (MIT License).
 
 ## Recognition
 
 Contributors are recognized in:
 - CONTRIBUTORS.md
 - Release notes
 - GitHub contributors graph
 
 ## Questions?
 
 - Open a GitHub Discussion for general questions
 - Open an Issue for bugs/feature requests
 - Check existing documentation first
 
 ---
 
 *Last updated: 2026-11-06*
