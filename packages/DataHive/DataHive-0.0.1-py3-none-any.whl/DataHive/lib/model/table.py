# Import necessary modules
import shutil


# Import custom classes and modules
from DataHive.lib.model.table_metadata import *
from DataHive.lib.model.row import *


# Define a Table class
class Table:
    def __init__(self, database, table_name, table_schema=None):
        # Define the path to the table's directory
        self.__path__ = os.path.join(database.get_path(), table_name)

        # Load the table schema if not provided
        if table_schema is None:
            table_schema = TableMetaData.load_table_schema(self.__path__, table_name)
        self.table_schema = table_schema
        self.__table_metadata__ = TableMetaData(self)

    # Serialize the table by creating necessary directories and metadata
    def serialize(self):
        os.makedirs(os.path.join(self.get_data_path()), exist_ok=True)
        os.makedirs(os.path.join(self.__path__, "Lock"), exist_ok=True)
        self.__table_metadata__.serialize()

    # Get the name of the table
    def get_name(self):
        return self.__table_metadata__.name

    # Get the path to the table's directory
    def get_path(self):
        return self.__path__

    # Get the path to the table's data directory
    def get_data_path(self):
        return os.path.join(self.__path__, "data")

    # Get the path to the table's lock directory
    def get_lock_path(self):
        return os.path.join(self.__path__, "lock")

    # Get the primary key column name of the table
    def get_primary_key(self):
        return self.__table_metadata__.primary_key

    # Check if rows can be overwritten in the table
    def can_overwrite(self):
        return eval(self.__table_metadata__.overwrite)

    # Get the indices associated with the table
    def get_indices(self):
        return self.__table_metadata__.index_keys

    # Set a row of data in the table
    def set(self, row):
        primary_key = row.get_primary_key
        existing_row = self.get_by_primary_key(primary_key) if primary_key else None
        if not self.can_overwrite() and row.row_exists():
            raise OverwriteError("data exists")
        existing_row.delete() if existing_row else None
        row.serialize()

    # Delete rows from the table based on a query
    def delete(self, query):
        rows = self.get(query)
        for row in rows:
            row.delete()
            pathlib.Path(row.get_row_path()).unlink()

    # Get rows from the table based on a query
    def get(self, query):
        efficient_index = self.__get_efficient_index__(query)
        if efficient_index is None:
            efficient_keys = self.__get_all_primary_keys__()
        else:
            efficient_keys = efficient_index.get_primary_keys(query[efficient_index])
        found_objects = self.__get_rows__(efficient_keys)
        return self.__filter_by_query__(found_objects, query)

    # Determine the most efficient index for a query
    def __get_efficient_index__(self, query):
        if not query or str(query).isspace:
            return None
        efficient_value = None
        for index_name in query.keys():
            current_index = self.__table_metadata__.get_index(index_name)
            current_value = current_index.get_index_value(query[index_name])
            if current_index and (not efficient_value or current_value.compare(efficient_value)) > 0:
                efficient_value = current_value
        return efficient_value.get_index()

    # Get all primary keys in the table
    def __get_all_primary_keys__(self):
        primary_keys = []
        for primary_key in os.listdir(self.get_data_path()):
            primary_keys.append(primary_key.replace(".json", ""))
        return primary_keys

    # Get a row by its primary key from the table
    def get_by_primary_key(self, primary_key):
        return Row.load_by_primary_key(self, primary_key)

    # Filter rows by a query
    @staticmethod
    def __filter_by_query__(found_objects, query):
        if not query or str(query).isspace():
            return found_objects
        filtered_objects = []
        for object_to_compare in found_objects:
            if object_to_compare and object_to_compare.has_attribute(query):
                filtered_objects.append(object_to_compare)
        return filtered_objects

    # Get rows based on primary keys
    def __get_rows__(self, primary_keys):
        rows = []
        for primary_key in primary_keys:
            rows.append(self.get_by_primary_key(str(primary_key)))
        return rows

    # Clear the table by removing its contents
    def clear(self):
        for table_element in os.listdir(self.__path__):
            path = os.path.join(self.__path__, table_element)
            if os.path.isdir(path):
                shutil.rmtree(path)
                os.mkdir(path)

    # Compare two objects by their attributes
    @staticmethod
    def compare(object_1, object_2):
        for attribute in object_2.items():
            if not object_1 or attribute[1] != object_1[attribute[0]]:
                return False
        return True
