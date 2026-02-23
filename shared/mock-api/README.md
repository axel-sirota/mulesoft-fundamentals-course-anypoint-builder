# Mock Customer API

Flask-based mock API used in Module 1 to demonstrate the "coupled way" of integration.

## Quick Start

```bash
cd shared/mock-api
pip install -r requirements.txt
python server.py
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/customers` | Returns all 10 customer records |
| GET | `/api/customers?industry=Technology` | Filter by industry (4 Technology records) |
| GET | `/api/customers/ACCT-001` | Single customer by ID |
| POST | `/api/customers/import` | Accepts JSON array, logs imports |

## Sample Record

```json
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
}
```

## Data

10 customer records (ACCT-001 through ACCT-010) with industries: Technology (4), Healthcare (2), Financial Services (2), Manufacturing (1), Retail (1). This data is consistent across all course modules.
