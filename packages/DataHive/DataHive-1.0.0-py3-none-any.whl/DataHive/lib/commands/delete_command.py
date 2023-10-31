# Import custom classes
from DataHive.lib.commands.abstract_command import *
from DataHive.lib.model.database import *


# Define a DeleteCommand class that inherits from AbstractCommand
class DeleteCommand(AbstractCommand):
    def __init__(self, database_name, table_name, query):
        # Store the query and validate the database_name and query
        self.query = DeleteCommand.validate(database_name, query)
        self.database_name = database_name
        self.table_name = table_name

    # Execute method to delete records from the specified table in the database
    def execute(self):
        # Create a Database instance with the specified database_name
        database = Database(database_name=self.database_name)
        # Call the delete method on the database to delete records from the table
        database.delete(self.table_name, self.query)

    @staticmethod
    def validate(database_name, query):
        # Validate the database_name parameter
        if not database_name:
            raise NoParameterError("database_name parameter not entered")

        try:
            # Validate and parse the query
            if query == "None":
                raise NoParameterError("data parameter not entered")
            return eval(query)
        except:
            raise NoParameterError("data parameter not entered")
