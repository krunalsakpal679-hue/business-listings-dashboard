-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS business_listings_db;
USE business_listings_db;

-- Drop table if exists to allow clean re-runs of schema.sql
DROP TABLE IF EXISTS listing_master;

-- Create listing_master Table
CREATE TABLE listing_master (
    id INT PRIMARY KEY AUTO_INCREMENT,
    business_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(500),
    phone VARCHAR(20),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add performance indexes for aggregation queries
CREATE INDEX idx_listing_city ON listing_master(city);
CREATE INDEX idx_listing_category ON listing_master(category);
CREATE INDEX idx_listing_source ON listing_master(source);
