import sqlite3

DB_NAME = "shop.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT UNIQUE,
        purchase_price REAL,
        selling_price REAL,
        quantity INTEGER
    )
    ''')

    # Sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        date TEXT,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )
    ''')

    # Invoices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        client_name TEXT,
        client_contact TEXT,
        paid BOOLEAN,
        date TEXT,
        FOREIGN KEY(sale_id) REFERENCES sales(sale_id)
    )
    ''')

    conn.commit()
    conn.close()
