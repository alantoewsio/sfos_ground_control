-- base/db/init/##_init_license.sql
-- Create licenses table
CREATE TABLE
    IF NOT EXISTS licenses (
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
CREATE TABLE
    IF NOT EXISTS license_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number TEXT,
        name TEXT,
        changed_fields TEXT,
        old_values TEXT,
        new_values TEXT,
        change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- */
-- /*
-- Create trigger to keep an audit trail of firewall record changes
DROP TRIGGER IF EXISTS log_license_changes;

CREATE TRIGGER IF NOT EXISTS log_license_changes AFTER
UPDATE ON licenses FOR EACH ROW BEGIN
INSERT INTO
    license_events (
        serial_number,
        name,
        changed_fields,
        old_values,
        new_values
    )
VALUES
    (
        OLD.serial_number,
        OLD.name,
        (
            SELECT
                GROUP_CONCAT (name, ', ')
            FROM
                (
                    SELECT
                        'uid'
                    WHERE
                        OLD.uid != NEW.uid
                    UNION ALL
                    SELECT
                        'serial_number'
                    WHERE
                        OLD.serial_number != NEW.serial_number
                    UNION ALL
                    SELECT
                        'name'
                    WHERE
                        OLD.name != NEW.name
                    UNION ALL
                    SELECT
                        'start_date'
                    WHERE
                        OLD.start_date != NEW.start_date
                    UNION ALL
                    SELECT
                        'expiry_date'
                    WHERE
                        OLD.expiry_date != NEW.expiry_date
                    UNION ALL
                    SELECT
                        'bundle'
                    WHERE
                        OLD.bundle != NEW.bundle
                    UNION ALL
                    SELECT
                        'status'
                    WHERE
                        OLD.status != NEW.status
                    UNION ALL
                    SELECT
                        'deactivation_reason'
                    WHERE
                        OLD.deactivation_reason != NEW.deactivation_reason
                    UNION ALL
                    SELECT
                        'type'
                    WHERE
                        OLD.type != NEW.type
                    UNION ALL
                    SELECT
                        'added'
                    WHERE
                        OLD.added != NEW.added
                    UNION ALL
                    SELECT
                        'updated'
                    WHERE
                        OLD.updated != NEW.updated
                )
        ),
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        OLD.uid
                    WHERE
                        OLD.uid != NEW.uid
                    UNION ALL
                    SELECT
                        OLD.serial_number
                    WHERE
                        OLD.serial_number != NEW.serial_number
                    UNION ALL
                    SELECT
                        OLD.name
                    WHERE
                        OLD.name != NEW.name
                    UNION ALL
                    SELECT
                        OLD.start_date
                    WHERE
                        OLD.start_date != NEW.start_date
                    UNION ALL
                    SELECT
                        OLD.expiry_date
                    WHERE
                        OLD.expiry_date != NEW.expiry_date
                    UNION ALL
                    SELECT
                        OLD.bundle
                    WHERE
                        OLD.bundle != NEW.bundle
                    UNION ALL
                    SELECT
                        OLD.status
                    WHERE
                        OLD.status != NEW.status
                    UNION ALL
                    SELECT
                        OLD.deactivation_reason
                    WHERE
                        OLD.deactivation_reason != NEW.deactivation_reason
                    UNION ALL
                    SELECT
                        OLD.type
                    WHERE
                        OLD.type != NEW.type
                    UNION ALL
                    SELECT
                        OLD.added
                    WHERE
                        OLD.added != NEW.added
                    UNION ALL
                    SELECT
                        OLD.updated
                    WHERE
                        OLD.updated != NEW.updated
                )
        ),
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        NEW.uid
                    WHERE
                        OLD.uid != NEW.uid
                    UNION ALL
                    SELECT
                        NEW.serial_number
                    WHERE
                        OLD.serial_number != NEW.serial_number
                    UNION ALL
                    SELECT
                        NEW.name
                    WHERE
                        OLD.name != NEW.name
                    UNION ALL
                    SELECT
                        NEW.start_date
                    WHERE
                        OLD.start_date != NEW.start_date
                    UNION ALL
                    SELECT
                        NEW.expiry_date
                    WHERE
                        OLD.expiry_date != NEW.expiry_date
                    UNION ALL
                    SELECT
                        NEW.bundle
                    WHERE
                        OLD.bundle != NEW.bundle
                    UNION ALL
                    SELECT
                        NEW.status
                    WHERE
                        OLD.status != NEW.status
                    UNION ALL
                    SELECT
                        NEW.deactivation_reason
                    WHERE
                        OLD.deactivation_reason != NEW.deactivation_reason
                    UNION ALL
                    SELECT
                        NEW.type
                    WHERE
                        OLD.type != NEW.type
                    UNION ALL
                    SELECT
                        NEW.added
                    WHERE
                        OLD.added != NEW.added
                    UNION ALL
                    SELECT
                        NEW.updated
                    WHERE
                        OLD.updated != NEW.updated
                )
        )
    );

-- */
-- Create trigger to log add events
-- /*
DROP TRIGGER IF EXISTS log_license_add;

CREATE TRIGGER IF NOT EXISTS log_license_add AFTER INSERT ON licenses FOR EACH ROW BEGIN
INSERT INTO
    license_events (
        serial_number,
        name,
        changed_fields,
        old_values,
        new_values
    )
VALUES
    (
        NEW.serial_number,
        NEW.name,
        'ADDED',
        '',
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        NEW.uid
                    UNION ALL
                    SELECT
                        NEW.serial_number
                    UNION ALL
                    SELECT
                        NEW.name
                    UNION ALL
                    SELECT
                        NEW.start_date
                    UNION ALL
                    SELECT
                        NEW.expiry_date
                    UNION ALL
                    SELECT
                        NEW.bundle
                    UNION ALL
                    SELECT
                        NEW.status
                    UNION ALL
                    SELECT
                        NEW.deactivation_reason
                    UNION ALL
                    SELECT
                        NEW.type
                    UNION ALL
                    SELECT
                        NEW.added
                    UNION ALL
                    SELECT
                        NEW.updated
                )
        )
    );

-- */
-- Create trigger to log license deletions
-- /*
DROP TRIGGER IF EXISTS log_license_delete;

CREATE TRIGGER IF NOT EXISTS log_license_delete AFTER DELETE ON licenses FOR EACH ROW BEGIN
INSERT INTO
    license_events (
        serial_number,
        name,
        changed_fields,
        old_values,
        new_values
    )
VALUES
    (
        OLD.serial_number,
        OLD.name,
        'DELETED',
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        OLD.uid
                    UNION ALL
                    SELECT
                        OLD.serial_number
                    UNION ALL
                    SELECT
                        OLD.name
                    UNION ALL
                    SELECT
                        OLD.start_date
                    UNION ALL
                    SELECT
                        OLD.expiry_date
                    UNION ALL
                    SELECT
                        OLD.bundle
                    UNION ALL
                    SELECT
                        OLD.status
                    UNION ALL
                    SELECT
                        OLD.deactivation_reason
                    UNION ALL
                    SELECT
                        OLD.type
                    UNION ALL
                    SELECT
                        OLD.added
                    UNION ALL
                    SELECT
                        OLD.updated
                )
        ),
        ''
    );

END;

-- */