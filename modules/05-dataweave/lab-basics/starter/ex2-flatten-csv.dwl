// Exercise 2: Flatten Nested Orders to CSV (JSON to CSV)
// Input: 5 orders with nested lineItems (ex2-input.json)
// Task: Flatten to CSV rows with orderId, customerName, orderDate, itemName, quantity, price
// Expected output: 15 rows (see ex2-expected.csv)
%dw 2.0
output application/csv
---
// TODO 1: Use flatMap to iterate over each order in the payload
// Hint: payload flatMap ((order) -> ...)

// TODO 2: Inside flatMap, use map to iterate over each order's lineItems
// Hint: order.lineItems map ((item) -> { ... })

// TODO 3: Build each row object with fields from both order and item:
//   - orderId: from the order
//   - customerName: from the order
//   - orderDate: from the order
//   - itemName: from the line item
//   - quantity: from the line item
//   - price: from the line item

[]
