import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE = 'agrigenius.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            state TEXT,
            district TEXT,
            latitude REAL,
            longitude REAL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Contact submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User activity log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feature TEXT NOT NULL,
            query_data TEXT,
            result_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Prediction history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            prediction_type TEXT NOT NULL,
            input_data TEXT,
            output_data TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@agrigenius.com', admin_hash, 'Administrator', 1))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# User management functions
def create_user(username, email, password, full_name=None, phone=None):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, phone))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        conn.close()
        return {'success': False, 'error': 'Username or email already exists'}

def verify_user(username, password):
    """Verify user credentials"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def update_user_location(user_id, latitude, longitude, state=None, district=None):
    """Update user location"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users 
        SET latitude = ?, longitude = ?, state = ?, district = ?
        WHERE id = ?
    ''', (latitude, longitude, state, district, user_id))
    conn.commit()
    conn.close()

def update_last_login(user_id):
    """Update last login timestamp"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    """Get all users (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, full_name, phone, state, district, created_at, last_login FROM users WHERE is_admin = 0')
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]

def delete_user(user_id):
    """Delete user (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ? AND is_admin = 0', (user_id,))
    conn.commit()
    conn.close()

# Contact form functions
def create_contact_submission(name, email, subject, message):
    """Create contact form submission"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contact_submissions (name, email, subject, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, subject, message))
    conn.commit()
    conn.close()
    return {'success': True}

def get_all_contacts():
    """Get all contact submissions (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_submissions ORDER BY created_at DESC')
    contacts = cursor.fetchall()
    conn.close()
    return [dict(contact) for contact in contacts]

def update_contact_status(contact_id, status):
    """Update contact submission status"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE contact_submissions SET status = ? WHERE id = ?', (status, contact_id))
    conn.commit()
    conn.close()

# Activity logging
def log_activity(user_id, activity_type, details=None):
    """Log user activity"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activity_log (user_id, activity_type, details)
        VALUES (?, ?, ?)
    ''', (user_id, activity_type, details))
    conn.commit()
    conn.close()

def log_analytics(user_id, feature, query_data=None, result_data=None):
    """Log analytics data"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analytics (user_id, feature, query_data, result_data)
        VALUES (?, ?, ?, ?)
    ''', (user_id, feature, query_data, result_data))
    conn.commit()
    conn.close()

def log_prediction(user_id, prediction_type, input_data, output_data, confidence=None):
    """Log prediction history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prediction_history (user_id, prediction_type, input_data, output_data, confidence)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, prediction_type, input_data, output_data, confidence))
    conn.commit()
    conn.close()

def get_user_predictions(user_id, limit=10):
    """Get user's prediction history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM prediction_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (user_id, limit))
    predictions = cursor.fetchall()
    conn.close()
    return [dict(pred) for pred in predictions]

# Analytics functions
def get_analytics_summary():
    """Get analytics summary (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Total users
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_admin = 0')
    total_users = cursor.fetchone()['count']
    
    # Total queries
    cursor.execute('SELECT COUNT(*) as count FROM analytics')
    total_queries = cursor.fetchone()['count']
    
    # Total contacts
    cursor.execute('SELECT COUNT(*) as count FROM contact_submissions')
    total_contacts = cursor.fetchone()['count']
    
    # Feature usage
    cursor.execute('''
        SELECT feature, COUNT(*) as count 
        FROM analytics 
        GROUP BY feature 
        ORDER BY count DESC
    ''')
    feature_usage = [dict(row) for row in cursor.fetchall()]
    
    # Recent activities
    cursor.execute('''
        SELECT a.*, u.username 
        FROM activity_log a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
        LIMIT 10
    ''')
    recent_activities = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_queries': total_queries,
        'total_contacts': total_contacts,
        'feature_usage': feature_usage,
        'recent_activities': recent_activities
    }

if __name__ == '__main__':
    init_db()
