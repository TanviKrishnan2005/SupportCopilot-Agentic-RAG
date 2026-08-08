import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "data" / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "orders.db"


# --------------------------------------------------
# Database Connection
# --------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()


# --------------------------------------------------
# Create Tables
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    warranty_months INTEGER NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    product_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    delivery_date TEXT,
    status TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id TEXT PRIMARY KEY,
    order_id TEXT,
    issue TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id))
""")


# --------------------------------------------------
# Products
# --------------------------------------------------

products = [
    ("P001", "Apple AirPods Pro (2nd Generation)", "Headphones & Earbuds", 24999, 12),
    ("P002", "Sony WH-1000XM5", "Headphones & Earbuds", 29990, 12),
    ("P003", "Dell XPS 13", "Laptops", 89990, 12),
    ("P004", "HP Victus 15", "Laptops", 74990, 12),
    ("P005", "Samsung Galaxy Watch 7", "Smartwatches", 29999, 12),
    ("P006", "JBL Flip 6", "Bluetooth Speakers", 9999, 12),
    ("P007", "Logitech MX Master 3S", "Computer Accessories", 8995, 12),
    ("P008", "Kindle Paperwhite", "Electronics", 14999, 12),
    ("P009", "Anker 20000mAh Power Bank", "Power Banks", 4499, 6),
    ("P010", "Xiaomi Smart Band 9", "Smartwatches", 3999, 12),
]


cursor.executemany("""
INSERT OR IGNORE INTO products
(product_id, product_name, category, price, warranty_months)
VALUES (?, ?, ?, ?, ?)
""", products)


# --------------------------------------------------
# Customers
# --------------------------------------------------

customers = [
    ("Priya Sharma", "priya.sharma@example.com"),
    ("Rahul Mehta", "rahul.mehta@example.com"),
    ("Sneha Patel", "sneha.patel@example.com"),
    ("Arjun Nair", "arjun.nair@example.com"),
    ("Ananya Singh", "ananya.singh@example.com"),
    ("Rohan Kapoor", "rohan.kapoor@example.com"),
    ("Meera Iyer", "meera.iyer@example.com"),
    ("Karan Malhotra", "karan.malhotra@example.com"),
    ("Ishita Rao", "ishita.rao@example.com"),
    ("Aditya Verma", "aditya.verma@example.com"),
]


# --------------------------------------------------
# Order Data
# --------------------------------------------------

statuses = [
    "Processing",
    "Shipped",
    "Out for Delivery",
    "Delivered"
]

payment_statuses = [
    "Paid",
    "Paid",
    "Paid",
    "Paid",
    "COD"
]

random.seed(42)

orders = []

start_date = datetime(2026, 7, 1)

for i in range(30):

    order_id = f"ORD{1001 + i}"

    customer_name, email = random.choice(customers)

    product = random.choice(products)

    product_id = product[0]
    price = product[3]

    order_date = start_date + timedelta(
        days=random.randint(0, 30)
    )

    status = random.choice(statuses)

    if status == "Delivered":
        delivery_date = order_date + timedelta(
            days=random.randint(2, 7)
        )
        delivery_date = delivery_date.strftime("%Y-%m-%d")
    else:
        delivery_date = None

    payment_status = random.choice(payment_statuses)

    # COD orders should not randomly exceed the COD limit
    if payment_status == "COD" and price > 20000:
        payment_status = "Paid"

    orders.append((
        order_id,
        customer_name,
        email,
        product_id,
        order_date.strftime("%Y-%m-%d"),
        delivery_date,
        status,
        payment_status,
        price
    ))


cursor.executemany("""
INSERT OR IGNORE INTO orders
(order_id, customer_name, email, product_id, order_date,
 delivery_date, status, payment_status, amount)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", orders)


# --------------------------------------------------
# Sample Support Tickets
# --------------------------------------------------

tickets = [
    (
        "T1001",
        "ORD1005",
        "Product arrived damaged",
        "Open",
        "2026-07-20 10:30:00"
    ),
    (
        "T1002",
        "ORD1012",
        "Refund request",
        "Closed",
        "2026-07-18 14:15:00"
    ),
    (
        "T1003",
        "ORD1018",
        "Package delivery delayed",
        "Open",
        "2026-07-25 09:45:00"
    ),
]


cursor.executemany("""
INSERT OR IGNORE INTO support_tickets
(ticket_id, order_id, issue, status, created_at)
VALUES (?, ?, ?, ?, ?)
""", tickets)


# --------------------------------------------------
# Save Changes
# --------------------------------------------------

connection.commit()

connection.close()

print(f"Database created successfully: {DATABASE_PATH}")
print("Products inserted:", len(products))
print("Orders inserted:", len(orders))
print("Support tickets inserted:", len(tickets))