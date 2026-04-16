"""
Application configuration for the SQL loading module.

This module centralizes all environment-based configuration values used to:
- connect to MongoDB
- access MongoDB source collections
- connect to MariaDB
"""

from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection settings
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_USERNAME = os.getenv("MONGO_USERNAME", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "root")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "tourisme_data")

# MongoDB source collections
MONGO_COLLECTION_CLEAN = os.getenv("MONGO_COLLECTION_CLEAN", "place_clean")
MONGO_COLLECTION_RATINGS = os.getenv("MONGO_COLLECTION_RATINGS", "place_ratings")

# MariaDB connection settings
SQL_HOST = os.getenv("SQL_HOST", "localhost")
SQL_PORT = int(os.getenv("SQL_PORT", "3306"))
SQL_USER = os.getenv("SQL_USER", "root")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "root")
SQL_DATABASE = os.getenv("SQL_DATABASE", "tourisme_dw")