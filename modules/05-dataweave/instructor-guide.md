# Module 5 — DataWeave: The Language of Integration — Instructor Guide

**Duration:** ~4 hours (1h theory/demo + 1.5h basics lab + 1h advanced lab + 30 min Mule flow lab)
**Format:** Theory → 5 Playground demos → Lab 1 (5 exercises) → Lab 2 (4 exercises) → Lab 3 (1 exercise)
**Day:** Day 3 morning
**Prerequisites:** Module 4 complete (students have built the cycle-9 enrichment engine)

---

## Pre-Class Setup

### Environment
- DataWeave Playground must be accessible: https://dataweave.mulesoft.com/
- Verify it loads (no corporate firewall blocking it)
- ACB (VS Code) installed — needed for Exercises 6, 9, and 10
- Module 4 cycle-9 project available (students need it for Exercise 10)

### Materials Ready
- `fixtures/` directory with all 20 input/output files
- `lab-basics/starter/` with 5 DW skeletons
- `lab-advanced/starter/` with 4 DW skeletons
- `lab-modular/starter/` with the cycle-9 project + TODO
- Solutions in each `solution/` directory

### Fallback
- All solutions are pre-validated — share after each exercise for comparison
- If Playground is down, ACB's DW Preview works as alternative (but slower)
- Exercise 10 does NOT require running infrastructure

---

## Bridge from Module 4 (3 min)

### What to Cover
- Ask: "Who found themselves Googling DataWeave syntax during Module 4?"
- Explain the three-stage progression: Playground → ACB → Mule Flow
- Have everyone open the Playground
- Quick orientation: Input (left), Script (center), Output (right)

### Key Message
- "Yesterday you used DataWeave as a tool inside flows. Today you master it as a language."
- Module 4 had 6 inline DW blocks — all simple field mapping. No `map`, no `filter`, no null handling. That changes now.

---

## Section 1: DataWeave Fundamentals (20 min)

### What to Cover
- Script structure: `%dw 2.0` header, `output` directive, `---` separator, body expression
- Accessing the Mule Event: `payload`, `attributes.queryParams`, `attributes.uriParams`, `vars`
- Selectors: single value (`.name`), multi-value (`.*name`), descendant (`..email`), filter (`[?($.industry == "Technology")]`)

### Talking Points
- "Every Transform Message, every set-variable expression, every Choice condition — that's DataWeave"
- "The header declares what you're producing. The body declares the shape. That's it."
- Tie back to Module 4: `#[attributes.uriParams.customerId]` was DataWeave, they just didn't realize it

### Demo
- Open Playground, paste a customer JSON array
- Show each selector type live: `.firstName`, `.*name`, `[?($.industry == "Technology")]`
- Show how changing `output application/json` to `output application/csv` reformats everything

---

## Section 2: Core Functions (20 min)

### What to Cover
- **map**: transform each element → show input/output with Customer 360 data
- **filter**: keep matching elements → chain with map
- **reduce**: aggregate to single value → named parameters `(item, acc = 0)`
- **groupBy**: returns an Object (not Array!) → key gotcha
- **distinctBy**: remove duplicates by field
- **flatten** / **flatMap**: nested arrays → flat
- **mapObject** / **pluck**: object ↔ array transforms

### Key Gotchas to Emphasize
1. **reduce parameter order**: `(item, accumulator)` — accumulator is SECOND, with default value
2. **groupBy returns Object**: students try to `map` over it — they need `pluck` to get back to array
3. **flatMap vs flatten+map**: `flatMap` is the idiomatic pattern for nested iteration

### Talking Points
- "These 8 functions handle 90% of all DataWeave transforms you'll ever write"
- "If you're writing a for loop in your head, use `map`. If you're writing an if statement, use `filter`."
- Show the chaining pattern: `payload filter (...) map (...) distinctBy (...)`

---

## Section 3: Format Conversions & Null Handling (10 min)

### What to Cover
- Format switching: change `output application/json` to `csv`, `xml`, etc.
- **CSV gotcha**: ALL CSV values are strings — must use `as Number` for arithmetic
- Null handling: `default` operator, chaining defaults, `skipNullOn="everywhere"`
- Pattern matching: `match { case ... if ... -> ... }`

### Key Gotcha
- The CSV string issue trips up 80% of students. Demo it live:
  - Input CSV with numbers → `reduce` sum → "Error: Cannot coerce String to Number"
  - Fix: `item.amount as Number`

