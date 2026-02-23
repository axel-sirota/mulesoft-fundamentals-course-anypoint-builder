"""
REST Enrichment API — Module 4 Infrastructure
FastAPI service providing company enrichment data for Customer 360.
Deployed on EC2 via Docker Compose, accessed by students' Mule flows.
"""

from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Customer Enrichment API",
    description="REST enrichment service for MuleSoft Basics course",
    version="1.0.0"
)

# Enrichment data matching the canonical 10 customers (ACCT-001..010)
ENRICHMENT_DATA = {
    "ACCT-001": {
        "customerId": "ACCT-001",
        "companyName": "Romaguera-Crona",
        "industry": "Technology",
        "employeeCount": 2500,
        "revenue": 450000000,
        "headquarters": "Austin, TX",
        "founded": 2008,
        "website": "https://romaguera-crona.example.com"
    },
    "ACCT-002": {
        "customerId": "ACCT-002",
        "companyName": "Deckow-Crist",
        "industry": "Technology",
        "employeeCount": 800,
        "revenue": 120000000,
        "headquarters": "San Francisco, CA",
        "founded": 2015,
        "website": "https://deckow-crist.example.com"
    },
    "ACCT-003": {
        "customerId": "ACCT-003",
        "companyName": "Keebler LLC",
        "industry": "Healthcare",
        "employeeCount": 5200,
        "revenue": 980000000,
        "headquarters": "Boston, MA",
        "founded": 1995,
        "website": "https://keebler-llc.example.com"
    },
    "ACCT-004": {
        "customerId": "ACCT-004",
        "companyName": "Robel-Corkery",
        "industry": "Technology",
        "employeeCount": 350,
        "revenue": 55000000,
        "headquarters": "Seattle, WA",
        "founded": 2019,
        "website": "https://robel-corkery.example.com"
    },
    "ACCT-005": {
        "customerId": "ACCT-005",
        "companyName": "Considine-Lockman",
        "industry": "Financial Services",
        "employeeCount": 3100,
        "revenue": 720000000,
        "headquarters": "Chicago, IL",
        "founded": 2001,
        "website": "https://considine-lockman.example.com"
    },
    "ACCT-006": {
        "customerId": "ACCT-006",
        "companyName": "Kulas Light Inc",
        "industry": "Manufacturing",
        "employeeCount": 8500,
        "revenue": 1500000000,
        "headquarters": "Detroit, MI",
        "founded": 1987,
        "website": "https://kulas-light.example.com"
    },
    "ACCT-007": {
        "customerId": "ACCT-007",
        "companyName": "Hoeger LLC",
        "industry": "Technology",
        "employeeCount": 150,
        "revenue": 22000000,
        "headquarters": "Denver, CO",
        "founded": 2021,
        "website": "https://hoeger-llc.example.com"
    },
    "ACCT-008": {
        "customerId": "ACCT-008",
        "companyName": "Stanton Group",
        "industry": "Healthcare",
        "employeeCount": 4200,
        "revenue": 650000000,
        "headquarters": "Nashville, TN",
        "founded": 2003,
        "website": "https://stanton-group.example.com"
    },
    "ACCT-009": {
        "customerId": "ACCT-009",
        "companyName": "Yost Partners",
        "industry": "Retail",
        "employeeCount": 1200,
        "revenue": 280000000,
        "headquarters": "Portland, OR",
        "founded": 2012,
        "website": "https://yost-partners.example.com"
    },
    "ACCT-010": {
        "customerId": "ACCT-010",
        "companyName": "McLaughlin & Sons",
        "industry": "Financial Services",
        "employeeCount": 6800,
        "revenue": 2100000000,
        "headquarters": "Charlotte, NC",
        "founded": 1992,
        "website": "https://mclaughlin-sons.example.com"
    }
}


@app.get("/api/enrich/{customer_id}")
def enrich_customer(customer_id: str):
    """Return enrichment data for a customer by ID."""
    data = ENRICHMENT_DATA.get(customer_id)
    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"No enrichment data found for customer: {customer_id}"
        )
    return {
        **data,
        "enrichedAt": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "enrichment-api", "customers": len(ENRICHMENT_DATA)}
