DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS customer_addresses CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS bouquets CASCADE;
DROP TABLE IF EXISTS flower_suppliers CASCADE;
DROP TABLE IF EXISTS flowers CASCADE;


CREATE TABLE customers (
    customer_id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL
);

COMMENT ON TABLE customers IS 'People who place orders in the flower store';

CREATE TABLE customer_addresses (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL UNIQUE REFERENCES customers(customer_id) ON DELETE CASCADE,
    street VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postcode VARCHAR(20),
    country VARCHAR(100) NOT NULL DEFAULT 'Ukraine'
);

CREATE TABLE suppliers (
    supplier_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE,
    phone VARCHAR(20)
);

COMMENT ON TABLE suppliers IS 'Companies that supply flowers to the store';

CREATE TABLE flowers (
    flower_id VARCHAR(36) PRIMARY KEY,
    flower_name VARCHAR(200) NOT NULL,
    color VARCHAR(50),
    category VARCHAR(50),
    price NUMERIC(10,2) NOT NULL CHECK (price > 0),
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0)
);

COMMENT ON TABLE flowers IS 'Flower stock items';

CREATE TABLE flower_suppliers (
    flower_id VARCHAR(36) NOT NULL REFERENCES flowers(flower_id) ON DELETE CASCADE,
    supplier_id VARCHAR(36) NOT NULL REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    supply_price NUMERIC(10,2) NOT NULL CHECK (supply_price > 0),
    PRIMARY KEY (flower_id, supplier_id)
);

CREATE TABLE bouquets (
    bouquet_id VARCHAR(36) PRIMARY KEY,
    bouquet_name VARCHAR(200) NOT NULL,
    description VARCHAR(500),
    price NUMERIC(10,2) NOT NULL CHECK (price > 0)
);

COMMENT ON TABLE bouquets IS 'Bouquets that customers can order';

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL REFERENCES customers(customer_id),
    order_date TIMESTAMP NOT NULL DEFAULT now(),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'confirmed', 'delivered', 'cancelled')),
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0)
);

CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    bouquet_id VARCHAR(36) NOT NULL REFERENCES bouquets(bouquet_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price > 0)
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_bouquet_id ON order_items(bouquet_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_flowers_category ON flowers(category);
