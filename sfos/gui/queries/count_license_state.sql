SELECT status, count(1) AS count 
FROM license_view 
GROUP BY status

