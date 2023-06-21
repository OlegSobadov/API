import sqlite3
from utils.json_utils import load_from_json


def save_to_database(results):
    # Connect to the database
    conn = sqlite3.connect('database/mydatabase.db')
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 publish_date TEXT)''')

    # Insert the results into the table
    for result in results:
        title = result['title']
        publish_date = result['publish_date']
        c.execute("INSERT INTO articles (title, publish_date) VALUES (?, ?)", (title, publish_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Assuming you have the 'results' list containing the data to be saved

# def main():
#     # Load results from JSON file
#     results = load_from_json('data/results.json')

#     # Save results to the SQL database
#     save_to_database(results)

# if __name__ == '__main__':
#     main()