from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'warehouse.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
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
        conn.execute('INSERT INTO items (name, quantity, location) VALUES (?, ?, ?)',
                     (name, quantity, location))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        location = request.form['location']

        conn.execute('UPDATE items SET name = ?, quantity = ?, location = ? WHERE id = ?',
                     (name, quantity, location, id))
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