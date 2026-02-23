---
description: Build a specific course module following the blueprint
---

# Build Module Command

Builds a complete module following the course blueprint and prompt specifications.

## Inputs
- **Module number**: Which module to build (1-7)

## Execution Flow

**1. Load Context**
- Read `prompts/mulesoft-course-blueprint.md` for overall structure.
- Read `prompts/prompt-module-{NN}.md` for the specific module prompt.
- Read `.claude/rules/` for HTML template, lab generation, and MuleSoft conventions.

**2. Research Phase (MANDATORY)**
- Run 4-5 web searches to validate MuleSoft patterns, RAML syntax, DataWeave patterns, or connector configs relevant to this module.
- Document validated findings in `plans/module-{NN}-plan.md`.

**3. Create Plan**
- Write detailed plan to `plans/module-{NN}-plan.md`.
- List every file to be created with its purpose.
- Present plan for approval before building.

**4. Build**
- Create files one by one following the prompt spec exactly.
- HTML notebooks: use template from `.claude/rules/html-template.md`.
- Lab starters: include TODOs with hints.
- Lab solutions: complete working implementations.
- Fixtures: realistic, consistent data using Customer 360 domain.

**5. Generate Student Version**
- Run `shared/scripts/generate-student-html.py` on the instructor HTML to produce `module-{NN}-student.html`.
- Verify the student version has **zero** `instructor-note` occurrences.
- Verify all diagrams, code blocks, and lab sections are preserved in the student version.

```bash
.venv/bin/python3 shared/scripts/generate-student-html.py modules/{module-dir}/module-{NN}.html
```

**6. Validate**
- Run through the validation checklist from the module prompt.
- Verify all diagrams, code snippets, and links are correct.
- For Python files: verify they run.
- For HTML files: verify structure is complete.
- Verify both instructor and student HTML files exist and render correctly.

## Usage
`/build-module 1` -> Builds Module 1 (Why MuleSoft?)
