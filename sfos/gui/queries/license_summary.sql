SELECT serial_number, companyName as company,
    (SELECT IIF(l.bundle IN ('Base Firewall', 'a-la-carte'), l.name, l.bundle)
        FROM license_view l 
        WHERE l.serial_number = i.serial_number AND l.remaining_days >-30
        ORDER BY l.remaining_days ASC
        LIMIT 1) AS 'expiring_next',
    (SELECT l.expiry_date
        FROM license_view l 
        WHERE l.serial_number = i.serial_number  AND l.remaining_days >-30
        ORDER BY l.remaining_days ASC
        LIMIT 1) AS 'expiry_date',
    (SELECT l.status_description
        FROM license_view l 
        WHERE l.serial_number = i.serial_number AND l.remaining_days >-30
       ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'days_remaining',
    (SELECT l.status 
        FROM license_view l 
        WHERE l.serial_number = i.serial_number AND l.name LIKE '%support%' AND l.remaining_days >-30
        ORDER BY l.remaining_days ASC
        LIMIT 1) AS 'support'
FROM inventory i