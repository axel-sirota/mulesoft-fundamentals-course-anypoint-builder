# Module 4: Building the Customer Enrichment Engine — Instructor Guide

**Duration:** ~6.5 hours (entire Day 2)
**Format:** 9 incremental theory → demo → lab cycles building one Mule project
**Prerequisites:** Module 3 RAML spec published to Exchange, infrastructure services running

---

## Pre-Class Setup

### Infrastructure
- ECS Fargate services must be running (REST :8090, SOAP :8091, PostgreSQL :5432)
- Verify: `curl http://<NLB_DNS>:8090/health` returns `{"status": "healthy"}`
- Verify: `curl http://<NLB_DNS>:8091/ws/address?wsdl` returns WSDL XML
- Share with students: NLB DNS name, API key (if enabled), DB credentials

### Student Environment
- Anypoint Code Builder (VS Code extension) installed and logged in
- Students have published their Module 3 RAML spec to Exchange
- Java 17 available (`java -version` shows 17.x)
- Maven configured with MuleSoft repositories

### Fallback
- All 9 solution checkpoints are in `lab/solution-cycle-01/` through `lab/solution-cycle-09/`
- If a student falls behind, they can copy the previous cycle's solution and continue

---

## Cycle 1: Scaffold from RAML & APIkit Router (45 min)

### Timing
- Theory: 10 min
- Demo: 15 min
- Lab: 20 min

### Demo Script
1. Click MuleSoft logo → Quick Actions → "Implement an API"
2. Search "Customer System API" → select v1 → Import
3. Wait for Maven to resolve (1-2 min)
4. Show `src/main/mule/` — point out generated files
5. Open main XML — highlight `<apikit:router config-ref="api-config"/>`
6. Show canvas view briefly (top-right icon toggle)
7. Right-click project → "Run Mule Application"
8. Wait for DEPLOYED message
9. `curl -s http://localhost:8081/api/customers | python3 -m json.tool`
10. Show stub response from RAML examples

### Talking Points
- "APIkit reads your RAML and generates routes automatically — zero code"
- "Every HTTP method + resource in your spec gets a flow stub"
- "We replace stubs with real logic over the next 8 cycles"

### Recovery
- If Exchange import fails: students can copy RAML from `lab/starter/customer-system-api/src/main/resources/api/`
- If Maven fails: check `~/.m2/settings.xml` has MuleSoft repos

### Validation
- `curl http://localhost:8081/api/customers` returns JSON array
- `curl http://localhost:8081/api/invalid` returns 405

---

## Cycle 2: DataWeave in Flows (45 min)

### Timing
- Theory: 15 min (Mule Event model is critical concept)
- Demo: 10 min
- Lab: 20 min

### Demo Script
1. Open the `get:\customers\(customerId):api-config` flow
2. Replace stub with `<set-variable>` for customerId
3. Add `<logger>` with DW expression
4. Add `<ee:transform>` with placeholder JSON
5. Restart → test with curl
6. Show logger output in terminal

### Talking Points
- "The Mule Event has three parts: attributes (headers, params), payload (body), variables (your scratch space)"
- "DataWeave expressions start with `#[` and end with `]`"
- "`vars.customerId` persists across the flow — payload changes with every processor"

### Recovery
- Common error: missing `xmlns:ee` namespace → "Did you add the ee namespace to the mule root element?"
- If DW syntax error: check for missing `%dw 2.0` header or `output` directive

### Validation
- `curl http://localhost:8081/api/customers/ACCT-001` returns JSON with customerId
- Terminal shows "Processing customer: ACCT-001"

---

## Cycle 3: REST Connector (45 min)

### Timing
- Theory: 10 min
- Demo: 15 min
- Lab: 20 min

### Demo Script
1. Open `global.xml` → add `<http:request-config name="Enrichment_API">`
2. In implementation, add `<flow-ref name="get-enrichment-data"/>`
3. Create `<sub-flow name="get-enrichment-data">` with HTTP Request
4. Add `<http:uri-params>` with DW expression
5. Update transform to map enrichment fields
6. Restart → `curl ACCT-001` → show company data

### Talking Points
- "HTTP Listener = inbound (someone calls you). HTTP Request = outbound (you call someone)"
- "Sub-flows keep your main flow clean — one responsibility per sub-flow"
- "URI params use DataWeave: `#[{customerId: vars.customerId}]`"

### Recovery
- Connection refused: verify enrichment API is running on port 8090
- 403 Forbidden: check if API key is required (`-H "X-API-Key: <key>"`)

### Validation
- Response includes `"company": "Romaguera-Crona"` for ACCT-001

---

## Cycle 4: Database Connector (45 min)

### Timing
- Theory: 10 min
- Demo: 15 min
- Lab: 20 min

