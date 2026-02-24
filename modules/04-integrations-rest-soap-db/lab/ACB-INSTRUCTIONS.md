# Module 4 — ACB Step-by-Step Instructions

Point-by-point instructions for each cycle. Every step tells you exactly what to click in Anypoint Code Builder.

---

## Before You Start

Make sure you have:
- Anypoint Code Builder (VS Code extension) installed and signed in
- The `customer-system-api` RAML published to Exchange (from Module 3)
- Infrastructure services running (your instructor will provide the host URL and API key)

---

## Cycle 1: Scaffold from RAML (APIkit)

**Goal:** Create a new Mule project from your RAML spec. APIkit auto-generates stub flows for every endpoint.

### Steps

1. **Open Command Palette**: Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
2. **Type**: `MuleSoft: Implement an API Specification`
3. **Select**: `From Exchange` when prompted for the source
4. **Search**: Type `customer-system-api` in the search box
5. **Select** your API specification and choose the latest version
6. **Project name**: Accept the default (`customer-system-api`) or type your own
7. **Location**: Choose a folder on your machine to create the project
8. **Wait** for ACB to scaffold the project — you'll see a progress notification

### What ACB Generates

After scaffolding, your project has:

```
customer-system-api/
├── pom.xml                          ← Maven dependencies (auto-generated)
├── mule-artifact.json               ← Mule runtime config
├── src/main/mule/
│   └── customer-system-api.xml      ← APIkit router + stub flows (auto-generated!)
├── src/main/resources/
│   ├── api/customer-system-api.raml ← Your RAML spec (imported from Exchange)
│   └── application.properties       ← Empty properties file
└── src/test/
```

### Explore the Generated Flows

1. **Open** `src/main/mule/customer-system-api.xml`
2. **Click** the canvas icon (Show Mule graphical mode) in the top-right of the editor
3. **You'll see** the main flow with:
   - **HTTP Listener** — receives incoming requests on `/api/*`
   - **APIkit Router** — routes requests to the correct flow based on method + path
4. **Scroll down** to see stub flows for each endpoint:
   - `get:\customers:api-config` — returns sample customer list
   - `get:\customers\(customerId):api-config` — returns sample single customer
   - `post:\customers:api-config` — returns sample created customer
   - `put:\customers\(customerId):api-config` — returns sample updated customer
   - `get:\customers\(customerId)\contacts:api-config` — returns sample contacts

### Validate

1. **Right-click** `customer-system-api.xml` in the Explorer panel
2. **Select**: `Run Mule Application` (or use the Run button)
3. **Open terminal** and run:
   ```
   curl http://localhost:8081/api/customers/ACCT-001
   ```
4. **Expected**: JSON response with sample customer data (from RAML examples)

> **Fallback**: If Exchange import fails, copy `customer-system-api.raml` from `lab/starter/` into your project's `src/main/resources/api/` folder, then use Command Palette > `MuleSoft: Implement this local API`.

---

## Cycle 2: Variables, Logger, and Transform Message

**Goal:** Replace the stub in the GET /{customerId} flow with real DataWeave logic.

### What You're Building

The GET /{customerId} flow will:
1. Extract `customerId` from the URL path
2. Log the customer ID being processed
3. Return a JSON response built with DataWeave

### Steps

1. **Open** `customer-system-api.xml` in canvas mode
2. **Click** on the `get:\customers\(customerId):api-config` flow
3. **Delete** the existing stub payload (click the Set Payload component > trash icon)

**Add Set Variable:**

4. **Click** the `+` (Add component) icon inside the flow
5. **Search**: `Set Variable` in the Add Component panel
6. **Select**: `Set Variable` under Core
7. **Configure** in the properties panel on the right:
   - **Name**: `customerId`
   - **Value**: `#[attributes.uriParams.customerId]`
   - **Display Name**: `Set customerId`

**Add Logger:**

8. **Click** the `+` icon after the Set Variable
9. **Search**: `Logger` > select it
10. **Configure**:
    - **Message**: `#['Processing customer: ' ++ vars.customerId]`
    - **Level**: `INFO`

**Add Transform Message:**

11. **Click** the `+` icon after the Logger
12. **Search**: `Transform Message` (under Core) > select it
13. **Click** the Transform component, then click `Edit` to open the DataWeave editor
14. **Write this DataWeave**:
    ```dataweave
    %dw 2.0
    output application/json
    ---
    {
        customerId: vars.customerId,
        message: "Enrichment coming in next cycles"
    }
    ```

