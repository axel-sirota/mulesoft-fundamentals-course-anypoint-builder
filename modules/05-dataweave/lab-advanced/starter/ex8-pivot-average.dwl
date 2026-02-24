// Exercise 8: Dynamic Keys + Reduce (Survey Pivot)
// Input: 30 survey responses — 6 questions x 5 respondents (ex8-input.json)
// Task: Pivot to {questionId: averageScore}
// Expected output: {"q1": 4.2, "q2": 3.8, ...} (see ex8-expected.json)
// GOTCHA: Dynamic keys need (parentheses) — without them you get literal string "questionId"
%dw 2.0
output application/json

import avg from dw::core::Arrays
---
// TODO 1: Group the payload by questionId
// Hint: payload groupBy $.questionId

// TODO 2: Use mapObject to transform each group into a key-value pair
// Hint: ... mapObject ((responses, questionId) -> { ... })

// TODO 3: Use dynamic key with parentheses and avg function:
//   (questionId): avg(responses map $.score)
// IMPORTANT: The parentheses around questionId make it a dynamic key!
// Without (): { questionId: ... } → literal key "questionId"
// With ():    { (questionId): ... } → uses the variable value as key

{}
