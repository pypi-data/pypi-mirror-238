# Import the ABC module for reference
from abc import ABC


# Define a class to hold constants for keys used in the database schema
class Keys(ABC):
    # Constants for keys
    TABLES = "Tables"
    DATABASE = "database_name"
    NAME = "name"
    COLUMNS = "columns"
    PRIMARY_KEY = "primary_key"
    INDEX_KEYS = "index_keys"
    OVERWRITE = "overwrite"
    CONSISTENCY = "consistency"  # TODO: still not supported
