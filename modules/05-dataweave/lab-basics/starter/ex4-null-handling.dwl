// Exercise 4: Null Handling (JSON to JSON)
// Input: 8 customers with null/missing fields (ex4-input.json)
// Task: Apply defaults for missing data, output clean JSON
// Expected output: All records with all fields populated (see ex4-expected.json)
// NOTE: "default" triggers on null AND missing fields, but NOT on "", 0, false, []
%dw 2.0
output application/json skipNullOn="everywhere"
---
// TODO 1: Map over each customer in the payload
// Hint: payload map { ... }

// TODO 2: Build each output object with:
//   - id: the customer's id
//   - fullName: concatenate firstName and lastName
//   - email: use default "unknown@example.com" for null/missing email
//   - phone: use default "N/A" for null/missing phone
//   - company: use default "Unaffiliated" for null/missing company
// Hint: $.email default "unknown@example.com"

[]
