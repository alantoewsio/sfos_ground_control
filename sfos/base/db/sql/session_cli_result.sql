-- base/db/sql/dashboard.sql
SELECT address, status, error as "last error message", last_online as "Last successuful update" from current_session_view