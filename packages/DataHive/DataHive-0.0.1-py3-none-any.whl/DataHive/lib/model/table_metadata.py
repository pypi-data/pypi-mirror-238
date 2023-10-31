# Import custom classes and modules
from DataHive.lib.model.primary_key_index import *
from DataHive.lib.model.schema_keys import Keys


# Define a TableMetaData class
class TableMetaData:
    def __init__(self, table):
        # Validate the table schema
        TableMetaData.__validate__(table.table_schema)

        # Set attributes based on the table schema
        self.__path__ = table.get_path()
        self.name = table.table_schema[Keys.NAME]
        self.primary_key = table.table_schema[Keys.PRIMARY_KEY]
        self.columns = table.table_schema[Keys.COLUMNS]
        self.overwrite = table.table_schema[Keys.OVERWRITE]
        self.index_keys = {self.primary_key: PrimaryKeyIndex(self.primary_key, self)}

        # Create Index objects for each defined index in the schema
        for index_name in table.table_schema.get(Keys.INDEX_KEYS):
            self.index_keys[index_name] = Index(index_name, self)

    # Get the path to the table's directory
    def get_path(self):
        return self.__path__

    # Serialize the table schema and associated indices
    def serialize(self):
        # Create the table schema JSON file
        TableMetaData.__create_table_schema__(self.__dict__, self.__path__)

        # Create necessary directories for indices
        os.makedirs(self.__path__, exist_ok=True)

        # Serialize the indices
        self.__serialize_indices__()

    # Validate the table schema
    @staticmethod
    def __validate__(table_schema):
        if Keys.COLUMNS not in table_schema:
            raise WrongParameterError("columns not found in the schema")
        if Keys.PRIMARY_KEY is table_schema and table_schema[Keys.PRIMARY_KEY] is None:
            raise WrongParameterError("Primary_key not found in the schema")
        if table_schema[Keys.PRIMARY_KEY] not in table_schema[Keys.COLUMNS]:
            raise WrongParameterError(f"Primary_key {table_schema[Keys.PRIMARY_KEY]} not found in the table: {table_schema[Keys.NAME]} schema")
        if Keys.INDEX_KEYS not in table_schema:
            table_schema[Keys.INDEX_KEYS] = []
        if Keys.OVERWRITE not in table_schema:
            table_schema[Keys.OVERWRITE] = False

    # Create the table schema JSON file
    @staticmethod
    def __create_table_schema__(table_schema, path):
        indices = table_schema[Keys.INDEX_KEYS]
        table_schema.update({Keys.INDEX_KEYS: TableMetaData.get_indices_names(table_schema[Keys.INDEX_KEYS])})
        with open(os.path.join(path, "{}_schema.json".format(table_schema[Keys.NAME])), 'w') as file:
            json.dump(table_schema, file)
        table_schema.update({Keys.INDEX_KEYS: indices})

    # Serialize the indices associated with the table
    def __serialize_indices__(self):
        for index_name in self.index_keys:
            self.index_keys[index_name].serialize()

    # Get names of defined indices
    @staticmethod
    def get_indices_names(index_keys):
        indices_names = []
        for index_name in index_keys:
            indices_names.append(index_name)
        return indices_names

    # Load the table schema from a JSON file
    @staticmethod
    def load_table_schema(path, table_name):
        with open(os.path.join(path, "{}_schema.json".format(table_name)), 'r') as file:
            return json.load(file)

    # Get an index by its name
    def get_index(self, index_name):
        for index in self.index_keys:
            if index.name == index_name:
                return index
        return None

    # Get primary keys associated with a specific index and value
    def get_index_primary_keys(self, index_name, index_value):
        for index in self.index_keys:
            if index.name == index_name:
                return index.get_primary_keys(index_value)
        raise WrongParameterError("Wrong index name entered")