### Talking Points
- "DataWeave is format-agnostic. Same transform logic, different output directive."
- "Always add `skipNullOn='everywhere'` unless you specifically want null keys in your output"

---

## Section 4: Reusable Modules (10 min)

### What to Cover
- Module file structure: `%dw 2.0` + `fun` declarations. **NO output, NO ---, NO body.**
- Three functions in `customer-utils.dwl`: `normalizePhone`, `classifySegment`, `mergeCustomer`
- Import syntax: `import normalizePhone from modules::customer-utils`
- `mergeWith` from `dw::core::Objects` — second argument wins on conflicts

### Critical Rule
- **Module file = declarations only.** If a student adds `output` or `---`, it won't work as an importable module. Hammer this distinction — it comes back in Exercises 6, 9, and 10.

---

## Section 5: Demo — DW Playground Live (15 min)

Five quick demos, 3 minutes each. All use fixture data from `fixtures/`.

### Demo 1: Filter + Map Chain
- Input: `ex1-input.json` (10 customers)
- Script: `payload filter ($.industry == "Technology") map { fullName: $.firstName ++ " " ++ $.lastName, email: $.email }`
- Result: 4 Technology customers

### Demo 2: flatMap for Nested Data
- Input: `ex2-input.json` (orders with lineItems)
- Common mistake: `payload map ((order) -> order.lineItems map (...))` → nested arrays
- Fix: `payload flatMap ((order) -> order.lineItems map (...))` → flat result

### Demo 3: groupBy + pluck Gotcha
- Input: customers array
- Show: `payload groupBy $.industry` → Object, not Array
- Fix: `... pluck ((items, key) -> { industry: key as String, count: sizeOf(items) })`

### Demo 4: CSV String Gotcha
- Input: `ex3-input.csv`
- Show: `reduce ((item, acc = 0) -> acc + item.amount)` → error
- Fix: `item.amount as Number`

### Demo 5: Null Safety
- Input: `ex4-input.json` (records with nulls)
- Show: without defaults → null values in output
- Fix: `$.email default "unknown@example.com"` + `skipNullOn="everywhere"`

---

## Lab 1: DataWeave Basics (90 min)

### Exercise Timing
| Exercise | Time | Difficulty | Key Concept |
|----------|------|-----------|-------------|
| 1: Filter & Map | 15 min | Easy | Core chaining pattern |
| 2: Flatten to CSV | 18 min | Medium | flatMap + format conversion |
| 3: Group & Aggregate | 18 min | Hard | groupBy + pluck + CSV strings |
| 4: Null Handling | 15 min | Medium | default + skipNullOn |
| 5: XML to JSON | 18 min | Hard | XML selectors, `.*`, `.@attr` |

