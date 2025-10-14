import csv
from db.database import get_connection

def export_invoices_csv(filename="invoices_export.csv"):
    """
    --- Added by Saalim Zafar: Export all invoices to CSV ---
    Exports invoice list with client info and total price
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.invoice_id, s.sale_id, i.client_name, i.client_contact, i.paid, i.date, s.total_price
        FROM invoices i
        JOIN sales s ON i.sale_id = s.sale_id
        ORDER BY i.invoice_id DESC
    ''')
    invoices = cursor.fetchall()
    conn.close()

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["InvoiceID", "SaleID", "Client", "Contact", "Paid", "Date", "Total"])
        for inv in invoices:
            writer.writerow([
                inv[0],
                inv[1],
                inv[2],
                inv[3],
                "Yes" if inv[4] else "No",
                inv[5],
                f"{inv[6]:.2f}"
            ])
