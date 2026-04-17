from sql_loader.src.mariadb_connection import MariaDBConnection
from sql_loader.src.schema import SchemaManager


def test_mariadb_connection_and_schema_creation():
    sql_connection = MariaDBConnection()

    try:
        sql_connection.connect_server()
        sql_connection.create_database_if_not_exists()
        sql_connection.reconnect_to_database()

        schema_manager = SchemaManager(sql_connection)
        schema_manager.create_tables()

        sql_connection.cursor.execute("SHOW TABLES")
        tables = {row[0] for row in sql_connection.cursor.fetchall()}

        assert "places" in tables
        assert "place_types" in tables
        assert "contacts" in tables
        assert "ratings" in tables

    finally:
        sql_connection.disconnect()


def test_truncate_tables_runs_successfully():
    sql_connection = MariaDBConnection()

    try:
        sql_connection.connect_server()
        sql_connection.create_database_if_not_exists()
        sql_connection.reconnect_to_database()

        schema_manager = SchemaManager(sql_connection)
        schema_manager.create_tables()
        schema_manager.truncate_tables()

        sql_connection.cursor.execute("SELECT COUNT(*) FROM places")
        places_count = sql_connection.cursor.fetchone()[0]

        sql_connection.cursor.execute("SELECT COUNT(*) FROM place_types")
        place_types_count = sql_connection.cursor.fetchone()[0]

        sql_connection.cursor.execute("SELECT COUNT(*) FROM contacts")
        contacts_count = sql_connection.cursor.fetchone()[0]

        sql_connection.cursor.execute("SELECT COUNT(*) FROM ratings")
        ratings_count = sql_connection.cursor.fetchone()[0]

        assert places_count == 0
        assert place_types_count == 0
        assert contacts_count == 0
        assert ratings_count == 0

    finally:
        sql_connection.disconnect()