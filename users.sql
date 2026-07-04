DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'flower_store_admin') THEN
        CREATE ROLE flower_store_admin LOGIN PASSWORD '1234!adM';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE flower_store_вb TO flower_store_admin;
GRANT USAGE, CREATE ON SCHEMA public TO flower_store_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flower_store_admin;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'flower_store_analyst') THEN
        CREATE ROLE flower_store_analyst LOGIN PASSWORD '123!AN';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE flower_store_вb TO flower_store_analyst;
GRANT USAGE ON SCHEMA public TO flower_store_analyst;
GRANT SELECT ON all_orders TO flower_store_analyst;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'flower_store_manager') THEN
        CREATE ROLE flower_store_manager LOGIN PASSWORD '123!manage';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE flower_store_вb TO flower_store_manager;
GRANT USAGE ON SCHEMA public TO flower_store_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON flowers, suppliers, flower_suppliers, bouquets TO flower_store_manager;
GRANT SELECT ON orders, order_items TO flower_store_manager;

