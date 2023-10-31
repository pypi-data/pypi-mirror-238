# Import custom classes and exceptions
from DataHive.lib.commands.abstract_command import *
from DataHive.lib.model.database import *


# Define a GetCommand class that inherits from AbstractCommand
class GetCommand(AbstractCommand):
    def __init__(self, database_name, table_name, query):
        # Validate the database_name and table_name parameters
        GetCommand.validate(database_name, table_name)

        # Store the database_name and table_name
        self.database_name = database_name
        self.table_name = table_name

        # Parse and store the query as a dictionary or use an empty dictionary if query is None or empty
        self.query = {} if not query else eval(query)

    # Execute method to retrieve data from the specified table in the database
    def execute(self):
        # Create a Database instance with the specified database_name
        database = Database(database_name=self.database_name)
        # Call the get method on the database to retrieve data from the table
        return database.get(self.table_name, self.query)

    @staticmethod
    def validate(database_name, table_name):
        # Validate the database_name and table_name parameters
        if database_name is None or database_name == "" or database_name == " ":
            raise NoParameterError("Database parameter not entered")
        if table_name is None or table_name == "" or table_name == " ":
            raise NoParameterError("Table parameter not entered")
