# Import custom classes
from DataHive.lib.commands.abstract_command import *
from DataHive.lib.model.database import *


# Define a CreateCommand class that inherits from AbstractCommand
class CreateCommand(AbstractCommand):
    def __init__(self, schema_path):
        # Validate the schema_path parameter
        CreateCommand.__validate__(schema_path)

        # Store the schema_path and retrieve the schema data
        self.schema_path = schema_path
        self.schema_data = CreateCommand.__get_database_schema__(schema_path)

    # Execute method to create a database based on the schema
    def execute(self):
        # Create a Database instance using the schema data
        database = Database(self.schema_data)
        # Serialize and store the database
        database.serialize()

    @staticmethod
    def __validate__(schema_path):
        # Check if the schema_path is empty or None
        if not schema_path:
            raise NoParameterError("schema_path parameter not entered")

        # Check if the schema file exists
        if not os.path.isfile(schema_path):
            raise WrongParameterError("Schema doesn't exist")

    @staticmethod
    def __get_database_schema__(schema_path):
        # Read and load the schema data from the specified file
        with open(schema_path, 'r') as file:
            return json.load(file)
