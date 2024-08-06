class BoundedStack:
    def __init__(self, capacity):
        """
        Initializes a bounded stack with the given capacity.

        Args:
        - capacity (int): The maximum capacity of the bounded stack.
                          Must be a non-negative integer.

        Raises:
        - AssertionError: If capacity is not an integer or if it's negative.
        """
        assert isinstance(capacity, int), ('Error: Type error: %s' % (type(capacity)))
        assert capacity >= 0, ('Error: Illegal capacity: %d' % (capacity))
        self.__items = []  # Initialize the stack as an empty list
        self.__capacity = capacity  # Set the maximum capacity of the stack

    def len(self):
        """
        Returns the number of items in the stack.

        Returns:
        - int: The number of items in the stack.
        """
        return len(self.__items)

    def push(self, item):
        """
        Pushes an item onto the stack.

        Args:
        - item: The item to be pushed onto the stack.
        """
        self.__items.append(item)  # Append the item to the stack
        self.__capacity += 1  # Increase the capacity of the stack

    def pop(self):
        """
        Removes and returns the top item from the stack.

        Returns:
        - The top item from the stack.

        Raises:
        - Exception: If the stack is empty.
        """
        if len(self.__items) == 0:
            raise Exception('empty stack')
        self.__capacity -= 1  # Decrease the capacity of the stack
        return self.__items.pop()

    def peek(self):
        """
        Returns the top item from the stack without removing it.

        Returns:
        - The top item from the stack.

        Raises:
        - Exception: If the stack is empty.
        """
        if len(self.__items) < 1:
            raise Exception('empty stack')
        return self.__items[0]

    def isEmpty(self):
        """
        Checks if the stack is empty.

        Returns:
        - bool: True if the stack is empty, False otherwise.
        """
        return len(self.__items) == 0

    def isFull(self):
        """
        Checks if the stack is full.

        Returns:
        - bool: True if the stack is full, False otherwise.
        """
        if len(self.__items) == self.__capacity:
            return True

    def size(self):
        """
        Returns the number of items in the stack.

        Returns:
        - int: The number of items in the stack.
        """
        return len(self.__items)

    def capacity(self):
        """
        Returns the capacity of the stack.

        Returns:
        - int: The maximum capacity of the stack.
        """
        return self.__capacity

    def clear(self):
        """
        Removes all items from the stack, and sets the size to 0.
        """
        self.__items = []

    def index(self, item):
        """
        Returns the index of the first occurrence of the given item in the stack.

        Args:
        - item: The item to search for in the stack.

        Returns:
        - int: The index of the first occurrence of the item in the stack.
        """
        return self.__item[item]

    def items(self):
        """
        Returns a copy of the items in the stack.

        Returns:
        - list: A copy of the items in the stack.
        """
        return self.__items

    def __str__(self):
        """
        Returns a string representation of the stack.

        Returns:
        - str: A string representation of the stack.
        """
        str_exp = ""
        for item in self.__items:
            str_exp += (str(item) + " ")
        return str_exp

    def __repr__(self):
        """
        Returns a string representation of the bounded stack object.

        Returns:
        - str: A string representation of the bounded stack object.
        """
        return str(self.__items) + " Max=" + str(self.__capacity)

    def with_same_letter(self):
        """
        Checks if all items in the stack are the same letter.

        Returns:
        - bool: True if all items in the stack are the same letter, False otherwise.
        """
        if not self.isEmpty():
            first_element = self.peek()
            return all(item == first_element for item in self.items())
        return False
