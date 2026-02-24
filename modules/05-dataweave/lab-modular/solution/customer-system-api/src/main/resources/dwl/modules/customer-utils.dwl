// Shared DataWeave Module: customer-utils
// Reusable functions for Customer 360 domain
// Created in Module 5 Exercise 6, used by Exercise 9 and Module 4 flows
// Module files: NO output, NO ---, NO body expression
%dw 2.0
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
