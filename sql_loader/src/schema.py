class SchemaManager:
    """
    Manage the creation and reset of the MariaDB schema used for SQL export.

    This class is responsible only for:
    - creating the relational tables
    - truncating tables before a full reload
    """

    def __init__(self, sql_connection):
        """
        Initialize the schema manager.

        Args:

        
            sql_connection: Active MariaDB connection wrapper.
        """
        self.sql_connection = sql_connection
        self.cursor = sql_connection.cursor

    def create_tables(self):
        """
        Create all required tables in the target MariaDB database
        if they do not already exist.
        """
        # Main relational table containing the cleaned place information.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS places (
                uuid VARCHAR(255) PRIMARY KEY,
                mongo_id VARCHAR(255),
                label TEXT,
                description TEXT,
                price INT,
                uri TEXT,
                latitude DECIMAL(10, 7),
                longitude DECIMAL(10, 7),
                street_address TEXT,
                address_locality VARCHAR(255),
                postal_code VARCHAR(50)
            )
        """)

        # Child table used to store one or more types for each place.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS place_types (
                uuid VARCHAR(255),
                type_value VARCHAR(255),
                FOREIGN KEY (uuid) REFERENCES places(uuid)
            )
        """)

        # Child table used to store contact information when available.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                uuid VARCHAR(255),
                name TEXT,
                email TEXT,
                telephone TEXT,
                homepage TEXT,
                FOREIGN KEY (uuid) REFERENCES places(uuid)
            )
        """)

        # Ratings table populated from the generated MongoDB rating collection.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INT PRIMARY KEY AUTO_INCREMENT,
                uuid VARCHAR(255),
                rating INT,
                comment TEXT,
                FOREIGN KEY (uuid) REFERENCES places(uuid)
            )
        """)

        # Persist schema creation once all tables are defined.
        self.sql_connection.commit()

    def truncate_tables(self):
        """
        Empty all target tables before reloading the exported data.

        Foreign key checks are temporarily disabled to allow truncation
        in the correct order.
        """
        # Disable foreign key checks to safely truncate dependent tables.
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("TRUNCATE TABLE ratings")
        self.cursor.execute("TRUNCATE TABLE contacts")
        self.cursor.execute("TRUNCATE TABLE place_types")
        self.cursor.execute("TRUNCATE TABLE places")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        # Persist the cleanup before launching a new full load.
        self.sql_connection.commit()