### Demo Script
1. Open `pom.xml` → add DB connector + PostgreSQL driver dependencies
2. Save → wait for Maven to resolve
3. Open `global.xml` → add `<db:config name="PostgreSQL_Config">`
4. Create `<sub-flow name="get-customer-score">` with `<db:select>`
5. Show parameterized query: `:customerId` placeholder
6. Store enrichment in variable BEFORE DB call (payload gets overwritten)
7. Update transform to merge both sources
8. Restart → test → show score + segment

### Talking Points
- "CRITICAL: Each processor overwrites payload. Store previous results in variables!"
- "Parameterized queries use `:name` — NEVER concatenate strings (SQL injection)"
- "DB results are always an array — even for one row. Use `payload[0]`"

### Recovery
- "Class not found: org.postgresql.Driver" → missing postgresql dependency in pom.xml
- Connection refused → check DB host/port, ensure PostgreSQL is running

### Validation
- Response includes `"score": 85` and `"segment": "premium"` for ACCT-001

---

## Cycle 5: SOAP Connector (30 min)

### Timing
- Theory: 10 min
- Demo: 10 min
- Lab: 10 min

### Demo Script
1. Open `pom.xml` → add WSC connector dependency
2. Open `global.xml` → add `<wsc:config>` with WSDL URL
3. Create `<sub-flow name="validate-address">` with `<wsc:consume>`
4. **Key moment:** Show namespace in DW body: `ns addr http://example.com/address`
5. Show WSDL in browser to find the namespace
6. Restart → test → show addressValid + confidence

### Talking Points
- "SOAP is XML-based — you build the request body with DataWeave using XML namespaces"
- "The namespace MUST match what's in the WSDL's targetNamespace"
- "Open the WSDL URL in your browser to find the right namespace and operation name"

### Recovery
- Namespace mismatch: check `?wsdl` endpoint for actual targetNamespace
- "Operation not found": operation name must match WSDL exactly (case-sensitive)

### Validation
- Response includes `"addressValid": true` and `"addressConfidence"` number

---

## Cycle 6: Global Elements & Refactoring (30 min)

### Timing
- Theory: 10 min
- Demo: 10 min
- Lab: 10 min

### Demo Script
1. Create `application.properties` in `src/main/resources/`
2. Add all property key-value pairs
3. Add `<configuration-properties>` to global.xml
4. Replace every hardcoded value with `${property.name}`
5. Restart → test → same results, cleaner code

### Talking Points
- "One file to change when you deploy to a different environment"
- "Never hardcode hosts, ports, or credentials in XML — properties file or env vars"
- "Sensitive values use `${ENV_VAR}` — set in Runtime Manager at deploy time"

### Recovery
- "Could not resolve placeholder" → property name typo, or missing configuration-properties element
- Properties file in wrong location → must be in `src/main/resources/`

### Validation
- All endpoints return identical data as before refactoring
- Zero hardcoded host/port values in any XML file

---

## Cycle 7: Scatter-Gather & Parallelism (45 min)

### Timing
- Theory: 15 min
- Demo: 15 min
- Lab: 15 min

### Demo Script
1. Replace three sequential flow-refs with `<scatter-gather>`
2. Each flow-ref gets its own `<route>` wrapper
3. Add merge Transform with `payload."0".payload` syntax
4. Show canvas view briefly — visual parallel branches
5. Restart → test → show unified response
6. Point out log timestamps — all three started nearly simultaneously

### Talking Points
- "Sequential: 3 seconds. Parallel: 1 second. Free performance."
- "Scatter-Gather keys are STRINGS: `payload.\"0\"` with quotes, not `payload.0`"
- "Route 0 = first route in XML order. Always comment which route is which"
- "If ANY route fails, the entire scatter-gather fails — we handle that in Cycle 9"

### Recovery
- "Expression payload.0 is not valid" → must use string keys: `payload."0"`
- Missing route data → check route order matches the merge transform

### Validation
- Single response includes company, score, AND addressValid

---

## Cycle 8: Choice Router (30 min)

### Timing
- Theory: 10 min
- Demo: 10 min
- Lab: 10 min

### Demo Script
1. Wrap scatter-gather in `<choice>` element
2. Add three `<when>` blocks for source=rest, source=db, source=soap
3. Move scatter-gather into `<otherwise>`
4. Each when block: single flow-ref + per-source Transform
5. Test all four paths with curl

### Talking Points
- "Choice = if/else in Mule. First matching `when` wins."
- "Otherwise = the default path — when no condition matches"
- "Query params accessed via `attributes.queryParams.source`"

### Recovery
- All routes return same data → check `expression` attribute syntax
- Otherwise never triggered → make sure expression uses `==` not `=`

### Validation
- `?source=rest` returns only enrichment data
- `?source=db` returns only score
- No parameter returns full merged response

---

## Cycle 9: Error Handling (45 min)

### Timing
- Theory: 15 min
- Demo: 15 min
- Lab: 15 min

