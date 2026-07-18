CREATE DATABASE IF NOT EXISTS capstone_db;
USE capstone_db;


-- Table: Customers (Isolates PII - Personally Identifiable Information)
CREATE TABLE IF NOT EXISTS customers (
    Customer_ID VARCHAR(50) PRIMARY KEY,
    Customer_Name VARCHAR(100) NOT NULL,
    Segment VARCHAR(50)
);

-- Table: Locations (Reduces geographic data redundancy)
CREATE TABLE IF NOT EXISTS locations (
    Postal_Code VARCHAR(20) PRIMARY KEY,
    Country VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Region VARCHAR(50)
);

-- Table: Products (Standardizes inventory data)
CREATE TABLE IF NOT EXISTS products (
    Product_ID VARCHAR(50) PRIMARY KEY,
    Category VARCHAR(50) NOT NULL,
    Sub_Category VARCHAR(50),
    Product_Name VARCHAR(255) NOT NULL
);

-- Table: Orders (Transactional header linking entities)
CREATE TABLE IF NOT EXISTS orders (
    Order_ID VARCHAR(50) PRIMARY KEY,
    Order_Date DATE NOT NULL,
    Ship_Date DATE,
    Ship_Mode VARCHAR(50),
    Customer_ID VARCHAR(50) NOT NULL,
    Postal_Code VARCHAR(20),
    FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID),
    FOREIGN KEY (Postal_Code) REFERENCES locations(Postal_Code)
);

-- Table: Order Details (Granular financial metrics)
CREATE TABLE IF NOT EXISTS order_details (
    Row_ID INT PRIMARY KEY,
    Order_ID VARCHAR(50) NOT NULL,
    Product_ID VARCHAR(50) NOT NULL,
    Sales DECIMAL(10, 2) DEFAULT 0.00,
    Quantity INT DEFAULT 1,
    Discount DECIMAL(4, 2) DEFAULT 0.00,
    Profit DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID),
    FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);


-- These indexes ensure Llama 3 / Gemini get data instantly without timeouts.
CREATE INDEX idx_customer_segment ON customers(Segment);
CREATE INDEX idx_location_region ON locations(Region);
CREATE INDEX idx_location_city ON locations(City);
CREATE INDEX idx_product_category ON products(Category);
CREATE INDEX idx_order_date ON orders(Order_Date);
CREATE INDEX idx_details_order_id ON order_details(Order_ID);
CREATE INDEX idx_details_product_id ON order_details(Product_ID);


-- Create the restricted user for the Python AI Agent
CREATE USER IF NOT EXISTS 'ai_agent_user'@'%' IDENTIFIED BY 'ai_password_123';

-- Grant STRICTLY Read-Only access. No INSERT, UPDATE, DELETE, or DROP allowed.
GRANT SELECT ON capstone_db.* TO 'ai_agent_user'@'%';

-- Reload privileges to ensure security rules apply immediately
FLUSH PRIVILEGES;