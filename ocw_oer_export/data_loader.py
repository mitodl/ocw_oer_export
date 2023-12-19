import json

def load_data_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            print(f"Data successfully loaded from {filename}.")
            return data
    except FileNotFoundError:
        print(f"{filename} not found.")
        return []

def save_data_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
        print(f"Data successfully saved to {filename}.")
