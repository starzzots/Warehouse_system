from flask import  Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from config import DB_PATH, SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash
import re
app = Flask(__name__)
app.secret_key = SECRET_KEY  # session and flash messages will work
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add missing columns (skip if they already exist)
try:
    cursor.execute("ALTER TABLE users ADD COLUMN username TEXT UNIQUE")
except sqlite3.OperationalError:
    print("username column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN street TEXT")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN state TEXT")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN zip_code TEXT")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()
print("Missing columns added successfully.")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/add', methods=('GET', 'POST'))
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        location = request.form['location']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO items (name, quantity, location) VALUES (?, ?, ?)',
            (name, quantity, location)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        street = request.form['street'].strip()
        state = request.form['state'].strip().upper()
        zip_code = request.form['zip_code'].strip()
        password = request.form['password']

        # --- Validation ---
        if not re.fullmatch(r'\d{5}', zip_code):
            flash("ZIP code must be 5 digits.", "danger")
            return redirect(url_for('sign_up'))

        if not re.fullmatch(r'[A-Z]{2}', state):
            flash("State must be 2 letters (e.g., NY, CA).", "danger")
            return redirect(url_for('sign_up'))

        conn = get_db_connection()
        existing_user = conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()

        if existing_user:
            flash("Username or email already exists.", "danger")
            conn.close()
            return redirect(url_for('sign_up'))

        # --- Insert user ---
        hashed_password = generate_password_hash(password)
        conn.execute(
            '''INSERT INTO users 
               (first_name, last_name, username, email, street, state, zip_code, password)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (first_name, last_name, username, email, street, state, zip_code, hashed_password)
        )
        conn.commit()
        conn.close()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('sign_up.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username_or_email, username_or_email)
        ).fetchone()
        conn.close()

        if user is None:
            flash("User not found!", "danger")
        elif not check_password_hash(user['password'], password):
            flash("Incorrect password!", "danger")
        else:
            # Login success
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['first_name']}!", "success")
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        location = request.form['location']

        conn.execute(
            'UPDATE items SET name = ?, quantity = ?, location = ? WHERE id = ?',
            (name, quantity, location, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_item.html', item=item)


@app.route('/delete/<int:id>')
def delete_item(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
