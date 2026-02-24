// Exercise 6: Reusable Module (customer-utils)
// IMPORTANT: Module files have NO output directive, NO --- separator, NO body expression
// Only %dw 2.0 header + fun/var/import declarations
// Test with: ex6-phone-tests.json and ex6-merge-tests.json
%dw 2.0
import mergeWith from dw::core::Objects

// TODO 1: Define normalizePhone(phone: String): String
// Strip all non-digit characters, then format as (XXX) XXX-XXXX
// Rules:
//   - 10 digits → format as (XXX) XXX-XXXX
//   - 11 digits starting with "1" → strip leading 1, then format
//   - Anything else → return original phone string
// Hints:
//   - Use: phone replace /[^\d]/ with "" to strip non-digits
//   - Use do { var digits = ... --- body } for local variables
//   - Use sizeOf(digits) to check length
//   - Use digits[0 to 2] for substring (inclusive range)

// TODO 2: Define classifySegment(score: Number): String
// Rules:
//   - score > 80 → "premium"
//   - score > 50 → "standard"
//   - otherwise → "basic"

// TODO 3: Define mergeCustomer(source: Object, enrichment: Object): Object
// Merge enrichment data into source, where SOURCE fields win on conflicts
// Hint: mergeWith from dw::core::Objects — second argument wins
// So: enrichment mergeWith source → source fields override enrichment
