SELECT 
    i.*, 
    (SELECT IIF(l.bundle IN ('Base Firewall', 'a-la-carte'), l.name, l.bundle)
     FROM license_view l 
     WHERE l.serial_number = i.serial_number 
       AND l.remaining_days >-30
       ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'Next Expiry',
    (SELECT l.expiry_date
     FROM license_view l 
     WHERE l.serial_number = i.serial_number 
       AND l.remaining_days >-30
       ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'Expiry Date',
    (SELECT l.status_description
     FROM license_view l 
     WHERE l.serial_number = i.serial_number 
       AND l.remaining_days >-30
       ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'Time Remaining',
    (SELECT l.status_description 
     FROM license_view l 
     WHERE l.serial_number = i.serial_number 
       AND l.name LIKE '%support%'
       AND l.remaining_days >-30
       ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'Support'
FROM 
    inventory i;