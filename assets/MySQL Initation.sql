CREATE DATABASE `revou_project` ;

USE revou_project

--user table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE,
    company_type VARCHAR(255),
    employer_name VARCHAR(255) UNIQUE,
    company_email VARCHAR(255) UNIQUE,
    address VARCHAR(255), 
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE about_company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES company(id),
    company_type VARCHAR(255),
    address VARCHAR(255),
    phonenumber VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    about_us VARCHAR(255),
    email VARCHAR(255),
);

CREATE TABLE about_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id),
    name VARCHAR(255) UNIQUE,
    about_user VARCHAR(255),
    phonenumber VARCHAR(20) UNIQUE,
    skill JSON,
    file_resume VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE post_job (
    id INT AUTO_INCREMENT PRIMARY KEY,
    about_company_id INT,
    FOREIGN KEY (about_company_id) REFERENCES about_company(id),
    job_name VARCHAR(255),
    job_description VARCHAR(255),
    post_until DATE,
    qualification JSON,
    benefit JSON,
    address_job VARCHAR(255),
	job_level ENUM('Entry-level', 'Intermediate', 'First-level management', 'Senior management') DEFAULT 'Entry-level',
    job_category VARCHAR(255),
    vacancy VARCHAR(255),
    educational_requirement VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);