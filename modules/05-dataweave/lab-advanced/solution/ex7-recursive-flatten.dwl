// Solution: Exercise 7 — Recursive Flatten (Org Hierarchy)
// CHALLENGE: Recursively flatten a tree into a flat array with parentId references
// Hand-verified against expected output — recursive DW is error-prone
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json

fun flattenOrg(nodes, parentId = null) =
  nodes flatMap ((node) ->
    [{
      id: node.id,
      name: node.name,
      title: node.title,
      parentId: parentId
    }] ++ (
      if (node.reports?)
        flattenOrg(node.reports, node.id)
      else
        []
    )
  )
---
flattenOrg(payload.org)
