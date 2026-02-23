# MuleSoft Technical Conventions

Standards for all MuleSoft artifacts generated in this course. Follow these exactly.

---

## MuleSoft MCP Server Tools

When building Mule projects, prefer MCP tools over manual file creation:

| Tool | When to Use |
|------|-------------|
| `create_mule_project` | Starting each lab — scaffolds project structure |
| `generate_mule_flow` | Building flows — AI generates Mule XML via quality pipeline |
| `generate_api_spec` | Module 3 — AI generates RAML/OAS specs |
| `create_api_spec_project` | Scaffolding RAML project structure |
| `implement_api_spec` | Generating APIkit flows from a spec |
| `generate_or_modify_munit_test` | Every lab — generates test cases with mocks |
| `validate_project` | Validating project structure before committing |
| `search_asset` | Finding connectors/templates on Exchange |
| `deploy_mule_application` | Module 7 — deploy to CloudHub 2.0 |
| `dataweave_run_script_tool` | Module 5 — validate DW transforms |
| `dataweave_create_sample_data` | Module 5 — generate test fixtures |
| `mock_api_spec` | Testing endpoints via mocking service |

**Flow**: Always try MCP tool first → review generated output → manually adjust if needed.

---

## RAML 1.0 Conventions

### File Structure
```
api-name/
├── api-name.raml          # Main spec (with !include refs)
├── data-types/
│   ├── customer.raml      # #%RAML 1.0 DataType fragment
│   └── contact.raml
├── traits/
│   └── error-responses.raml  # #%RAML 1.0 Trait fragment
└── examples/
    ├── customer-example.json
    └── contact-example.json
```

### Naming
- File names: `kebab-case.raml`
- Data type names: `PascalCase` (e.g., `Customer`, `ErrorResponse`)
- Trait names: `camelCase` (e.g., `errorResponses`, `paginated`)
- Resource paths: `/lowercase-kebab-case`
- URI params: `camelCase` in braces (e.g., `/{customerId}`)
- Query params: `camelCase` (e.g., `?industryFilter`)

### Required Patterns
- Always define `title`, `version`, `baseUri`
- Use `types:` for data types (not `schemas:` — deprecated)
- Optional fields use `?` suffix: `phone?: string`
- Always include `example:` or `examples:` on response bodies
- Use traits for cross-cutting concerns (errors, pagination)
- Apply traits with `is: [traitName]`
- Use `!include` for modular specs (data types, traits, examples)

### Example Data
- Customer IDs: `ACCT-001` through `ACCT-010` (consistent across all modules)
- Contact IDs: `CONT-001` through `CONT-020`
- Use realistic but fictional data (names, emails, companies)
- Industries: Technology, Healthcare, Financial Services, Manufacturing, Retail

---

## Mule 4 XML Flow Conventions

### Project Structure
```
src/
├── main/
│   ├── mule/
│   │   ├── main.xml              # APIkit router + main flow
│   │   ├── implementation.xml     # Business logic flows
│   │   ├── global-config.xml      # All global elements
│   │   └── error-handler.xml      # Global error handlers
│   └── resources/
│       ├── application.properties # Default properties
│       ├── api/                   # RAML spec files
│       └── dwl/                   # External DataWeave (.dwl) files
└── test/
    ├── munit/                     # MUnit test suites
    └── resources/                 # Test fixtures
```

### Flow Naming
- Main API flow: `{api-name}-main`
- APIkit-generated flows: `get:\resource:api-config`, `post:\resource:api-config`
- Implementation sub-flows: `{verb}-{resource}-implementation`
- Utility sub-flows: `get-enrichment-data`, `get-customer-score`, `validate-address`
- Error handler flows: `global-error-handler`

### Global Elements
- Define ALL connector configs in `global-config.xml`
- Use property placeholders: `${property.name}` — never hardcode values
- Naming: `{Connector_Type}_Config` (e.g., `HTTP_Listener_Config`, `Source_SF_Config`)
- Group related configs with XML comments

### Properties File Convention
```properties
# HTTP Listener
http.host=0.0.0.0
http.port=8081

# REST Enrichment API
enrichment.api.host=${EC2_HOST}
enrichment.api.port=8090
enrichment.api.basePath=/api

# PostgreSQL
db.host=${EC2_HOST}
db.port=5432
db.name=customer360
db.user=mulesoft
db.password=${DB_PASSWORD}

# SOAP Address Validation
soap.address.wsdl=http://${EC2_HOST}:8091/ws/address?wsdl

# Salesforce Source
sf.source.consumerKey=${SF_SOURCE_CLIENT_ID}
sf.source.consumerSecret=${SF_SOURCE_CLIENT_SECRET}
```

Sensitive values use `${}` placeholders — set via Runtime Manager properties at deploy time.

