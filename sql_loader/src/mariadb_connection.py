import mysql.connector
from .configs import SQL_HOST, SQL_PORT, SQL_USER, SQL_PASSWORD, SQL_DATABASE


class MariaDBConnection:
    """
    Handle the connection lifecycle to the MariaDB server and database.

    This class is responsible only for:
    - connecting to the MariaDB server
    - creating the target database if needed
    - reconnecting to the selected database
    - committing and closing the connection
    """

    def __init__(self):
        """
        Initialize the MariaDB connection wrapper.
        """
        self.connection = None
        self.cursor = None

    def connect_server(self):
        """
        Connect to the MariaDB server without selecting a database first.
        """
        self.connection = mysql.connector.connect(
            host=SQL_HOST,
            port=SQL_PORT,
            user=SQL_USER,
            password=SQL_PASSWORD,
        )
        self.cursor = self.connection.cursor()

    def create_database_if_not_exists(self):
        """
        Create the target MariaDB database if it does not already exist.
        """
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {SQL_DATABASE}")
        self.connection.commit()

    def reconnect_to_database(self):
        """
        Reconnect to MariaDB and select the target database.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

        self.connection = mysql.connector.connect(
            host=SQL_HOST,
            port=SQL_PORT,
            user=SQL_USER,
            password=SQL_PASSWORD,
            database=SQL_DATABASE,
        )
        self.cursor = self.connection.cursor()

    def commit(self):
        """
        Commit the current transaction.
        """
        self.connection.commit()

    def disconnect(self):
        """
        Close the MariaDB cursor and connection if they are open.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()