import sqlite3
from flask import Flask, render_template, request, redirect
import threading, os

# --- Flask setup ---
app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# --- CRUD Routes ---
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    qty = request.form['quantity']
    price = request.form['price']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
              (name, qty, price))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    name = request.form['name']
    qty = request.form['quantity']
    price = request.form['price']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE items SET name=?, quantity=?, price=? WHERE id=?",
              (name, qty, price, item_id))
    conn.commit()
    conn.close()
    return redirect('/')

# --- Launcher for Web + WebView ---
def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == "__main__":
    # You can switch between browser or webview mode
    USE_WEBVIEW = True

    if USE_WEBVIEW:
        import webview
        threading.Thread(target=run_flask, daemon=True).start()
        webview.create_window("Inventory Manager", "http://127.0.0.1:5000")
        webview.start()
    else:
        import webbrowser
        threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
        run_flask()
