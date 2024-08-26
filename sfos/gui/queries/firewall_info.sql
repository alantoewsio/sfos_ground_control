SELECT Setting, 
    serial_number as 'Serial Number',
    address as 'Address', 
    model as 'Model', 
    version as 'Firmware Version', 
    company as 'Company', 
    status as 'Status', 
    last_online ||' ('||days_ago||' days ago)' as 'Last Contacted', 
    error as 'Failure Reason',
    fails as 'Failed Attempts'
FROM (SELECT 'Value' as Setting ) as Setting, 
    inventory_view 
WHERE serial_number = ?
