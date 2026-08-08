import sqlite3
from pathlib import Path


# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "data" / "database" / "orders.db"


# Connect to database
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()


# -----------------------------------------
# Show products
# -----------------------------------------

print("\n--- PRODUCTS ---")

products = cursor.execute("""
    SELECT product_id, product_name, price, warranty_months
    FROM products
""").fetchall()

for product in products:
    print(product)


# -----------------------------------------
# Show orders
# -----------------------------------------

print("\n--- ORDERS ---")

orders = cursor.execute("""
    SELECT
        order_id,
        customer_name,
        product_id,
        status,
        payment_status,
        amount
    FROM orders
""").fetchall()

for order in orders:
    print(order)


# -----------------------------------------
# Show support tickets
# -----------------------------------------

print("\n--- SUPPORT TICKETS ---")

tickets = cursor.execute("""
    SELECT
        ticket_id,
        order_id,
        issue,
        status
    FROM support_tickets
""").fetchall()

for ticket in tickets:
    print(ticket)


connection.close()