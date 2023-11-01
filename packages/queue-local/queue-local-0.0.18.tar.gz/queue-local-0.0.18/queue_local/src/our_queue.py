import os
import sys
from abc import ABC, abstractmethod

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class OurQueue(ABC):

    @abstractmethod
    def push(self, item):
        """
        Pushes an item to the queue.

        Args:
            item: The item to be pushed to the queue.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Gets an item from the queue and deletes it.

        Returns:
            The item retrieved from the queue.
        """
        pass

    @abstractmethod
    def peek(self):
        """
        Gets the head of the queue without deleting it.

        Returns:
            The item at the head of the queue.
        """
        pass
