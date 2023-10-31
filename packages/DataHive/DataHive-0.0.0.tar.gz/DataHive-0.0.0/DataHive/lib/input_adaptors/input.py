# Import the argparse module for parsing command-line arguments
import argparse


# Define a function called parse_args() for parsing command-line arguments
def parse_args():
    # Create an ArgumentParser object with a simplified description
    parser = argparse.ArgumentParser(
        prog='DataHive',
        description="DataHive - A tool for managing JSON file databases.")

    # Define command-line arguments and their types, as well as improved help messages and examples
    parser.add_argument(
        '-c',
        "--command",
        type=str,
        help="Specify the operation (create, get, set, or delete).",
        choices=["create", "get", "set", "delete"],
        required=True  # Make the 'command' argument required
    )
    parser.add_argument(
        "-sc",
        "--schema_path",
        type=str,
        help="Specify the path to the JSON schema file defining the database structure."
    )
    parser.add_argument(
        "-db",
        "--database",
        type=str,
        help="Specify the name of the database where the data is stored."
    )
    parser.add_argument(
        "-t",
        "--table",
        type=str,
        help="Specify the name of a specific table in the database."
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Specify a query string to filter data (for 'get' or 'delete' operations)."
    )

    # Parse the command-line arguments and return the result
    return parser.parse_args()
