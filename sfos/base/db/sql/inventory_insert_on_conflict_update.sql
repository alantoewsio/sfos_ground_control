-- base/db/sql/inventoru_insert_on_conflict_update.sql
-- inserts are correctly logged as additions and updates are correctly logged as updates
INSERT INTO inventory (
    address, model, displayVersion, version, serial_number, companyName, 
    username, verify_tls, message, last_result, consecutive_fails, 
    reply_ms, updated, last_seen
)
VALUES (
    :address, :model, :displayVersion, :version, :serial_number, :companyName, 
    :username, :verify_tls, :message, :last_result, :consecutive_fails, 
    :reply_ms, :updated, :last_seen
)
ON CONFLICT(address) DO UPDATE SET
    serial_number = CASE WHEN excluded.serial_number != inventory.serial_number 
        AND excluded.serial_number IS NOT NULL THEN excluded.serial_number ELSE inventory.serial_number END,
    model = CASE WHEN excluded.model != inventory.model 
        AND excluded.model IS NOT NULL THEN excluded.model ELSE inventory.model END,
    displayVersion = CASE WHEN excluded.displayVersion != inventory.displayVersion 
        AND excluded.displayVersion IS NOT NULL THEN excluded.displayVersion ELSE inventory.displayVersion END,
    version = CASE WHEN excluded.version != inventory.version 
        AND excluded.version IS NOT NULL THEN excluded.version ELSE inventory.version END,
    companyName = CASE WHEN excluded.companyName != inventory.companyName 
        AND excluded.companyName IS NOT NULL THEN excluded.companyName ELSE inventory.companyName END,
    username = CASE WHEN excluded.username != inventory.username 
        AND excluded.username IS NOT NULL THEN excluded.username ELSE inventory.username END,
    verify_tls = CASE WHEN excluded.verify_tls != inventory.verify_tls 
        AND excluded.verify_tls IS NOT NULL THEN excluded.verify_tls ELSE inventory.verify_tls END,
    message = CASE WHEN excluded.message != inventory.message 
        AND excluded.message IS NOT NULL THEN excluded.message ELSE inventory.message END,
    last_result = CASE WHEN excluded.last_result != inventory.last_result 
        AND excluded.last_result IS NOT NULL THEN excluded.last_result ELSE inventory.last_result END,
    consecutive_fails = CASE WHEN excluded.consecutive_fails != inventory.consecutive_fails 
        AND excluded.consecutive_fails IS NOT NULL THEN excluded.consecutive_fails ELSE inventory.consecutive_fails END,
    reply_ms = CASE WHEN excluded.reply_ms != inventory.reply_ms 
        AND excluded.reply_ms IS NOT NULL THEN excluded.reply_ms ELSE inventory.reply_ms END,
    updated = CURRENT_TIMESTAMP,
    last_seen = CASE WHEN excluded.last_seen IS NOT NULL 
        THEN excluded.last_seen ELSE inventory.last_seen END;
