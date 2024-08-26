-- base/db/sql/inventory_insert_or_replace.sql
-- Updates are logged as new entries with this method.
INSERT OR REPLACE INTO inventory (
    address, serial_number, model, displayVersion, version, serial_number, companyName, 
    username, verify_tls, message, last_result, consecutive_fails, 
    reply_ms, updated, last_seen
)
VALUES (
    :address, :serial_number, :model, :displayVersion, :version, :serial_number, :companyName, 
    :username, :verify_tls, :message, :last_result, :consecutive_fails, 
    :reply_ms, :updated, :last_seen
);
