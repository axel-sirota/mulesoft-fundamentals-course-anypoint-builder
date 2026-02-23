---
description: Generate a research export document for external review
---

# Research Export Command

Generate a structured Markdown document to explain a complex problem to an external expert or colleague.

## Execution Flow

**1. Gather Context**
- Read current module/component being worked on.
- Read the error logs or problem description provided by the user.

**2. Generate Document**
Create a file `plans/research-[topic]-[date].md` with:

```markdown
# Research Export: [Topic]

## 1. Problem Statement
- **Goal**: What are we trying to do?
- **Blocker**: What is stopping us?
- **Module/Component**: Which part of the course?

## 2. Attempted Solutions
- Approach A: [Result]
- Approach B: [Result]

## 3. Relevant Code
[Insert snippet or file reference]

## 4. Specific Questions
- [Question 1]
- [Question 2]

## 5. Sources Consulted
- [URLs]
```
