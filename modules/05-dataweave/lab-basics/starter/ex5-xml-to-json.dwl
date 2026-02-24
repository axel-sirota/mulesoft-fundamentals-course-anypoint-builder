// Exercise 5: XML to JSON (Flatten nested catalog)
// Input: XML catalog with 2-level nested categories and products (ex5-input.xml)
// Task: Flatten to array of products with categoryName from parent
// Expected output: 12 flat product objects (see ex5-expected.json)
// GOTCHA: Use .*category (multi-value selector) NOT .category (returns first only!)
// GOTCHA: Use .@attrName to access XML attributes
%dw 2.0
output application/json
---
// TODO 1: Select ALL top-level categories using .*category multi-value selector
// Hint: payload.catalog.*category

// TODO 2: Use flatMap to iterate top categories, then flatMap again for sub-categories
// Hint: ... flatMap ((topCat) -> topCat.*category flatMap ((subCat) -> ...))

// TODO 3: Use map to iterate products within each sub-category
// Hint: subCat.*product map ((prod) -> { ... })

// TODO 4: Build each product object with:
//   - productId: from the product's "id" attribute (prod.@id)
//   - name: the product's text content (prod as String)
//   - price: from the product's "price" attribute, cast to Number (prod.@price as Number)
//   - categoryName: from the sub-category's "name" attribute (subCat.@name as String)

[]
