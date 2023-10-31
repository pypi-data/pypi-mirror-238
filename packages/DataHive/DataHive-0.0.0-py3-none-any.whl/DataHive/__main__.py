# Import necessary modules and classes from your application
from DataHive.lib.input_adaptors.input import *
from DataHive.lib.commands.command_factory import *
from DataHive.lib.input_adaptors.parser_adaptor import *
from DataHive.lib.output.output_message import *


def main():
    # Try to execute commands and handle exceptions
    try:
        # Create an input adaptor by parsing command-line arguments
        input_adaptor = ParsedInput(parse_args())

        # Create a command based on the input
        command = CommandFactory(input_adaptor).create()

        # Execute the command and capture the result
        result = command.execute()

        # Create an OutputMessage object with the command name and result
        output_object = OutputMessage(command_name=input_adaptor.command, result=result)

    except Exception as e:
        # If an exception occurs, create an OutputMessage object with the exception
        output_object = OutputMessage(exception=e)

    # Print the attributes of the output_object as a dictionary
    print(output_object.__dict__)


if __name__ == "__main__":
    main()
