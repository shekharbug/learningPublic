import mysql.connector
from mysql.connector import Error

def connect_to_docker_mysql():
    """Connects to the MySQL container and fetches user data."""
    connection = None
    try:
        # Establish the connection
        # Host is 'localhost' because we mapped the port to our host machine
        connection = mysql.connector.connect(
            host='localhost',
            database='my_app_db', # Matches MYSQL_DATABASE from docker run
            user='app_user',     # Matches MYSQL_USER from docker run
            password='app_password', # Matches MYSQL_PASSWORD from docker run
            port=3306
        )

        if connection.is_connected():
            print(f"Successfully connected to MySQL Server version {connection.get_server_info()}")
            cursor = connection.cursor(dictionary=True) # Fetch rows as dictionaries

            # Select data from the 'users' table
            select_query = "SELECT id, name, email, age FROM users"
            cursor.execute(select_query)
            users = cursor.fetchall()

            print("\n--- Users in the Database ---")
            if users:
                # Print header dynamically
                header = list(users[0].keys())
                print(" | ".join([col.ljust(max(len(col), 15)) for col in header])) # Adjust width
                print("-" * (len(" | ".join([col.ljust(max(len(col), 15)) for col in header]))))

                # Print data
                for user in users:
                    row_data = [str(user[col]).ljust(max(len(col), 15)) for col in header]
                    print(" | ".join(row_data))
            else:
                print("No users found in the 'users' table.")

    except Error as e:
        print(f"Error connecting to MySQL or executing query: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    connect_to_docker_mysql()