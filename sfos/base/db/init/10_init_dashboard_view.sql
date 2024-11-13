-- base/db/init/##_init_dashboard_view.sql
-- /*
DROP VIEW IF EXISTS inventory_dashboard;

CREATE VIEW
    IF NOT EXISTS inventory_dashboard AS
SELECT
    serial_number,
    status,
    address,
    model,
    version,
    company,
    error,
    last_Online,
    days_ago,
    fails,
    (
        SELECT
            IIF (
                l.bundle IN ('Base Firewall', 'a-la-carte'),
                l.name,
                l.bundle
            )
        FROM
            license_view l
        WHERE
            l.serial_number = i.serial_number
            AND l.remaining_days > -30
        ORDER BY
            l.remaining_days ASC
        LIMIT
            1
    ) AS 'next_license_expiring',
    (
        SELECT
            l.expiry_date
        FROM
            license_view l
        WHERE
            l.serial_number = i.serial_number
            AND l.remaining_days > -30
        ORDER BY
            l.remaining_days ASC
        LIMIT
            1
    ) AS 'expiry_date',
    (
        SELECT
            l.status_description
        FROM
            license_view l
        WHERE
            l.serial_number = i.serial_number
            AND l.remaining_days > -30
        ORDER BY
            l.remaining_days ASC
        LIMIT
            1
    ) AS 'license_status',
    (
        SELECT
            l.status
        FROM
            license_view l
        WHERE
            l.serial_number = i.serial_number
            AND l.name LIKE '%support%'
            AND l.remaining_days > -30
        ORDER BY
            l.remaining_days ASC
        LIMIT
            1
    ) AS 'support'
FROM
    inventory_view i;

-- */