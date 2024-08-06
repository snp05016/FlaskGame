import os
from bqueue import BoundedQueue
from bstack import BoundedStack

MAX = 3         #max no of elements the flask can hold
flask_size = 4  #size of the flask

#ANSI ESCAPE CODES
ANSI = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "HRED": "\033[41m",
    "HGREEN": "\033[42m",
    "HBLUE": "\033[44m",
    "HORANGE": "\033[48;5;208m",
    "HYELLOW": "\033[43m",
    "HMAGENTA": "\033[45m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m",
    "CLEARLINE": "\033[0K"
}

# Storing the respective colors for each chemical
COLORS = {'AA': ANSI['HRED'], 'BB': ANSI['HBLUE'], 'CC': ANSI['HGREEN'],
          'DD': ANSI['HORANGE'], 'EE': ANSI['HYELLOW'], 'FF': ANSI['HMAGENTA']}

'''Read the file and initialize stacks
Open the file '6chemicals.txt' in read mode'''

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
    if os.name == "nt":  # windows
        os.system("cls")
    else:
        os.system("clear")  # unix (mac, linux, etc.)
def check_full(stack):
    """
    Checks if the stack is full based on two conditions:
    1. All items in the stack are the same letter.
    2. The number of items in the stack equals the maximum capacity.

    Args:
    - stack (BoundedStack): The bounded stack to be checked.

    Returns:
    - bool: True if the stack meets both conditions, False otherwise.
    """
    return True if stack.with_same_letter() and stack.len() == MAX else False
       
