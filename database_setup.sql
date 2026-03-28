

CREATE DATABASE IF NOT EXISTS securecart_db;
USE securecart_db;


CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2),
    category VARCHAR(100),
    image VARCHAR(500),
    rating DECIMAL(3, 2) DEFAULT 4.5,
    stock INT DEFAULT 100,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_featured (featured)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    shipping DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_status (status),
    INDEX idx_email (email)
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id)
);

-- Sample Products
INSERT INTO products (name, description, price, original_price, category, image, rating, stock, featured) VALUES
('Wireless Headphones', 'Premium noise-cancelling wireless headphones with 30-hour battery life', 2999.00, 4999.00, 'electronics', '/static/images/headphones.jpg', 4.5, 50, TRUE),
('Smart Watch', 'Fitness tracker with heart rate monitor and GPS', 3499.00, 5999.00, 'electronics', '/static/images/smartwatch.jpg', 4.7, 30, TRUE),
('Cotton T-Shirt', 'Comfortable premium cotton t-shirt - Various colors', 499.00, 999.00, 'fashion', '/static/images/tshirt.jpg', 4.3, 100, TRUE),
('Running Shoes', 'Lightweight running shoes for athletes - Breathable mesh', 1999.00, 3499.00, 'sports', '/static/images/shoes.jpg', 4.6, 40, TRUE),
('Coffee Maker', 'Automatic coffee maker with timer and warming plate', 2499.00, 3999.00, 'home', '/static/images/coffee.jpg', 4.4, 25, TRUE),
('Face Cream', 'Anti-aging moisturizing face cream with SPF 30', 899.00, 1499.00, 'beauty', '/static/images/cream.jpg', 4.8, 60, TRUE),
('Bluetooth Speaker', 'Portable wireless speaker with bass boost - Waterproof', 1499.00, 2499.00, 'electronics', '/static/images/speaker.jpg', 4.5, 45, FALSE),
('Denim Jeans', 'Stretchable slim-fit denim jeans - Premium quality', 1299.00, 2199.00, 'fashion', '/static/images/jeans.jpg', 4.2, 80, FALSE),
('Yoga Mat', 'Non-slip exercise yoga mat - Extra thick cushioning', 799.00, 1299.00, 'sports', '/static/images/yoga.jpg', 4.4, 70, FALSE),
('Kitchen Knife Set', 'Professional stainless steel knife set - 5 pieces', 1899.00, 2999.00, 'home', '/static/images/knives.jpg', 4.6, 35, FALSE),
('Lipstick Set', 'Matte finish lipstick collection - 6 shades', 699.00, 1199.00, 'beauty', '/static/images/lipstick.jpg', 4.5, 90, FALSE),
('Fiction Novel', 'Bestselling mystery thriller novel - Hardcover edition', 299.00, 499.00, 'books', '/static/images/book.jpg', 4.7, 120, FALSE),
('Laptop Backpack', 'Water-resistant laptop backpack - Up to 15.6 inches', 1599.00, 2499.00, 'electronics', '/static/images/backpack.jpg', 4.6, 55, FALSE),
('Summer Dress', 'Floral print summer dress - Light and breezy', 1099.00, 1899.00, 'fashion', '/static/images/dress.jpg', 4.4, 65, FALSE),
('Dumbbell Set', 'Adjustable dumbbell set - 5kg to 25kg', 2999.00, 4499.00, 'sports', '/static/images/dumbbell.jpg', 4.5, 30, FALSE),
('Blender', '1000W high-speed blender - 3 speed settings', 2199.00, 3299.00, 'home', '/static/images/blender.jpg', 4.3, 40, FALSE),
('Hair Straightener', 'Ceramic hair straightener with temperature control', 1299.00, 2099.00, 'beauty', '/static/images/straightener.jpg', 4.6, 50, FALSE),
('Cookbook', 'International cuisine cookbook - 200+ recipes', 399.00, 699.00, 'books', '/static/images/cookbook.jpg', 4.5, 85, FALSE);

-- Verify data
SELECT 'Products inserted:' as Message, COUNT(*) as Count FROM products;
SELECT 'Database setup complete!' as Status;
