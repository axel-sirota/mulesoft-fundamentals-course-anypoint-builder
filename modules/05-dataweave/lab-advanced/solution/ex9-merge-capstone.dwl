// Solution: Exercise 9 — Merge Transform Capstone
// Merge 3 data sources (REST, SOAP, DB) into enriched customer record
// Uses customer-utils module functions: normalizePhone, classifySegment, mergeCustomer
// Bridges to Module 4 Scatter-Gather merge pattern
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json

import mergeWith from dw::core::Objects

fun normalizePhone(phone: String): String =
  do {
    var digits = phone replace /[^\d]/ with ""
    ---
    if (sizeOf(digits) == 10)
      "(" ++ digits[0 to 2] ++ ") " ++ digits[3 to 5] ++ "-" ++ digits[6 to 9]
    else if (sizeOf(digits) == 11 and digits[0] == "1")
      "(" ++ digits[1 to 3] ++ ") " ++ digits[4 to 6] ++ "-" ++ digits[7 to 10]
    else
      phone
  }

fun classifySegment(score: Number): String =
  if (score > 80) "premium"
  else if (score > 50) "standard"
  else "basic"

fun mergeCustomer(source: Object, enrichment: Object): Object =
  enrichment mergeWith source

var companyData = read(readUrl("classpath://fixtures/ex9-company.json", "text/plain"), "application/json")
var addressData = read(readUrl("classpath://fixtures/ex9-address.json", "text/plain"), "application/json")
var scoreData = read(readUrl("classpath://fixtures/ex9-score.json", "text/plain"), "application/json")
---
{
  customerId: companyData.customerId,
  companyName: companyData.companyName,
  industry: companyData.industry,
  employeeCount: companyData.employeeCount,
  revenue: companyData.revenue,
  headquarters: companyData.headquarters,
  founded: companyData.founded,
  website: companyData.website,
  address: {
    street: addressData.validationResult.standardizedAddress.street,
    city: addressData.validationResult.standardizedAddress.city,
    state: addressData.validationResult.standardizedAddress.state,
    postalCode: addressData.validationResult.standardizedAddress.postalCode,
    country: addressData.validationResult.standardizedAddress.country,
    validated: addressData.validationResult.status == "VALID",
    deliverability: addressData.validationResult.deliverability
  },
  creditScore: scoreData.score,
  segment: classifySegment(scoreData.score),
  lastScoreUpdate: scoreData.last_updated
}
