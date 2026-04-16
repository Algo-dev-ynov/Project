from .normalizer import SQLValueNormalizer


class PlaceExporter:
    """
    Export the cleaned place documents from MongoDB to MariaDB.

    This class is responsible only for exporting data related to:
    - places
    - place types
    - contacts
    """

    def __init__(self, mongo_reader, sql_connection):
        """
        Initialize the place exporter.

        Args:

        
            mongo_reader: Object used to access MongoDB collections.
            sql_connection: Active MariaDB connection wrapper.
        """
        self.mongo_reader = mongo_reader
        self.sql_connection = sql_connection
        self.cursor = sql_connection.cursor

    def export(self):
        """
        Export all cleaned place records from MongoDB into MariaDB.

        The method reads documents from the `place_clean` collection and
        distributes their data into three relational tables:
        - places
        - place_types
        - contacts
        """
        clean_collection = self.mongo_reader.get_clean_collection()

        insert_place_query = """
            INSERT INTO places (
                uuid, mongo_id, label, description, price, uri,
                latitude, longitude, street_address, address_locality, postal_code
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        insert_type_query = """
            INSERT INTO place_types (uuid, type_value)
            VALUES (%s, %s)
        """

        insert_contact_query = """
            INSERT INTO contacts (uuid, name, email, telephone, homepage)
            VALUES (%s, %s, %s, %s, %s)
        """

        for record in clean_collection.find():
            # Insert one cleaned MongoDB document into the three SQL target tables.
            self._insert_place(record, insert_place_query)
            self._insert_place_types(record, insert_type_query)
            self._insert_contact(record, insert_contact_query)

        # Commit once after the full export to persist all inserted rows.
        self.sql_connection.commit()

    def _insert_place(self, record, query):
        """
        Insert the main place information into the `places` table.

        Args:


            record: One MongoDB document from `place_clean`.
            query: SQL insert query for the `places` table.
        """
        # Nested MongoDB objects are extracted first to simplify SQL insertion.
        geo = record.get("geo") or {}
        address = record.get("address") or {}

        self.cursor.execute(
            query,
            (
                SQLValueNormalizer.normalize(record.get("uuid")),
                SQLValueNormalizer.normalize(record.get("_id")),
                SQLValueNormalizer.normalize(record.get("label")),
                SQLValueNormalizer.normalize(record.get("description")),
                record.get("price"),
                SQLValueNormalizer.normalize(record.get("uri")),
                geo.get("latitude"),
                geo.get("longitude"),
                SQLValueNormalizer.normalize(address.get("streetAddress")),
                SQLValueNormalizer.normalize(address.get("addressLocality")),
                SQLValueNormalizer.normalize(address.get("postalCode")),
            ),
        )

    def _insert_place_types(self, record, query):
        """
        Insert all type values of a place into the `place_types` table.

        Args:


            record: One MongoDB document from `place_clean`.
            query: SQL insert query for the `place_types` table.
        """
        uuid = SQLValueNormalizer.normalize(record.get("uuid"))

        # A place can belong to multiple types, so one SQL row is inserted per type.
        for type_value in record.get("type", []):
            self.cursor.execute(
                query,
                (
                    uuid,
                    SQLValueNormalizer.normalize(type_value),
                ),
            )

    def _insert_contact(self, record, query):
        """
        Insert the contact information of a place into the `contacts` table.

        A contact row is inserted only if at least one contact field is present.

        Args:


            record: One MongoDB document from `place_clean`.
            query: SQL insert query for the `contacts` table.
        """
        contact = record.get("contact") or {}

        contact_name = contact.get("name")
        email = contact.get("email")
        telephone = contact.get("telephone")
        homepage = contact.get("homepage")

        # Avoid inserting empty contact rows when no contact information is available.
        if any([contact_name, email, telephone, homepage]):
            self.cursor.execute(
                query,
                (
                    SQLValueNormalizer.normalize(record.get("uuid")),
                    SQLValueNormalizer.normalize(contact_name),
                    SQLValueNormalizer.normalize(email),
                    SQLValueNormalizer.normalize(telephone),
                    SQLValueNormalizer.normalize(homepage),
                ),
            )


class RatingExporter:
    """
    Export rating documents from MongoDB to MariaDB.

    This class is responsible only for exporting data from the
    `place_ratings` collection into the `ratings` table.
    """

    def __init__(self, mongo_reader, sql_connection):
        """
        Initialize the rating exporter.

        Args:


            mongo_reader: Object used to access MongoDB collections.
            sql_connection: Active MariaDB connection wrapper.
        """
        self.mongo_reader = mongo_reader
        self.sql_connection = sql_connection
        self.cursor = sql_connection.cursor

    def export(self):
        """
        Export all rating documents from MongoDB into the `ratings` table.
        """
        ratings_collection = self.mongo_reader.get_ratings_collection()

        insert_rating_query = """
            INSERT INTO ratings (uuid, rating, comment)
            VALUES (%s, %s, %s)
        """

        for record in ratings_collection.find():
            # Insert each generated rating into the SQL ratings table.
            self._insert_rating(record, insert_rating_query)

        # Commit once after exporting all rating records.
        self.sql_connection.commit()

    def _insert_rating(self, record, query):
        """
        Insert one rating record into the `ratings` table.

        Args:


            record: One MongoDB document from `place_ratings`.
            query: SQL insert query for the `ratings` table.
        """
        self.cursor.execute(
            query,
            (
                SQLValueNormalizer.normalize(record.get("uuid")),
                record.get("rating"),
                SQLValueNormalizer.normalize(record.get("comment")),
            ),
        )