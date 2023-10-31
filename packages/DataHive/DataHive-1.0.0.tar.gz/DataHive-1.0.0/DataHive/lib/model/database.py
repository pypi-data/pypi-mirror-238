# Import the Table class from a custom module
from DataHive.lib.model.table import *


# Define a Database class
class Database:
    # Define the path to the database storage directory
    DATABASE_PATH = os.path.join(str(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'storage')

    # Initialize the Database instance
    def __init__(self, schema_data=None, database_name=None):
        # Validate the provided schema_data or database_name
        Database.__validate__(schema_data, database_name)

        # Initialize the database based on either schema_data or database_name
        if schema_data:
            self.__initialize_by_schema_data__(schema_data)
        else:
            self.__initialize_by_database_name__(database_name)

    # Initialize the database based on schema_data
    def __initialize_by_schema_data__(self, schema_data):
        # Set the path and database name
        self.__path__ = os.path.join(self.DATABASE_PATH, schema_data[Keys.DATABASE])
        self.__database_name__ = schema_data[Keys.DATABASE]

        # Initialize tables based on schema
        self.tables = {}
        for table_schema in schema_data[Keys.TABLES]:
            self.tables[table_schema[Keys.NAME]] = Table(self, table_schema[Keys.NAME], table_schema)

    # Initialize the database based on database_name
    def __initialize_by_database_name__(self, database_name):
        # Set the path and database name
        self.__path__ = os.path.join(Database.DATABASE_PATH, database_name)

        # Check if the database directory exists
        if not os.path.exists(self.__path__):
            raise WrongParameterError("Wrong database entered")

        self.__database_name__ = database_name

        # Initialize tables based on existing tables in the directory
        self.tables = {}
        for table_name in os.listdir(self.__path__):
            self.tables[table_name] = Table(self, table_name=table_name)

    # Get the path of the database
    def get_path(self):
        return self.__path__

    # Serialize the database by creating directories for tables and serializing tables
    def serialize(self):
        os.makedirs(self.__path__, exist_ok=True)
        self.__serialize_tables__()

    # Validate that either schema_data or database_name is provided
    @staticmethod
    def __validate__(schema_data, database_name):
        if ((schema_data is None or schema_data[Keys.DATABASE].isspace()) and
                (database_name is None or str(database_name).isspace())):
            raise WrongParameterError("No database detected")
        # for table_schema in schema_data[Keys.TABLES]:
        #     if Keys.NAME not in table_schema:
        #         raise WrongParameterError("table name not found in the schema")

    # Serialize all tables in the database
    def __serialize_tables__(self):
        for table_name in self.tables:
            self.tables[table_name].serialize()

    # Get a specific table by name
    def get_table(self, table_name):
        if table_name not in self.tables:
            raise WrongParameterError("Wrong table entered")
        return self.tables[table_name]

    # Set data in a specific table
    def set(self, table_name, data):
        table = self.get_table(table_name)
        table.set(Row(table, data))

    # Clear all tables in the database
    def clear(self):
        for table_name in self.tables:
            self.tables[table_name].clear()

    # Delete data from a specific table
    def delete(self, table_name, data):
        table = self.get_table(table_name)
        table.delete(data)

    # Get data from a specific table based on a query
    def get(self, table_name, query):
        table = self.get_table(table_name)
        rows = table.get(query)
        data = []
        for row in rows:
            data.append(row.get_data())
        return data
