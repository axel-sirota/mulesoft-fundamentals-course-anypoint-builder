// Exercise 7: Recursive Flatten (Org Hierarchy) — CHALLENGE
// Input: Nested org tree with reports arrays (ex7-input.json)
// Task: Flatten to array of {id, name, title, parentId}
// Expected output: 10 flat records (see ex7-expected.json)
// WARNING: Recursion in DataWeave is tricky. Take it step by step.
%dw 2.0
output application/json

// TODO 1: Define a recursive function flattenOrg(nodes, parentId = null)
// The function should:
//   a) Use flatMap to iterate over each node in nodes
//   b) For each node, emit an object with: id, name, title, parentId
//   c) If node has reports (check with node.reports?), recursively call
//      flattenOrg(node.reports, node.id) and concatenate with ++
//   d) If no reports, concatenate with empty array []
//
// Skeleton:
// fun flattenOrg(nodes, parentId = null) =
//   nodes flatMap ((node) ->
//     [{ id: ..., name: ..., title: ..., parentId: ... }] ++ (
//       if (node.reports?)
//         flattenOrg(???, ???)
//       else
//         []
//     )
//   )
---
// TODO 2: Call flattenOrg with the top-level org array
// Hint: flattenOrg(payload.org)

[]
