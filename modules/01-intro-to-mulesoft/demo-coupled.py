"""
demo-coupled.py — The Coupled Way
This script does EXACTLY what the Mule flow does... but badly.
Run it. Then ask yourself: would you trust this at 3am?
"""
import requests

# HARDCODED URL: Grep through 15 scripts and pray you find them all
SOURCE_URL = "http://localhost:5173/api/customers"
TARGET_URL = "http://localhost:5173/api/customers/import"

# NO ERROR HANDLING: If the source is down, nobody knows until Monday morning
response = requests.get(SOURCE_URL)
customers = response.json()

# INLINE TRANSFORM: Duplicated in etl_contacts.py and sync_accounts.py
# If the field mapping changes, you edit this and 3 other scripts
tech_customers = [
    {
        "full_name": f"{c['firstName']} {c['lastName']}",   # NO AUTH: Hope nobody finds this endpoint
        "contact_email": c["email"],
        "organization": c["company"],
        "location": f"{c['billingCity']}, {c['billingState']}",
        "source": "sf-org-a"  # HARDCODED: What about org-b? org-c?
    }
    for c in customers
    if c["industry"] == "Technology"  # NO RETRY: If it fails, it fails
]

# NO LOGGING: print() is not observability
print(f"Found {len(tech_customers)} Technology customers")

# DUPLICATED LOGIC: This same POST exists in 4 other scripts
result = requests.post(TARGET_URL, json=tech_customers)
print(f"Import result: {result.json()}")

# ============================================
# Now ask yourself:
#
# 1. What if you need a second data source?
#    → Duplicate the entire script with a new URL.
#
# 2. What if the API schema changes?
#    → Find and fix every script that calls it.
#
# 3. What if you need an enrichment step in the middle?
#    → Add more inline code. More duplication.
#
# 4. What if this needs to run on a schedule?
#    → cron job? systemd? Hope it doesn't overlap.
#
# 5. What if you need error handling and retry?
#    → Wrap everything in try/except. In every script.
#
# Now imagine all 5 for 15 scripts. That's why MuleSoft exists.
# ============================================
