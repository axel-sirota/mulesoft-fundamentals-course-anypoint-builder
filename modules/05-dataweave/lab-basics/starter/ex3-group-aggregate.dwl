// Exercise 3: Group & Aggregate (CSV to JSON)
// Input: 20 sales records (ex3-input.csv)
// Task: Group by customerName, calculate totalAmount and orderCount per customer
// Expected output: 5 customer summaries (see ex3-expected.json)
// WARNING: CSV values are ALL strings! You must coerce amounts with "as Number"
%dw 2.0
output application/json
---
// TODO 1: Group the payload by customerName
// Hint: payload groupBy $.customerName
// NOTE: groupBy returns an Object, NOT an Array!

// TODO 2: Use pluck to convert the grouped Object into an Array
// Hint: ... pluck ((items, customerName) -> { ... })
// Remember: pluck gives you (value, key) — value is the array of items

// TODO 3: For each group, build an object with:
//   - customerName: the group key (cast to String: customerName as String)
//   - totalAmount: reduce items to sum of amounts (MUST cast: item.amount as Number)
//   - orderCount: count items using sizeOf(items)
// Hint: items reduce ((item, acc = 0) -> acc + (item.amount as Number))

[]
