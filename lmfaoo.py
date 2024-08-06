import os
from bqueue import BoundedQueue
from bstack import BoundedStack

MAX = 3         # Max no of elements the flask can hold
flask_size = 4  # Size of the flask
ANSI = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "HRED": "\033[41m",
    "HGREEN": "\033[42m",
    "HBLUE": "\033[44m",
    "HORANGE": "\033[48;2;255;165;0m",
    "HYELLOW": "\033[43m",
    "HMAGENTA": "\033[45m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m",
    "CLEARLINE": "\033[0K"
}
# Storing the respective colors for each chemical
COLORS = {'AA': ANSI['HRED'], 'BB': ANSI['HBLUE'], 'CC': ANSI['HGREEN'],
          'DD': ANSI['HORANGE'], 'EE': ANSI['HYELLOW'], 'FF': ANSI['HMAGENTA']}

def print_location(x, y, text):
    '''
    Prints text at the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
        - text (str): text to print
    Returns: N/A
    '''
    print("\033[{1};{0}H{2}".format(x, y, text))
    
def move_cursor(x, y):
    '''
    Moves the cursor to the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
    Returns: N/A
    '''
    print("\033[{1};{0}H".format(x, y), end='')

def clear_screen():
    '''
    Clears the terminal screen for future contents.
    Input: N/A
    Returns: N/A
    '''
    if os.name == "nt":  # Windows
        os.system("cls")
    else:
        os.system("clear")  # Unix (mac, linux, etc.)

def read_chemical_data():
    '''
    Read the chemical data from the file and initialize stacks.
    Open the file 'chemicals.txt' in read mode.
    '''
    with open('6chemicals.txt', 'r') as file:
        # Read the first line of the file
        firstline = file.readline()
        firstline = firstline.strip()  
        # Extract the number of flasks and chemicals from the first line
        num_flask = int(firstline[0])
        num_chemicals = int(firstline[2])
        # Read the chemical data from the file
        chemical_data = file.readlines()
        # Create a BoundedQueue to store chemicals temporarily
        queue = BoundedQueue(flask_size)
        # Create a list of BoundedStacks to represent the flasks
        stacks = [BoundedStack(flask_size) for i in range(num_flask)]
        
        # Iterate over each line of chemical data
        for line in chemical_data:
            line = line.strip()  # Remove leading/trailing whitespace
            
            # Check if the line indicates a pour operation
            if 'F' in line and len(line) >= 3:
                # Extract information about flask number and from which flask to dequeue
                flask_number_to_dequeue = int(line[0])
                from_flask = int(line[len(line)-1])
                dequeue_into = from_flask - 1  # Adjust for zero-based indexing
                
                # Dequeue chemicals from the queue and enqueue into the specified flask
                for j in range(flask_number_to_dequeue):
                    stacks[dequeue_into].push(queue.dequeue())
            else:
                # If the line is not a pour operation, enqueue the chemical into the queue
                if not queue.isFull():
                    queue.enqueue(line)
    return num_flask, num_chemicals, stacks

def string_stacks(stacks, source_flask=None, destination_flask=None):
    """
    Generate a string representation of the current state of the flasks.

    Args:
        stacks (list): A list of BoundedStack objects representing the flasks.
        source_flask (int): Index of the source flask.
        dest_flask (int): Index of the destination flask.

    Returns:
        str: A string representing the current state of the flasks, with chemicals colored
             according to their type and stack numbers labeled at the bottom.
    """
    result = ""  # Initialize an empty string to store the result
    
    # Loop through the rows of the flasks from top to bottom
    for i in range(flask_size - 1, -1, -1):
        # Loop through each stack (flask) in the list of stacks
        for stack_index, stack in enumerate(stacks):
            try:
                if not stack.isEmpty():
                    # Get the item at index i from the current stack
                    item = stack.items()[i]
                    # Add background color based on chemical type and center the item in the cell
                    result += f"|{COLORS[item]}{item:^2}{ANSI['RESET']}|  "
                else:
                    # If the stack is empty, add an empty cell
                    result += "|  |  "
            except IndexError:
                # Handle the case when accessing an index that is out of range for the stack
                if stack.is_full_with_same_letter() and stack.len() == MAX:
                    if i == flask_size - 1:
                        result += "+--+  "  # Print +--+ only once at the top of a full flask
                    else:
                        result += "|  |  "  # Otherwise, add an empty cell
                else:
                    result += "|  |  "  # Add an empty cell if the stack is not full
            # Add a newline if this is the last stack in the list of stacks
            if stack_index == len(stacks) - 1:
                result += "\n"

    # Add a line at the bottom of the flasks to separate from the stack numbers
    result += "+--+  " * len(stacks) + "\n"
    return result  # Return the resulting string

