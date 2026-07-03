CREATE OR REPLACE FUNCTION update_order_total()
returns trigger
AS $$
BEGIN
    UPDATE orders
    SET total_amount = COALESCE(
        (SELECT SUM(quantity * unit_price)
         FROM order_items 
         WHERE order_id = COALESCE(NEW.order_id, OLD.order_id)), 0)
    WHERE order_id = COALESCE(NEW.order_id, OLD.order_id);
 
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_update_order_total ON order_items;
 
CREATE TRIGGER trg_update_order_total
AFTER INSERT OR UPDATE OR delete
ON order_items
FOR EACH ROW
EXECUTE function
update_order_total();
 
INSERT INTO order_items (id, order_id, bouquet_id, quantity, unit_price)
VALUES (500001, 2, '03e01185-4411-466d-b65f-a1d0b5531715', 1, 15.50);

SELECT total_amount FROM orders WHERE order_id = 2;