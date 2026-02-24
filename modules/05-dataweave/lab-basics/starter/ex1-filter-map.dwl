// Exercise 1: Filter & Map (JSON to JSON)
// Input: 10 customers (ex1-input.json)
// Task: Filter Technology customers, map to {fullName, email, company}
// Expected output: 4 records (see ex1-expected.json)
%dw 2.0
output application/json
---
// TODO 1: Filter the payload to keep only customers where industry == "Technology"
// Hint: Use the filter function — payload filter ($.field == "value")

// TODO 2: Map each filtered customer to a new object with:
//   - fullName: concatenate firstName and lastName with a space
//   - email: the customer's email
//   - company: the customer's company
// Hint: Use the map function — arrayResult map { key: $.field }
// Hint: String concatenation uses ++ operator: $.firstName ++ " " ++ $.lastName

[]
