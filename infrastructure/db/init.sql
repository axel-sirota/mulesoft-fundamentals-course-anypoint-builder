-- Customer Scores — Module 4 Infrastructure
-- PostgreSQL schema + seed data for Customer 360 enrichment.
-- Scores: 0-100. Segments: premium (>80), standard (51-80), basic (<=50).

CREATE TABLE customer_scores (
    customer_id VARCHAR(20) PRIMARY KEY,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    segment VARCHAR(20) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed data matching canonical 10 customers (ACCT-001..010)
INSERT INTO customer_scores (customer_id, score, segment) VALUES
    ('ACCT-001', 85, 'premium'),
    ('ACCT-002', 72, 'standard'),
    ('ACCT-003', 91, 'premium'),
    ('ACCT-004', 58, 'standard'),
    ('ACCT-005', 88, 'premium'),
    ('ACCT-006', 45, 'basic'),
    ('ACCT-007', 63, 'standard'),
    ('ACCT-008', 95, 'premium'),
    ('ACCT-009', 42, 'basic'),
    ('ACCT-010', 78, 'standard');
