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
