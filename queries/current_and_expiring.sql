SELECT serial_number, status,
    MAX(CASE WHEN bundle != 'a-la-carte' THEN bundle END) AS Bundle, 
    MIN(CASE WHEN bundle != 'a-la-carte' THEN expiry_date END) AS BundleExpiry, 
    COUNT(CASE WHEN bundle = 'a-la-carte' THEN expiry_date END) AS 'A-la-Carte Subs',
    MIN(CASE WHEN bundle = 'a-la-carte' THEN expiry_date END) AS 'Next A-la-Carte Expiry',    
    ExpiryDays
FROM (
    SELECT *, 
        CAST(julianday(expiry_date) - julianday(current_timestamp) AS int) AS ExpiryDays 
    FROM licenses 
    WHERE serial_number != '' 
        AND status != 'INACTIVE' 
        AND ExpiryDays > -30
    )    
GROUP BY serial_number
ORDER BY ExpiryDays ASC

