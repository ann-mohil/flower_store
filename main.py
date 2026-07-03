import random
import uuid

import psycopg2
from psycopg2 import Error
from psycopg2.extras import execute_values
from faker import Faker


HOST = 'localhost'
USER = 'postgres'
PASSWORD = '12345'
DATABASE = 'flower_store_вb'
PORT = '5432'

fake = Faker()

N_CUSTOMERS = 5_000
N_FLOWERS = 40
N_SUPPLIERS = 10
N_BOUQUETS = 60
N_ORDERS = 100_000
AVG_ITEMS_PER_ORDER = 5

STARTING_ORDER_ID = 3
STARTING_ITEM_ID = 4

CATEGORIES = ["rose", "tulip", "lily", "peony", "orchid", "chrysanthemum", "sunflower"]
COLORS = ["red", "white", "pink", "yellow", "purple", "orange"]


def create_connection():
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DATABASE,
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None


def execute_query(connection, query, data):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")


def bulk_insert(cur, table, columns, rows, page_size=5000):
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING"
    execute_values(cur, query, rows, page_size=page_size)


def insert_demo_data(connection):
    customers_query = """
    INSERT INTO customers (customer_id, full_name, email, phone)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (customer_id) DO NOTHING
    """
    customers_data = [
        (str(uuid.uuid4()), "Olena Kovalenko", "olena.kovalenko@example.com", "0501234567"),
        (str(uuid.uuid4()), "Dmytro Melnyk", "dmytro.melnyk@example.com", "0671112233"),
    ]
    for data in customers_data:
        execute_query(connection, customers_query, data)

    customer_addresses_query = """
    INSERT INTO customer_addresses (id, customer_id, street, city, postcode, country)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """
    customer_addresses_data = [
        (str(uuid.uuid4()), customers_data[0][0], "Khreshchatyk St, 12", "Kyiv", "01001", "Ukraine"),
        (str(uuid.uuid4()), customers_data[1][0], "Shevchenka Ave, 5", "Lviv", "79000", "Ukraine"),
    ]
    for data in customer_addresses_data:
        execute_query(connection, customer_addresses_query, data)

    suppliers_query = """
    INSERT INTO suppliers (supplier_id, name, email, phone)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (supplier_id) DO NOTHING
    """
    suppliers_data = [
        (str(uuid.uuid4()), "KvitPostach LLC", "sales@kvitpostach.ua", "0442223344"),
        (str(uuid.uuid4()), "GreenLeaf Supply", "contact@greenleaf.ua", "0445556677"),
    ]
    for data in suppliers_data:
        execute_query(connection, suppliers_query, data)

    flowers_query = """
    INSERT INTO flowers (flower_id, flower_name, color, category, price, stock_quantity)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (flower_id) DO NOTHING
    """
    flowers_data = [
        (str(uuid.uuid4()), "Rose", "Red", "rose", 1.50, 800),
        (str(uuid.uuid4()), "Tulip", "Yellow", "tulip", 0.90, 1200),
    ]
    for data in flowers_data:
        execute_query(connection, flowers_query, data)

    flower_suppliers_query = """
    INSERT INTO flower_suppliers (flower_id, supplier_id, supply_price)
    VALUES (%s, %s, %s)
    ON CONFLICT (flower_id, supplier_id) DO NOTHING
    """
    flower_suppliers_data = [
        (flowers_data[0][0], suppliers_data[0][0], 0.80),
        (flowers_data[1][0], suppliers_data[1][0], 0.45),
    ]
    for data in flower_suppliers_data:
        execute_query(connection, flower_suppliers_query, data)

    bouquets_query = """
    INSERT INTO bouquets (bouquet_id, bouquet_name, description, price)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (bouquet_id) DO NOTHING
    """
    bouquets_data = [
        (str(uuid.uuid4()), "Spring Morning", "Roses and tulips, a gentle composition", 45.00),
        (str(uuid.uuid4()), "Classic", "15 red roses", 60.00),
    ]
    for data in bouquets_data:
        execute_query(connection, bouquets_query, data)

    orders_query = """
    INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (order_id) DO NOTHING
    """
    orders_data = [
        (1, customers_data[0][0], "2026-06-14 10:22:00", "delivered", 0),
        (2, customers_data[1][0], "2026-06-20 15:03:00", "pending", 0),
    ]
    for data in orders_data:
        execute_query(connection, orders_query, data)

    order_items_query = """
    INSERT INTO order_items (id, order_id, bouquet_id, quantity, unit_price)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """
    order_items_data = [
        (1, orders_data[0][0], bouquets_data[1][0], 1, 60.00),
        (2, orders_data[0][0], bouquets_data[0][0], 1, 45.00),
        (3, orders_data[1][0], bouquets_data[0][0], 1, 45.00),
    ]
    for data in order_items_data:
        execute_query(connection, order_items_query, data)

    print("Demo data inserted.")


