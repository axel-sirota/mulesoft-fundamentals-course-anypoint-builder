// Exercise 9: Merge Transform Capstone (3 sources to 1 enriched customer)
// Inputs: ex9-company.json (REST), ex9-address.json (SOAP), ex9-score.json (DB)
// Task: Merge into single enriched customer record
// Expected output: Complete customer with address, score, segment (see ex9-expected.json)
// This mirrors the Module 4 Scatter-Gather merge transform
%dw 2.0
output application/json

import mergeWith from dw::core::Objects

// TODO 1: Define the three helper functions from Exercise 6
// (In a real Mule project, you'd import these from customer-utils.dwl)
// - normalizePhone(phone: String): String
// - classifySegment(score: Number): String
// - mergeCustomer(source: Object, enrichment: Object): Object

// TODO 2: Load the three data sources using readUrl
// In DW Playground: use inline var declarations
// var companyData = read(readUrl("classpath://fixtures/ex9-company.json", "text/plain"), "application/json")
// var addressData = read(readUrl("classpath://fixtures/ex9-address.json", "text/plain"), "application/json")
// var scoreData = read(readUrl("classpath://fixtures/ex9-score.json", "text/plain"), "application/json")
// In DW Playground: paste the JSON directly as var values
---
// TODO 3: Build the merged output object with:
//   - Company fields: customerId, companyName, industry, employeeCount, revenue,
//     headquarters, founded, website (from companyData)
//   - Address block: street, city, state, postalCode, country, validated (boolean),
//     deliverability (from addressData.validationResult.standardizedAddress)
//   - Score fields: creditScore, segment (using classifySegment function),
//     lastScoreUpdate (from scoreData)

{}
