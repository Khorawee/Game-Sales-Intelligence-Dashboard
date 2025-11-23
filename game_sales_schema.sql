-- =====================================================
--  GAME SALES DATABASE SCHEMA (FULLY NORMALIZED 3NF)
-- =====================================================

CREATE DATABASE IF NOT EXISTS game_sales
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE game_sales;

-- =====================================================
--  DROP OLD TABLES & VIEWS
-- =====================================================

-- Drop views first (views cannot be dropped by DROP TABLE)
DROP VIEW IF EXISTS view_sales_year;
DROP VIEW IF EXISTS view_sales_platform;
DROP VIEW IF EXISTS view_sales_genre;

-- Drop tables in correct FK order
DROP TABLE IF EXISTS prediction_log;
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS vgsales;
DROP TABLE IF EXISTS model_info;
DROP TABLE IF EXISTS platform;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS publisher;

-- =====================================================
--  DIMENSION TABLES (Normalized)
-- =====================================================

CREATE TABLE platform (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE genre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE publisher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- =====================================================
--  FACT TABLE: VG SALES (Fully Normalized)
-- =====================================================

CREATE TABLE vgsales (
    id INT AUTO_INCREMENT PRIMARY KEY,

    `Rank` INT,
    game_name VARCHAR(255) NOT NULL,

    platform_id INT NOT NULL,
    genre_id INT NOT NULL,
    publisher_id INT NOT NULL,

    Year INT NOT NULL CHECK (Year >= 1970 AND Year <= 2050),

    NA_Sales DOUBLE DEFAULT 0,
    EU_Sales DOUBLE DEFAULT 0,
    JP_Sales DOUBLE DEFAULT 0,
    Other_Sales DOUBLE DEFAULT 0,

    Global_Sales DOUBLE DEFAULT 0 CHECK (Global_Sales >= 0),

    -- Prevent duplicate games on the same platform & year
    UNIQUE KEY uq_game (game_name, platform_id, Year),

    -- Index for analytics
    INDEX idx_platform_year (platform_id, Year),
    INDEX idx_genre_year (genre_id, Year),
    INDEX idx_year (Year),

    FOREIGN KEY (platform_id) REFERENCES platform(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(id)
);

-- =====================================================
--  PREDICTION RESULTS
-- =====================================================

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,

    game_name VARCHAR(255),
    platform VARCHAR(50),
    genre VARCHAR(50),
    publisher VARCHAR(100),
    Year INT,

    NA_Sales DOUBLE DEFAULT 0,
    EU_Sales DOUBLE DEFAULT 0,
    JP_Sales DOUBLE DEFAULT 0,
    Other_Sales DOUBLE DEFAULT 0,

    Predicted_Sales DOUBLE,
    Predicted_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
--  MODEL PERFORMANCE INFORMATION
-- =====================================================

CREATE TABLE model_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50),
    rmse DOUBLE,
    r2 DOUBLE,
    best_params JSON,
    saved_path VARCHAR(255),
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
--  ANALYTIC VIEWS
-- =====================================================

CREATE VIEW view_sales_year AS
SELECT Year, SUM(Global_Sales) AS Total_Sales
FROM vgsales
GROUP BY Year;

CREATE VIEW view_sales_platform AS
SELECT p.name AS Platform, SUM(v.Global_Sales) AS Total_Sales
FROM vgsales v
JOIN platform p ON v.platform_id = p.id
GROUP BY p.name;

CREATE VIEW view_sales_genre AS
SELECT g.name AS Genre, SUM(v.Global_Sales) AS Total_Sales
FROM vgsales v
JOIN genre g ON v.genre_id = g.id
GROUP BY g.name;

-- =====================================================
--  PREDICTION LOG TRIGGER
-- =====================================================

CREATE TABLE prediction_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id INT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER trg_after_prediction_insert
AFTER INSERT ON predictions
FOR EACH ROW
BEGIN
    INSERT INTO prediction_log (prediction_id)
    VALUES (NEW.id);
END $$

DELIMITER ;