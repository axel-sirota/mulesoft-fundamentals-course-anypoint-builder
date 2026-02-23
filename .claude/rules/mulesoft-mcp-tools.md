# MuleSoft MCP Tools — Status & Usage Guide

Tested 2026-02-23. Auth is working (connected app + scopes). AI generation tools require **Agentforce** entitlement which needs a non-trial Salesforce org — **not available for this project**. This is permanent; do not retry these tools.

---

## Working Tools

| Tool | What It Does | Key Params |
|------|-------------|------------|
| `search_asset` | Find connectors/templates on Exchange | `searchQuery` |
| `list_api_instances` | List API instances in an environment | `page` (required) |
| `list_applications` | List deployed apps | `environmentName` (required) |
| `get_platform_insights` | Usage trends, call volume, latency | Set at least one `include*` flag to `true` |
| `get_reuse_metrics` | Asset reuse across org | `includeReuseMetrics: true` |
| `create_mule_project` | Scaffold a Mule 4 project (pom, XML, dirs) | `projectName`, `projectPath` |
| `create_api_spec_project` | Scaffold RAML or OAS project | `projectName`, `projectPath`, `language` |
| `create_mcp_server` | Returns prompt for building MCP server flows | `projectPath`, `projectXmlPath`, `originalPrompt` |
| `manage_flex_gateway_policy_project` | Returns CLI instructions for PDK | (none) |
| `get_flex_gateway_policy_example` | Returns Rust source examples | `feature` (e.g. `header_manipulation`) |

## Broken Tools (Require Agentforce)

These call the **MuleDX AI API** backend which requires Agentforce to be enabled in Access Management.

| Tool | Error | Workaround |
|------|-------|------------|
| `generate_api_spec` | "Failed calling MuleDX AI API to generate API Design Spec" | Write RAML/OAS specs manually — we know the conventions |
| `generate_mule_flow` | Returns `status: failed_to_generate_use_prompt_to_llm` | Use the `prompt_to_llm` field as a guide, then write Mule XML manually |

### Why They Fail

Both tools call the MuleDX AI API which requires Agentforce. Agentforce requires a non-trial Salesforce org with admin setup. Our org is a trial — **never attempt these tools, always write specs and flows manually**.

## Tools Requiring Pre-existing Resources

| Tool | Prerequisite |
|------|-------------|
| `create_and_manage_api_instances` | Asset must exist in Exchange first (`assetId` must resolve) |
| `manage_api_instance_policy` | API instance must exist (`apiInstanceId`) |
| `create_and_manage_assets` | Requires `groupId` from org + proper `classifier` + supporting files |
| `update_mule_application` | App must be deployed (`applicationId`, `environmentId`) |
| `deploy_mule_application` | Needs a built project or Exchange asset |
| `run_local_mule_application` | Needs Maven + Mule runtime installed locally |

---

## Workflow for This Course

Since `generate_api_spec` and `generate_mule_flow` are unavailable:

1. **Scaffolding** → Use `create_mule_project` and `create_api_spec_project` (both work)
2. **RAML specs (Module 3)** → Write manually following conventions in `mulesoft-conventions.md`
3. **Mule XML flows (Module 4)** → Write manually; `generate_mule_flow`'s `prompt_to_llm` output provides useful structure hints
4. **Asset search** → Use `search_asset` to find correct connector GAV coordinates for pom.xml
5. **Deployment (Module 7)** → Use `deploy_mule_application` (untested but should work with a built project)
