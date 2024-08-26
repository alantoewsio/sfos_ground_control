SELECT 
    change_timestamp as 'Timestamp',
    source as 'Source',
    changed_fields as 'Change', 
    old_values as 'Original',
    new_values as 'New Values'    
FROM events
WHERE serial_number = ?