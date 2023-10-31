# Import custom classes and modules
from DataHive.lib.output.status import *


# Define an OutputMessage class to encapsulate command execution results
class OutputMessage:
    def __init__(self, command_name=None, result=None, exception=None):
        # Store the result of the command execution
        self.result = result

        # Determine the status based on whether an exception occurred
        self.status = Status.Success.name if exception is None else exception.status_code

        # Generate a message based on the command's success or the exception message
        self.message = command_name + " is a success" if exception is None else str(exception)
