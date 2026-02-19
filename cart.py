from storage import load_json, save_json
from products import get_product

def load_carts():
    return load_json("carts.json", {})

def save_carts(carts):
    return save_json('carts.json', carts)

def get_cart(username):
    carts = load_carts()

    if username in carts:
        return carts[username]
    else:
        return {}

def add_to_cart(username, product_id, qty):
    if qty <= 0:
        return False
    
    foundProduct = get_product(product_id)

    if foundProduct == None:
        return False

    user_cart = get_cart(username)

    current_qty = user_cart.get(product_id, 0)

    new_qty = current_qty + qty

    if foundProduct["stock"] < new_qty:
        return False
    
    user_cart[product_id] = new_qty

    carts = load_carts()

    carts[username] = user_cart

    save_carts(carts)

    return True
    
def remove_from_cart(username, product_id, qty = None):
    user_cart = get_cart(username)

    if product_id not in user_cart:
        return False
        
    if qty is None:
        del user_cart[product_id]

    else:
        if qty <= 0:
            return False

        new_qty = user_cart[product_id] - qty
            
        if new_qty <= 0:
            del user_cart[product_id]
        else:
            user_cart[product_id] = new_qty
    
    carts = load_carts()
    
    if len(user_cart) == 0:
        if username in carts:
            del carts[username]
    else:
        carts[username] = user_cart

    save_carts(carts)
    return True

def clear_cart(username):
    carts = load_carts()

    if username in carts: 
        del carts[username]

    save_carts(carts)
    return True