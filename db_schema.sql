CREATE DATABASE pump;

CREATE USER pump WITH PASSWORD 'pump';
GRANT ALL PRIVILEGES ON DATABASE pump TO pump;
-- basic connectivity
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO pump;
-- ability to apply a series of add()s in a single commit()
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pump;

DROP TABLE IF EXISTS instances;
CREATE TABLE instances (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INT,
    fixed_price FLOAT,
    instance_type VARCHAR(100),
    product_description VARCHAR(100),
    reserved_instances_offering_id VARCHAR(100),
    usage_price FLOAT,
    currency_code VARCHAR(10),
    instance_tenancy VARCHAR(20),
    marketplace BOOLEAN,
    offering_class VARCHAR(20),
    offering_type VARCHAR(20),
    pricing_details JSONB,
    recurring_charges JSONB,
    scope VARCHAR(20)
);

-- Query used by get_instance_volume_analytics() using SQLAlchemy ORM wrappers
-- WITH instance_counts AS (
--     SELECT
--         ('hour', timestamp) AS timestamp_hour,
--         COUNT(*) AS total_count
--     FROM
--         instances
--     WHERE
--         instance_type = 'm5.large'
--         AND DATE(timestamp) = '2023-10-03'
--     GROUP BY
--         timestamp_hour
-- )
-- SELECT
--     MIN(total_count) AS min_count,
--     MAX(total_count) AS max_count,
--     AVG(total_count) AS avg_count
-- FROM
--     instance_counts;