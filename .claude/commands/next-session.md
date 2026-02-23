---
description: Generate a transition prompt for the next coding session
---

# Next Session Command

Wraps up the current work and generates a "Context Beacon" for the next session.

## Execution Flow

**1. Analyze Session**
- What files were created or changed?
- What modules are complete?
- What is pending or broken?

**2. Update Status**
- Check which modules have: HTML notebook, lab/starter, lab/solution, fixtures, infrastructure.
- Note any validation failures.

**3. Generate Transition Prompt**
Output a code block the user can use next time:

```markdown
# Session Transition
**Last Status**: [Success/Fail]
**Modules Complete**: [List]
**Stopped At**: [Module/File being worked on]
**Next Step**: [Immediate action for next session]
**Blockers**: [Any issues discovered]
```
