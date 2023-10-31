# Import the `abstractmethod` decorator from the `abc` module
from abc import abstractmethod


# Define an abstract base class called `AbstractCommand`
class AbstractCommand:
    # Declare an abstract method called `execute`
    @abstractmethod
    def execute(self):
        pass