### Error Handling Pattern
```xml
<!-- Always wrap risky operations in Try scope -->
<try>
  <!-- business logic -->
  <error-handler>
    <on-error-continue type="HTTP:NOT_FOUND" enableNotifications="false" logException="false">
      <!-- Return 404 JSON -->
    </on-error-continue>
    <on-error-continue type="*:CONNECTIVITY" enableNotifications="false" logException="false">
      <!-- Return 503 JSON -->
    </on-error-continue>
    <on-error-propagate type="ANY">
      <!-- Log and re-raise for global handler -->
    </on-error-propagate>
  </error-handler>
</try>
```

### Scatter-Gather Result Access
```
payload."0".payload  → Route 1 result
payload."1".payload  → Route 2 result
payload."2".payload  → Route 3 result
```
Always document which route is which with XML comments.

---

## DataWeave 2.0 Conventions

### File Structure
- Inline DW for simple expressions (< 5 lines)
- External `.dwl` files in `src/main/resources/dwl/` for complex transforms
- Reusable modules in `src/main/resources/dwl/modules/`

### Header
```dataweave
%dw 2.0
output application/json
---
```
Always specify `output` format. Never omit it.

### Naming
- Module files: `kebab-case.dwl` (e.g., `customer-utils.dwl`)
- Function names: `camelCase` (e.g., `normalizePhone`, `classifySegment`)
- Variable names: `camelCase` (e.g., `var enrichmentData = ...`)

### Core Functions (know these cold)
| Function | Use Case |
|----------|----------|
| `map` | Transform each element in array |
| `filter` | Keep elements matching condition |
| `reduce` | Aggregate to single value |
| `groupBy` | Group array by field value |
| `distinctBy` | Remove duplicates |
| `flatten` | Flatten nested arrays |
| `mapObject` | Transform object keys/values |
| `pluck` | Object → array |
| `orderBy` | Sort array |
| `joinBy` | Array → string |

### Null Safety
```dataweave
// ALWAYS handle nulls
payload.email default "unknown@example.com"
payload.phone default payload.altPhone default "N/A"

// Use skipNullOn for clean output
output application/json skipNullOn="everywhere"
```

### Validation
- **Every** DataWeave solution MUST be tested in the DataWeave Playground
- Add comment to validated solutions: `// Validated in DW Playground — verify before production use`
- Recursive patterns (Exercise 7) are error-prone — double-verify manually

---

## MUnit Test Conventions

### Test Structure
```xml
<munit:test name="test-happy-path" description="GET /customers/ACCT-001 returns enriched data">
  <!-- Given: mock external connectors -->
  <munit:behavior>
    <munit-tools:mock-when processor="http:request">
      <munit-tools:with-attributes>
        <munit-tools:with-attribute attributeName="config-ref" whereValue="Enrichment_API"/>
      </munit-tools:with-attributes>
      <munit-tools:then-return>
        <munit-tools:payload value="#[readUrl('classpath://test-data/enrichment-response.json')]"/>
      </munit-tools:then-return>
    </munit-tools:mock-when>
  </munit:behavior>

  <!-- When: execute the flow -->
  <munit:execution>
    <flow-ref name="get-customer-flow"/>
  </munit:execution>

  <!-- Then: assert results -->
  <munit:validation>
    <munit-tools:assert-that expression="#[payload.customerId]" is="#[MunitTools::equalTo('ACCT-001')]"/>
  </munit:validation>
</munit:test>
```

### Rules
- Mock **only** outbound connectors (HTTP Request, Database, WSC, Salesforce) — never mock flow-ref
- One test file per flow file: `test-implementation.xml` tests `implementation.xml`
- Test names: `test-{scenario}` (e.g., `test-invalid-id-returns-404`)
- Use `readUrl('classpath://test-data/...')` for fixture data
- Target 80%+ code coverage
- Always test: happy path, invalid input (404), connectivity failure (503)
- Use `generate_or_modify_munit_test` MCP tool to generate, then review

---

## Salesforce Connector Conventions

### Authentication
- Use **OAuth 2.0 Username-Password** for course simplicity
- Store all credentials in `application.properties` with `${sf.source.*}` / `${sf.target.*}` prefixes
- Never commit real credentials — use `.template` suffix for templates

### SOQL
- Always specify field list — never `SELECT *`
- Use parameterized queries where possible
- For batch: query all records, let Batch Job handle iteration

### Batch Job
- `blockSize="200"` (Salesforce API limit per call)
- `maxConcurrency="1"` for course labs (avoid API limits)
- Always use **Upsert** with External ID for idempotent operations
- External ID fields: `Source_Account_Id__c`, `Source_Contact_Id__c`

---

## Infrastructure Conventions (Docker)

### Ports
| Service | Port | Purpose |
|---------|------|---------|
| Mock API (Flask) | 5173 | Module 1 |
| REST Enrichment (FastAPI) | 8090 | Module 4 |
| SOAP Validation (Spyne) | 8091 | Module 4 |
| PostgreSQL | 5432 | Module 4 |
| Mule App (local) | 8081 | All modules |

### Docker Compose
- All services in one `docker-compose.yml`
- Use health checks for service readiness
- PostgreSQL uses `init.sql` for schema + seed data
- All images pinned to specific versions
