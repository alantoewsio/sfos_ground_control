-- base/db/sql/init_triggers.sql
-- /*
-- Create trigger to keep an audit trail of firewall record changes
DROP TRIGGER IF EXISTS log_inventory_changes;
CREATE TRIGGER IF NOT EXISTS log_inventory_changes
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
    INSERT INTO events (
        serial_number, address, changed_fields, old_values, new_values, source
    )
    VALUES (
        OLD.serial_number,
        OLD.address,        
        (SELECT GROUP_CONCAT(name, ', ') FROM (
            SELECT 'model' AS name WHERE OLD.model != NEW.model UNION ALL
            SELECT 'displayVersion' WHERE OLD.displayVersion != NEW.displayVersion UNION ALL
            SELECT 'version' WHERE OLD.version != NEW.version UNION ALL
            SELECT 'serial_number' WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT 'companyName' WHERE OLD.companyName != NEW.companyName UNION ALL
            SELECT 'username' WHERE OLD.username != NEW.username UNION ALL
            SELECT 'verify_tls' WHERE OLD.verify_tls != NEW.verify_tls UNION ALL
            SELECT 'message' WHERE OLD.message != NEW.message UNION ALL
            SELECT 'last_result' WHERE OLD.last_result != NEW.last_result            
            )
        ),
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT OLD.model AS value WHERE OLD.model != NEW.model UNION ALL
            SELECT OLD.displayVersion WHERE OLD.displayVersion != NEW.displayVersion UNION ALL
            SELECT OLD.version WHERE OLD.version != NEW.version UNION ALL
            SELECT OLD.serial_number WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT OLD.companyName WHERE OLD.companyName != NEW.companyName UNION ALL
            SELECT OLD.username WHERE OLD.username != NEW.username UNION ALL
            SELECT OLD.verify_tls WHERE OLD.verify_tls != NEW.verify_tls UNION ALL
            SELECT OLD.message WHERE OLD.message != NEW.message UNION ALL
            SELECT OLD.last_result WHERE OLD.last_result != NEW.last_result
            )
        ),
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT NEW.model AS value WHERE OLD.model != NEW.model UNION ALL
            SELECT NEW.displayVersion WHERE OLD.displayVersion != NEW.displayVersion UNION ALL
            SELECT NEW.version WHERE OLD.version != NEW.version UNION ALL
            SELECT NEW.serial_number WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT NEW.companyName WHERE OLD.companyName != NEW.companyName UNION ALL
            SELECT NEW.username WHERE OLD.username != NEW.username UNION ALL
            SELECT NEW.verify_tls WHERE OLD.verify_tls != NEW.verify_tls UNION ALL
            SELECT NEW.message WHERE OLD.message != NEW.message UNION ALL
            SELECT NEW.last_result WHERE OLD.last_result != NEW.last_result                      
            )
        ),
        'inventory'
    );
END;

-- */

-- Create trigger to log add events
-- /*
DROP TRIGGER IF EXISTS log_inventory_add;
CREATE TRIGGER IF NOT EXISTS log_inventory_add
AFTER INSERT ON inventory
FOR EACH ROW
BEGIN
    INSERT INTO events (serial_number, address, changed_fields, old_values, new_values, source)
    VALUES (
        NEW.serial_number,
        NEW.address,
        'ADDED',
        '',
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT NEW.model AS value UNION ALL
            SELECT NEW.displayVersion UNION ALL
            SELECT NEW.version UNION ALL
            SELECT NEW.serial_number UNION ALL
            SELECT NEW.companyName UNION ALL
            SELECT NEW.username UNION ALL
            SELECT NEW.verify_tls UNION ALL
            SELECT NEW.message UNION ALL
            SELECT NEW.last_result UNION ALL
            SELECT NEW.consecutive_fails UNION ALL
            SELECT NEW.reply_ms UNION ALL
            SELECT NEW.added UNION ALL
            SELECT NEW.updated UNION ALL
            SELECT NEW.last_seen
        )),
        'inventory'
    );
END;
-- */

-- Create trigger to log inventory deletions
-- /*
DROP TRIGGER IF EXISTS log_inventory_delete;
CREATE TRIGGER IF NOT EXISTS log_inventory_delete
AFTER DELETE ON inventory
FOR EACH ROW
BEGIN
    INSERT INTO events (serial_number, address, changed_fields, old_values, new_values, source)
    VALUES (
        OLD.serial_number,
        OLD.address,
        'DELETED',
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT OLD.model AS value UNION ALL
            SELECT OLD.displayVersion UNION ALL
            SELECT OLD.version UNION ALL
            SELECT OLD.serial_number UNION ALL
            SELECT OLD.companyName UNION ALL
            SELECT OLD.username UNION ALL
            SELECT OLD.verify_tls UNION ALL
            SELECT OLD.message UNION ALL
            SELECT OLD.last_result UNION ALL
            SELECT OLD.consecutive_fails UNION ALL
            SELECT OLD.reply_ms UNION ALL
            SELECT OLD.added UNION ALL
            SELECT OLD.updated UNION ALL
            SELECT OLD.last_seen
        )),
        '',
        'inventory'
    );
END;
-- */