def string_stacks(stacks,source_flask = None, destination_flask = None):
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
                    item = stack.items()[i]#.items returns the string of the stack
                    # Add background color based on chemical type and center the item in the cell
                    result += f"|{COLORS[item]}{item:^2}{ANSI['RESET']}|  "
                else:
                        # If the stack is empty, add an empty cell
                    result += "|  |  "
            except IndexError:
                # Handle the case when accessing an index that is out of range for the stack
                # is.full_with_same_letter is implemented in bstacks and .len() also in bstacks
                if check_full(stack):
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
    Generate a visual representation of the stacks of flasks (if there are 8 flasks, then 4 and 4), optionally highlighting the source and destination flasks.

    Args:
    - stacks (list): A list of lists representing the stacks of flasks.
    - source_flask (int, optional): The index of the source flask to be highlighted.
    - dest_flask (int, optional): The index of the destination flask to be highlighted.

    Returns:
    - str: A string containing the visual representation of the stacks, with optional highlighting of source and destination flasks.
    """
    # if the number of stacks are less than 4 or equal to 4
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
    # if the number of stacks are more than 4
    else:
        chunks = [stacks[i:i+4] for i in range(0, len(stacks), 4)]
        output = ""
        for index, chunk in enumerate(chunks):
            output += string_stacks(chunk, source_flask, dest_flask)
            output += ""  # Add spacing for stack numbers
            for i in range(len(chunk)):
                flask_number = (index * 4) + i + 1
                if flask_number == source_flask:
                    output += f"{ANSI['RED']}{flask_number:^5}{ANSI['RESET']} "  # Set color to red for source flask
                elif flask_number == dest_flask:
                    output += f"{ANSI['GREEN']}{flask_number:^5}{ANSI['RESET']} "  # Set color to green for dest flask
                else:
                    output += f"{flask_number:^5} "  # Print stack numbers centered under each flask
            output += "\n\n"
        return output

def win_condition(stacks):
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
        if check_full(stack)==True:
            win_no += 1
    # Check if the number of winning stacks equals the total number of stacks minus the difference between
    # the initial number of flasks and the initial number of chemicals
    if win_no == len(stacks) - (num_flask - num_chemicals):
        return True
    else:
        return False
    
def move_stack(stacks, source_input, destination_input):
    """
    Move an item from the source flask to the destination flask.

    This function pops an item from the top of the source flask stack and pushes it onto the top
    of the destination flask stack, effectively moving the item from one flask to another.

    Parameters:
        stacks (list): A list of stacks representing the flasks.
        source_input (int): The index of the source flask from which to move the item.
        destination_input (int): The index of the destination flask to which to move the item.

    Returns:
        None
    """
    item = stacks[int(source_input) - 1].pop()
    stacks[int(destination_input) - 1].push(item)

def main():
    """
    Main function to run the Magical Flask Game.
    
    This function controls the flow of the game, including selecting source and destination flasks,
    checking the validity of user inputs, pouring liquids between flasks, and checking for win conditions.
    
    The game continues in a loop until the win condition is met or the user chooses to exit.
    """
    source_input_constant = 0 # intialized it so that the value of source input changes everytime a user inputs something, to change colors of number of stack
    dest_input_constant = 0 # intialized it so that the value of destination input changes everytime a user inputs something, to change colors of number of stack
    while True:
        # Clear the screen and print game title
        clear_screen()
        
        print_location(0, 2, 'Magical Flask Game')
        
        # Flag to check if source flask selection is valid
        source_flag = True
        
        # Flag to check if destination flask selection is valid
        destination_flag = True
        
        #print source and destination flasks in specified locations
        print_location(1, 4, 'Select source flask:')
        print_location(1, 5, 'Select destination flask:')
        print_location(1, 3+(flask_size), print_stacks(stacks,int(source_input_constant),int(dest_input_constant)))
        # Loop until valid source flask is selected
        while source_flag:
            # Prompt user to select source flask
            move_cursor(22, 4)
            source_input = input()

            #if the user enters quit then print thank you and exit the game
            if source_input.lower() == 'exit':
                if len(stacks) <= 4 : 
                    print_location(1, 6, ANSI["CLEARLINE"])
                    move_cursor(1,15)
                    exit()
                else:
                    print_location(1, 6, ANSI["CLEARLINE"])
                    move_cursor(1, 21)
                    exit()
                
            # Check if input is not a number
            elif not source_input.isdigit():
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            # Check if input is out of range
            elif not (0 <= int(source_input) - 1 < len(stacks)):
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            # Check if source flask is empty
            elif stacks[int(source_input) - 1].len() == 0:
                print_location(0, 6, "Cannot pour from that flask. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            # Check if source flask is full with the same letter
            # is.full_with_same_letter is implemented in bstacks and .len() also in bstacks
            elif check_full(stacks[int(source_input) - 1]):
                print_location(0, 6, "Cannot pour from that flask. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            else:
                source_flag = False
                print_location(1, 6, ANSI['CLEARLINE'])
                # print_location(1, 7, print_stacks(stacks, int(source_input)))
                source_input_constant = source_input# constant becomes the input to use to print the color numbers for the flasks
        ######comment below code if you dont want to change the source flask number to red as soon as a valid source is entered.IT WAS NOT SPECIFIED IN THE ASSIGMENT HOW TO IMPLEMENT IT##### 
        print_location(1, 3+flask_size, print_stacks(stacks,int(source_input),None))
        while destination_flag:
            # Prompt user to select destination flask
            move_cursor(27, 5)
            dest_input = input()
    
            # if the user enters quit it will exit
            if dest_input.lower() == 'exit':
                if len(stacks) <= 4 : 
                    print_location(1, 6, ANSI["CLEARLINE"])
                    move_cursor(1,15)
                    exit()
                else:
                    print_location(1, 6, ANSI["CLEARLINE"])
                    move_cursor(1, 21)
                    exit()
                
            # Check if input is not a number
            elif not dest_input.isdigit():
                print_location(0, 6, "Invalid input. Try Again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])
                
            # Check if input is out of range
            elif not (0 <= int(dest_input) - 1 < len(stacks)):
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            # Check if destination flask is full
            elif stacks[int(dest_input) - 1].len() == flask_size:
                print_location(0, 6, "Cannot pour into that flask. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            # Check if destination flask is full with the same letter
            elif check_full(stacks[int(dest_input) - 1]):   
                print_location(0, 6, "Cannot pour into that flask. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            # Check if source and destination flasks are the same
            elif source_input == dest_input:
                print_location(0, 6, "Cannot pour into the same flask. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            else:
                destination_flag = False#false so the loop doesnt repeat
                move_stack(stacks,source_input,dest_input)#moves the element from source to destination flask
                dest_input_constant  = dest_input

        #Check if win condition is met
        if win_condition(stacks):
            print_location(27, 5, dest_input) 
            print_location(1, 7, print_stacks(stacks, int(source_input), int(dest_input)))
            #Clear destination flask indicator
            if len(stacks) <= 4:
                print_location(1,6,ANSI["CLEARLINE"])
                print_location(0, 15, "You win!")
            else:
                print_location(1,6,ANSI["CLEARLINE"])
                print_location(0, 21, "You win!")
            exit()               
            
if __name__ == "__main__":
    main()