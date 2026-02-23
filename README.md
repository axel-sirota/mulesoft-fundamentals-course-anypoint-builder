# MuleSoft Basics for Salesforce Teams — 3-Day Course

A comprehensive instructor-led training course that takes Salesforce developers, admins, and architects from zero MuleSoft knowledge to building production-ready integrations.

## The Storyline: Customer 360

Every module contributes to one continuous application. Students build pieces of a real integration pipeline that connects by Day 3 into a working system:

- **Day 1** — Design: API-led connectivity concepts, Anypoint Platform tour, RAML API specification
- **Day 2** — Build: 9 incremental cycles building a Customer Enrichment Engine (REST, SOAP, DB, Scatter-Gather, error handling)
- **Day 3** — Transform & Deploy: DataWeave deep dive, Salesforce batch ETL with referential integrity, CloudHub deployment, AI classification

## Prerequisites

All free — no credit card required:

| Tool | Setup |
|------|-------|
| Anypoint Platform | [30-day free trial](https://anypoint.mulesoft.com/login/signup) |
| Anypoint Code Builder | [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=MuleSoftInc.mule-dx-extension-pack) (works in Cursor too) |
| Salesforce Developer Orgs | [2 free orgs](https://developer.salesforce.com/signup) (different emails) |
| Java 17+ | Required for Mule runtime |
| Maven 3.9+ | Required for building Mule projects |
| Docker | For EC2 infrastructure services (instructor-managed) |
| Node.js 20+ | For MuleSoft MCP server (optional) |

See [docs/environment-setup.md](docs/environment-setup.md) for detailed setup instructions.

## Module Overview

| # | Module | Duration | Day |
|---|--------|----------|-----|
| 1 | [Why MuleSoft?](modules/01-intro-to-mulesoft/module-01.html) | 60 min | 1 |
| 2 | [Anypoint Platform Tour](modules/02-anypoint-platform-tour/module-02.html) | 60 min | 1 |
| 3 | [API Design (RAML)](modules/03-api-design/module-03.html) | ~3 hours | 1 |
| 4 | [Building Integrations](modules/04-integrations-rest-soap-db/module-04.html) | All Day | 2 |
| 5 | [DataWeave](modules/05-dataweave/module-05.html) | ~3.5 hours | 3 |
| 6 | [Salesforce Batch ETL](modules/06-salesforce-etl-batch/module-06.html) | ~3 hours | 3 |
| 7 | [Deploy + AI](modules/07-deploy-manage-llm/module-07.html) | ~2 hours | 3 |

## Infrastructure (Instructor-Managed)

Module 4 requires three services running on an EC2 instance:

| Service | Port | Purpose |
|---------|------|---------|
| REST Enrichment API (FastAPI) | 8090 | Company enrichment data |
| SOAP Address Validation (Spyne) | 8091 | Address validation + confidence |
| PostgreSQL | 5432 | Customer scores + segments |

See [infrastructure/README.md](infrastructure/README.md) for deployment instructions.

## Repo Structure

```
shared/          — Mock API, DataWeave modules, property templates
infrastructure/  — Docker Compose services for Module 4
modules/         — 7 module directories (HTML notebooks + lab starters/solutions)
docs/            — Setup guide, instructor guide, troubleshooting
prompts/         — Claude Code build prompts (internal)
```

## For Instructors

See [docs/instructor-guide.md](docs/instructor-guide.md) for timing, demo tips, and recovery steps.
