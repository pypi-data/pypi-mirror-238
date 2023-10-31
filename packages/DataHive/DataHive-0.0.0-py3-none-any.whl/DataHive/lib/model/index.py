# Import necessary modules
import pathlib


# Import custom exceptions and classes
from DataHive.lib.output.exceptions import *
from DataHive.lib.model.index_value import *


# Define an Index class
class Index:
    def __init__(self, index_name, table_metadata):
        # Validate the index name against table columns
        Index.__validate_index__(index_name, table_metadata.columns)

        # Store the index name and build the path for the index
        self.name = index_name
        self.__path__ = os.path.join(table_metadata.get_path(), "indices", self.name)

    # Get the path of the index
    def get_path(self):
        return self.__path__

    # Validate the index name against table columns
    @staticmethod
    def __validate_index__(index_name, table_columns):
        if index_name not in table_columns:
            raise WrongParameterError("Index {} not found in table columns".format(index_name))

    # Serialize the index by creating its directory
    def serialize(self):
        os.makedirs(self.__path__, exist_ok=True)

    # Get primary keys associated with a specific value in the index
    def get_primary_keys(self, value_name):
        return IndexValue(self, value_name).get_primary_keys()

    # Update the primary keys for a specific value in the index
    def __update_value__(self, value_name, primary_keys):
        if not primary_keys:
            pathlib.Path(os.path.join(self.__path__, "{}.json".format(value_name))).unlink()
        else:
            with open(os.path.join(self.__path__, "{}.json".format(value_name)), 'w') as file:
                json.dump(primary_keys, file)

    # Add a primary key to a specific value in the index
    def add_value(self, value_name, primary_key):
        primary_keys = self.get_primary_keys(value_name)
        primary_keys.append(primary_key)
        self.__update_value__(value_name, primary_keys)

    # Remove a primary key from a specific value in the index
    def remove_value(self, value_name, primary_key):
        primary_keys = self.get_primary_keys(value_name)
        if primary_key in primary_keys:
            primary_keys.remove(primary_key)
        self.__update_value__(value_name, primary_keys)

    # Get the IndexValue object for a specific value in the index
    def get_index_value(self, value_name):
        return IndexValue(self, value_name)
