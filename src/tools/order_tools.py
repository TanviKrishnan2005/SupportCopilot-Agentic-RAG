import sqlite3
from pathlib import Path
from datetime import datetime

from langchain_core.tools import tool


# --------------------------------------------------
# Database Path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "data" / "database" / "orders.db"


# --------------------------------------------------
# Get Order Status
# --------------------------------------------------

@tool
def get_order_status(order_id: str):
    """Get the current status and details of an order."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    query = """
        SELECT
            o.order_id,
            o.customer_name,
            p.product_name,
            o.order_date,
            o.delivery_date,
            o.status,
            o.payment_status,
            o.amount
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        WHERE o.order_id = ?
    """

    cursor.execute(query, (order_id,))

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return {
            "success": False,
            "message": f"No order found with ID {order_id}."
        }

    return {
        "success": True,
        "order_id": order[0],
        "customer_name": order[1],
        "product_name": order[2],
        "order_date": order[3],
        "delivery_date": order[4],
        "status": order[5],
        "payment_status": order[6],
        "amount": order[7]
    }


# --------------------------------------------------
# Check Refund Eligibility
# --------------------------------------------------

@tool
def check_refund_eligibility(order_id: str):
    """Check whether an order is eligible for a refund."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    query = """
        SELECT
            order_id,
            delivery_date,
            status,
            amount
        FROM orders
        WHERE order_id = ?
    """

    cursor.execute(query, (order_id,))

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return {
            "eligible": False,
            "message": f"No order found with ID {order_id}."
        }

    order_id, delivery_date, status, amount = order

    # Order must be delivered
    if status != "Delivered":
        return {
            "eligible": False,
            "message": "The order has not been delivered yet."
        }

    # Check delivery date
    delivery = datetime.strptime(
        delivery_date,
        "%Y-%m-%d"
    )

    today = datetime.now()

    days_since_delivery = (
        today - delivery
    ).days

    # NovaCart allows returns within 30 days
    if days_since_delivery <= 30:
        return {
            "eligible": True,
            "order_id": order_id,
            "amount": amount,
            "days_since_delivery": days_since_delivery,
            "message": "Order is eligible for a refund."
        }

    return {
        "eligible": False,
        "order_id": order_id,
        "amount": amount,
        "days_since_delivery": days_since_delivery,
        "message": "Order is outside the 30-day return window."
    }


# --------------------------------------------------
# Create Support Ticket
# --------------------------------------------------

@tool
def create_ticket(order_id: str, issue: str):
    """Create a support ticket for an order."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Check whether the order exists
    cursor.execute(
        "SELECT order_id FROM orders WHERE order_id = ?",
        (order_id,)
    )

    order = cursor.fetchone()

    if order is None:
        connection.close()

        return {
            "success": False,
            "message": f"No order found with ID {order_id}."
        }

    # Get the next ticket number
    cursor.execute(
        "SELECT COUNT(*) FROM support_tickets"
    )

    ticket_count = cursor.fetchone()[0]

    ticket_id = f"T{1001 + ticket_count}"

    # Create ticket
    cursor.execute("""
        INSERT INTO support_tickets
        (ticket_id, order_id, issue, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        ticket_id,
        order_id,
        issue,
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "ticket_id": ticket_id,
        "order_id": order_id,
        "issue": issue,
        "status": "Open",
        "message": "Support ticket created successfully."
    }


# --------------------------------------------------
# Test Tools
# --------------------------------------------------

if __name__ == "__main__":

    order_id = input("Enter Order ID: ").strip()

    print("\nOrder Status:")
    print(get_order_status.invoke(order_id))

    print("\nRefund Eligibility:")
    print(check_refund_eligibility.invoke(order_id))

    issue = input("\nEnter support issue: ").strip()

    print("\nCreate Ticket:")
    print(create_ticket.invoke({
        "order_id": order_id,
        "issue": issue
    }))