def print_stacks(stacks, source_flask=None, dest_flask=None):
    """
    Generates a visual representation of the flask stacks with optional highlighting for source and destination flasks.

    Args:
        stacks (list): A list of flask stacks.
        source_flask (int, optional): The index of the source flask to highlight. Defaults to None.
        dest_flask (int, optional): The index of the destination flask to highlight. Defaults to None.

    Returns:
        str: A formatted string representing the flask stacks with optional highlighting for source and destination flasks.
    """

    if len(stacks) <= 4:
        result = string_stacks(stacks, source_flask, dest_flask)
        for i in range(len(stacks)):
            flask_number = i + 1
            if flask_number == source_flask:
                result += f"{ANSI['RED']}{flask_number:^5}{ANSI['RESET']} "  # Set color to red for source flask
            elif flask_number == dest_flask:
                result += f"{ANSI['GREEN']}{flask_number:^5}{ANSI['RESET']} "  # Set color to green for dest flask
            else:
                result += f"{flask_number:^5} "  # Print stack numbers centered under each flask
        return result
    else:
        chunks = [stacks[i:i+4] for i in range(0, len(stacks), 4)]
        output = ""
        for index, chunk in enumerate(chunks):
            output += string_stacks(chunk, source_flask, dest_flask)
            output += ""  # Add spacing for stack numbers
            for i in range(len(chunk)):
                flask_number = index * 4 + i + 1
                if flask_number == source_flask:
                    output += f"{ANSI['RED']}{flask_number:^5}{ANSI['RESET']} "  # Set color to red for source flask
                elif flask_number == dest_flask:
                    output += f"{ANSI['GREEN']}{flask_number:^5}{ANSI['RESET']} "  # Set color to green for dest flask
                else:
                    output += f"{flask_number:^5} "  # Print stack numbers centered under each flask
            output += "\n\n"
        return output


def win_condition(stacks,num_flask, num_chemicals):
    """
    Checks if the win condition for the game is met.

    Args:
        stacks (list): A list of BoundedStack objects representing the flasks.

    Returns:
        bool: True if the win condition is met, False otherwise.
    """
    win_no = 0
    # Iterate over each stack (flask) in the list of stacks
    for stack in stacks:
        # Check if the stack is full with the same letter and has the maximum capacity
        if stack.is_full_with_same_letter() and stack.len() == MAX:
            win_no += 1
    # Check if the number of winning stacks equals the total number of stacks minus the difference between
    # the initial number of flasks and the initial number of chemicals
    if win_no == len(stacks) - (num_flask - num_chemicals):
        return True
    else:
        return False

def main():
    """Main function for the Magical Flask Game."""
    
    # Read initial game data
    num_flask, num_chemicals, stacks = read_chemical_data()
    
    # Initialize source and destination flask input constants
    source_input_constant = 0
    dest_input_constant = 0
    
    while True:
        # Clear screen and display game title
        clear_screen()
        print_location(0, 2, 'Magical Flask Game')
        
        # Display current flask stacks and user prompt
        print_location(1, 7, print_stacks(stacks, int(source_input_constant), int(dest_input_constant)))
        
        # Initialize flags for source and destination flask selection
        source_flag = True
        destination_flag = True
        
        # Prompt user to select source flask
        print_location(1, 4, 'Select source flask:')
        print_location(1, 5, 'Select destination flask:')
        
        # Source flask selection loop
        while source_flag:
            move_cursor(22, 4)
            source_input = input()
            
            # Check for exit command
            if source_input.lower() == 'exit':
                if len(stacks) <= 4: 
                    print_location(1, 15, 'Thank you for playing!')
                else:
                    print_location(1, 21, 'Thank you for playing!')
                exit()
            
            # Validate source flask input
            elif not source_input.isdigit() or not (0 <= int(source_input) - 1 < len(stacks)) or stacks[int(source_input) - 1].len() == 0 or (stacks[int(source_input) - 1].is_full_with_same_letter() and stacks[int(source_input) - 1].len() == MAX):
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(21, 4, ANSI["CLEARLINE"])
                
            else:
                source_flag = False
                print_location(1, 6, ANSI['CLEARLINE'])
                print_location(1, 7, print_stacks(stacks, int(source_input)))
                source_input_constant = source_input
        
        # Destination flask selection loop
        while destination_flag:
            move_cursor(27, 5)
            dest_input = input()
            
            # Check for exit command
            if dest_input.lower() == 'exit':
                if len(stacks) <= 4: 
                    print_location(1, 15, 'Thank you for playing!')
                else:
                    print_location(1, 21, 'Thank you for playing!')
                exit()
            
            # Validate destination flask input
            elif not dest_input.isdigit() or not (0 <= int(dest_input) - 1 < len(stacks)) or stacks[int(dest_input) - 1].len() == flask_size or (stacks[int(dest_input) - 1].is_full_with_same_letter() and stacks[int(dest_input) - 1].len() == MAX) or source_input == dest_input:
                print_location(0, 6, "Invalid input. Try Again." + ANSI["CLEARLINE"])
                print_location(27, 5, ANSI["CLEARLINE"])
                
            else:
                destination_flag = False
                item = stacks[int(source_input) - 1].pop()
                stacks[int(dest_input) - 1].push(item)
                print_location(1, 6, ANSI['CLEARLINE'])
                print_location(1, 7, print_stacks(stacks, None, int(dest_input)))
                dest_input_constant = dest_input
        
        # Check for win condition
        if win_condition(stacks, num_flask, num_chemicals):
            print_location(27, 5, dest_input) 
            print_location(1, 7, print_stacks(stacks, int(source_input), int(dest_input)))
            if len(stacks) <= 4:
                print_location(0, 15, "You win!")
            else:
                print_location(0, 21, "You win!")
            exit()


if __name__ == "__main__":
    main()
