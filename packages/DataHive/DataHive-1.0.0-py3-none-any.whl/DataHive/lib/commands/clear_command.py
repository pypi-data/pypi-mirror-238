# Import required classes from custom modules
from DataHive.lib.commands.abstract_command import *
from DataHive.lib.model.database import *


# Define a ClearCommand class that inherits from AbstractCommand
class ClearCommand(AbstractCommand):
    def __init__(self, database_name):
        # Validate the database_name parameter
        ClearCommand.validate(database_name)
        self.database_name = database_name

    # Execute method to clear the specified database
    def execute(self):
        # Create a Database instance with the provided database_name
        database = Database(database_name=self.database_name)
        # Clear the database
        database.clear()

    @staticmethod
    def validate(database_name):
        # Validate that the database_name is not None or empty
        if database_name is None or len(database_name) == 0:
            raise NoParameterError("database_name parameter not entered")
