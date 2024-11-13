-- Drop existing triggers so they are created up-to-date
DROP TRIGGER IF EXISTS log_inventory_deletes;

CREATE TRIGGER IF NOT EXISTS log_inventory_deletes AFTER DELETE ON inventory FOR EACH ROW BEGIN
INSERT INTO
    inventory_events (
        serial_number,
        address,
        changed_fields,
        old_values,
        new_values
    )
VALUES
    (
        OLD.serial_number,
        OLD.address,
        'DELETED',
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        OLD.model AS value
                    UNION ALL
                    SELECT
                        OLD.displayVersion
                    UNION ALL
                    SELECT
                        OLD.version
                    UNION ALL
                    SELECT
                        OLD.serial_number
                    UNION ALL
                    SELECT
                        OLD.companyName
                    UNION ALL
                    SELECT
                        OLD.username
                    UNION ALL
                    SELECT
                        OLD.verify_tls
                    UNION ALL
                    SELECT
                        OLD.message
                    UNION ALL
                    SELECT
                        OLD.last_result
                    UNION ALL
                    SELECT
                        OLD.consecutive_fails
                    UNION ALL
                    SELECT
                        OLD.reply_ms
                    UNION ALL
                    SELECT
                        OLD.added
                    UNION ALL
                    SELECT
                        OLD.updated
                    UNION ALL
                    SELECT
                        OLD.last_seen
                )
        ),
        ''
    );