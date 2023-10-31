# Import custom classes
from DataHive.lib.commands.abstract_command import *
from DataHive.lib.model.database import *


# Define a SetCommand class that inherits from AbstractCommand
class SetCommand(AbstractCommand):
    def __init__(self, database_name, table_name, data):
        # Store the data and validate the database_name and data
        self.data = SetCommand.validate(database_name, data)
        self.database_name = database_name
        self.table_name = table_name

    # Execute method to set data in the specified table of the database
    def execute(self):
        # Create a Database instance with the specified database_name
        database = Database(database_name=self.database_name)
        # Call the set method on the database to set data in the table
        database.set(self.table_name, self.data)

    @staticmethod
    def validate(database_name, data):
        # Validate the database_name parameter
        if database_name is None or len(database_name) == 0:
            raise NoParameterError("database_name parameter not entered")

        try:
            # Validate and parse the data
            if data == "None":
                raise NoParameterError("data parameter not entered")
            return eval(data)
        except:
            raise NoParameterError("data parameter not entered")
