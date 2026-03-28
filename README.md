This proposal presents SecureCart, a full-stack e-commerce web application developed by Pavithra Devi, a BCA student. The project focuses on providing a secure and user-friendly platform for online product purchases. It demonstrates practical implementation of web development technologies and secure transaction handling. This work is submitted as part of academic requirements.


# 🛡️ SecureCart Marketplace

> A modern, secure e-commerce marketplace platform with premium dark theme design

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.14-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🛍️ **E-Commerce Core**

- Product catalog with categories
- Advanced search and filtering
- Shopping cart management
- Secure checkout process
- Order tracking and confirmation

### 🔒 **Security**

- SSL/TLS encryption
- PCI DSS compliant design
- Secure payment gateway integration
- Fraud protection
- Two-factor authentication ready

### 🎨 **Premium Design**

- Modern dark theme
- Glassmorphism effects
- Smooth animations
- Fully responsive (Mobile, Tablet, Desktop)
- Professional UI/UX

### 📱 **Pages Included**

1. **Home** - Hero section, categories, featured products
2. **Products** - Full catalog with search/filter
3. **Product Detail** - Reviews, ratings, image gallery
4. **Shopping Cart** - Cart management
5. **Checkout** - Secure payment flow
6. **Order Success** - Animated confirmation
7. **Login/Signup** - User authentication
8. **User Dashboard** - Profile, Orders, Settings
9. **Admin Dashboard** - Management panel
10. **Security** - Trust-building information

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.10+
- MySQL 8.0+
- pip (Python package manager)

### **Installation**

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/securecart-marketplace.git
cd securecart-marketplace
```

2. **Create virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure database**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your MySQL credentials
# DB_PASSWORD=your_mysql_password
```

5. **Run the application**

```bash
python app.py
```

6. **Access the application**

```
Open browser: http://localhost:5000
```

---

## 📁 Project Structure

```
securecart-marketplace/
├── templates/              # HTML pages
│   ├── index.html         # Home page
│   ├── products.html      # Product listing
│   ├── product-detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order-success.html
│   ├── login.html
│   ├── user-dashboard.html
│   ├── admin-dashboard.html
│   ├── profile.html
│   ├── orders.html
│   └── security.html
│
├── static/
│   ├── css/
│   │   └── style.css      # Premium Dark/Light Theme CSS
│   ├── js/
│   │   ├── main.js
│   │   ├── products.js
│   │   ├── product-detail.js
│   │   ├── cart.js
│   │   ├── checkout.js
│   │   ├── auth.js
│   │   ├── theme.js
│   │   └── order-success.js
│   └── images/
│
├── app.py                 # Flask application
├── auth.py                # Authentication logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore
├── Procfile              # Heroku deployment
├── runtime.txt           # Python version
└── README.md
```

---

## 🗄️ Database Schema

### **Tables**

**products**

- Product catalog with pricing, categories, ratings
- Discount support
- Stock management

**orders**

- Customer information
- Shipping details
- Payment tracking
- Order status

**order_items**

- Line items per order
- Product-order relationships

---

## 🔧 Configuration

### **Environment Variables**

Create `.env` file:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=securecart_db
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

### **Database Setup**

The application automatically:

- Creates database
- Creates tables
- Inserts sample data (12 products)

Manual setup (optional):

```bash
mysql -u root -p < database_setup.sql
```

---

## 🎨 Technology Stack

| Layer        | Technology                      |
| ------------ | ------------------------------- |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend**  | Python 3.14, Flask 3.0          |
| **Database** | MySQL 8.0                       |
| **Styling**  | Custom CSS (Dark/Light Themes)  |
| **Fonts**    | Google Fonts (Inter)            |

---

## 📊 API Endpoints

### **Products**

```
GET  /api/products              # List all products
GET  /api/products?category=X   # Filter by category
GET  /api/products?search=X     # Search products
GET  /api/products/<id>         # Get single product
```

### **Checkout**

```
POST /api/checkout              # Process order
```

### **Auth**

```
Post /api/auth/login            # Login
Post /api/auth/signup           # Signup
```

---

## 🚀 Deployment

### **Heroku**

```bash
heroku create your-app-name
heroku addons:create cleardb:ignite
git push heroku main
heroku open
```

### **Docker**

```bash
docker-compose up -d
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourname](https://github.com/yourname)
- Email: your.email@example.com

---

## 🌟 Star this repo if you find it helpful!

**Built with ❤️ using Flask and Python**

# screenshots 

<img width="1332" height="748" alt="Picture1" src="https://github.com/user-attachments/assets/fb8a3f9c-bcbd-4e4a-8828-240af7ee1dd6" />

<img width="1290" height="726" alt="Picture3" src="https://github.com/user-attachments/assets/2cdc6279-f1f6-43fd-9d0a-868bc48c94b4" />

<img width="1272" height="715" alt="Picture5" src="https://github.com/user-attachments/assets/26c84d5b-e77d-4e8f-bca5-777840842a0b" />

<img width="1272" height="715" alt="Picture4" src="https://github.com/user-attachments/assets/069174ff-4973-4559-a2e1-325e1b7b6434" />

<img width="1283" height="722" alt="Picture2" src="https://github.com/user-attachments/assets/76ce415f-3aee-4b78-b37c-7ef4f6a02fdd" />

