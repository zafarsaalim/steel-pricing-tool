from db.database import get_connection

def get_summary():
    """
    --- Added by Saalim Zafar: Summary stats ---
    Returns total sales and number of unpaid invoices
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total_price) FROM sales')
    total_sales = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM invoices WHERE paid=0')
    unpaid_count = cursor.fetchone()[0] or 0
    conn.close()
    return total_sales, unpaid_count
