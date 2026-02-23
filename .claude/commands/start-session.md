---
description: Begin a development session with active context
---

# Start Session Command

Initializes the AI context for the current work session.

## Execution Flow

**1. Context Check**
- Read `CLAUDE.md` and `.claude/rules/` to understand project conventions.
- Read `prompts/mulesoft-course-blueprint.md` to understand overall course structure.
- Check which modules exist under `modules/` and `infrastructure/`.

**2. Progress Summary**
- Display what has been built so far (which modules, which files exist).
- Identify what is missing or incomplete.

**3. Session Goal**
- Ask: "What is the goal for this session?"
- Cross-reference with the blueprint to confirm alignment.

**4. Rule Enforcement**
- Load active rules from `.claude/rules/` (html-template, lab-generation, mulesoft-conventions, course-docs).
- Remind: all plans go in `plans/` folder before execution.

**5. Ready State**
- Confirm readiness: "Context loaded. Ready to build."