### Demo Script
1. Wrap entire choice in `<try>` scope
2. Add `<error-handler>` with three handlers
3. `on-error-continue type="HTTP:NOT_FOUND"` → 404 JSON
4. `on-error-continue type="HTTP:CONNECTIVITY, DB:CONNECTIVITY, WSC:CONNECTIVITY"` → 503 JSON
5. `on-error-propagate type="ANY"` → log + re-throw
6. Test invalid customer → show 404 response
7. Stop a Docker service → show 503 response
8. Restart service → show recovery

### Talking Points
- "on-error-continue = catch and recover (flow returns your custom response)"
- "on-error-propagate = catch, log, and re-throw (flow fails)"
- "Error types follow NAMESPACE:IDENTIFIER pattern — HTTP:NOT_FOUND, DB:CONNECTIVITY"
- "CONNECTIVITY is a parent type — catches HTTP:CONNECTIVITY, DB:CONNECTIVITY, etc."

### Recovery
- Error handler not triggering → check `type` attribute matches exactly
- 500 instead of 404 → error type might be different; check Mule logs for actual error type

### Validation
- `ACCT-001` returns full enriched response
- `INVALID-999` returns `{"error": "Customer not found"}`
- Stopped service returns `{"error": "Service unavailable"}`

---

## End-of-Day Wrap-Up (15 min)

### Recap
Walk through the final architecture diagram showing all 9 layers:
1. APIkit Router (Cycle 1)
2. DataWeave variables and transforms (Cycle 2)
3. REST connector (Cycle 3)
4. Database connector (Cycle 4)
5. SOAP connector (Cycle 5)
6. Properties externalization (Cycle 6)
7. Scatter-Gather parallelism (Cycle 7)
8. Choice routing (Cycle 8)
9. Error handling (Cycle 9)

### DataWeave Concepts Introduced Today (Bridge to Module 5)
Students used DataWeave all day without a formal introduction. Highlight what they already know:
- Script structure: `%dw 2.0`, `output application/json`, `---`
- Object construction: `{ key: value }` syntax
- Variable access: `vars.customerId`, `payload.companyName`, `attributes.queryParams.source`
- Array indexing: `payload[0].score`, `payload."0".payload` (Scatter-Gather)
- String concatenation: `'Processing: ' ++ vars.customerId`
- Built-in functions: `now()`
- XML namespaces in DW: `ns addr http://example.com/address`

What they have NOT seen (Module 5 covers these):
- Collection functions: `map`, `filter`, `reduce`, `groupBy`
- Format conversion (JSON to CSV, XML to JSON)
- Null handling (`default`, `skipNullOn`)
- Reusable modules (`fun` declarations, `import` syntax)
- External `.dwl` files (Module 5 Exercise 10 refactors today's cycle-9 project!)

### Preview Day 3
- Module 5: DataWeave deep dive — master the language behind everything you built today
- Module 6: Salesforce connector + batch ETL (reuses DataWeave modules from Module 5)
- Module 7: Deploy to CloudHub + API management
- "The cycle-9 project you built today comes back in Module 5 — you'll refactor its DataWeave into external files with reusable modules"

### Student Takeaway
- Complete solution in `lab/solution-cycle-09/`
- Each checkpoint available for reference
- HTML notebook with all code snippets and diagrams

---

## Key Talking Points (For the Whole Module)

- "Each processor overwrites payload. If you need data later, store it in a variable FIRST."
- "Sub-flows keep main flows readable — one responsibility per sub-flow"
- "Scatter-Gather keys are strings: `payload.\"0\"` with quotes, not `payload.0`"
- "Never concatenate strings in SQL queries — always use parameterized queries with `:name`"
- "DB results are always an array, even for one row. Use `payload[0]` to get the first element."
- "SOAP namespaces must match the WSDL's targetNamespace exactly — open the ?wsdl URL to check"
- "Properties externalize config. If you're hardcoding a host, port, or credential, stop and use `${property.name}`"
- "on-error-continue = catch and handle. on-error-propagate = catch, log, re-throw."
- "9 cycles, one project. Each layer adds to the previous. This is how real Mule apps are built."

## Potential Questions

- "Why 9 separate cycles instead of building everything at once?" — Incremental learning. Each cycle introduces exactly one concept. You test it, verify it works, then add the next layer. In practice, real projects also build incrementally.
- "Can I use HTTP Request for SOAP instead of WSC?" — Technically yes, but WSC handles WSDL parsing, envelope generation, and namespace management. HTTP Request would require manually building XML envelopes.
- "What if Scatter-Gather is slower than sequential?" — Only if routes are very fast (sub-ms). For real external calls (50-500ms each), parallel is always faster. The overhead is negligible.
- "Why not use Choice router conditions in the RAML?" — The RAML defines the API contract. Routing logic is implementation detail — belongs in the Mule flow, not the spec.
- "How do I debug DataWeave errors?" — Check the Mule console for the exact error type and line. In Module 5, we'll use the DW Playground where errors are shown instantly.
