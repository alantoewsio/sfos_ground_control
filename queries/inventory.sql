SELECT address as Address,
    serial_number as 'Serial Number',
    model as Model,
    displayVersion as Version,
    companyName as Company,
    message as 'Error Message',
    last_result as Status,
    strftime('%Y-%m-%d %H:%M:%S', last_seen) as 'Last Seen Date' ,
    CAST (strftime('%j',current_timestamp) - strftime('%j',last_seen) AS INT) as 'Days Ago' 
FROM inventory
ORDER BY 'Last Seen Date' ASC NULLS FIRST, Status