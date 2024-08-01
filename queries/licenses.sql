SELECT *, 
    CAST(julianday(expiry_date) - julianday(current_timestamp) AS int) AS ExpiryDays 
FROM licenses 
WHERE serial_number != '' 
