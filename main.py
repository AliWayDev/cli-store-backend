from users import register, login
from products import list_products, search_products, get_product
from cart import add_to_cart, remove_from_cart, get_cart
from orders import checkout, get_order_history


def input_int(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Please enter a number.")


def showProduct(products):

    if not products:
        print("No products found.")
        return
    
    print("\n====== PRODUCTS")

    for i in products:
        print(f"ID: {i['product_id']}")
        print(f"NAME: {i['name']}")
        print(f"Price: {i['price']}")
        print(f"Stock: {i['stock']}")

    print("======\n")


def showCart(username):

    obtained_cart = get_cart(username)

    if not obtained_cart:
        if len(obtained_cart) == 0:
            print("Your cart is empyt!")
            return
    
    print("\n ===== Your Cart")
    all = 0
    for product_id, qty in obtained_cart.items():

        i = get_product(product_id)

        if i is None:
            continue

        subtotal = i["price"] * qty
        all += subtotal

        print(f"{i['name']} ({product_id})")
        print(f"Qty: {qty} ({product_id})")
        print(f"Unit: {i['price']} ({product_id})")
        print(f"Subtotal: {subtotal} ({product_id})")

    print("-----------------\n")


def showReceipt(order):

    print("======Recipt")
    print(f"Order ID: {order['order_id']}")
    print(f"User: {order['username']}")
    print(f"Time: {order['timestamp']}")
    print("\nItems:")

    for it in order["items"]:
        subtotal = it["qty"] * it["unit_price"]
        print(f"- {it['name']} | Qty: {it['qty']} | Unit: {it['unit_price']} | Sub: {round(subtotal, 2)}")
    
    print(f"\nTOTAL: {order['total']}")

    print("==============\n")

def storemenu(username):
    while True:
        print("=== STORE MENU")
        print("1) Browse products")
        print("2) Search products")
        print("3) Add to cart")
        print("4) Remove from cart")
        print("5) View cart")
        print("6) Checkout")
        print("7) Order history")
        print("0) Logout")

        choice = input("Choose: ").strip()

        if choice == "1":

            showProduct(list_products())

        elif choice == "2":

            keyword = input("Search keyword: ").strip()
            showProduct(search_products(keyword))

        elif choice == "3":

            product_id = input("Product ID: ").strip()
            qty = input_int("Qty: ")
            ok = add_to_cart(username, product_id, qty)
            print("Added to cart.\n" if ok else "Failed to add (check stock/product).\n")

        elif choice == "4":
            
            product_id = input("Product ID: ").strip()
            mode = input("Type 'all' to remove item, or enter qty: ").strip().lower()
            if mode == "all":
                ok = remove_from_cart(username, product_id, None)
            else:
                try:
                    ok = remove_from_cart(username, product_id, int(mode))
                except ValueError:
                    ok = False
            print("Cart updated.\n" if ok else "Failed to remove.\n")

        elif choice == "5":
            showCart(username)

        elif choice == "6":

            order = checkout(username)
            if order is None:
                print("Checkout failed or cart empty.\n")
            else:
                showReceipt(order)

        elif choice == "7":

            history = get_order_history(username)

            if not history:
                print("\nNo orders yet.\n")
            else:
                print("\n--- ORDER HISTORY ---")
                for o in history:
                    print(f"{o['order_id']} | {o['timestamp']} | Total: {o['total']}")
                print("---------------------\n")

        elif choice == "0":
            print("Logged out.\n")
            return

        else:
            print("Invalid option.\n")


def welcomMenu():

    while True:
        print("=== WELCOME MEUN")
        print("1) Registre")
        print("2) Login")
        print("0) Exit")

        choic = input("Choose: ").strip()

        if choic == "1":
            username = input("Username: ").strip()
            password = input("Password (min 6 chars): ").strip()

            ok = register(username, password)

            print("Registered!\n" if ok else "Register failed.\n")

        elif choic == "2":

            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = login(username, password)

            if user is None: 

                print("Login failed.\n")
                
            else:
                print(f"Welcome, {user['username']}!\n")
                storemenu(user["username"])

        elif choic == "0":
            print("Bye!")
            return

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    welcomMenu()

