from storage import load_json, save_json

def load_products():
    return load_json("products.json", [])

def save_products(products):
    return save_json("products.json", products)

def get_product(product_id):
    arr = load_products()

    for u in arr:
        if(u['product_id'] == product_id): 
            return u
    return None

def list_products():
    arr = load_products()

    return arr

def search_products(keyword):
    results = []

    for product in list_products():
        if keyword.lower() in product["name"].lower():
            results.append(product)
    return results

def validate_stock(product_id, qty):
    foundProduct = get_product(product_id)

    if foundProduct == None:
        return False

    if foundProduct['stock'] >= qty:
        return True
    else:
        return False
    