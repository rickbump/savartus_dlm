import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, database):
    """Creates and returns a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None
### ------------------------------------ ###
def create_database(connection, db_name):
    """Connects to MySQL server and creates a new database."""
    try:
        # Establish connection to the MySQL server (without specifying a database)
        if connection.is_connected():
            print("Connected to MySQL server")

            # Create a cursor and execute the database creation SQL
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created successfully (or already exists)")

    except Error as e:
        print(f"Error: '{e}'")
### ------------------------------------ ###
def create_processed_files_table(connection):
    """Creates a table in the MySQL database."""
    try:
        if connection.is_connected():
            print("Connected to MySQL server")
        cursor = connection.cursor()
        print("cursor connected")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_size INT,
                file_type VARCHAR(100),
                process_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                additional_data TEXT
            )
        ''')
        connection.commit()
        print("Table 'processed_files' created successfully")
    except Error as e:
        print(f"Error: '{e}'")
### ------------------------------------ ###
def create_test_table(connection):
    """Creates a table in the MySQL database."""
    try:
        if connection.is_connected():
            print("Connected to MySQL server")
        cursor = connection.cursor()
        print("cursor connected")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test (
                additional_data TEXT
            )
        ''')
        connection.commit()
        print("Table 'processed_files' created successfully")
    except Error as e:
        print(f"Error: '{e}'")
### ------------------------------------ ###
def view_schema(connection, db_name):
    """Connects to MySQL database and displays the schema (tables and columns) of the specified database."""
    try:
        if connection.is_connected():
            print(f"Connected to MySQL server. Retrieving schema for '{db_name}'.")

            cursor = connection.cursor()

            # Query to get tables and columns from information_schema
            cursor.execute(f'''
                SELECT 
                    TABLE_NAME, COLUMN_NAME, DATA_TYPE 
                FROM 
                    information_schema.COLUMNS 
                WHERE 
                    TABLE_SCHEMA = '{db_name}';
            ''')

            # Fetch and display results
            schema = cursor.fetchall()
            print(f"\nSchema for database '{db_name}':")
            for table_name, column_name, data_type in schema:
                print(f"Table: {table_name} | Column: {column_name} | Data Type: {data_type}")

    except Error as e:
        print(f"Error: '{e}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

### ------------------------------------ ###

# Create a reusable connection

host = '127.0.0.1'  # Change this to your MySQL server host
user = 'default'  # Change to your MySQL username
password = 'SOPHIA'  # Change to your MySQL password
database = None
db_name = 'savartus_dlm_db'  # Change to your database name

connection = create_connection(host, user, password, database)
if connection:
    print('connected')
    create_database(connection, db_name)
    print('created db')
    connection = create_connection(host, user, password, db_name)
    create_processed_files_table(connection)
    create_test_table(connection)
    print('created table')
    view_schema(connection, db_name)
    connection.close()