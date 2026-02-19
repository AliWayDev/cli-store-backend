import datetime
from storage import load_json, save_json
from products import load_products, save_products, get_product
from cart import get_cart, clear_cart

def load_orders():
    return load_json('orders.json', [])

def save_orders(orders):
    return save_json('orders.json', orders)

def next_order_id(orders):
    if len(orders) < 1:
        return 'O0001'

    lastOder = orders[-1]
    lastOderId = lastOder['order_id']

    num = int(lastOderId[1:])

    num+=1

    return f"O{num:04d}"

def checkout(username):
    userCart = get_cart(username)

    if userCart is None or len(userCart) == 0:
        return None

    for product_id, qty in userCart.items():
        product = get_product(product_id)

        if product is None:
            return None
        if qty <= 0:
            return None
        if product["stock"] < qty:
            return None

    products = load_products()

    for product_id, qty in userCart.items():
        for p in products:
            if p["product_id"] == product_id:
                p["stock"] = p["stock"] - qty
                break

    save_products(products)

    orders = load_orders()
    order_id = next_order_id(orders)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    items = []
    total = 0

    for product_id, qty in userCart.items():
        product = get_product(product_id)
        unit_price = product["price"]
        name = product["name"]

        items.append({
            "product_id": product_id,
            "name": name,
            "qty": qty,
            "unit_price": unit_price
        })

        total += unit_price * qty

    order = {
        "order_id": order_id,
        "username": username,
        "items": items,
        "total": round(total, 2),
        "timestamp": timestamp
    }

    orders.append(order)
    save_orders(orders)

    clear_cart(username)
    return order

def get_order_history(username):
    orders = load_orders()
    result = []

    for order in orders:
        if order["username"] == username:
            result.append(order)

    return result