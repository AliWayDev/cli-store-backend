from storage import load_json, save_json

def load_users():
    return load_json("users.json", [])

def find_user(arr, username):
    for u in arr:
        if(u['username'] == username): 
            return u
    return None

def check_user_existance(username):
    db_users = load_users()

    is_user_exist = find_user(db_users, username)

    if is_user_exist:
        return is_user_exist
    else: 
        return False

def save_users(users):
    return save_json("users.json", users)
    
def register(username, password):

    if len(username.strip()) == 0 or len(password) < 6 :
        return False
    
    foundUser = check_user_existance(username)

    if foundUser:
        return False
    
    users = load_users()
    users.append({"username": username.strip(), "password": password})

    save_users(users)

    return True

def login(username, password):
    foundUser = check_user_existance(username)

    if not foundUser:
        return None
    
    if(foundUser['password'] != password):
        return None
    else: 
        return foundUser 
