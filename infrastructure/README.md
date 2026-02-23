# Infrastructure Services

Docker Compose services used by Module 4 labs. Deployed on an EC2 instance managed by the instructor.

## Services

| Service | Port | Purpose |
|---------|------|---------|
| REST Enrichment API (FastAPI) | 8090 | `GET /api/enrich/{customerId}` — company enrichment data |
| SOAP Address Validation (Spyne) | 8091 | `ValidateAddress` operation — address normalization + confidence |
| PostgreSQL | 5432 | `customer_scores` table — score + segment per customer |

## Quick Start

```bash
cd infrastructure
docker-compose up -d --build
```

Wait ~30 seconds for all services to start, then verify:

```bash
# REST API
curl http://localhost:8090/api/enrich/ACCT-001
curl http://localhost:8090/health

# SOAP Service (WSDL)
curl http://localhost:8091/?wsdl

# PostgreSQL
PGPASSWORD=mulesoft123 psql -h localhost -U mulesoft -d customer360 -c "SELECT * FROM customer_scores;"
```

## EC2 Deployment

1. Launch an EC2 instance (t3.medium recommended) with Docker installed
2. Clone the repo: `git clone <repo-url> && cd mulesoft-course/infrastructure`
3. Start services: `docker-compose up -d --build`
4. Open security group ports: 8090, 8091, 5432 to student IP range

## PostgreSQL Credentials

| Property | Value |
|----------|-------|
| Database | customer360 |
| Username | mulesoft |
| Password | mulesoft123 |

## Troubleshooting

**SOAP WSDL not loading:** Spyne may take 10-15 seconds to initialize. Retry after waiting.

**PostgreSQL connection refused:** Check that the container is healthy: `docker-compose ps`. If restarting, the `pgdata` volume preserves data — to reset, run `docker-compose down -v` then `docker-compose up -d`.

**Port conflicts:** If ports 8090/8091/5432 are in use locally, stop conflicting services or modify the port mappings in `docker-compose.yml`.
