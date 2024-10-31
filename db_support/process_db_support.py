import mysql.connector
from mysql.connector import Error
import json

def db_connection(config_file):
    """Loads database configuration from a JSON file and creates a MySQL connection."""
    try:
        # Load the configuration from the JSON file
        with open(config_file, 'r') as file:
            config = json.load(file)

        # Create and return the database connection
        connection = mysql.connector.connect(
            host=config['db_connection_host'],
            user=config['db_connection_user'],
            password=config['db_connection_password'],
            database=config['db_connection_db_name']
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection

    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        return None
    except Error as e:
        print(f"Database connection error: '{e}'")
        return None
    except KeyError as e:
        print(f"Missing configuration key: '{e}'")
        return None
### ------------------------------------ ###
def insert_row(config_file, table_name, row_data):
    """
    Inserts a row into the specified table by connecting to the database using config from a JSON file.
    """
    # Establish the database connection
    connection = db_connection(config_file)

    if not connection:
        print("Failed to connect to database.")
        return

    try:
        cursor = connection.cursor()

        # Prepare the insert query
        columns = ', '.join(row_data.keys())
        print(columns)
        placeholders = ', '.join(['%s'] * len(row_data))
        print(placeholders)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(query)

        # Execute the query
        cursor.execute(query, list(row_data.values()))
        connection.commit()
        print("Row inserted successfully.")

    except Error as e:
        print(f"Error inserting row: '{e}'")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")
### ------------------------------------ ###
def view_table_contents(config_file, table_name):
    """
    Connects to the database and retrieves all rows from the specified table.

    Parameters:
    - config_file: Path to the JSON file with database configuration.
    - table_name: Name of the table to view.
    """
    connection = db_connection(config_file)

    if not connection:
        print("Failed to connect to database.")
        return

    try:
        cursor = connection.cursor()
        # Execute the SELECT query
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        column_names = [i[0] for i in cursor.description]

        # Display the data
        print(f"\nContents of table '{table_name}':")
        print(column_names)
        for row in rows:
            print(row)

    except Error as e:
        print(f"Error retrieving table contents: '{e}'")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

### ------------------------------------ ###


# View the table contents
config_file = '/home/rbump/savartus_dlm/config.json'  # Path to your JSON config file
table_name = 'processed_files'   # Replace with your table name
row_data = {                     # Data to insert
    'file_name': 'bumper.txt',
    'file_size': 12048,
    'file_type': 'text',
    'additional_data': 'Some additional information'
}

# Insert the row
#insert_row(config_file, table_name, row_data)
view_table_contents(config_file, table_name)