def generate_bulk_data(connection):
    cur = connection.cursor()

    customer_ids = [str(uuid.uuid4()) for _ in range(N_CUSTOMERS)]
    customers = [
        (cid, f"{fake.first_name()} {fake.last_name()}", fake.unique.email(), fake.phone_number()[:20])
        for cid in customer_ids
    ]
    bulk_insert(cur, "customers", ["customer_id", "full_name", "email", "phone"], customers)

    addresses = [
        (str(uuid.uuid4()), cid, fake.street_address(), fake.city(), fake.postcode(), "Ukraine")
        for cid in customer_ids
    ]
    bulk_insert(cur, "customer_addresses", ["id", "customer_id", "street", "city", "postcode", "country"], addresses)

    flower_ids = [str(uuid.uuid4()) for _ in range(N_FLOWERS)]
    flowers = [
        (fid, fake.word().capitalize() + " Flower", random.choice(COLORS), random.choice(CATEGORIES),
         round(random.uniform(0.5, 5.0), 2), random.randint(100, 2000))
        for fid in flower_ids
    ]
    bulk_insert(cur, "flowers", ["flower_id", "flower_name", "color", "category", "price", "stock_quantity"], flowers)

    supplier_ids = [str(uuid.uuid4()) for _ in range(N_SUPPLIERS)]
    suppliers = [
        (sid, fake.company(), fake.unique.company_email(), fake.phone_number()[:20])
        for sid in supplier_ids
    ]
    bulk_insert(cur, "suppliers", ["supplier_id", "name", "email", "phone"], suppliers)

    flower_suppliers = []
    for fid in flower_ids:
        for sid in random.sample(supplier_ids, k=random.randint(1, 3)):
            flower_suppliers.append((fid, sid, round(random.uniform(0.2, 3.0), 2)))
    bulk_insert(cur, "flower_suppliers", ["flower_id", "supplier_id", "supply_price"], flower_suppliers)

    bouquet_ids = [str(uuid.uuid4()) for _ in range(N_BOUQUETS)]
    bouquets = [
        (bid, fake.catch_phrase() + " Bouquet", fake.sentence(nb_words=10), round(random.uniform(15, 90), 2))
        for bid in bouquet_ids
    ]
    bulk_insert(cur, "bouquets", ["bouquet_id", "bouquet_name", "description", "price"], bouquets)

    connection.commit()
    print("Bulk reference data inserted.")

    statuses = ["pending", "confirmed", "delivered", "cancelled"]
    order_ids = list(range(STARTING_ORDER_ID, STARTING_ORDER_ID + N_ORDERS))
    order_rows = [
        (oid, random.choice(customer_ids), fake.date_time_between(start_date="-2y", end_date="now"),
         random.choice(statuses), 0)
        for oid in order_ids
    ]
    bulk_insert(cur, "orders", ["order_id", "customer_id", "order_date", "status", "total_amount"], order_rows, page_size=5000)
    connection.commit()
    print(f"Inserted {len(order_ids)} orders.")

    bouquet_price_by_id = {b[0]: b[3] for b in bouquets}
    next_item_id = STARTING_ITEM_ID
    total_items = 0
    batch = []
    for oid in order_ids:
        for _ in range(random.randint(2, AVG_ITEMS_PER_ORDER * 2 - 2)):
            bid = random.choice(bouquet_ids)
            price = bouquet_price_by_id[bid]
            batch.append((next_item_id, oid, bid, random.randint(1, 5), price))
            next_item_id += 1
            total_items += 1
        if len(batch) >= 10000:
            bulk_insert(cur, "order_items", ["id", "order_id", "bouquet_id", "quantity", "unit_price"], batch, page_size=10000)
            connection.commit()
            batch = []
    if batch:
        bulk_insert(cur, "order_items", ["id", "order_id", "bouquet_id", "quantity", "unit_price"], batch, page_size=10000)
        connection.commit()

    print(f"Inserted {total_items} order_items rows (trigger recalculated each order's total_amount).")
    cur.close()


def main():
    connection = create_connection()
    if connection is None:
        return

    insert_demo_data(connection)
    generate_bulk_data(connection)

    connection.close()


if __name__ == "__main__":
    main()