# Import necessary modules
import uuid
import os
import json
import pathlib


# Define a class called 'Row'
class Row:
    # Initialize the 'Row' object with the provided 'table' and 'data'
    def __init__(self, table, data):
        # Store the 'table' and 'data' attributes
        self.__table__ = table
        self.__data__ = data

        # Generate a primary key if not provided in 'data'
        self.__data__[table.get_primary_key()] = self.__get_primary_key__()

        # Define the path for the lock file
        self.__lock_path__ = os.path.join(self.__table__.get_lock_path(), "{}.json".format(self.get_primary_key()))

    # Get the data stored in the 'Row' object
    def get_data(self):
        return self.__data__

    # Generate a primary key if not provided
    def __get_primary_key__(self):
        primary_key = self.__data__.get(self.__table__.get_primary_key()) if self.__data__.get(
            self.__table__.get_primary_key()) else str(uuid.uuid4().hex)
        return primary_key

    # Get the primary key from 'data'
    def get_primary_key(self):
        return self.__data__[self.__table__.get_primary_key()]

    # Get the path for the row's data file
    def get_row_path(self):
        return os.path.join(self.__table__.get_data_path(), "{}.json".format(self.get_primary_key()))

    # Check if the row's data file exists
    def row_exists(self):
        return os.path.exists(self.get_row_path())

    # Serialize the 'Row' object to a JSON file
    def serialize(self):
        self.__lock__()
        with open(self.get_row_path(), 'w') as file:
            json.dump(self.__data__, file)
        self.__add_to_index__()
        self.__unlock__()

    # Add the data to the associated indices
    def __add_to_index__(self):
        indices = self.__table__.get_indices()
        for index in indices:
            if index != self.__table__.get_primary_key() and index in self.__data__:
                indices[index].add_value(self.__data__[index], self.get_primary_key())

    # Remove the data from the associated indices
    def __delete_index__(self):
        indices = self.__table__.get_indices()
        for index in indices:
            if index != self.__table__.get_primary_key() and index in self.__data__:
                indices[index].remove_value(self.__data__[index], self.get_primary_key())

    # Delete the 'Row' object and its associated data
    def delete(self):
        self.__check_lock__()
        self.__delete_index__()

    # Load a 'Row' object by its primary key
    @staticmethod
    def load_by_primary_key(table, primary_key):
        path = os.path.join(table.get_data_path(), "{}.json".format(primary_key))
        if not (path and os.path.isfile(path)):
            return None
        with open(path, 'r') as file:
            data = json.load(file)
        return Row(table, data)

    # Check if the 'Row' object has the specified attribute values
    def has_attribute(self, query):
        for attribute in query.items():
            if not self.__data__ or attribute[1] != self.__data__[attribute[0]]:
                return False
        return True

    # Lock the 'Row' object to prevent concurrent access
    def __lock__(self):
        try:
            with open(self.__lock_path__, 'x'):
                pass
        except:
            self.__lock__()

    # Check if the 'Row' object is locked and wait until it's unlocked
    def __check_lock__(self):
        while os.path.exists(self.__lock_path__):
            pass

    # Unlock the 'Row' object to allow other operations
    def __unlock__(self):
        pathlib.Path(self.__lock_path__).unlink()