-- /*
-- Create trigger to keep an audit trail of firewall record changes
DROP TRIGGER IF EXISTS log_license_changes;
CREATE TRIGGER IF NOT EXISTS log_license_changes
AFTER UPDATE ON licenses
FOR EACH ROW
BEGIN
    INSERT INTO events (
        serial_number, address, changed_fields, old_values, new_values, source
    )
    VALUES (
        OLD.serial_number,
        OLD.address,        
        (SELECT GROUP_CONCAT(name, ', ') FROM (
            SELECT 'uid' WHERE OLD.uid != NEW.uid UNION ALL
            SELECT 'serial_number' WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT 'name' WHERE OLD.name != NEW.name UNION ALL
            SELECT 'start_date' WHERE OLD.start_date != NEW.start_date UNION ALL
            SELECT 'expiry_date' WHERE OLD.expiry_date != NEW.expiry_date UNION ALL
            SELECT 'bundle' WHERE OLD.bundle != NEW.bundle UNION ALL
            SELECT 'status' WHERE OLD.status != NEW.status UNION ALL
            SELECT 'deactivation_reason' WHERE OLD.deactivation_reason != NEW.deactivation_reason UNION ALL
            SELECT 'type' WHERE OLD.type != NEW.type UNION ALL
            SELECT 'added' WHERE OLD.added != NEW.added UNION ALL
            SELECT 'updated' WHERE OLD.updated != NEW.updated            
            )
        ),
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT OLD.uid WHERE OLD.uid != NEW.uid UNION ALL
            SELECT OLD.serial_number WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT OLD.name WHERE OLD.name != NEW.name UNION ALL
            SELECT OLD.start_date WHERE OLD.start_date != NEW.start_date UNION ALL
            SELECT OLD.expiry_date WHERE OLD.expiry_date != NEW.expiry_date UNION ALL
            SELECT OLD.bundle WHERE OLD.bundle != NEW.bundle UNION ALL
            SELECT OLD.status WHERE OLD.status != NEW.status UNION ALL
            SELECT OLD.deactivation_reason WHERE OLD.deactivation_reason != NEW.deactivation_reason UNION ALL
            SELECT OLD.type WHERE OLD.type != NEW.type UNION ALL
            SELECT OLD.added WHERE OLD.added != NEW.added UNION ALL
            SELECT OLD.updated WHERE OLD.updated != NEW.updated
            )
        ),
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT NEW.uid WHERE OLD.uid != NEW.uid UNION ALL
            SELECT NEW.serial_number WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT NEW.name WHERE OLD.name != NEW.name UNION ALL
            SELECT NEW.start_date WHERE OLD.start_date != NEW.start_date UNION ALL
            SELECT NEW.expiry_date WHERE OLD.expiry_date != NEW.expiry_date UNION ALL
            SELECT NEW.bundle WHERE OLD.bundle != NEW.bundle UNION ALL
            SELECT NEW.status WHERE OLD.status != NEW.status UNION ALL
            SELECT NEW.deactivation_reason WHERE OLD.deactivation_reason != NEW.deactivation_reason UNION ALL
            SELECT NEW.type WHERE OLD.type != NEW.type UNION ALL
            SELECT NEW.added WHERE OLD.added != NEW.added UNION ALL
            SELECT NEW.updated WHERE OLD.updated != NEW.updated                      
            )
        ),
        'licenses'
    );
END;

-- */

-- Create trigger to log add events
-- /*
DROP TRIGGER IF EXISTS log_inventory_add;
CREATE TRIGGER IF NOT EXISTS log_inventory_add
AFTER INSERT ON inventory
FOR EACH ROW
BEGIN
    INSERT INTO events (serial_number, address, changed_fields, old_values, new_values, source)
    VALUES (
        NEW.serial_number,
        NEW.address,
        'ADDED',
        '',
        (SELECT GROUP_CONCAT(value, ', ') FROM (
            SELECT NEW.uid UNION ALL
            SELECT NEW.serial_number UNION ALL
            SELECT NEW.name UNION ALL
            SELECT NEW.start_date UNION ALL
            SELECT NEW.expiry_date UNION ALL
            SELECT NEW.bundle UNION ALL
            SELECT NEW.status UNION ALL
            SELECT NEW.deactivation_reason UNION ALL
            SELECT NEW.type UNION ALL
            SELECT NEW.added UNION ALL
            SELECT NEW.updated
        )),
        'licenses'
    );
END;
-- */

-- Create trigger to log inventory deletions
-- /*
DROP TRIGGER IF EXISTS log_inventory_delete;
CREATE TRIGGER IF NOT EXISTS log_inventory_delete
AFTER DELETE ON inventory
FOR EACH ROW
BEGIN
    INSERT INTO events (serial_number, address, changed_fields, old_values, new_values, source)
    VALUES (
        OLD.serial_number,
        OLD.address,
        'DELETED',
        (SELECT GROUP_CONCAT(value, ', ') FROM (            
            SELECT OLD.uid UNION ALL
            SELECT OLD.serial_number UNION ALL
            SELECT OLD.name UNION ALL
            SELECT OLD.start_date UNION ALL
            SELECT OLD.expiry_date UNION ALL
            SELECT OLD.bundle UNION ALL
            SELECT OLD.status UNION ALL
            SELECT OLD.deactivation_reason UNION ALL
            SELECT OLD.type UNION ALL
            SELECT OLD.added UNION ALL
            SELECT OLD.updated
        )),
        '',
        'licenses'
    );
END;
-- */