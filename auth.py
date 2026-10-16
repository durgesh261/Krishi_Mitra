from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify

def login_required(f):
    """Decorator to require login - secures premium farming features while keeping Mandi, News, and Deals public"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # If API / AJAX request, return JSON 401
            if request.path.startswith('/api/') or request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'error': 'Please sign in to access this feature.',
                    'login_required': True,
                    'redirect_url': url_for('login')
                }), 401

            flash('Please sign in to access this feature. (Mandi Bhav, News, and Deals are freely accessible without sign in).', 'warning')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/') or request.is_json:
                return jsonify({'success': False, 'error': 'Admin login required', 'login_required': True}), 401
            flash('Please login as administrator to access this page.', 'warning')
            return redirect(url_for('login', next=request.path))
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
