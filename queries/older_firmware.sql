SELECT * FROM inventory where version not in (
    SELECT latest from (
        SELECT SUBSTRING(version, 1, 4) as major_ver, 
               MAX(version) as latest 
        FROM inventory where version is not null 
        GROUP BY major_ver 
        ORDER BY latest DESC 
        LIMIT 2
    )
)