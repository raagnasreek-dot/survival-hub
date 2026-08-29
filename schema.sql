CREATE DATABASE IF NOT EXISTS survival_hub;
USE survival_hub;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS food_centers (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    center_name VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7)
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    contact VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_name VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7)
);

CREATE TABLE IF NOT EXISTS schemes (
    scheme_id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_name VARCHAR(200) NOT NULL,
    description TEXT,
    eligibility TEXT,
    apply_location VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS saved_items (
    saved_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_type VARCHAR(30) NOT NULL,
    item_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_saved_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE
);

INSERT INTO food_centers (center_name, location, phone, latitude, longitude)
SELECT 'Community Food Center', 'Abids, Hyderabad', '9000000001', 17.3890, 78.4867
WHERE NOT EXISTS (SELECT 1 FROM food_centers);

INSERT INTO jobs (job_title, company, location, contact)
SELECT 'Office Assistant', 'Local Employment Center', 'Secunderabad', '9000000002'
WHERE NOT EXISTS (SELECT 1 FROM jobs);

INSERT INTO hospitals (hospital_name, location, phone, latitude, longitude)
SELECT 'Government Hospital', 'Koti, Hyderabad', '9000000003', 17.3840, 78.4860
WHERE NOT EXISTS (SELECT 1 FROM hospitals);

INSERT INTO schemes (scheme_name, description, eligibility, apply_location)
SELECT 'Government Welfare Scheme', 'Support and welfare assistance for eligible citizens.', 'Eligibility depends on the scheme.', 'Nearest MeeSeva / government office'
WHERE NOT EXISTS (SELECT 1 FROM schemes);
