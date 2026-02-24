// Solution: Exercise 8 — Dynamic Keys + Reduce (Survey Pivot)
// Pivot survey responses to {questionId: averageScore}
// GOTCHA: Dynamic keys need (parentheses) — without them you get literal "questionId"
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json

import avg from dw::core::Arrays
---
payload groupBy $.questionId
  mapObject ((responses, questionId) -> {
    (questionId): avg(responses map $.score)
  })
