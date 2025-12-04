import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, g

# --- Configuration ---
app = Flask(__name__)
# IMPORTANT: Use a strong secret key in production
app.secret_key = 'your_super_secret_key_for_session_management' 
DATABASE = 'employee_manager.db'

# --- Database Setup Functions ---

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Use sqlite3.Row objects for dictionary-like access to query results
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database schema and creates a default user."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # 1. Users Table for Authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # 2. Employees Table for Data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                emp_id TEXT UNIQUE NOT NULL,
                salary REAL NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        
        # Create a default admin user if one doesn't exist (password is 'admin')
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))
            db.commit()
            print("Default user 'admin' created.")
        except sqlite3.IntegrityError:
            print("Default user 'admin' already exists.")
            
        # Add some initial employee data
        initial_employees = [
            ('Alice Johnson', 'E1001', 75000.00, 'New York'),
            ('Bob Smith', 'E1002', 62000.50, 'San Francisco'),
            ('Charlie Brown', 'E1003', 88000.00, 'London')
        ]
        
        for name, emp_id, salary, location in initial_employees:
            try:
                cursor.execute("INSERT INTO employees (name, emp_id, salary, location) VALUES (?, ?, ?, ?)", 
                               (name, emp_id, salary, location))
            except sqlite3.IntegrityError:
                # Skip if employee ID already exists
                pass

        db.commit()
        print("Database initialized and initial employees added.")

# Initialize database on first run
if not os.path.exists(DATABASE):
    init_db()


# --- Authentication Decorator ---

def login_required(f):
    """Decorator to restrict access to authenticated users."""
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            # If not logged in, redirect to the login page
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


# --- Routes ---

@app.route('/', methods=['GET'])
@login_required
def dashboard():
    """The main employee dashboard showing all records."""
    db = get_db()
    cursor = db.cursor()
    employees = cursor.execute("SELECT * FROM employees ORDER BY id DESC").fetchall()
    
    # Pass the employee data to the template
    return render_template('index.html', page='dashboard', employees=employees, success_message=session.pop('success', None))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login and authentication."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        
        # NOTE: Simple unhashed password check for demonstration. 
        # In production, use werkzeug.security.check_password_hash.
        user = cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", 
            (username, password)
        ).fetchone()
        
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', page='login', error='Invalid credentials. Try username: admin, password: admin')

    # If already logged in, redirect to dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
        
    return render_template('index.html', page='login')


@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/employee', methods=['POST'])
@login_required
def add_employee():
    """Adds a new employee record."""
    db = get_db()
    name = request.form.get('name')
    emp_id = request.form.get('emp_id')
    salary = request.form.get('salary')
    location = request.form.get('location')

    try:
        db.execute(
            "INSERT INTO employees (name, emp_id, salary, location) VALUES (?, ?, ?, ?)",
            (name, emp_id, salary, location)
        )
        db.commit()
        session['success'] = f"Employee {name} added successfully!"
    except sqlite3.IntegrityError:
        session['success'] = f"Error: Employee ID {emp_id} already exists."
    except Exception as e:
        session['success'] = f"An error occurred: {e}"
        
    return redirect(url_for('dashboard'))


@app.route('/employee/<int:id>', methods=['POST'])
@login_required
def update_employee(id):
    """Updates an existing employee record."""
    db = get_db()
    name = request.form.get('name')
    emp_id = request.form.get('emp_id')
    salary = request.form.get('salary')
    location = request.form.get('location')

    try:
        db.execute(
            "UPDATE employees SET name = ?, emp_id = ?, salary = ?, location = ? WHERE id = ?",
            (name, emp_id, salary, location, id)
        )
        db.commit()
        session['success'] = f"Employee ID {emp_id} updated successfully!"
    except sqlite3.IntegrityError:
        session['success'] = f"Error: Employee ID {emp_id} is already in use by another record."
    except Exception as e:
        session['success'] = f"An error occurred: {e}"
        
    return redirect(url_for('dashboard'))


@app.route('/employee/<int:id>/delete', methods=['POST'])
@login_required
def delete_employee(id):
    """Deletes an employee record."""
    db = get_db()
    cursor = db.cursor()
    
    # Get the name/ID before deletion for the success message
    employee = cursor.execute("SELECT name, emp_id FROM employees WHERE id = ?", (id,)).fetchone()
    
    if employee:
        db.execute("DELETE FROM employees WHERE id = ?", (id,))
        db.commit()
        session['success'] = f"Employee {employee['name']} ({employee['emp_id']}) deleted successfully!"
    else:
        session['success'] = "Error: Employee not found."
        
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Ensure the database is initialized
    with app.app_context():
        init_db()
        
    # Run the app
    app.run(debug=True)

