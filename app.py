from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

from auth import (
    authenticate_user, register_user, login_required, role_required,
    get_current_user, is_authenticated, get_redirect_for_role, SECRET_KEY
)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', SECRET_KEY)  # For session management
CORS(app)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Pavi@123'),  # Update with your MySQL password
    'database': os.getenv('DB_NAME', 'securecart_db')
}

def get_db_connection():
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        cursor.execute("""
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id VARCHAR(50) NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                quantity INT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)
        
        connection.commit()
        print("✅ Database initialized successfully!")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📦 Inserting sample products...")
            sample_products = [
                ('Wireless Headphones', 'Premium noise-cancelling wireless headphones', 2999.00, 4999.00, 'electronics', '/static/images/headphones.jpg', 4.5, 50, True),
                ('Smart Watch', 'Fitness tracker with heart rate monitor', 3499.00, 5999.00, 'electronics', '/static/images/smartwatch.jpg', 4.7, 30, True),
                ('Cotton T-Shirt', 'Comfortable premium cotton t-shirt', 499.00, 999.00, 'fashion', '/static/images/tshirt.jpg', 4.3, 100, True),
                ('Running Shoes', 'Lightweight running shoes for athletes', 1999.00, 3499.00, 'sports', '/static/images/shoes.jpg', 4.6, 40, True),
                ('Coffee Maker', 'Automatic coffee maker with timer', 2499.00, 3999.00, 'home', '/static/images/coffee.jpg', 4.4, 25, True),
                ('Face Cream', 'Anti-aging moisturizing face cream', 899.00, 1499.00, 'beauty', '/static/images/cream.jpg', 4.8, 60, True),
                ('Bluetooth Speaker', 'Portable wireless speaker with bass boost', 1499.00, 2499.00, 'electronics', '/static/images/speaker.jpg', 4.5, 45, False),
                ('Denim Jeans', 'Stretchable slim-fit denim jeans', 1299.00, 2199.00, 'fashion', '/static/images/jeans.jpg', 4.2, 80, False),
                ('Yoga Mat', 'Non-slip exercise yoga mat', 799.00, 1299.00, 'sports', '/static/images/yoga.jpg', 4.4, 70, False),
                ('Kitchen Knife Set', 'Professional stainless steel knife set', 1899.00, 2999.00, 'home', '/static/images/knives.jpg', 4.6, 35, False),
                ('Lipstick Set', 'Matte finish lipstick collection', 699.00, 1199.00, 'beauty', '/static/images/lipstick.jpg', 4.5, 90, False),
                ('Fiction Novel', 'Bestselling mystery thriller novel', 299.00, 499.00, 'books', '/static/images/book.jpg', 4.7, 120, False),
            ]
            
            cursor.executemany("""
                INSERT INTO products (name, description, price, original_price, category, image, rating, stock, featured)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_products)
            
            connection.commit()
            print("✅ Sample products inserted!")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error initializing database: {e}")


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/products')
def products_page():
    """Products listing page"""
    return render_template('products.html')

@app.route('/cart')
def cart_page():
    """Shopping cart page"""
    return render_template('cart.html')

@app.route('/checkout')
def checkout_page():
    """Checkout page"""
    return render_template('checkout.html')

@app.route('/product-detail')
def product_detail_page():
    """Product detail page"""
    return render_template('product-detail.html')

@app.route('/login')
def login_page():
    """Login/Signup page"""
    return render_template('login.html')

@app.route('/order-success')
def order_success_page():
    """Order success page"""
    return render_template('order-success.html')

@app.route('/security')
def security_page():
    """Security information page"""
    return render_template('security.html')

@app.route('/user-dashboard')
@login_required
def user_dashboard():
    """User dashboard page - requires login"""
    user = get_current_user()
    return render_template('user-dashboard.html', user=user)

@app.route('/admin-dashboard')
@role_required(['admin'])
def admin_dashboard():
    """Admin dashboard page - requires admin role"""
    user = get_current_user()
    return render_template('admin-dashboard.html', user=user)

@app.route('/manager-dashboard')
@role_required(['manager', 'admin'])
def manager_dashboard():
    """Store manager dashboard page - requires manager or admin role"""
    user = get_current_user()
    return render_template('manager-dashboard.html', user=user)






