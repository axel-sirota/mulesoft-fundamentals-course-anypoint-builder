---
description: Design architecture and skeleton for a module or infrastructure component
---

# Architect Command

Initiates architecture design before implementation. Design first, build second.

## Execution Flow

**1. Context Loading**
- Read `prompts/mulesoft-course-blueprint.md` for overall course architecture.
- Read the specific module prompt if applicable.
- Read `.claude/rules/` for conventions.

**2. Design Phase**
- Define the file structure and dependencies.
- If infrastructure: design docker-compose services, ports, data schemas.
- If module: design HTML notebook sections, lab flow, fixture data.
- If Mule project: design flow structure, connectors, properties.

**3. Skeleton Implementation**
- Scaffold the directory structure.
- Create placeholder files with TODOs.
- Verify the skeleton is valid (directories exist, file structure matches blueprint).

**4. Planning**
- Break down implementation into sessions.
- Write plan to `plans/` directory.
- Present for approval.

## Usage
`/architect infrastructure` -> Designs EC2 docker-compose services
`/architect module-04` -> Designs Module 4 notebook + 9 cycle labs
