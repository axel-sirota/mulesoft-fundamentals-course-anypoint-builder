// Solution: Exercise 2 — Flatten Nested Orders to CSV
// Use flatMap to flatten nested lineItems, output as CSV
// Validated in DW Playground — verify before production use
%dw 2.0
output application/csv
---
payload flatMap ((order) ->
  order.lineItems map ((item) -> {
    orderId: order.orderId,
    customerName: order.customerName,
    orderDate: order.orderDate,
    itemName: item.itemName,
    quantity: item.quantity,
    price: item.price
  })
)
