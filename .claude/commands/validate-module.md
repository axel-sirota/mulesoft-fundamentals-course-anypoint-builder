---
description: Run validation checklist for a completed module
---

# Validate Module Command

Runs the validation checklist from the module prompt to verify completeness and correctness.

## Inputs
- **Module number**: Which module to validate (1-7)

## Execution Flow

**1. Load Validation Checklist**
- Read `prompts/prompt-module-{NN}.md` and extract the VALIDATION section.

**2. File Existence Check**
- Verify all expected files exist (HTML notebook, starter, solution, fixtures).

**3. Content Validation**
- HTML: check for mermaid diagram blocks, Prism.js code blocks, collapsible details tags.
- Code: verify Python scripts have no syntax errors (`python -m py_compile`).
- Fixtures: verify JSON is valid (`python -m json.tool`), CSV has expected row counts.
- RAML: verify YAML structure is valid.

**4. Data Consistency**
- Customer IDs consistent (ACCT-001 through ACCT-010).
- Cross-reference fixture inputs with expected outputs.

**5. Infrastructure (if applicable)**
- Docker Compose: validate YAML syntax.
- Services: check port configurations match module docs.

**6. Dual HTML Versions**
- Verify both `module-{NN}.html` (instructor) and `module-{NN}-student.html` (student) exist.
- Verify instructor version has `<details class="instructor-note">` blocks.
- Verify student version has **zero** occurrences of `instructor-note`.
- Verify student version retains all diagrams, code blocks, lab steps, and navigation.
- If student version is missing or stale, regenerate:
  ```bash
  .venv/bin/python3 shared/scripts/generate-student-html.py modules/{module-dir}/module-{NN}.html
  ```

**7. Report**
Output a pass/fail report for each checklist item.
