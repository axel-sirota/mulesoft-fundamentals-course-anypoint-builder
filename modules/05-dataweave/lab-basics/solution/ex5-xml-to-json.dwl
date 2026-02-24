// Solution: Exercise 5 — XML to JSON (Flatten nested catalog)
// Use .*category multi-value selector and .@attr for XML attributes
// GOTCHA: .element returns FIRST match only; .*element returns ALL as array
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json
---
payload.catalog.*category flatMap ((topCat) ->
  topCat.*category flatMap ((subCat) ->
    subCat.*product map ((prod) -> {
      productId: prod.@id,
      name: prod as String,
      price: prod.@price as Number,
      categoryName: subCat.@name as String
    })
  )
)