### Validate

```bash
curl http://localhost:8081/api/customers/ACCT-001
```

**Expected:**
```json
{
  "customerId": "ACCT-001",
  "message": "Enrichment coming in next cycles"
}
```

---

## Cycle 3: REST Connector (Enrichment API)

**Goal:** Call an external REST API to get company enrichment data for the customer.

### What You're Building

```
Request → Set Variable → Logger → [HTTP Request to REST API] → Transform → Response
```

The HTTP Request connector calls `GET /api/enrich/{customerId}` on the enrichment service and returns company data (name, industry, employee count, revenue).

### Steps

**Create a new file for implementation logic:**

1. **Right-click** `src/main/mule/` in Explorer > `New File` > name it `implementation.xml`
2. ACB creates the Mule XML skeleton for you

**Add global HTTP Request config:**

3. **Open** `customer-system-api.xml` (or create a `global.xml` — right-click `src/main/mule/` > New File > `global.xml`)
4. **In canvas mode**, click `+` at the global level
5. **Search**: `HTTP` > select `Request configuration`
6. **Configure**:
   - **Name**: `Enrichment_API`
   - **Host**: `localhost` (you'll change this to the NLB host in Cycle 6)
   - **Port**: `8090`
   - **Base Path**: `/api`

**Create the sub-flow:**

7. **In** `implementation.xml`, canvas mode
8. **Click** `+ Add Flow` at the bottom of the canvas
9. **Name it**: `get-enrichment-data`
10. **Change type** to `Sub-Flow` (click the flow name > toggle in properties)
11. **Click** `+` inside the sub-flow
12. **Search**: `HTTP` > `Request`
13. **Configure**:
    - **Connector configuration**: Select `Enrichment_API` from dropdown
    - **Method**: `GET`
    - **Path**: `/enrich/{customerId}`
    - **URI Parameters**: Click `+` to add: Key = `customerId`, Value = `#[vars.customerId]`

**Wire the main flow to the sub-flow:**

14. **Open** `customer-system-api.xml`
15. **In the** `get:\customers\(customerId):api-config` flow, after the Logger, click `+`
16. **Search**: `Flow Reference` > select it
17. **Configure**: **Flow name** = `get-enrichment-data`

**Update the Transform:**

18. **Click** the Transform Message component
19. **Update DataWeave** to extract REST response fields:
    ```dataweave
    %dw 2.0
    output application/json
    ---
    {
        customerId: vars.customerId,
        company: payload.companyName,
        industry: payload.industry,
        employees: payload.employeeCount,
        revenue: payload.revenue
    }
    ```

### Validate

```bash
curl http://localhost:8081/api/customers/ACCT-001
```

**Expected:**
```json
{
  "customerId": "ACCT-001",
  "company": "Romaguera-Crona",
  "industry": "Technology",
  "employees": 450,
  "revenue": 52000000
}
```

---

## Cycle 4: Database Connector (PostgreSQL)

**Goal:** Query PostgreSQL for the customer's credit score and segment.

### What You're Building

The flow now calls two sources sequentially: REST API, then Database. You need to save the REST result in a variable before the DB call overwrites the payload.

### Steps

**Add Database connector dependency (if not auto-added):**

1. ACB may prompt you to add the dependency. If not, open `pom.xml` and add the Database connector dependency, or use the canvas — when you add a DB component and it's not found locally, toggle **Search in Exchange** to download it.

**Add global Database config:**

2. **Open** `global.xml` in canvas mode
3. **Click** `+` at the global level
4. **Search**: `Database` > `Generic Connection`
5. **Configure**:
   - **Name**: `PostgreSQL_Config`
   - **URL**: `jdbc:postgresql://localhost:5432/customer360`
   - **Driver class name**: `org.postgresql.Driver`
   - **User**: `mulesoft`
   - **Password**: `mulesoft` (you'll externalize this in Cycle 6)

**Add a Set Variable to save REST data:**

6. **Open** the main flow in `customer-system-api.xml`
7. **After** the Flow Reference to `get-enrichment-data`, click `+`
8. **Add** `Set Variable`:
   - **Name**: `enrichmentData`
   - **Value**: `#[payload]`

**Create the DB sub-flow:**

9. **Open** `implementation.xml`
10. **Add** a new Sub-Flow named `get-customer-score`
11. **Click** `+` inside the sub-flow
12. **Search**: `Database` > `Select`
13. **Configure**:
    - **Connector configuration**: Select `PostgreSQL_Config`
    - **SQL Query Text**:
      ```sql
      SELECT score, segment, last_updated
      FROM customer_scores
      WHERE customer_id = :customerId
      ```
    - **Input Parameters**: `#[{customerId: vars.customerId}]`

**Wire it up:**

14. **Back in** the main flow, after Set Variable `enrichmentData`, add another `Flow Reference`
15. **Flow name**: `get-customer-score`

**Update Transform to merge both sources:**

16. **Update** the Transform Message:
    ```dataweave
    %dw 2.0
    output application/json
    var scoreData = payload[0]
    ---
    {
        customerId: vars.customerId,
        company: vars.enrichmentData.companyName,
        industry: vars.enrichmentData.industry,
        employees: vars.enrichmentData.employeeCount,
        revenue: vars.enrichmentData.revenue,
        score: scoreData.score,
        segment: scoreData.segment
    }
    ```

### Validate

```bash
curl http://localhost:8081/api/customers/ACCT-001
```

**Expected:** JSON with company data AND score/segment fields.

---

## Cycle 5: SOAP Connector (Address Validation)

**Goal:** Call a SOAP web service to validate the customer's address.

### What You're Building

Three data sources now fire sequentially: REST → DB → SOAP. Each result is saved in a variable before the next call.

### Steps

**Add Web Service Consumer dependency:**

1. Same as Cycle 4 — when you add a WSC component from the canvas, toggle **Search in Exchange** if needed.

**Add global WSC config:**

2. **Open** `global.xml` in canvas mode
3. **Click** `+` > search `Web Service Consumer` > `Configuration`
4. **Configure**:
   - **Name**: `Address_Validation`
   - **WSDL Location**: `http://localhost:8091/?wsdl`
   - **Service**: `AddressService`
   - **Port**: `AddressPort`

**Save DB result before SOAP call:**

5. **In** the main flow, after the Flow Reference to `get-customer-score`, add `Set Variable`:
   - **Name**: `scoreData`
   - **Value**: `#[payload[0]]`

**Create the SOAP sub-flow:**

6. **Open** `implementation.xml`
7. **Add** new Sub-Flow named `validate-address`
8. **Click** `+` > search `Web Service Consumer` > `Consume`
9. **Configure**:
   - **Connector configuration**: `Address_Validation`
   - **Operation**: `ValidateAddress`
10. **Set the SOAP body** — click the body field and enter this DataWeave:
    ```dataweave
    %dw 2.0
    output application/xml
    ns addr http://example.com/address
    ---
    addr#ValidateAddress: {
        addr#street: "123 Innovation Drive",
        addr#city: "Austin",
        addr#state: "TX",
        addr#postalCode: "78701"
    }
    ```

**Wire and merge:**

11. **In** the main flow, add `Flow Reference` to `validate-address`
12. **Update** the Transform to merge all three:
    ```dataweave
    %dw 2.0
    output application/json
    ---
    {
        customerId: vars.customerId,
        company: vars.enrichmentData.companyName,
        industry: vars.enrichmentData.industry,
        employees: vars.enrichmentData.employeeCount,
        revenue: vars.enrichmentData.revenue,
        score: vars.scoreData.score,
        segment: vars.scoreData.segment,
        addressValid: payload.body.ValidateAddressResponse.isValid,
        addressConfidence: payload.body.ValidateAddressResponse.confidence,
        enrichedAt: now()
    }
    ```

### Validate

```bash
curl http://localhost:8081/api/customers/ACCT-001
```

**Expected:** JSON with company + score + address validation fields.

---

## Cycle 6: Global Elements and Properties

**Goal:** Externalize all hardcoded values (hosts, ports, credentials) into `application.properties`.

### What You're Changing

No new connectors. You're refactoring — moving hardcoded values to property placeholders so the same project works in any environment.

### Steps

**Add configuration-properties to global.xml:**

1. **Open** `global.xml` in XML mode (click the code icon, not canvas)
2. **Add** as the first child element inside `<mule>`:
   ```xml
   <configuration-properties file="application.properties" doc:name="Configuration properties"/>
   ```

**Fill application.properties:**

3. **Open** `src/main/resources/application.properties`
4. **Add** these properties (replace HOST with instructor-provided NLB DNS):
   ```properties
   http.host=0.0.0.0
   http.port=8081

   enrichment.api.host=HOST_FROM_INSTRUCTOR
   enrichment.api.port=8090
   enrichment.api.basePath=/api

   db.host=HOST_FROM_INSTRUCTOR
   db.port=5432
   db.name=customer360
   db.user=mulesoft
   db.password=PASSWORD_FROM_INSTRUCTOR

   soap.address.wsdl=http://HOST_FROM_INSTRUCTOR:8091/?wsdl
   ```

**Update global configs to use placeholders:**

5. **HTTP Listener**: Change host to `${http.host}`, port to `${http.port}`
6. **Enrichment_API**: Change host to `${enrichment.api.host}`, port to `${enrichment.api.port}`, basePath to `${enrichment.api.basePath}`
7. **PostgreSQL_Config**: Change URL to `jdbc:postgresql://${db.host}:${db.port}/${db.name}`, user to `${db.user}`, password to `${db.password}`
8. **Address_Validation**: Change wsdlLocation to `${soap.address.wsdl}`

### Validate

Same curl command as Cycle 5 — output should be identical. The refactoring doesn't change behavior.

---

## Cycle 7: Scatter-Gather (Parallel Enrichment)

**Goal:** Replace sequential calls with parallel execution using Scatter-Gather.

### What You're Building

Instead of REST → save → DB → save → SOAP → merge, all three run **simultaneously**:

```
                  ┌─→ Route 1: REST enrichment ─→┐
Request → SG  ───┼─→ Route 2: DB score       ───┼─→ Merge Transform → Response
                  └─→ Route 3: SOAP address   ──→┘
```

### Steps

**Remove sequential flow-refs and set-variables:**

1. **Open** the main flow in canvas mode
2. **Delete** the three Flow References and the two Set Variables (enrichmentData, scoreData)

**Add Scatter-Gather:**

3. **Click** `+` where the flow-refs were
4. **Search**: `Scatter-Gather` (under Core > Routers)
5. **Select** it — ACB adds it with two default routes

**Configure routes:**

6. **Click** Route 1 > `+` > `Flow Reference` > **Flow name**: `get-enrichment-data`
7. **Click** Route 2 > `+` > `Flow Reference` > **Flow name**: `get-customer-score`
8. **Add a third route**: Click the `+` icon on the Scatter-Gather to add Route 3
9. **Click** Route 3 > `+` > `Flow Reference` > **Flow name**: `validate-address`

**Update the Transform:**

10. **After** the Scatter-Gather, add/update the Transform Message:
    ```dataweave
    %dw 2.0
    output application/json
    var enrichment = payload."0".payload
    var scoreData  = payload."1".payload[0]
    var address    = payload."2".payload
    ---
    {
        customerId:        vars.customerId,
        company:           enrichment.companyName,
        industry:          enrichment.industry,
        employees:         enrichment.employeeCount,
        revenue:           enrichment.revenue,
        score:             scoreData.score,
        segment:           scoreData.segment,
        addressValid:      address.body.ValidateAddressResponse.isValid,
        addressConfidence: address.body.ValidateAddressResponse.confidence,
        enrichedAt:        now()
    }
    ```

> **Key concept**: Scatter-Gather results are accessed as `payload."0".payload` (Route 1), `payload."1".payload` (Route 2), etc. The string index corresponds to route order.

### Validate

Same curl — same response, but now all three calls run in parallel (faster!).

---

## Cycle 8: Choice Router (Conditional Routing)

**Goal:** Add a `?source=` query parameter to select which data source(s) to use.

### What You're Building

```
                          ┌─ source=rest → REST only ──────────→ Response
Request → Choice Router ──┼─ source=db   → DB only   ──────────→ Response
                          ├─ source=soap → SOAP only ──────────→ Response
                          └─ otherwise   → Scatter-Gather ─────→ Response
```

### Steps

**Wrap Scatter-Gather in Choice:**

1. **In canvas mode**, click `+` before the Scatter-Gather
2. **Search**: `Choice` (under Core > Routers)
3. **Select** it — ACB adds it with one `When` route and an `Otherwise`

**Move Scatter-Gather into Otherwise:**

4. **Cut** the Scatter-Gather + its Transform (select, Cmd+X)
5. **Click** inside `Otherwise` > paste (Cmd+V)
   - Alternatively, do this in XML mode — it's often easier for structural moves

**Add When routes:**

6. **Click** the Choice component > click `+` to add When routes (you need 3 total)

7. **When 1 — REST only**:
   - **Expression**: `#[attributes.queryParams.source == 'rest']`
   - Add inside: `Flow Reference` to `get-enrichment-data`
   - Add after: `Transform Message` returning REST-only JSON

8. **When 2 — DB only**:
   - **Expression**: `#[attributes.queryParams.source == 'db']`
   - Add inside: `Flow Reference` to `get-customer-score`
   - Add after: `Transform Message` returning DB-only JSON

9. **When 3 — SOAP only**:
   - **Expression**: `#[attributes.queryParams.source == 'soap']`
   - Add inside: `Flow Reference` to `validate-address`
   - Add after: `Transform Message` returning SOAP-only JSON

### Validate

```bash
# All sources (default — hits Scatter-Gather)
curl http://localhost:8081/api/customers/ACCT-001

# REST only
curl "http://localhost:8081/api/customers/ACCT-001?source=rest"

# DB only
curl "http://localhost:8081/api/customers/ACCT-001?source=db"

# SOAP only
curl "http://localhost:8081/api/customers/ACCT-001?source=soap"
```

---

## Cycle 9: Error Handling (Try Scope)

**Goal:** Add graceful error handling so failures return proper HTTP status codes instead of stack traces.

### What You're Building

```
Request → Try Scope ──→ Choice Router (from Cycle 8)
                    └── Error Handler
                         ├─ HTTP:NOT_FOUND      → 404 JSON
                         ├─ *:CONNECTIVITY       → 503 JSON
                         └─ ANY                  → log + re-throw
```

### Steps

**Wrap Choice in Try scope:**

1. **In canvas mode**, click `+` before the Choice Router
2. **Search**: `Try` (under Core > Error Handling)
3. **Select** it — ACB adds a Try scope
4. **Move** the Choice Router inside the Try scope (cut/paste or drag, or do in XML mode)

**Add error handlers:**

5. **Click** the Try scope > you'll see an Error Handler section at the bottom
6. **Click** `+` in the Error Handler

7. **On Error Continue — NOT_FOUND (404)**:
   - **Type**: `HTTP:NOT_FOUND`
   - Add inside: `Set Variable` — name: `httpStatus`, value: `404`
   - Add: `Transform Message`:
     ```dataweave
     %dw 2.0
     output application/json
     ---
     {
         error: "Customer not found",
         customerId: vars.customerId,
         status: 404
     }
     ```

8. **On Error Continue — CONNECTIVITY (503)**:
   - Click `+` to add another error handler
   - **Type**: `HTTP:CONNECTIVITY, DB:CONNECTIVITY, WSC:CONNECTIVITY`
   - Add inside: `Set Variable` — name: `httpStatus`, value: `503`
   - Add: `Transform Message`:
     ```dataweave
     %dw 2.0
     output application/json
     ---
     {
         error: "Service temporarily unavailable",
         customerId: vars.customerId,
         status: 503
     }
     ```

9. **On Error Propagate — ANY (catch-all)**:
   - Click `+` to add another error handler
   - Select `On Error Propagate` (not Continue)
   - **Type**: `ANY`
   - Add: `Logger` with message `#['Unhandled error for customer: ' ++ (vars.customerId default 'unknown')]`

### Validate

```bash
# Happy path — should still work
curl http://localhost:8081/api/customers/ACCT-001

# Invalid customer — should return 404 JSON (if REST API returns 404)
curl http://localhost:8081/api/customers/INVALID-999

# Stop one backend service, then call — should return 503 JSON
curl http://localhost:8081/api/customers/ACCT-001
```

**Expected for 503:**
```json
{
  "error": "Service temporarily unavailable",
  "customerId": "ACCT-001",
  "status": 503
}
```

---

## Solution Checkpoints

After each cycle, compare your project with the reference solution:

| Cycle | Solution Directory |
|-------|-------------------|
| 1 | `lab/solution-cycle-01/` |
| 2 | `lab/solution-cycle-02/` |
| 3 | `lab/solution-cycle-03/` |
| 4 | `lab/solution-cycle-04/` |
| 5 | `lab/solution-cycle-05/` |
| 6 | `lab/solution-cycle-06/` |
| 7 | `lab/solution-cycle-07/` |
| 8 | `lab/solution-cycle-08/` |
| 9 | `lab/solution-cycle-09/` |

If you get stuck, open the solution XML files and compare with yours. Focus on the `implementation.xml` and `global.xml` files — those change the most between cycles.
