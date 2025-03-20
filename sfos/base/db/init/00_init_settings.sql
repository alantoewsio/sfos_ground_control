-- Create licenses table
CREATE TABLE
    IF NOT EXISTS settings (
        key TEXT UNIQUE,
        value TEXT DEFAULT NULL        
    );