import json
import os

db = './data/'

def mk_data_dir ():
    if not os.path.exists("data"):
        os.mkdir("data")

def load_json (filename, default):
    mk_data_dir()

    target_file_name = os.path.join(db, filename)

    if os.path.isfile(target_file_name):

        try:
            with open(target_file_name, 'r') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            return default
    else:
        return default

def save_json (filename, data):
    mk_data_dir()

    target_file_name = os.path.join(db, filename)

    with open(target_file_name, 'w') as f:
        json.dump(data, f, indent=2)