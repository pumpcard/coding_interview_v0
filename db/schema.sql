CREATE TABLE instance_offerings (
    id SERIAL PRIMARY KEY,
    duration INT NOT NULL,
    fixed_price MONEY NOT NULL,
    instance_type VARCHAR(255) NOT NULL,
    product_description VARCHAR(255) NOT NULL,
    reserved_instances_offering_id VARCHAR(255) UNIQUE NOT NULL,
    usage_price MONEY NOT NULL,
    currency_code VARCHAR(255) NOT NULL,
    instance_tenancy VARCHAR(255) NOT NULL,
    marketplace BOOLEAN NOT NULL,
    offering_class VARCHAR(255) NOT NULL,
    offering_type VARCHAR(255) NOT NULL
);

CREATE TABLE pricing_details (
    id SERIAL PRIMARY KEY,
    count INT NOT NULL,
    price MONEY NOT NULL,
    instance_offering_id INT NOT NULL,
    FOREIGN KEY (instance_offering_id) REFERENCES instance_offerings(id)
);

CREATE TABLE recurring_charges (
    id SERIAL PRIMARY KEY,
    amount MONEY NOT NULL,
    frequency VARCHAR(255) NOT NULL,
    instance_offering_id INT NOT NULL,
    FOREIGN KEY (instance_offering_id) REFERENCES instance_offerings(id)
);

CREATE INDEX instance_offerings_by_instance_type ON instance_offerings(instance_type);
CREATE INDEX instance_offerings_by_fixed_price ON instance_offerings(fixed_price);
CREATE INDEX instance_offerings_by_usage_price ON instance_offerings(usage_price);
CREATE INDEX instance_offerings_by_duration ON instance_offerings(duration);
