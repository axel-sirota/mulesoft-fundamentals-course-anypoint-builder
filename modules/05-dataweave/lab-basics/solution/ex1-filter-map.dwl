// Solution: Exercise 1 — Filter & Map
// Filter Technology customers, map to simplified contact objects
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json
---
payload filter ($.industry == "Technology") map {
  fullName: $.firstName ++ " " ++ $.lastName,
  email: $.email,
  company: $.company
}
