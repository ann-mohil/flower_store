CREATE OR REPLACE PROCEDURE place_order(
    p_customer_id VARCHAR(36),
    p_bouquet_id VARCHAR(36),
    p_quantity INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_quantity <= 0 THEN
        RAISE EXCEPTION 'Quantity must be positive';
    END IF;
 
    IF NOT EXISTS (SELECT 1 FROM bouquets WHERE bouquet_id = p_bouquet_id) THEN
        RAISE EXCEPTION 'Bouquet % does not exist', p_bouquet_id;
    END IF;
 
    INSERT INTO orders (order_id, customer_id, status, total_amount)
    SELECT COALESCE(MAX(order_id), 0) + 1, p_customer_id, 'confirmed', 0
    FROM orders;

    INSERT INTO order_items (id, order_id, bouquet_id, quantity, unit_price)
    SELECT
        (SELECT COALESCE(MAX(id), 0) + 1 FROM order_items),
        (SELECT MAX(order_id) FROM orders),
        p_bouquet_id,
        p_quantity,
        price
   FROM bouquets
   WHERE bouquet_id = p_bouquet_id;
END;
$$;
 
CALL place_order('54d44d2b-0ecb-4428-bde7-b9a181f55e4d', '81dffaf9-74a1-4971-ac3d-d6fa7273b326', 3);
 