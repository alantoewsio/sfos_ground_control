SELECT serial_number, 
       IIF(active_days <0, 'FUTURE',IIF(remaining_days >=0, 'ACTIVE', 'EXPIRED')) AS status,
       IIF(active_days <0, 
        'Not valid for '|| -active_days||' days',IIF(remaining_days >=0, 
        'Valid for next '||remaining_days||' days', 
        'Expired '||-remaining_days||' days ago')) AS status_description,       
       active_days, 
       remaining_days,
       bundle,
       name,
       start_date,
       expiry_date,
       deactivation_reason,
       updated
FROM (
    SELECT serial_number, type, bundle, name,            
        start_date,
        expiry_date,
        deactivation_reason,
        CAST(min(julianday(current_timestamp),julianday(expiry_date))-julianday(start_date)  AS int) AS active_days,
        CAST(julianday(expiry_date) - julianday(current_timestamp) AS int) AS remaining_days,
        updated
    FROM licenses
    ORDER BY serial_number ASC, status ASC, remaining_days ASC
)
WHERE type IS NOT 'null' and serial_number IS NOT ''