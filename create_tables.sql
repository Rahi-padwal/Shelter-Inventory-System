-- Pet Management System Database Schema
-- MySQL Database Creation Script

-- Create database
CREATE DATABASE IF NOT EXISTS pet_management;
USE pet_management;

-- Users table for authentication and role management
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role ENUM('admin', 'employee') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pets table for animal records
CREATE TABLE pets (
    pet_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_name VARCHAR(100) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    status ENUM('available', 'adopted', 'foster') DEFAULT 'available' NOT NULL,
    description TEXT,
    img_url VARCHAR(500),
    shelter_no VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Donations table for financial contributions
CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    purpose VARCHAR(200),
    donor_name VARCHAR(100) NOT NULL,
    donor_email VARCHAR(120) NOT NULL,
    donor_phone VARCHAR(20),
    message TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Adoptions table for pet adoptions
CREATE TABLE adoptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    adopt_name VARCHAR(100) NOT NULL,
    adopt_email VARCHAR(120) NOT NULL,
    adopt_phone VARCHAR(20),
    pet_id INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    address TEXT,
    user_id INT,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Medical records table for pet health tracking
CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    treatment_type VARCHAR(200) NOT NULL,
    treat_date DATE NOT NULL,
    donor_id INT,
    vaccines TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (donor_id) REFERENCES donations(id) ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX idx_pets_status ON pets(status);
CREATE INDEX idx_pets_created_at ON pets(created_at);
CREATE INDEX idx_donations_date ON donations(date);
CREATE INDEX idx_donations_user_id ON donations(user_id);
CREATE INDEX idx_adoptions_date ON adoptions(date);
CREATE INDEX idx_adoptions_user_id ON adoptions(user_id);
CREATE INDEX idx_adoptions_pet_id ON adoptions(pet_id);
CREATE INDEX idx_medical_records_pet_id ON medical_records(pet_id);
CREATE INDEX idx_medical_records_treat_date ON medical_records(treat_date);
CREATE INDEX idx_medical_records_donor_id ON medical_records(donor_id);

-- Sample data insertion
-- Insert sample users
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@petmanagement.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2a', 'admin'),
('employee1', 'employee1@petmanagement.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2a', 'employee'),
('employee2', 'employee2@petmanagement.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2a', 'employee');

-- Insert sample pets
INSERT INTO pets (pet_name, breed, age, gender, status, description, img_url, shelter_no) VALUES
('Buddy', 'Golden Retriever', 3, 'male', 'available', 'Friendly and energetic dog, great with kids', 'https://example.com/buddy.jpg', 'SH001'),
('Luna', 'Persian Cat', 2, 'female', 'available', 'Calm and gentle cat, perfect for apartment living', 'https://example.com/luna.jpg', 'SH002'),
('Max', 'German Shepherd', 5, 'male', 'adopted', 'Loyal and protective dog, needs experienced owner', 'https://example.com/max.jpg', 'SH003');

-- Insert sample donations
INSERT INTO donations (amount, purpose, donor_name, donor_email, donor_phone, message, user_id) VALUES
(100.00, 'General care', 'John Smith', 'john@example.com', '+1234567890', 'Happy to help the animals', 2),
(250.50, 'Medical treatment', 'Jane Doe', 'jane@example.com', '+1987654321', 'For medical expenses', 3);

-- Insert sample adoption
INSERT INTO adoptions (adopt_name, adopt_email, adopt_phone, pet_id, address, user_id) VALUES
('Mike Johnson', 'mike@example.com', '+1122334455', 3, '123 Main St, City, State 12345', 2);

-- Insert sample medical records
INSERT INTO medical_records (pet_id, treatment_type, treat_date, donor_id, vaccines, description) VALUES
(1, 'Vaccination', '2024-01-15', 1, 'Rabies, DHPP', 'Annual vaccination checkup'),
(2, 'Spay surgery', '2024-01-20', 2, 'None', 'Spay surgery performed successfully');

-- Note: Default password for all users is 'password123'
-- In production, use proper password hashing
