-- base/db/sql/init_tables.sql
-- /*
-- Create Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    address TEXT UNIQUE,
    serial_number TEXT UNIQUE,
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
    last_seen TIMESTAMP DEFAULT NULL
);
-- */
-- Update table to account for changes
ALTER TABLE inventory RENAME COLUMN Model TO model;

-- /*
-- Create licenses table
CREATE TABLE IF NOT EXISTS licenses (
    uid TEXT UNIQUE,
    serial_number TEXT,
    name TEXT,
    start_date TIMESTAMP DEFAULT NULL,
    expiry_date TIMESTAMP DEFAULT NULL,
    bundle TEXT DEFAULT '',
    status TEXT DEFAULT '',
    deactivation_reason TEXT DEFAULT '',
    type TEXT DEFAULT '',
    added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- */

--/*
-- Create eventlog table
-- DROP TABLE events;
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number TEXT,
    address TEXT,
    changed_fields TEXT,
    old_values TEXT,
    new_values TEXT,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT
);
