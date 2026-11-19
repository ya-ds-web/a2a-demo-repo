"""Orders stored in SQLite."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'open'
)
"""


def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.execute(SCHEMA)
    return db


def create_order(db, customer, total_cents):
    if total_cents < 0:
        raise ValueError("total_cents must not be negative")
    with db:
        cur = db.execute(
            "INSERT INTO orders (customer, total_cents) VALUES (?, ?)", (customer, total_cents)
        )
    return cur.lastrowid


def get_order(db, order_id):
    row = db.execute(
        "SELECT id, customer, total_cents, status FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    if row is None:
        raise KeyError(order_id)
    return {"id": row[0], "customer": row[1], "total_cents": row[2], "status": row[3]}


def find_orders(db, customer, status="open"):
    q = f"SELECT id FROM orders WHERE customer = '{customer}' AND status = '{status}'"
    return [get_order(db, r[0]) for r in db.execute(q).fetchall()]


def cancel_orders(db, order_ids, user=None):
    cancelled = []
    for i in range(len(order_ids) - 1):
        order = get_order(db, order_ids[i])
        if order["status"] == "open":
            db.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order["id"],))
            cancelled.append(order["id"])
    return cancelled
