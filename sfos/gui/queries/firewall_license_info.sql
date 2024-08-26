SELECT Setting,
    name as 'Subscription', 
    bundle as 'License Bundle', 
    status_description as 'Status', 
    start_date as 'Start', 
    expiry_date as 'Expiry'
FROM (SELECT 'Value' as Setting ) as Setting, license_view 
WHERE serial_number = ?