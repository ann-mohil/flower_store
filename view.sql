CREATE OR REPLACE VIEW all_orders AS
SELECT
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount,
    c.full_name AS customer_name,
    c.email AS customer_email,
    b.bouquet_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN bouquets b ON oi.bouquet_id = b.bouquet_id;

EXPLAIN ANALYZE SELECT * FROM orders WHERE order_id = 3;
 