-- 1. Create the database
CREATE DATABASE IF NOT EXISTS stock_analysis;
USE stock_analysis;

-- 2. Create stock_data table
CREATE TABLE IF NOT EXISTS stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    symbol VARCHAR(20),
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    INDEX(symbol),
    INDEX(date)
);

-- 3. Create sector_data table
CREATE TABLE IF NOT EXISTS sector_data (
    symbol VARCHAR(20) PRIMARY KEY,
    sector VARCHAR(50),
    company VARCHAR(50)
);

-- 4. Sample sector data insert (replace with your actual sector data)
INSERT INTO sector_data (symbol, sector) VALUES
    ('AAPL', 'Technology'),
    ('MSFT', 'Technology'),
    ('JPM', 'Financial');