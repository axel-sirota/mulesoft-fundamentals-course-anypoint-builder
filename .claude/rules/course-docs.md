# Course Documentation Standards

Rules for writing course content — HTML notebooks, lab instructions, and supporting docs.

---

## Pedagogical Pattern (Non-Negotiable)

Every module follows this cycle, repeated per concept:

```
THEORY (mermaid diagrams + code snippets showing the concept)
  → DEMO (instructor shows it working live — collapsible instructions)
    → LAB (students build it — starter + solution provided)
      → iterate for next concept
```

No module is "just theory." No module is "just a walkthrough." Every single module has all three. The demos bridge "I understand the concept" and "I can build it myself."

---

## Writing Style

### Prose
- Write in prose paragraphs, not bullet lists, for conceptual explanations
- Bullet lists only for: steps, checklists, comparisons
- Conversational instructor tone — not academic, not chatbot-casual
- Address students as "you" — "You'll build a Mule flow that..."
- Present tense for concepts: "DataWeave handles format conversion natively."
- Active voice always: "The router validates the request" not "The request is validated"

### Technical Accuracy
- Every code snippet must be syntactically correct and copy-pasteable
- XML snippets must be valid XML (proper escaping of `<`, `>`, `&` in HTML)
- RAML snippets must be valid RAML 1.0
- DataWeave snippets must be valid DW 2.0 syntax
- SOQL must be valid Salesforce query syntax
- URLs must be realistic but use placeholders for host: `EC2_HOST`, `YOUR_APP_NAME`

### Code Snippet Rules
- Every snippet is annotated — comments explaining what each part does
- Snippets build progressively (Snippet 3 adds to Snippet 2)
- Show input → transform → output when demonstrating DataWeave
- Maximum ~30 lines per snippet. Break longer code into multiple snippets.
- Always include the `%dw 2.0` header and `output` directive for DataWeave
- For Mule XML, show relevant fragment only — not the entire file unless necessary

---

## Diagram Standards (Mermaid)

### When to Use Which Diagram Type
| Type | Use Case |
|------|----------|
| `graph TD` (top-down) | Architecture layers, component relationships |
| `graph LR` (left-right) | Process flows, data pipelines |
| `sequenceDiagram` | API call sequences, auth flows, request/response |
| `flowchart` | Decision trees, Choice router logic |
| `classDiagram` | Data models (RAML types) |

### Style Rules
- Every diagram has a caption below it
- Use color styling for layers: green (Experience), blue (Process), orange (System)
- Label every arrow — no unlabeled connections
- Keep diagrams under 15 nodes — split into multiple if larger
- Use subgraphs to group related nodes

### Minimum Diagrams Per Module
- Module 1: 5 (spaghetti, +1 system, 3-layer, platform map, course roadmap)
- Module 2: 3 (platform architecture, API lifecycle, MCP server)
- Module 3: 3 (system API position, RAML vs OAS, API gateway)
- Module 4: 9 (one per cycle minimum)
- Module 5: 2 (DW in flow, shared module)
- Module 6: 5 (SF operations, OAuth, batch lifecycle, external ID, two-phase migration)
- Module 7: 5 (deployment options, code-to-CloudHub, API gateway, MAC architecture, MAC in ETL)

---

## Demo Instructions

### Format
Always inside a collapsible `<details class="instructor-note">`:

```html
<details class="instructor-note">
  <summary>Instructor Demo: {Title} ({duration})</summary>
  <ol>
    <li>Step with exact command or click path</li>
    <li>Step with expected visible result</li>
    <li>Talking point: "Ask the room: ..."</li>
  </ol>
</details>
```

### Rules
- Numbered steps, not bullets
- Include exact commands (`curl`, `mvn`, terminal commands)
- Include expected output or visual result for each step
- Include talking points and audience questions
- Include recovery steps if something fails
- Duration estimate in the summary

---

## Lab Instructions

### Format in HTML Notebook
Each lab step is a card with:
1. Step number (large, prominent)
2. Title (what you're doing)
3. Instructions (concise — what to do, not how the world works)
4. Code to type/paste (in a code block with copy button)
5. Validation checkpoint (green box): "Expected: {specific observable result}"

### Validation Checkpoints
- Must be **observable** — something the student can see/verify
- Not vague: "It works" ← BAD
- Specific: "GET /api/customers returns JSON array of 4 Technology customers" ← GOOD
- Include: expected HTTP status, expected payload shape, expected log message
- One validation per step, not batched at the end

### Lab Difficulty Progression
- Steps 1-3: Follow along (copy-paste with minor changes)
- Steps 4-6: Apply pattern (same pattern, different resource)
- Steps 7+: Extend (combine patterns, less hand-holding)
- Bonus/Optional: Challenge (minimal hints, references to docs)

---

## Customer 360 Domain Data

### Consistent Data Across All Modules

The same 10 customers appear everywhere:

| ID | First | Last | Company | Industry |
|----|-------|------|---------|----------|
| ACCT-001 | Leanne | Graham | Romaguera-Crona | Technology |
| ACCT-002 | Ervin | Howell | Deckow-Crist | Technology |
| ACCT-003 | Clementine | Bauch | Keebler LLC | Healthcare |
| ACCT-004 | Patricia | Lebsack | Robel-Corkery | Technology |
| ACCT-005 | Chelsey | Dietrich | Considine-Lockman | Financial Services |
| ACCT-006 | Dennis | Schulist | Kulas Light Inc | Manufacturing |
| ACCT-007 | Kurtis | Weissnat | Hoeger LLC | Technology |
| ACCT-008 | Nicholas | Runolfsdottir | Stanton Group | Healthcare |
| ACCT-009 | Glenna | Reichert | Yost Partners | Retail |
| ACCT-010 | Clementina | DuBuque | McLaughlin & Sons | Financial Services |

These 10 records are used in:
- `shared/mock-api/server.py` (Module 1)
- RAML examples (Module 3)
- REST enrichment API responses (Module 4 infrastructure)
- PostgreSQL seed data (Module 4 infrastructure)
- DataWeave fixture files (Module 5)

Module 6 uses an expanded set of 50 accounts (including these 10) for batch ETL.

---

## File Naming

### Modules
```
modules/01-intro-to-mulesoft/
modules/02-anypoint-platform-tour/
modules/03-api-design/
modules/04-integrations-rest-soap-db/
modules/05-dataweave/
modules/06-salesforce-etl-batch/
modules/07-deploy-manage-llm/
```

### HTML Notebooks
`module-{NN}.html` inside each module directory.

### Labs
```
lab/starter/    — starting point for students
lab/solution/   — complete working implementation
```

For modules with multiple labs:
```
lab-basics/starter/
lab-basics/solution/
lab-advanced/starter/
lab-advanced/solution/
lab-modular/starter/    (optional/bonus)
lab-modular/solution/
```

---

## Navigation

Every notebook has a footer with:
```html
<footer class="module-footer">
  <a href="../{prev-module}/module-{NN}.html">← Module {N-1}: {Title}</a>
  <a href="../{next-module}/module-{NN}.html">Next: Module {N+1} — {Title} →</a>
</footer>
```

Module 1 has no "previous" link. Module 7 ends with "Course Complete."
