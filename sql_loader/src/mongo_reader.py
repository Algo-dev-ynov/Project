from pymongo import MongoClient
from .configs import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_DATABASE,
    MONGO_COLLECTION_CLEAN,
    MONGO_COLLECTION_RATINGS,
)


class MongoReader:
    """
    Handle the connection to MongoDB and provide access to source collections.

    This class is responsible only for:
    - connecting to MongoDB
    - returning the collections needed for SQL export
    - closing the MongoDB connection
    """

    def __init__(self):
        """
        Initialize the MongoDB reader.
        """
        self.client = None
        self.db = None

    def connect(self):
        """
        Open the MongoDB connection and select the target database.
        """
        # Build the authenticated MongoDB connection string from configuration values.
        connection_string = (
            f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@"
            f"{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
        )

        # Open the client and select the configured source database.
        self.client = MongoClient(connection_string)
        self.db = self.client[MONGO_DATABASE]

    def get_clean_collection(self):
        """
        Return the MongoDB collection containing cleaned places.

        Returns:


            The `place_clean` MongoDB collection.
        """
        # This collection is the main source used to populate SQL place tables.
        return self.db[MONGO_COLLECTION_CLEAN]

    def get_ratings_collection(self):
        """
        Return the MongoDB collection containing generated ratings.

        Returns:

        
            The `place_ratings` MongoDB collection.
        """
        # This collection is used to populate the SQL ratings table.
        return self.db[MONGO_COLLECTION_RATINGS]

    def disconnect(self):
        """
        Close the MongoDB connection if it is open.
        """
        # Close the client only if a connection has been initialized.
        if self.client:
            self.client.close()