@app.route('/user/profile')
@login_required
def user_profile():
    """User profile settings page"""
    user = get_current_user()
    return render_template('profile.html', user=user)

@app.route('/user/orders')
@login_required
def user_orders():
    """User order history page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login_page'))
        
    email = user.get('email')
    orders = []
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Fetch orders for this email
            cursor.execute("SELECT * FROM orders WHERE email = %s ORDER BY created_at DESC", (email,))
            orders = cursor.fetchall() or []
            
            # Fetch items for each order
            for order in orders:
                cursor.execute("SELECT name, quantity, price FROM order_items WHERE order_id = %s", (order['order_id'],))
                items = cursor.fetchall()
                order['items'] = items if items else []
                
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching orders: {e}")
        
    return render_template('orders.html', user=user, orders=orders)


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle user login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        user = authenticate_user(email, password)
        
        if user:
            session['user'] = user
            session.permanent = True
            
            redirect_url = get_redirect_for_role(user['role'])
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                },
                'redirect': redirect_url
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """Handle user registration"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')
        
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        success, message = register_user(email, password, name, phone)
        
        if success:
            user = authenticate_user(email, password)
            if user:
                session['user'] = user
                session.permanent = True
                
                return jsonify({
                    'success': True,
                    'message': 'Account created successfully',
                    'user': {
                        'name': user['name'],
                        'email': user['email'],
                        'role': user['role']
                    },
                    'redirect': get_redirect_for_role(user['role'])
                }), 200
        
        return jsonify({'success': False, 'message': message}), 400
        
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """Handle user logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/auth/current-user', methods=['GET'])
def api_current_user():
    """Get current logged in user"""
    if is_authenticated():
        return jsonify({
            'success': True,
            'user': get_current_user()
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products or filtered products"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        category = request.args.get('category')
        search = request.args.get('search')
        featured = request.args.get('featured')
        limit = request.args.get('limit')
        
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if category and category != 'all':
            query += " AND category = %s"
            params.append(category)
        
        if search:
            query += " AND (name LIKE %s OR description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        if featured == 'true':
            query += " AND featured = TRUE"
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += f" LIMIT {int(limit)}"
        
        cursor.execute(query, params)
        products = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        for product in products:
            product['price'] = float(product['price'])
            product['original_price'] = float(product['original_price']) if product['original_price'] else float(product['price'])
            product['rating'] = float(product['rating']) if product['rating'] else 4.5
        
        return jsonify(products)
        
    except Error as e:
        print(f"Error fetching products: {e}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if product:
            product['price'] = float(product['price'])
            product['original_price'] = float(product['original_price']) if product['original_price'] else float(product['price'])
            product['rating'] = float(product['rating']) if product['rating'] else 4.5
            return jsonify(product)
        else:
            return jsonify({'error': 'Product not found'}), 404
            
    except Error as e:
        print(f"Error fetching product: {e}")
        return jsonify({'error': 'Failed to fetch product'}), 500

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout and create order"""
    try:
        data = request.json
        
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO orders (order_id, customer_name, email, phone, address, city, state, pincode,
                              payment_method, subtotal, shipping, tax, total, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            order_id,
            data['fullName'],
            data['email'],
            data['phone'],
            data['address'],
            data['city'],
            data['state'],
            data['pincode'],
            data['paymentMethod'],
            data['subtotal'],
            data['shipping'],
            data['tax'],
            data['total'],
            'completed'  # In production, this would be 'pending' until payment confirmation
        ))
        
        for item in data['items']:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, price, quantity)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                order_id,
                item['id'],
                item['name'],
                item['price'],
                item['quantity']
            ))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'orderId': order_id,
            'message': 'Order placed successfully!'
        })
        
    except Error as e:
        print(f"Error processing checkout: {e}")
        return jsonify({'success': False, 'message': 'Failed to process order'}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n🚀 Starting SecureCart Marketplace...")
    print("📊 Initializing database...\n")
    
    init_database()
    
    print("\n🌐 Server starting on http://localhost:5000")
    print("✨ SecureCart Marketplace is ready!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
