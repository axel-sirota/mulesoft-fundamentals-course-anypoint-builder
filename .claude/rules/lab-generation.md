# Lab Generation Rules

Standards for generating lab starters, solutions, and fixtures across all modules.

---

## The Build Loop (Per Lab)

Follow this sequence every time. Do not skip steps.

```
1. Generate solution FIRST (using MCP tools where possible)
2. Validate solution works (run, test, verify output)
3. Strip solution → create starter (replace implementations with TODOs)
4. Walk through starter as if you're a student → find gaps?
5. Generate lab instructions for the HTML notebook
6. Create demo artifacts (completed versions of every instructor demo in the module)
7. Generate MUnit tests for the solution
8. Verify tests pass against solution
9. Verify demo artifacts run/render correctly
10. Commit solution + starter + tests + demos + instructions
```

**Critical**: Solution is ALWAYS built first. Starter is derived from solution by removing implementation and adding TODOs. Never build starter first. Demo artifacts are NON-NEGOTIABLE — they are the instructor's safety net, the time-pressure fallback, and the student's take-home reference.

---

## Starter Files

### What a Starter Contains
- Complete project structure (directories, pom.xml, configs)
- All dependencies declared in pom.xml
- Property files with placeholder values
- Flow XML with structure intact but implementations replaced by TODO comments
- RAML skeletons with resource structure but types/examples as TODOs

### TODO Format
```xml
<!-- TODO 1: Add HTTP Request connector to call enrichment API
     Hint: Use the Enrichment_API global config
     Expected: GET /api/enrich/{customerId} returns company data -->
```

```yaml
# TODO 1: Define the Customer data type
# Properties: id, firstName, lastName, email, phone (optional),
#   company, industry
# Hint: Optional fields use '?' suffix
```

