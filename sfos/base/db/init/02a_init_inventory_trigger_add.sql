-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS log_inventory_inserts;

CREATE TRIGGER log_inventory_inserts AFTER INSERT ON inventory FOR EACH ROW BEGIN
    INSERT INTO inventory_events (
        serial_number,
        address,
        changed_fields,
        old_values,
        new_values
    )
    VALUES (
        NEW.serial_number,
        NEW.address,
        'ADDED',
        '',
        (
            SELECT GROUP_CONCAT(value, ', ')
            FROM (
                SELECT NEW.model AS value
                    UNION ALL
                SELECT
                    NEW.displayVersion
                    UNION ALL
                SELECT
                    NEW.version
                    UNION ALL
                SELECT
                    NEW.serial_number
                    UNION ALL
                SELECT
                    NEW.companyName
                    UNION ALL
                SELECT
                    NEW.username
                    UNION ALL
                SELECT
                    NEW.verify_tls
                    UNION ALL
                SELECT
                    NEW.message
                    UNION ALL
                SELECT
                    NEW.last_result
                    UNION ALL
                SELECT
                    NEW.consecutive_fails
                    UNION ALL
                SELECT
                    NEW.reply_ms
                    UNION ALL
                SELECT
                    NEW.added
                    UNION ALL
                SELECT
                    NEW.updated
                    UNION ALL
                SELECT
                    NEW.last_seen
            )
        )
    );
