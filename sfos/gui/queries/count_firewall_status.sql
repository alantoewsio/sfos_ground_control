SELECT status as status, count(1) AS count 
FROM inventory_view 
GROUP BY Status
ORDER BY status DESC
