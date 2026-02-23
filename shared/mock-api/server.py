"""
Mock Customer API for MuleSoft Basics Course — Module 1
Flask server providing GET /api/customers and POST /api/customers/import.
Used throughout the course as the "coupled way" data source.
"""

from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================
# Customer 360 — Canonical 10 Records
# These same records appear across ALL modules:
#   - shared/mock-api (here)
#   - infrastructure/rest-api (enrichment data)
#   - infrastructure/db (customer scores)
#   - Module 3 RAML examples
#   - Module 5 DataWeave fixtures
#   - Module 6 test data (first 10 of 50)
# ============================================

CUSTOMERS = [
    {
        "id": "ACCT-001",
        "firstName": "Leanne",
        "lastName": "Graham",
        "email": "leanne.graham@romaguera.com",
        "phone": "(512) 555-0101",
        "company": "Romaguera-Crona",
        "industry": "Technology",
        "billingStreet": "742 Evergreen Terrace",
        "billingCity": "Austin",
        "billingState": "TX",
        "billingPostalCode": "78701"
    },
    {
        "id": "ACCT-002",
        "firstName": "Ervin",
        "lastName": "Howell",
        "email": "ervin.howell@deckow.com",
        "phone": "(415) 555-0102",
        "company": "Deckow-Crist",
        "industry": "Technology",
        "billingStreet": "1600 Amphitheatre Pkwy",
        "billingCity": "San Francisco",
        "billingState": "CA",
        "billingPostalCode": "94102"
    },
    {
        "id": "ACCT-003",
        "firstName": "Clementine",
        "lastName": "Bauch",
        "email": "clementine.bauch@keebler.com",
        "phone": "(617) 555-0103",
        "company": "Keebler LLC",
        "industry": "Healthcare",
        "billingStreet": "350 Fifth Avenue",
        "billingCity": "Boston",
        "billingState": "MA",
        "billingPostalCode": "02101"
    },
    {
        "id": "ACCT-004",
        "firstName": "Patricia",
        "lastName": "Lebsack",
        "email": "patricia.lebsack@robel.com",
        "phone": "(206) 555-0104",
        "company": "Robel-Corkery",
        "industry": "Technology",
        "billingStreet": "400 Broad St",
        "billingCity": "Seattle",
        "billingState": "WA",
        "billingPostalCode": "98109"
    },
    {
        "id": "ACCT-005",
        "firstName": "Chelsey",
        "lastName": "Dietrich",
        "email": "chelsey.dietrich@considine.com",
        "phone": "(312) 555-0105",
        "company": "Considine-Lockman",
        "industry": "Financial Services",
        "billingStreet": "233 S Wacker Dr",
        "billingCity": "Chicago",
        "billingState": "IL",
        "billingPostalCode": "60606"
    },
    {
        "id": "ACCT-006",
        "firstName": "Dennis",
        "lastName": "Schulist",
        "email": "dennis.schulist@kulas.com",
        "phone": "(313) 555-0106",
        "company": "Kulas Light Inc",
        "industry": "Manufacturing",
        "billingStreet": "1 Woodward Ave",
        "billingCity": "Detroit",
        "billingState": "MI",
        "billingPostalCode": "48226"
    },
    {
        "id": "ACCT-007",
        "firstName": "Kurtis",
        "lastName": "Weissnat",
        "email": "kurtis.weissnat@hoeger.com",
        "phone": "(303) 555-0107",
        "company": "Hoeger LLC",
        "industry": "Technology",
        "billingStreet": "1144 15th St",
        "billingCity": "Denver",
        "billingState": "CO",
        "billingPostalCode": "80202"
    },
    {
        "id": "ACCT-008",
        "firstName": "Nicholas",
        "lastName": "Runolfsdottir",
        "email": "nicholas.runolfsdottir@stanton.com",
        "phone": "(615) 555-0108",
        "company": "Stanton Group",
        "industry": "Healthcare",
        "billingStreet": "501 Broadway",
        "billingCity": "Nashville",
        "billingState": "TN",
        "billingPostalCode": "37203"
    },
    {
        "id": "ACCT-009",
        "firstName": "Glenna",
        "lastName": "Reichert",
        "email": "glenna.reichert@yost.com",
        "phone": "(503) 555-0109",
        "company": "Yost Partners",
        "industry": "Retail",
        "billingStreet": "750 NW 42nd St",
        "billingCity": "Portland",
        "billingState": "OR",
        "billingPostalCode": "97209"
    },
    {
        "id": "ACCT-010",
        "firstName": "Clementina",
        "lastName": "DuBuque",
        "email": "clementina.dubuque@mclaughlin.com",
        "phone": "(704) 555-0110",
        "company": "McLaughlin & Sons",
        "industry": "Financial Services",
        "billingStreet": "200 S Tryon St",
        "billingCity": "Charlotte",
        "billingState": "NC",
        "billingPostalCode": "28202"
    }
]


@app.route("/api/customers", methods=["GET"])
def get_customers():
    """Return all customers, optionally filtered by industry."""
    industry = request.args.get("industry")
    if industry:
        filtered = [c for c in CUSTOMERS if c["industry"].lower() == industry.lower()]
        return jsonify(filtered)
    return jsonify(CUSTOMERS)


@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Return a single customer by ID."""
    customer = next((c for c in CUSTOMERS if c["id"] == customer_id), None)
    if customer is None:
        return jsonify({"error": "Customer not found", "customerId": customer_id}), 404
    return jsonify(customer)


@app.route("/api/customers/import", methods=["POST"])
def import_customers():
    """Accept a JSON array of customers and log the import."""
    data = request.get_json(force=True, silent=True) or []
    timestamp = datetime.now(timezone.utc).isoformat()
    for record in data:
        name = record.get("full_name", record.get("firstName", "Unknown"))
        print(f"  [{timestamp}] Imported: {name}")
    return jsonify({
        "status": "success",
        "imported": len(data),
        "timestamp": timestamp
    }), 200


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Mock Customer API — MuleSoft Basics Course")
    print("=" * 50)
    print(f"  GET  http://localhost:5000/api/customers")
    print(f"  GET  http://localhost:5000/api/customers/ACCT-001")
    print(f"  GET  http://localhost:5000/api/customers?industry=Technology")
    print(f"  POST http://localhost:5000/api/customers/import")
    print("=" * 50 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
