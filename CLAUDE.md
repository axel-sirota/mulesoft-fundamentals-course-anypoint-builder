# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **3-day MuleSoft Basics ILT course** for Salesforce teams, built around a **Customer 360** storyline. The course has 7 modules, each with an HTML notebook, lab starters (with TODOs), and complete solutions. The repository is in active build phase — directory scaffolding exists but most content files still need to be created.

## Session Workflow

Always use slash commands to orchestrate work:

| Command | Purpose |
|---------|---------|
| `/start-session` | Initialize context, check progress, confirm session goal |
| `/build-module N` | Build a specific module (loads prompt, researches, plans, builds, validates) |
| `/validate-module N` | Run validation checklist against a completed module |
| `/next-session` | Generate handoff context beacon for the next session |
| `/architect X` | Design architecture for a component before building |
| `/research X` | Deep research with 3 cycles of hypothesis → evidence → refutation |
| `/code-review` | Systematic review of materials for quality, consistency, security |

**Build loop per module:** Solution FIRST → validate it works → strip to create starter with TODOs → generate lab instructions → generate MUnit tests → verify tests pass → commit.

## Key Source Documents

All generation is driven by these files — read them before building anything:

- `prompts/mulesoft-course-blueprint.md` — Master blueprint (3-day schedule, all 7 modules, infrastructure specs, data domain)
- `prompts/prompt-module-{01-07}.md` — Per-module generation prompts with exact specifications for HTML sections, diagrams, code snippets, lab steps, and validation checkpoints
- `plans/course-build-plan.md` — Phased build strategy with dependency graph, risk assessment, and 13-session execution plan

## Build Order & Dependencies

Critical sequencing (cannot be parallelized):
1. `shared/mock-api/` → Module 1 (demo uses it)
2. Module 3 RAML solution → Module 4 starter (scaffolded from RAML)
3. Module 4 solution → Module 7 starter (deploys Module 4 project)
4. Module 5 Exercise 6 solution → `shared/dataweave-modules/customer-utils.dwl`

Can be parallelized: shared/mock-api + infrastructure, Modules 1+2, Module 5 fixtures + Module 6 test-data.

## Repository Structure

```
modules/{01-07}-*/           # Each module: HTML notebook + lab/starter + lab/solution
  module-{NN}.html           # Instructor version (source of truth, has instructor notes)
  module-{NN}-student.html   # Student version (auto-generated, no instructor notes)
  lab/starter/               # Student starting point with numbered TODOs
  lab/solution/              # Complete working implementation

infrastructure/              # Docker services for Module 4 labs
  docker-compose.yml         # REST API (8090) + SOAP (8091) + PostgreSQL (5432)
  rest-api/                  # FastAPI enrichment service
  soap-service/              # Spyne address validation
  db/                        # PostgreSQL init.sql with customer_scores

shared/                      # Cross-module shared assets
  mock-api/                  # Flask mock API for Module 1 (port 5173)
  scripts/                   # Build scripts (generate-student-html.py)
  dataweave-modules/         # Reusable DW module (from Module 5 Ex6)
  properties/                # SF credential templates
  test-resources/            # Shared test fixtures

prompts/                     # Generation specs (DO NOT modify)
plans/                       # Build plans (gitignored)
docs/                        # Setup guide, instructor guide, troubleshooting
```

## Infrastructure Ports

| Service | Port | Module |
|---------|------|--------|
| Mock API (Flask) | 5173 | Module 1 |
| REST Enrichment (FastAPI) | 8090 | Module 4 |
| SOAP Validation (Spyne) | 8091 | Module 4 |
| PostgreSQL | 5432 | Module 4 |
| Mule App (local) | 8081 | All modules |

## Customer 360 Domain Data

10 core customers (ACCT-001 through ACCT-010) must appear **identically** across all modules: mock-api, RAML examples, REST enrichment API, PostgreSQL seeds, DataWeave fixtures, and Module 6 test data (first 10 of 50 accounts). See the canonical table in `.claude/rules/course-docs.md`.

## MCP Tools

Prefer MuleSoft MCP server tools over manual file creation for Mule projects:
- `create_mule_project` — scaffolding
- `generate_mule_flow` — XML flows via quality pipeline
- `generate_api_spec` / `create_api_spec_project` — RAML/OAS specs
- `implement_api_spec` — APIkit flows from spec
- `generate_or_modify_munit_test` — test generation
- `validate_project` — structure validation before commit
- `dataweave_run_script_tool` / `dataweave_create_sample_data` — DW validation

Flow: MCP tool first → review output → manually adjust if needed.

## HTML Notebooks

Self-contained HTML files with inline CSS. CDN deps: Mermaid 11 (diagrams), Prism 1.29 (syntax highlighting with copy buttons), Inter + JetBrains Mono fonts. Must render at 18px+ for projector readability. Full template spec in `.claude/rules/html-template.md`.

DataWeave has no Prism grammar — use `language-javascript` as visual fallback with `data-label="DataWeave"` on the `<pre>` tag.

### Dual Versions (Instructor & Student)

Every module produces **two** HTML files:
- `module-{NN}.html` — **Instructor version** (source of truth). Contains `<details class="instructor-note">` blocks with demo scripts, talking points, and click paths.
- `module-{NN}-student.html` — **Student version** (auto-generated). Identical content minus all instructor notes and their CSS.

**Workflow:** Always edit the instructor version. Then regenerate the student version:
```bash
.venv/bin/python3 shared/scripts/generate-student-html.py --all
```

**Never edit student files directly.** They are derived artifacts.

## Validation Commands

```bash
# Python scripts
.venv/bin/python3 -m py_compile path/to/script.py

# JSON fixtures
.venv/bin/python3 -m json.tool path/to/file.json > /dev/null

# Infrastructure services
docker-compose -f infrastructure/docker-compose.yml up -d
curl http://localhost:8090/api/enrich/ACCT-001
curl http://localhost:8091/ws/address?wsdl
psql -h localhost -p 5432 -U mulesoft -d customer360 -c "SELECT * FROM customer_scores LIMIT 1;"

# Mule projects (in project directory)
mvn clean package
mvn clean test  # MUnit tests only
```

## Known High-Risk Items

1. **DataWeave Exercise 7 (Recursive Flatten)** — LLMs struggle with recursion in DW. Double-verify manually.
2. **SOAP Service (Spyne)** — Last release Feb 2022, WSDL generation is finicky. Test early.
3. **Module 4 Complexity** — 9 incremental cycles building one project across all of Day 2. Largest module.
4. **Mule XML Generation** — MCP quality pipeline achieves ~90% validity. Always review generated XML.

## Naming Conventions Quick Reference

| Artifact | Convention | Example |
|----------|-----------|---------|
| RAML files | kebab-case.raml | `customer-system-api.raml` |
| RAML data types | PascalCase | `Customer`, `ErrorResponse` |
| RAML traits | camelCase | `errorResponses`, `paginated` |
| Mule flow names | verb-resource-implementation | `get-customer-implementation` |
| Global configs | Connector_Type_Config | `HTTP_Listener_Config` |
| Properties | dot.separated.lowercase | `http.port`, `db.host` |
| DataWeave files | kebab-case.dwl | `customer-utils.dwl` |
| DW functions | camelCase | `normalizePhone`, `classifySegment` |
| Fixture files | exN-descriptor.ext | `ex1-input.json`, `ex9-expected.json` |
