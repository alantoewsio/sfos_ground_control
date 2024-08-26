-- base/db/sql/init_views.sql

-- Create an inventory view that adds date calculations to the last seen date
DROP VIEW IF EXISTS inventory_view;
DROP VIEW IF EXISTS license_view;
DROP VIEW IF EXISTS inventory_dashboard;

-- /*
CREATE VIEW IF NOT EXISTS inventory_view AS
SELECT address,
    serial_number,
    model,
    displayVersion as 'version',
    companyName as 'company',
    message as 'error',
    last_result as 'status',
    strftime('%Y-%m-%d %H:%M:%S', last_seen) as 'last_online',
    Cast ((strftime('%j',current_timestamp) - strftime('%j',last_seen)) * 24 * 60 As Integer) as 'mins_ago',
    CAST (strftime('%j',current_timestamp) - strftime('%j',last_seen) AS INT) as 'days_ago',
    consecutive_fails as fails
FROM inventory
ORDER BY 'last_online' ASC NULLS FIRST, Status;
--*/

-- Create a licensing file view that adds date calculations


-- /*
CREATE VIEW IF NOT EXISTS license_view AS
SELECT serial_number, 
       IIF(active_days <0, 'FUTURE',IIF(remaining_days >=0, 'ACTIVE', 'EXPIRED')) AS status,
       IIF(active_days <0, 
        'Not valid for '|| -active_days||' days',
        IIF(remaining_days >=0, 
            IIF(remaining_days > 90, 
            'Active',
            'Expiring in '||remaining_days||' days'),          
        'Expired '||-remaining_days||' days ago')) AS status_description,       
       active_days, 
       remaining_days,
       bundle,
       name,
       start_date,
       expiry_date,
       deactivation_reason,
       updated
FROM (
    SELECT serial_number, type, bundle, name,            
        start_date,
        expiry_date,
        deactivation_reason,
        CAST(min(julianday(current_timestamp),julianday(expiry_date))-julianday(start_date)  AS int) AS active_days,
        CAST(julianday(expiry_date) - julianday(current_timestamp) AS int) AS remaining_days,
        updated
    FROM licenses
    ORDER BY serial_number ASC, status ASC, remaining_days ASC
)
WHERE type IS NOT 'null' and serial_number IS NOT '';
-- */


-- /*
CREATE VIEW IF NOT EXISTS inventory_dashboard AS
SELECT serial_number, status, address, model, version, company, error, last_Online, days_ago, fails,
    (SELECT IIF(l.bundle IN ('Base Firewall', 'a-la-carte'), l.name, l.bundle)
        FROM license_view l 
        WHERE l.serial_number = i.serial_number AND l.remaining_days >-30
        ORDER BY l.remaining_days ASC
        LIMIT 1) AS 'next_license_expiring',
    (SELECT l.expiry_date
        FROM license_view l 
        WHERE l.serial_number = i.serial_number  AND l.remaining_days >-30
        ORDER BY l.remaining_days ASC
        LIMIT 1) AS 'expiry_date',
    (SELECT l.status_description
        FROM license_view l 
        WHERE l.serial_number = i.serial_number AND l.remaining_days >-30
       ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'license_status',
    (SELECT l.status 
        FROM license_view l 
        WHERE l.serial_number = i.serial_number AND l.name LIKE '%support%' AND l.remaining_days >-30
        ORDER BY l.remaining_days ASC
        LIMIT 1) AS 'support'
FROM inventory_view i;
-- */