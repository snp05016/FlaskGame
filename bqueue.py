class BoundedQueue:
    """
    A class representing a bounded queue.

    Attributes:
    - __items: A list representing the elements in the queue.
    - __capacity: An integer representing the maximum capacity of the queue.
    """

    def __init__(self, capacity):
        """
        Initializes a new bounded queue with the given capacity.

        Args:
        - capacity: An integer representing the maximum capacity of the queue.
        """
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity)))
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))
        self.__items = []
        self.__capacity = capacity

    def enqueue(self, item):
        """
        Adds a new item to the back of the queue.

        Args:
        - item: The element to be enqueued.

        Raises:
        - Exception: If the queue is full.
        """
        if len(self.__items) >= self.__capacity:
            raise Exception('Error: Queue is full')
        self.__items.append(item)

    def dequeue(self):
        """
        Removes and returns the front-most item in the queue.

        Returns:
        - The object that was dequeued.

        Raises:
        - Exception: If the queue is empty.
        """
        if len(self.__items) <= 0:
            raise Exception('Error: Queue is empty')
        return self.__items.pop(0)

    def peek(self):
        """
        Returns the front-most item in the queue without removing it.

        Returns:
        - The object at the front of the queue.

        Raises:
        - Exception: If the queue is empty.
        """
        if len(self.__items) <= 0:
            raise Exception('Error: Queue is empty')
        return self.__items[0]

    def isEmpty(self):
        """
        Checks if the queue is empty.

        Returns:
        - True if the queue is empty, False otherwise.
        """
        return len(self.__items) == 0

    def isFull(self):
        """
        Checks if the queue is full.

        Returns:
        - True if the queue is full, False otherwise.
        """
        return len(self.__items) == self.__capacity

    def size(self):
        """
        Returns the number of items in the queue.

        Returns:
        - The number of items in the queue.
        """
        return len(self.__items)

    def capacity(self):
        """
        Returns the maximum capacity of the queue.

        Returns:
        - The maximum capacity of the queue.
        """
        return self.__capacity

    def clear(self):
        """
        Removes all items from the queue, resetting its size to 0.
        """
        self.__items = []

    def __str__(self):
        """
        Returns a string representation of the queue.

        Returns:
        - A string representation of the queue.
        """
        str_exp = ""
        for item in self.__items:
            str_exp += (str(item) + " ")
        return str_exp

    def __repr__(self):
        """
        Returns a string representation of the object bounded queue.

        Returns:
        - A string representation of the object bounded queue.
        """
        return str(self) + " Max=" + str(self.__capacity)
