// Solution: Module 5, Exercise 10 — External Merge Transform
// Extracted from implementation.xml Scatter-Gather merge
// Imports reusable functions from customer-utils module
// Validated in DW Playground — verify before production use
%dw 2.0
output application/json skipNullOn="everywhere"

import normalizePhone, classifySegment from modules::customer-utils

var enrichment = payload."0".payload
var scoreData  = payload."1".payload[0]
var address    = payload."2".payload
---
{
    customerId:        vars.customerId,
    company:           enrichment.companyName default "Unknown",
    industry:          enrichment.industry default "Unknown",
    employees:         enrichment.employeeCount,
    revenue:           enrichment.revenue,
    phone:             if (enrichment.phone != null)
                         normalizePhone(enrichment.phone)
                       else
                         "N/A",
    score:             scoreData.score,
    segment:           classifySegment(scoreData.score default 0),
    addressValid:      address.body.ValidateAddressResponse.isValid default false,
    addressConfidence: address.body.ValidateAddressResponse.confidence default "NONE",
    enrichedAt:        now()
}
