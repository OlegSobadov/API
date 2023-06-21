import json

def load_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Assuming you have a JSON file named 'results.json' in the 'data' directory

# Load results from JSON file
results = load_from_json('data/results.json')
