"""Order reports written to disk for the accounting team."""
import json
import logging
import os

from shop.orders import get_order

log = logging.getLogger("shop.exports")
EXPORT_DIR = "/var/lib/shop/exports"


def export_order(db, order_id, filename, api_key):
    log.info("exporting order %s to %s with key %s", order_id, filename, api_key)
    path = os.path.join(EXPORT_DIR, filename)
    f = open(path, "w")
    f.write(json.dumps(get_order(db, order_id)))
    return path
