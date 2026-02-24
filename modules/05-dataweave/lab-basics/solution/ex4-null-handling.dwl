// Solution: Exercise 4 — Null Handling
// Apply defaults for null/missing fields, output clean JSON
// "default" triggers on null AND missing fields
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json skipNullOn="everywhere"
---
payload map {
  id: $.id,
  fullName: $.firstName ++ " " ++ $.lastName,
  email: $.email default "unknown@example.com",
  phone: $.phone default "N/A",
  company: $.company default "Unaffiliated"
}