### Pacing Strategy
- Walk the room during Exercises 3 and 5 — those are the hardest
- Exercise 3: watch for the CSV string gotcha (demo'd in Section 5)
- Exercise 5: make sure students switch Playground input type to XML
- If students finish early, suggest chaining `orderBy` to sort results
- Share solutions from `lab-basics/solution/` after each exercise

### Common Student Issues
- Exercise 2: Using `map` instead of `flatMap` → nested arrays
- Exercise 3: Forgetting `as Number` on CSV amount values
- Exercise 5: Using `.category` instead of `.*category` (single vs multi-value selector)

---

## Lab 2: DataWeave Advanced (60 min)

### Exercise Timing
| Exercise | Time | Difficulty | Key Concept |
|----------|------|-----------|-------------|
| 6: Reusable Module | 15 min | Medium | fun declarations, do { } scope |
| 7: Recursive Flatten | 15 min | Hard (Challenge) | Recursive function + flatMap |
| 8: Dynamic Keys + Average | 10 min | Medium | `(key)` syntax, avg from dw::core::Arrays |
| 9: Merge Capstone | 20 min | Medium | readUrl, classpath, multi-source merge |

### Pacing Strategy
- Exercise 6: Most students need help with `do { var ... --- body }` for normalizePhone
- Exercise 7: **Hardest exercise in the module.** Walk the room actively. If stuck after 10 min, show the function signature: `fun flattenOrg(nodes, parentId = null) = nodes flatMap ((node) -> ...)`
- Exercise 8: Quick once they understand dynamic keys with parentheses: `{ (key): value }`
- Exercise 9: Encourage the ACB approach if time permits — `readUrl("classpath://...")` mirrors real Mule flows

### The Recursive Flatten Warning
- Exercise 7 is marked CHALLENGE for a reason
- The recursive pattern is `flatMap` + conditional `if (node.reports?) flattenOrg(node.reports, node.id) else []`
- If a student is truly stuck, let them skip to Exercise 8 and come back

---

## Lab 3: DW in a Mule Flow (30 min)

### What to Cover
- The `resource` attribute: `<ee:set-payload resource="dwl/enrich-merge.dwl" />`
- External DW file vs inline CDATA — when to use which
- Module file (`customer-utils.dwl`) vs transform script (`enrich-merge.dwl`) — the NO output/NO --- rule
- Null handling applied to real integration data

### Exercise 10: Refactor the Scatter-Gather Merge

| Step | Time | What Students Do |
|------|------|-----------------|
| 1: Open project | 2 min | Find the TODO in implementation.xml |
| 2: Add customer-utils.dwl | 3 min | Copy Ex6 solution into `dwl/modules/` |
| 3: Create enrich-merge.dwl | 10 min | Write external DW with imports + null handling |
| 4: Wire resource attribute | 5 min | Replace inline CDATA with `resource="dwl/..."` |
| 5: Compare before/after | 10 min | Walk through the improvement table |

### Key Talking Points
- "Inline CDATA is fine for 3-line transforms. For anything bigger, extract to a .dwl file."
- "The resource path is relative to `src/main/resources/` — not the project root"
- "Module imports use `::` notation: `import ... from modules::customer-utils`"
- "This is exactly how production Mule apps are structured — reusable DW modules shared across flows"

### Common Mistakes
- Wrong resource path: `src/main/resources/dwl/enrich-merge.dwl` instead of `dwl/enrich-merge.dwl`
- Adding `output` directive to the module file (customer-utils.dwl is a module — no output!)
- Forgetting `skipNullOn="everywhere"` in the external script

### This Does NOT Require Infrastructure
- The refactoring is structural — files exist, XML compiles, DW syntax is valid
- If infra is running and time allows, students can test it live

---

## Wrap-Up & Bridge to Module 6 (5 min)

### Recap
Walk through what was covered:
1. Selectors and script structure
2. Core functions: map, filter, reduce, groupBy, mapObject, pluck
3. Format conversion (JSON ↔ CSV ↔ XML)
4. Null handling (default, skipNullOn)
5. Reusable modules (fun declarations, import syntax)
6. Advanced patterns (recursion, dynamic keys, reduce with accumulators)
7. External DW files in Mule projects (resource attribute)

### Three-Stage Completion
- "You started in the Playground with zero setup. You moved to ACB for project context. You ended in a real Mule project. That's the full journey."

### Bridge to Module 6
- "In Module 6 you'll use these DataWeave skills to build a Salesforce batch ETL pipeline"
- "The `customer-utils.dwl` module you created will be reused to normalize and classify customer data during the ETL"
- "DataWeave powers every transform in the batch — from Salesforce query results to upsert payloads"

---

## Key Talking Points (For the Whole Module)

- "DataWeave is functional — no loops, no mutable state. Describe the shape you want."
- "If you're thinking 'for loop', use `map`. If you're thinking 'if statement', use `filter`."
- "The Playground is your best friend — use it anytime, even after this course"
- "Modules are the key to DRY DataWeave — one function definition, import everywhere"
- "Every CSV value is a string. Every. Single. One. Always coerce with `as Number`."
- "groupBy returns an Object, not an Array. Use pluck to get back to an array."

## Potential Questions

- "Can I use DataWeave outside MuleSoft?" — The online Playground works standalone. DataWeave CLI exists but requires MuleSoft tooling.
- "How does DW compare to XSLT?" — Both are declarative transformation languages. DW handles JSON/CSV/XML natively; XSLT is XML-only. DW is far more concise.
- "Why not just use JavaScript/Python for transforms?" — DW is built into the Mule runtime, executes in the same JVM, handles format conversion natively, and integrates with flow variables. External scripts require additional connectors and serialization overhead.
- "When should I use inline DW vs external .dwl files?" — Rule of thumb: under 5 lines, keep inline. Over 5 lines or reused across flows, extract to .dwl.
- "What if my recursive function causes a stack overflow?" — DataWeave doesn't optimize tail recursion. For very deep trees (100+ levels), consider iterative approaches or pre-processing. In practice, business data rarely nests beyond 5-10 levels.
