
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify
import hashlib
import secrets

SECRET_KEY = secrets.token_hex(32)

USERS_DB = {
    'admin@securecart.com': {
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'name': 'Admin User',
        'role': 'admin',
        'phone': '+91 9999999999'
    },
    'manager@securecart.com': {
        'password': hashlib.sha256('manager123'.encode()).hexdigest(),
        'name': 'Store Manager',
        'role': 'manager',
        'phone': '+91 8888888888'
    },
    'user@securecart.com': {
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'John Doe',
        'role': 'user',
        'phone': '+91 7777777777'
    }
}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def authenticate_user(email, password):
    """Authenticate user and return user data if valid"""
    user = USERS_DB.get(email)
    if user and verify_password(password, user['password']):
        return {
            'email': email,
            'name': user['name'],
            'role': user['role'],
            'phone': user['phone']
        }
    return None

def register_user(email, password, name, phone=''):
    """Register new user (always creates 'user' role)"""
    if email in USERS_DB:
        return False, "Email already exists"
    
    USERS_DB[email] = {
        'password': hash_password(password),
        'name': name,
        'role': 'user',  # Default role
        'phone': phone
    }
    return True, "User registered successfully"

def login_required(f):
    """Decorator to protect routes - requires login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    """Decorator to protect routes - requires specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash('Please login to access this page', 'error')
                return redirect(url_for('login_page'))
            
            user_role = session['user'].get('role')
            if user_role not in allowed_roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current logged in user from session"""
    return session.get('user')

def is_authenticated():
    """Check if user is authenticated"""
    return 'user' in session

def get_redirect_for_role(role):
    """Get appropriate dashboard URL based on user role"""
    role_redirects = {
        'admin': '/admin-dashboard',
        'manager': '/manager-dashboard',
        'user': '/user-dashboard'
    }
    return role_redirects.get(role, '/')
