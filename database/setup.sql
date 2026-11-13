-- ==========================================
-- PENNYPILOT DATABASE SETUP
-- ==========================================

-- 1. Create database
CREATE DATABASE IF NOT EXISTS pennypilot_db;

USE pennypilot_db;


-- ==========================================
-- 2. USERS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- 3. CATEGORIES TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_type ENUM('INCOME', 'EXPENSE') NOT NULL
);


-- ==========================================
-- 4. TRANSACTIONS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    category_id INT NOT NULL,

    amount DECIMAL(12,2) NOT NULL,

    transaction_type ENUM('INCOME', 'EXPENSE') NOT NULL,

    description VARCHAR(255),

    transaction_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transaction_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_transaction_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id),

    CONSTRAINT chk_transaction_amount
        CHECK (amount > 0)
);


-- ==========================================
-- 5. INSERT DEFAULT CATEGORIES
-- ==========================================

INSERT INTO categories (category_name, category_type)
SELECT 'Salary', 'INCOME'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Salary'
      AND category_type = 'INCOME'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Freelancing', 'INCOME'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Freelancing'
      AND category_type = 'INCOME'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Business', 'INCOME'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Business'
      AND category_type = 'INCOME'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Investments', 'INCOME'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Investments'
      AND category_type = 'INCOME'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Other Income', 'INCOME'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Other Income'
      AND category_type = 'INCOME'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Food', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Food'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Travel', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Travel'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Shopping', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Shopping'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Bills', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Bills'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Education', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Education'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Entertainment', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Entertainment'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Healthcare', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Healthcare'
      AND category_type = 'EXPENSE'
);

INSERT INTO categories (category_name, category_type)
SELECT 'Other Expense', 'EXPENSE'
WHERE NOT EXISTS (
    SELECT 1 FROM categories
    WHERE category_name = 'Other Expense'
      AND category_type = 'EXPENSE'
);


-- ==========================================
-- 6. VERIFY DATABASE
-- ==========================================

SHOW TABLES;

SELECT * FROM categories;