# Import custom command classes
from DataHive.lib.commands.create_command import *
from DataHive.lib.commands.set_command import *
from DataHive.lib.commands.get_command import *
from DataHive.lib.commands.delete_command import *
from DataHive.lib.commands.clear_command import *


# Define a CommandFactory class
class CommandFactory:
    def __init__(self, input_adaptor):
        # Define a set of available commands
        available_commands = {"create", "set", "get", "delete", "clear"}

        # Validate the input_adaptor and available_commands
        CommandFactory.validate(input_adaptor, available_commands)

        # Store the input_adaptor for creating commands
        self.input_adaptor = input_adaptor

    # Create and return an appropriate command based on the input command
    def create(self):
        cmd = str(self.input_adaptor.command).lower()
        if cmd == "create":
            return CreateCommand(self.input_adaptor.schema_path)
        elif cmd == "set":
            return SetCommand(self.input_adaptor.database, self.input_adaptor.table, self.input_adaptor.query)
        elif cmd == "get":
            return GetCommand(self.input_adaptor.database, self.input_adaptor.table, self.input_adaptor.query)
        elif cmd == "delete":
            return DeleteCommand(self.input_adaptor.database, self.input_adaptor.table, self.input_adaptor.query)
        elif cmd == "clear":
            return ClearCommand(self.input_adaptor.database)

    @staticmethod
    def validate(input_adaptor, available_commands):
        # Check if the input command is in the set of available commands
        if input_adaptor.command not in available_commands:
            raise WrongParameterError("Wrong command entered")
