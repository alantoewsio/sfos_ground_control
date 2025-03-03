-- Drop existing triggers so they are created up-to-date
DROP TRIGGER IF EXISTS log_inventory_updates;

CREATE TRIGGER log_inventory_updates 
  AFTER UPDATE ON inventory FOR EACH ROW 
BEGIN
  INSERT INTO
    inventory_events (
      serial_number,
      address,
      changed_fields,
      old_values,
      new_values
    )
  VALUES
    (
      OLD.serial_number,
      OLD.address,
      (
        SELECT GROUP_CONCAT (name, ', ')
        FROM
          (
            SELECT 'model' AS name WHERE OLD.model != NEW.model UNION ALL
            SELECT 'displayVersion' WHERE OLD.displayVersion != NEW.displayVersion UNION ALL
            SELECT 'version' WHERE OLD.version != NEW.version UNION ALL
            SELECT 'serial_number' WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT 'companyName' WHERE OLD.companyName != NEW.companyName UNION ALL
            SELECT 'username' WHERE OLD.username != NEW.username UNION ALL
            SELECT 'verify_tls' WHERE OLD.verify_tls != NEW.verify_tls UNION ALL
            SELECT 'message' WHERE OLD.message != NEW.message UNION ALL
            SELECT 'last_result' WHERE OLD.last_result != NEW.last_result
          )
      ),
      (
        SELECT GROUP_CONCAT (value, ', ')
        FROM
          (
            SELECT OLD.model AS value WHERE OLD.model != NEW.model UNION ALL
            SELECT OLD.displayVersion WHERE OLD.displayVersion != NEW.displayVersion UNION ALL
            SELECT OLD.version WHERE OLD.version != NEW.version UNION ALL
            SELECT OLD.serial_number WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT OLD.companyName WHERE OLD.companyName != NEW.companyName UNION ALL
            SELECT OLD.username WHERE OLD.username != NEW.username UNION ALL
            SELECT OLD.verify_tls WHERE OLD.verify_tls != NEW.verify_tls UNION ALL
            SELECT OLD.message WHERE OLD.message != NEW.message UNION ALL
            SELECT OLD.last_result WHERE OLD.last_result != NEW.last_result 
          )
      ),
      (
        SELECT GROUP_CONCAT (value, ', ')
        FROM
          (
            SELECT NEW.model AS value WHERE OLD.model != NEW.model UNION ALL
            SELECT NEW.displayVersion WHERE OLD.displayVersion != NEW.displayVersion UNION ALL
            SELECT NEW.version WHERE OLD.version != NEW.version UNION ALL
            SELECT NEW.serial_number WHERE OLD.serial_number != NEW.serial_number UNION ALL
            SELECT NEW.companyName WHERE OLD.companyName != NEW.companyName UNION ALL
            SELECT NEW.username WHERE OLD.username != NEW.username UNION ALL
            SELECT NEW.verify_tls WHERE OLD.verify_tls != NEW.verify_tls UNION ALL
            SELECT NEW.message WHERE OLD.message != NEW.message UNION ALL
            SELECT NEW.last_result WHERE OLD.last_result != NEW.last_result 
          )
      )
    );