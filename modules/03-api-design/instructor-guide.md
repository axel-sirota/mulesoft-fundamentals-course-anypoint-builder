# Module 3 — API Design with RAML (75 min)

## Flow

### 1. API-Led in Practice (20 min)

- Figure 1 — Customer System API at the System layer, wrapping Salesforce
  - "We're building the bottom layer first — the foundation"
  - System APIs are thin wrappers: expose clean REST, hide backend complexity
- **RAML vs OpenAPI** comparison:
  - Both are API spec languages, RAML is MuleSoft's native choice
  - RAML = YAML-based, uses `!include` for modularity, built-in types system
  - OAS = JSON/YAML, wider ecosystem (Swagger), more tooling outside MuleSoft
  - "We use RAML because MuleSoft tooling is optimized for it — ACB scaffolds directly from RAML"
  - Show the comparison table in the notebook
- **Building RAML concept by concept** — this is the meat:
  1. **Root**: `title`, `version`, `baseUri` — the identity card
  2. **Resources & Methods**: `/customers`, `/customers/{customerId}` — the contract shape
  3. **Data Types**: `Customer`, `Contact` — PascalCase, define the payload structure
     - Optional fields with `?` suffix
     - Enums for constrained values (industry, status)
  4. **Examples**: inline JSON examples — tied to types, used for mocking
  5. **Traits**: `errorResponses` — cross-cutting concerns applied with `is: [traitName]`
  6. **Query Parameters**: `industry`, `limit` — filtering and pagination
  7. **Modular specs**: `!include` for types, traits, examples — keep the root file clean
- Build these incrementally with code snippets — each one adds to the previous

### 2. API Policies & Governance (10 min)

- Figure 2 — API Gateway enforces policies before requests hit your code
  - Rate Limiting: protect from overload (10 req/min example)
  - Client ID Enforcement: only registered apps can call
  - IP Allowlist: restrict to known networks
  - OAuth 2.0: user-level auth on top of app-level
- "Your implementation code never knows about policies — the gateway handles it"
- "We won't configure policies now — that's Module 7 when we deploy"

### 3. Demo: Designing in ACB (~15 min)

- Live demo: create a RAML spec from scratch in ACB
  - Use `demo-customer-api.raml` as your safety net if live coding fails
  - Start with root element, add `/customers` resource, define `Customer` type
  - Show the API Console preview (if available in ACB)
  - Show how ACB validates RAML in real-time (Problems panel)
- Talking points during demo:
  - "Notice how ACB gives you autocomplete for RAML keywords"
  - "The indentation matters — YAML is whitespace-sensitive"
  - "Every example should match the type definition exactly"

### 4. Lab 1: Build Your API Contract (30 min)

- 8 steps, progressive difficulty:
  1. Create RAML project in ACB (scaffold)
  2. Define root elements (title, version, baseUri)
  3. Add `/customers` resource with GET
  4. Define `Customer` data type with all properties
  5. Add response body with type and example
  6. Add `/customers/{customerId}` with GET
  7. Add query parameter `industry` on collection GET
  8. Add error responses (404, 500) using a trait
- Common student issues:
  - YAML indentation errors (tabs vs spaces — RAML requires spaces)
  - Missing `?` on optional fields
  - Example JSON not matching type definition (extra/missing fields)
  - Forgetting `#%RAML 1.0` header
- Walk around during steps 4-6 — that's where most errors happen

### 5. Lab 2 (Bonus): Modularize Your Spec (15 min if time)

- Take the single-file spec and break it into:
  - `data-types/customer.raml`, `data-types/contact.raml`
  - `traits/error-responses.raml`
  - `examples/*.json`
- Use `!include` references from the root file
- "This is how real-world specs are organized — nobody ships a 500-line RAML file"
- Skip if running behind — it's a bonus

## Key Talking Points

- "API-first means the spec IS the contract — code implements it, not the other way around"
- "If it's not in the spec, it doesn't exist" — the spec is the single source of truth
- RAML types are your data model — they generate the scaffolded flows in Module 4
- Examples aren't just docs — ACB uses them for mocking and testing
- "Tomorrow you'll scaffold a full Mule project from this spec — that's why getting it right matters"

## Potential Questions

- "Why not just write the code directly?" — API-first catches design issues before you write code, plus the spec generates stubs
- "Can I use OAS instead?" — yes, ACB supports both, but course uses RAML
- "What about versioning?" — `version: v1` in baseUri, MuleSoft supports version management in Exchange
- "How do I test my spec?" — API Console in ACB, or publish to Exchange and use the mocking service
