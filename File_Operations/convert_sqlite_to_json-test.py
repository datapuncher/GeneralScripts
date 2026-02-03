#!/usr/bin/python

import sqlite3
import json

def sqlite_to_json():
    # Connect to the SQLite database
    db_path = input("Enter the SQLite file including the path: ")
    json_path = input("Enter the name of the output JSON file: ")
    table_name = input("Please input the table to be exported: ")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    db_data = {}

    for table in tables:
#       table_name = input("Please input the table to be exported: ")
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        db_data[table_name] = [dict(zip(columns, row)) for row in rows]

    # Close the connection
    conn.close()

    # Write to JSON file
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(db_data, json_file, indent=4, ensure_ascii=False)

    print(f"Database exported to {json_path}")

# Example usage
if __name__ == "__main__":
    sqlite_to_json()
