# Import the enum module
import enum


# Define an enumeration class Status
class Status(enum.Enum):
    # Define enumeration members with associated integer values
    Success = 0  # Indicates a successful operation
    NoParameterError = 1  # Indicates an error due to missing parameters
    WrongParameterError = 2  # Indicates an error due to incorrect parameters
    OverwriteError = 3  # Indicates an error related to overwriting existing data
