from .src.mongo_reader import MongoReader
from .src.mariadb_connection import MariaDBConnection
from .src.schema import SchemaManager
from .src.exporter import PlaceExporter, RatingExporter


def main():
    """
    Run the full export pipeline from MongoDB to MariaDB.

    Workflow:
    1. Connect to MongoDB.
    2. Connect to MariaDB.
    3. Create the target database and tables.
    4. Truncate tables before reloading data.
    5. Export places and ratings.
    """
    mongo_reader = MongoReader()
    sql_connection = MariaDBConnection()

    try:
        # Open connections to both the source MongoDB and the target MariaDB server.
        mongo_reader.connect()

        sql_connection.connect_server()
        sql_connection.create_database_if_not_exists()
        sql_connection.reconnect_to_database()

        # Prepare the SQL schema before loading fresh data.
        schema_manager = SchemaManager(sql_connection)
        schema_manager.create_tables()
        schema_manager.truncate_tables()

        # Launch the export in two separate responsibilities: places and ratings.
        place_exporter = PlaceExporter(mongo_reader, sql_connection)
        rating_exporter = RatingExporter(mongo_reader, sql_connection)

        place_exporter.export()
        rating_exporter.export()

        print("Export MongoDB -> MariaDB terminé avec succès.")

    finally:
        # Always close database connections, even if an error occurs during export.
        mongo_reader.disconnect()
        sql_connection.disconnect()


if __name__ == "__main__":
    main()