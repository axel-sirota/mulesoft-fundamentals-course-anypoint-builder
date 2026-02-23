---
description: Perform comprehensive code review of course materials
---

# Code Review Command

Systematic review of course materials — code, HTML notebooks, fixtures, and lab content.

## Review Checklist

**1. Context Load**
- Read `.claude/rules/` to load style guides and conventions.

**2. Security Audit**
- Check for hardcoded secrets in property files or scripts.
- Verify `.gitignore` excludes credentials, .env files, and IDE configs.
- Check Python scripts for injection vulnerabilities.

**3. Content Quality**
- HTML notebooks: all mermaid diagrams valid, Prism.js snippets correct, collapsible sections work.
- Code snippets: syntax-highlighted correctly, copy buttons present.
- Lab instructions: clear TODOs, validation checkpoints present.

**4. Data Consistency**
- Customer IDs (ACCT-001 through ACCT-010) consistent across all modules.
- Fixture data matches between input and expected output files.
- Mock API data matches course domain (Customer 360).

**5. Completeness**
- Every module has: HTML notebook, lab/starter, lab/solution.
- Every lab has: clear instructions, validation checkpoints, starter with TODOs, complete solution.
- Infrastructure files: docker-compose runs, services respond on correct ports.

**6. Testing**
- Python scripts run without errors.
- DataWeave solutions match expected fixtures.
- Docker services start and respond.
