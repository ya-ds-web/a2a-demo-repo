import pytest

from shop.orders import connect, create_order, get_order


def test_create_and_fetch():
    db = connect()
    order_id = create_order(db, "ana", 1250)
    assert get_order(db, order_id) == {"id": order_id, "customer": "ana", "total_cents": 1250, "status": "open"}


def test_negative_total_is_refused():
    with pytest.raises(ValueError):
        create_order(connect(), "ana", -1)


def test_unknown_order():
    with pytest.raises(KeyError):
        get_order(connect(), 99)
