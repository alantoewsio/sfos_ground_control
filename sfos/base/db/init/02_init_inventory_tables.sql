-- base/db/init/##_init_inventory.sql
-- Create Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    address TEXT PRIMARY KEY,
    serial_number TEXT,
    model TEXT,
    displayVersion TEXT,
    version TEXT,
    companyName TEXT,
    username TEXT,
    verify_tls TEXT,
    message TEXT,
    last_result TEXT DEFAULT '',
    consecutive_fails INTEGER DEFAULT 0,
    reply_ms INTEGER DEFAULT -1,
    added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT NULL,
    session_id TEXT DEFAULT NULL,
    CONSTRAINT unique_address_serial_number UNIQUE (address, serial_number) ON CONFLICT REPLACE
);

-- Create event table for inventory and license changes
CREATE TABLE
    IF NOT EXISTS inventory_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number TEXT,
        address TEXT,
        changed_fields TEXT,
        old_values TEXT,
        new_values TEXT,
        change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
