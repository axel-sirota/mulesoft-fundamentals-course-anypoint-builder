# Module 2 — Anypoint Platform Tour (60 min)

## Flow

### 1. Platform Architecture (15 min)

- Figure 1 — three groups: Design & Build, Deploy & Run, Secure & Govern
  - Stress that Exchange is the glue — everything publishes to or consumes from it
- Figure 2 — runtime request flow
  - Trace a request: Client -> Gateway -> Mule Runtime -> Your Flow -> External Systems -> back
  - Blue = platform handles it, Orange = you build it, Gray = external
  - "You only write the orange parts"
- Figure 3 — API lifecycle mapped to course days
  - Day 1 = steps 1-2 (design, publish)
  - Day 2 = steps 3-6 (build, test)
  - Day 3 = steps 7-8 (deploy, govern)
- Figure 4 — MCP Server (mention briefly)
  - AI-assisted development from IDE, 40+ tools
  - "We won't use it in labs but it's where MuleSoft is heading"
- Code Snippets — show what each component produces:
  - Design Center -> RAML spec
  - ACB -> Mule XML flow
  - Runtime Manager -> deploy config
  - API Manager -> policy config

### 2. Component Deep Dive (10 min)

- Figure 5 — Web UI navigation (hamburger menu)
- Walk through each component verbally:
  - **Design Center**: API Designer (browser-based RAML editor), API Designer has been superseded by ACB for most teams
  - **Exchange**: the asset catalog — connectors, templates, APIs, everything is an asset
  - **Runtime Manager**: where you monitor deployed apps, view logs, alerts
  - **API Manager**: policies (rate limiting, auth), SLA tiers, analytics
  - **Visualizer**: dependency graph of your API network — "the wow factor for managers"
- **ACB Deep Dive** (this is where they'll live):
  - Figure 6 — VS Code layout: Activity Bar -> MuleSoft Panel -> Canvas/XML Editor -> Bottom panels
  - Figure 7 — Canvas workflow: add component, configure, test, repeat
  - Figure 8 — Command Palette commands (Ctrl+Shift+P): know the key ones
  - Figure 9 — Web UI vs ACB mapping: "almost everything has an ACB equivalent"
  - Key message: "you CAN stay in your IDE for 90% of the workflow"

### 3. Demo: Platform Walkthrough (15 min)

- Open anypoint.mulesoft.com in browser
- Walk through in this order:
  1. Landing page -> hamburger menu -> show all sections
  2. Design Center -> show API Designer (we'll use ACB instead)
  3. Exchange -> search for "Salesforce Connector" -> show asset detail page
  4. Runtime Manager -> show an environment (even if empty)
  5. API Manager -> show where policies would go
  6. (Optional) Visualizer -> show the network graph view
- Then open VS Code with ACB:
  1. Show MuleSoft icon in Activity Bar
  2. Show Quick Actions panel
  3. Show Command Palette MuleSoft commands
  4. Show Canvas vs XML toggle
- "This is your kitchen — now you know where everything is"

### 4. Lab: Platform Scavenger Hunt (15-20 min)

- 6 tasks exploring the platform
- Students log into anypoint.mulesoft.com with their trial org
- They find specific things: Exchange assets, Runtime Manager environments, etc.
- Plus an environment readiness checklist (ACB installed, Java, Maven)
- Walk around — common issues:
  - Trial org expired
  - ACB extension not showing up (needs VS Code reload)
  - Maven not on PATH

## Key Talking Points

- "Know your kitchen before you cook" — this module is orientation
- Exchange is the heart of reuse — if it's not in Exchange, it doesn't exist
- ACB is VS Code — not a custom IDE, just extensions on top of VS Code
- Canvas view is training wheels — real devs toggle to XML, but canvas helps learn
- The platform is opinionated — that's a feature, not a bug

## Potential Questions

- "Do I need the web UI at all?" — yes for some things (Visualizer, analytics, org admin), but day-to-day is ACB
- "Is ACB free?" — comes with Anypoint license, the VS Code extension itself is free to install
- "Can I use IntelliJ instead?" — no, ACB is VS Code only (mention MuleSoft used to have Anypoint Studio on Eclipse, now deprecated)
