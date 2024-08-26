SELECT (SELECT l.status
     FROM license_view l 
     WHERE l.serial_number = i.serial_number 
       AND l.name LIKE '%support%'
       AND l.remaining_days >-30       
     ORDER BY l.remaining_days ASC
     LIMIT 1) AS 'status',
     count(1) as count
FROM inventory i
GROUP BY status