-- base/db/init/##_init_users.sql
--/*
-- Create user table
CREATE TABLE
    IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        display_name TEXT,
        title TEXT
    );

-- */
--/*
-- Create eventlog table
-- DROP TABLE events;
CREATE TABLE
    IF NOT EXISTS user_change_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event TEXT,
        changes TEXT,
        old_values TEXT,
        new_values TEXT,
        change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source TEXT
    );

-- */
-- /*
-- Create trigger to keep an audit trail of user record changes
DROP TRIGGER IF EXISTS user_changes;

CREATE TRIGGER IF NOT EXISTS user_changes AFTER
UPDATE ON users FOR EACH ROW BEGIN
INSERT INTO
    user_change_events (user_id, username, change, old_values, new_values)
VALUES
    (
        OLD.id,
        OLD.username,
        (
            SELECT
                GROUP_CONCAT (name, ', ')
            FROM
                (
                    SELECT
                        'email'
                    WHERE
                        OLD.email != NEW.email
                    UNION ALL
                    SELECT
                        'password'
                    WHERE
                        OLD.password != NEW.password
                    UNION ALL
                    SELECT
                        'display_name'
                    WHERE
                        OLD.display_name != NEW.display_name
                    UNION ALL
                    SELECT
                        'title'
                    WHERE
                        OLD.title != NEW.title
                )
        ),
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        OLD.email
                    WHERE
                        OLD.email != NEW.email
                    UNION ALL
                    SELECT
                        OLD.password
                    WHERE
                        OLD.password != NEW.password
                    UNION ALL
                    SELECT
                        OLD.display_name
                    WHERE
                        OLD.display_name != NEW.display_name
                    UNION ALL
                    SELECT
                        OLD.title
                    WHERE
                        OLD.title != NEW.title
                )
        ),
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        NEW.email
                    WHERE
                        OLD.email != NEW.email
                    UNION ALL
                    SELECT
                        NEW.password
                    WHERE
                        OLD.password != NEW.password
                    UNION ALL
                    SELECT
                        NEW.display_name
                    WHERE
                        OLD.display_name != NEW.display_name
                    UNION ALL
                    SELECT
                        NEW.title
                    WHERE
                        OLD.title != NEW.title
                )
        )
    );

END;

-- */
-- Create trigger to log add events
-- /*
DROP TRIGGER IF EXISTS user_add;

CREATE TRIGGER IF NOT EXISTS user_add AFTER INSERT ON users FOR EACH ROW BEGIN
INSERT INTO
    user_change_events (user_id, username, change, old_values, new_values)
VALUES
    (
        NEW.id,
        NEW.username,
        'ADDED',
        '',
        (
            SELECT
                GROUP_CONCAT (value, ', ')
            FROM
                (
                    SELECT
                        NEW.email
                    UNION ALL
                    SELECT
                        NEW.password
                    UNION ALL
                    SELECT
                        NEW.display_name
                    UNION ALL
                    SELECT
                        NEW.title
                )
        )
    );

END;

-- */
-- Create trigger to log inventory deletions
-- /*
DROP TRIGGER IF EXISTS user_delete;

CREATE TRIGGER IF NOT EXISTS user_delete AFTER DELETE ON users FOR EACH ROW BEGIN
INSERT INTO
    user_change_events (user_id, username, change, old_values, new_values)
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
                        OLD.email
                    UNION ALL
                    SELECT
                        OLD.password
                    UNION ALL
                    SELECT
                        OLD.display_name
                    UNION ALL
                    SELECT
                        OLD.title
                )
        ),
        ''
    );

END;

-- */