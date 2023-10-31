# Import necessary modules
import os
import json


# Define an IndexValue class
class IndexValue:
    def __init__(self, index, value_name):
        # Store the index and value_name
        self.__index__ = index
        self.__value_name__ = value_name

    # Get primary keys associated with this index value
    def get_primary_keys(self):
        # Check if this is a PrimaryKeyIndex (only one primary key)
        if "PrimaryKeyIndex" in str(self.__index__.__class__):
            return [self.__value_name__]

        primary_keys = []
        path = os.path.join(self.__index__.get_path(), "{}.json".format(self.__value_name__))
        # Read primary keys from a JSON file if it exists
        if os.path.isfile(path):
            with open(path, 'r') as file:
                primary_keys = json.load(file)
        return primary_keys

    # Compare this index value with another index value
    def compare(self, value_to_compare):
        # Compare the number of primary keys associated with each value
        first_value = len(self.get_primary_keys())
        second_value = len(value_to_compare.get_primary_keys())
        return first_value - second_value

    # Get the parent index object
    def get_index(self):
        return self.__index__