### Rules
- Number all TODOs sequentially: `TODO 1`, `TODO 2`, etc.
- Every TODO includes: what to do, a hint, and what the expected result is
- TODOs match the lab steps in the HTML notebook 1:1
- Starter must compile/parse without errors (even with TODOs — they're in comments)
- Starter must run (returning mock data or empty responses is fine)

---

## Solution Files

### What a Solution Contains
- Complete, working implementation
- All flows implemented
- All DataWeave transforms complete
- All properties populated (with EC2_HOST placeholder for infra)
- All MUnit tests passing

### Rules
- Must produce the exact output described in lab validation checkpoints
- Python scripts: must run with `python3 script.py` (no modifications needed)
- Mule projects: must run locally with `mvn clean package` succeeding
- DataWeave: must match expected fixture output when tested in DW Playground
- Every solution file has a header comment:

```xml
<!-- Solution: Module 4, Cycle 3 — REST Connector
     This is the complete implementation. Compare with your starter. -->
```

```dataweave
// Solution: Exercise 1 — Filter & Map
// Validated in DW Playground — verify before production use
```

---

## Demo Artifacts

Demos are the instructor's **safety net**, **time-pressure fallback**, and **student take-home**. Every instructor demo section in the HTML notebook must have a corresponding artifact that can be shown directly if the live demo fails or time runs short.

### Two Types of Demo Artifacts

**Standalone demos** — The demo builds something DIFFERENT from the lab:
- Create a separate `demo-{descriptive-name}.{ext}` file at the **module root level**
- Examples: `demo-coupled.py` (Module 1), `demo-customer-api.raml` (Module 3)
- The packaging script automatically collects these into a `demos/` folder in the zip

**Lab-as-demo** — The demo builds the SAME thing as the lab:
- `lab/solution/` serves double duty as the demo artifact — no separate file needed
- Examples: Module 4 (cycles build the same project), Module 6 (batch ETL)
- Document this in the HTML with a comment: `<!-- Demo artifact: lab/solution/ -->`

### Naming Convention
- Files: `demo-{descriptive-name}.{ext}` (e.g., `demo-coupled.py`, `demo-customer-api.raml`)
- Placed at module root: `modules/{NN}-{name}/demo-{name}.{ext}`
- The `collect_demo_files()` function in `package-student-materials.py` picks up all non-HTML files at module root

### Rules
- Every `<details class="instructor-note">` demo section MUST have an artifact (standalone or lab/solution)
- Demo artifacts must be runnable/valid: Python compiles, RAML/YAML parses, Mule XML is well-formed
- Header comment linking to the demo section:
  ```python
  # Demo: Module 1, Section 2 — The Coupled Way
  # Run: python3 demo-coupled.py (with mock API running on port 5173)
  ```
  ```yaml
  # Demo: Module 3, Section 3 — Designing in ACB
  # This is the completed spec the instructor creates during the live demo.
  ```
- Platform UI walkthroughs (Module 2) are the ONE exception — no artifact needed for clicking through a browser

### Module Demo Artifact Map

| Module | Demo | Artifact Type | File |
|--------|------|--------------|------|
| 1 | Coupled Python | Standalone | `demo-coupled.py` |
| 1 | MuleSoft Way | Lab-as-demo | `lab/starter/` (pre-built project) |
| 2 | Platform Tour | Exception | None (UI walkthrough) |
| 3 | Design in ACB | Standalone | `demo-customer-api.raml` |
| 4 | Cycles 1-9 | Lab-as-demo | `lab/solution/` (cycle-9 state) |
| 5 | DW Playground | Lab-as-demo | Fixture files + exercise solutions |
| 6 | SF Batch ETL | Lab-as-demo | `lab/solution/` |
| 7 | Deploy + MAC | Lab-as-demo | `lab/solution/` |

---

## Fixture Files (Module 5)

### Naming Convention
```
fixtures/
├── ex1-input.json          # Exercise 1 input
├── ex1-expected.json       # Exercise 1 expected output
├── ex2-input.json
├── ex2-expected.csv         # Note: output format matches exercise
├── ex3-input.csv            # Note: input format varies
├── ex3-expected.json
├── ex9-company.json         # Multi-input exercises use descriptive names
├── ex9-address.json
├── ex9-score.json
└── ex9-expected.json
```

### Data Rules
- All fixtures use the Customer 360 domain
- Customer IDs: `ACCT-001` through `ACCT-010`
- Data is realistic, diverse, and memorable
- Industries: Technology (at least 4), Healthcare, Financial Services, Manufacturing, Retail
- Names: diverse, fictional, consistent across modules
- Input files contain enough records to exercise the transform (typically 8-20 records)
- Expected output files are the **exact** output of a correct DataWeave solution

### Validation
- JSON files: valid JSON (test with `python3 -m json.tool`)
- CSV files: valid CSV with consistent delimiters and quoting
- XML files: well-formed XML
- Expected outputs match solutions exactly (byte-for-byte comparison where possible)

---

## Test Data (Module 6)

### accounts.csv
- 50 records with columns: Name, Industry, Phone, BillingStreet, BillingCity, BillingState, BillingPostalCode
- Industries distributed: ~15 Technology, ~10 Healthcare, ~10 Financial Services, ~8 Manufacturing, ~7 Retail
- Real US cities and states, diverse geographic spread
- Fictional company names (never use real companies)

### contacts.csv
- 100 records with columns: FirstName, LastName, Email, Phone, Title, AccountName
- Each Contact references one of the 50 Accounts by AccountName
- ~2 Contacts per Account average (some 1, some 3)
- Titles: CEO, CTO, VP Sales, VP Engineering, Director of Marketing, Account Manager, etc.
- Diverse names, valid email format: `firstname.lastname@companyname.com`

---

## Mule Project Labs (Modules 4, 6, 7)

### Incremental Build Pattern (Module 4)
Module 4 builds one project across 9 cycles. Each cycle adds to the previous.

```
cycle-01: Scaffold from RAML (APIkit stubs)
cycle-02: + DataWeave in flows (variables, transforms)
cycle-03: + REST connector (enrichment API)
cycle-04: + Database connector (PostgreSQL)
cycle-05: + SOAP connector (address validation)
cycle-06: + Global elements & properties (refactoring)
cycle-07: + Scatter-Gather (parallel enrichment)
cycle-08: + Choice router (conditional routing)
cycle-09: + Error handling (Try scope)
```

- Starter = cycle-01 state
- Solution = cycle-09 state (complete)
- Each cycle's lab instructions reference the PREVIOUS cycle's output as starting point
- Git tags: `module-04/cycle-01` through `module-04/cycle-09`

### Non-Incremental Labs (Modules 3, 5)
- Starter and solution are independent
- Each lab exercise is self-contained
- Solutions don't depend on previous exercises (except Exercise 9 uses Exercise 6's module)

---

## Quality Checklist (Run Before Commit)

For every lab:
- [ ] Solution produces correct output
- [ ] Starter compiles/parses without errors
- [ ] All TODOs are numbered and have hints
- [ ] Lab steps in HTML match TODOs in starter 1:1
- [ ] Validation checkpoints are specific and testable
- [ ] Fixture data is consistent with Customer 360 domain
- [ ] No hardcoded secrets or real credentials
- [ ] Property templates use `REPLACE_WITH_*` or `${PLACEHOLDER}` format
- [ ] Demo artifacts exist for every instructor demo section (standalone or lab/solution)
- [ ] Demo artifacts run/compile/parse without errors
- [ ] Demo artifacts match the expected output described in instructor notes
