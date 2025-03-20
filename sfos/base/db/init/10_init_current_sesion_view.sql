-- base/db/init/##_init_inventory_view.sql
-- Create an inventory view that adds date calculations to the last seen date
DROP VIEW IF EXISTS current_Session_view;

-- /*
CREATE VIEW
    IF NOT EXISTS current_Session_view AS
SELECT
    address,
    serial_number,
    model,
    displayVersion as 'version',
    companyName as 'company',
    message as 'error',
    last_result as 'status',
    strftime ('%Y-%m-%d %H:%M:%S', last_seen) as 'last_online',
    Cast(
        (
            strftime ('%j', current_timestamp) - strftime ('%j', last_seen)
        ) * 24 * 60 As Integer
    ) as 'mins_ago',
    CAST(
        strftime ('%j', current_timestamp) - strftime ('%j', last_seen) AS INT
    ) as 'days_ago',
    consecutive_fails as fails
FROM
    inventory
WHERE session_id = (
    SELECT value 
    FROM settings 
    WHERE key='current_session_id')
ORDER BY
    'last_online' ASC NULLS FIRST,
    Status;

--*/