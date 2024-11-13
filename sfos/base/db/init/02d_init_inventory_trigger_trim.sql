DROP TRIGGER IF EXISTS trim_inventory_events_history;

CREATE TRIGGER IF NOT EXISTS trim_inventory_events_history AFTER INSERT ON inventory_events BEGIN
DELETE FROM inventory_events WHERE id NOT IN (SELECT id FROM inventory_events ORDER BY change_timestamp DESC LIMIT 100000);