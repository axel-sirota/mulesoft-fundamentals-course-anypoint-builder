// Solution: Exercise 3 — Group & Aggregate (CSV to JSON)
// Group sales by customer, calculate totalAmount and orderCount
// GOTCHA: CSV values are ALL strings — must coerce with "as Number"
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json
---
payload groupBy $.customerName pluck ((items, customerName) -> {
  customerName: customerName as String,
  totalAmount: items reduce ((item, acc = 0) -> acc + (item.amount as Number)),
  orderCount: sizeOf(items)
})
