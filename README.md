# flower_store
flower_store_db - база даних для ведення обліку клієнтів, їх замовлень, квітів, їх постачальників та асортименту букетів.(всього 8 таблиць)


Relationship types demonstrated:
1:1 — customers ↔ customer_addresses: кожен клієнт має рівно одну адресу(constraint: UNIQUE)

1:many — customers → orders, orders → order_items, bouquets → order_items: один клієнт має багато замовлень, одне замовлення — багато позицій.

many:many — flowers ↔ suppliers (flower_suppliers): один вид квітів може постачати кілька постачальників, один постачальник - багато різновидів квітів.

Серед використаних constraints:

NOT NULL, UNIQUE(email), NOT NULL CHECK(price/stock_quantity/status), зокрема деякі значення поставили по default(статус замовлення 'pending', що означає 'в обробці'; країна Ukraine в таблиці з адресами клієнтів)

Також задіяні PRIMARY KEY / FOREIGN KEY для цілісності даних.

До структури додані індекси на деякі стовпчики, перевіривши через EXPLAIN ANALYZE підтвердили, що після додавання індексів запит виконується набагато швидше (Index Scan на противагу Seq Scan).


View all_orders обʼєднує дані з orders, customers, bouquets, order_items в одне зручне представлення(через JOIN).


Реалізована процедура place_order(customer_id, bouquet_id, quantity) - власне оформлює замовлення, перевіряє наявність букета, додає в orders.


Trigger trg_update_order_total (AFTER INSERT/UPDATE/DELETE на order_items) автоматично викликає відповідну функцію та рахує orders.total_amount.


Users:

flower_store_admin - full привілегії

flower_store_analyst - read-only через all_orders view

flower_store_manager - read-only on orders/order_items; вносити зміни в flowers, suppliers, flower_suppliers, bouquets

flower_store_adflower_store_adminm
