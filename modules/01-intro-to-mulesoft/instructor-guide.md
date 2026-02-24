# Module 1 — Why MuleSoft? (45 min)

## Flow

### 1. The Problem: Point-to-Point Spaghetti (10 min)

- Open with Figure 1 (6 systems, 15 connections) — ask the room "who has seen this?"
- Show Figure 2 (add 1 system = 21 connections) — the n(n-1)/2 formula, growth is quadratic
- Show Code Snippet 1 (coupled Python) — hardcoded URLs, no error handling, format-specific
- Ask: "what happens when the CRM vendor changes?" — answer: you rewrite everything
- **Demo: run `demo-coupled.py`** with mock API on port 5173
  - `cd shared/mock-api && .venv/bin/python3 server.py` (background)
  - `cd modules/01-intro-to-mulesoft && .venv/bin/python3 demo-coupled.py`
  - Point out: it works but it's brittle — what if the API is down? format changes?

### 2. The Solution: API-Led Connectivity (10 min)

- Figure 3 — three layers: Experience, Process, System
- Key message: each layer is independently deployable and reusable
- **Customer 360 walkthrough** — map the 3 layers to our course project:
  - System: Salesforce connector, REST enrichment, DB, SOAP
  - Process: orchestration, scatter-gather, DataWeave transforms
  - Experience: the final API consumers call
- Code Snippet 2 — show the Mule XML equivalent (declarative, config-driven)
- Code Snippet 3 — before/after comparison (Python vs DataWeave)
- Hammer home: "you describe WHAT, not HOW"

### 3. Where MuleSoft Fits: Anypoint Platform (5 min)

- Figure 4 — the 5-step lifecycle: Design Center -> Exchange -> ACB -> Runtime Manager -> API Manager
- Quick taste of each component (Code Snippet 4a-d):
  - RAML spec (Module 3)
  - Mule XML flow (Module 4)
  - DataWeave transform (Module 5)
  - CloudHub deploy (Module 7)
- **Demo: run the pre-built Mule flow** (lab/solution project)
  - This is the "after" — show the same customer data but through a proper Mule flow
  - Side-by-side comparison: Python script vs Mule flow doing the same thing

### 4. The 3-Day Journey (5 min)

- Figure 5 — complete Customer 360 architecture, every module contributes
- Walk through what they'll build each day:
  - Day 1: Design (API spec) + Platform orientation
  - Day 2: Build (flows, connectors, DataWeave) — the bulk
  - Day 3: Connect (Salesforce ETL) + Deploy + Governance
- "By Friday you'll have a working Customer 360 API deployed to CloudHub"

### 5. Lab: Compare Both Approaches (20 min)

- Part 1 (5 min): students run the coupled Python script themselves
- Part 2 (10 min): students open the Mule project, explore it, run it
- Part 3 (5 min): reflection worksheet — what's different? what's better?
- Walk around, make sure mock API is running for everyone
- Common issues: port 5173 already in use, Python not found — check .venv

## Key Talking Points

- "Integration is 60% of enterprise IT spend" — this is why MuleSoft exists
- The spaghetti problem is real — every Salesforce team has lived it
- API-led is not just architecture, it's reuse strategy
- MuleSoft is declarative: XML config, not imperative code
- DataWeave is the secret weapon — you'll spend a full day on it (Module 5)

## Potential Questions

- "Why not just use Python/Node?" — you can, but you maintain everything yourself (auth, retry, monitoring, governance)
- "Is MuleSoft only for Salesforce?" — no, 400+ connectors, but SF teams are the sweet spot
- "What about iPaaS competitors?" — acknowledge them, MuleSoft's differentiator is the full lifecycle (design to governance)
