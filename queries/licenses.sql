SELECT serial_number as 'Serial Number', name as 'Name', bundle as 'Bundle', status as 'Status', 
    start_date as 'Start', expiry_date, 'Expiry', 
    CAST(julianday(expiry_date) - julianday(current_timestamp) AS int) AS ExpiryDays,
    updated as 'Last Checked'
FROM licenses 
WHERE serial_number != '' 
