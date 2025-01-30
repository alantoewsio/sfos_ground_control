-- base/db/init/##_init_license_view.sql
-- /*
DROP VIEW IF EXISTS license_view;

CREATE VIEW
    IF NOT EXISTS license_view AS
SELECT
    serial_number,
    IIF (
        active_days < 0,
        'FUTURE',
        IIF (remaining_days >= 0, 'ACTIVE', 'EXPIRED')
    ) AS status,
    IIF (
        active_days < 0,
        'Not valid for ' || - active_days || ' days',
        IIF (
            remaining_days >= 0,
            IIF (
                remaining_days > 90,
                'Active',
                'Expiring in ' || remaining_days || ' days'
            ),
            'Expired ' || - remaining_days || ' days ago'
        )
    ) AS status_description,
    active_days,
    remaining_days,
    bundle,
    name,
    start_date,
    expiry_date,
    deactivation_reason,
    updated
FROM
    (
        SELECT
            serial_number,
            type,
            bundle,
            name,
            strftime ('%Y-%m-%d', start_date) as 'start_date',
            strftime ('%Y-%m-%d', expiry_date) as 'expiry_date',
            deactivation_reason,
            CAST(
                min(
                    julianday (current_timestamp),
                    julianday (expiry_date)
                ) - julianday (start_date) AS int
            ) AS active_days,
            CAST(
                julianday (expiry_date) - julianday (current_timestamp) AS int
            ) AS remaining_days,
            strftime ('%Y-%m-%d %H:%M:%S', updated) as 'updated'
        FROM
            licenses
        ORDER BY
            serial_number ASC,
            status ASC,
            remaining_days ASC
    )
WHERE
    type IS NOT 'null'
    and serial_number IS NOT '';

-- */