from bstack import BoundedStack
from bqueue import BoundedQueue
import os

# Initializing all the necessary constants
MAX = 3
FLASK_SIZE = 4
# Dictionary of all the ANSI values that we will use throughout
ANSI = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "HRED": "\033[41m",
    "HGREEN": "\033[42m",
    "HBLUE": "\033[44m",
    "HORANGE": "\033[48m",
    "HYELLOW": "\033[43m",
    "HMAGENTA": "\033[45m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m",
    "CLEARLINE": "\033[0K"
}
# Storing the respective colors for each chemical
COLORS = {'AA': ANSI['HRED'], 'BB': ANSI['HBLUE'], 'CC': ANSI['HGREEN'],
          'DD': ANSI['HRED'], 'EE': ANSI['HYELLOW'], 'FF': ANSI['HMAGENTA']}

# Defining all the functions we will need for displaying ANSI characters in the terminal


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


def CheckIfFull(flask):
    '''
    Checks if the current flask is full and returns True if it is, else returns False
    Input:Flask
    Output:True or False
    '''
    if flask.size() == MAX:
        if len(set(str(flask).split())) == 1:
            return True
    return False


def move(start, to, stacks):
    '''
    Moves the chemical from one flask to another. Returns the appropriate error message if element is moved from a empty flask 
    Input:
        -start: Index of the source flask in 'stacks'
        -to: Index of the destination flask in 'stacks'
        -stacks: list of the flasks' bounded stacks
    Output: None
    '''
    try:
        stacks[to-1].push(stacks[start-1].pop())
    except Exception:
        print_location(1, 6, 'Cannot move from an empty flask')


def seal_flask(flask_no):
    '''
    Prints the seal on the flask received as input
    Input:
        -flask_no: The count of the flask to be sealed 
    Output:None
    '''
    print_location(1+(6*flask_no), 7, '+--+')


def print_flask(stacks, flask_from=None, flask_to=None):
    '''
    Prints the flasks as needeed
    Input:
        -flask_from: Index of the source flask in 'stacks'
        -flask_to: Index of the destination flask in 'stacks'
        -stacks: list of the flasks' bounded stacks
    Output: Prints the lines at position column 1, row 7 
    '''
    flask = ''
    flask_list = []
    end_line = ''
    numbers = ''
    # TODO IN PROGRESS
    no_of_lines = 1
    if NUMBER_OF_FLASK//4 != 0:
        no_of_lines = NUMBER_OF_FLASK//4
    for i in range(1, FLASK_SIZE+1):
        line = ''
        for stack in stacks:
            # For positions where there are elements
            if (5-i) <= stack.size():  # 5-i -> The number of the row
                # Creates a temporary bounded stack to store the popped values from the individual 'flask' stacks temporarily
                temp = BoundedStack(FLASK_SIZE)
                while 5-i <= stack.size():
                    # temp_element -> Temporarily stores the popped element from the flask
                    temp_element = stack.pop()
                    # The popped element is then pushed into the temporary BStack
                    temp.push(temp_element)
                # line -> a string storing the current line of flasks, with the appropriate colors
                line += f'|{COLORS[temp_element]+temp_element+ANSI["RESET"]:2}|  '
                for k in range(temp.size()):
                    # Returns the flasks to their original state
                    stack.push(temp.pop())
            else:
                # For places where there are no elements
                line += f"|{'  ':2}|  "
        end_line = f'''+--+  '''*len(stacks)
        line += '\n'  # Moves to the next line
        # Appnds the line to the flask_list
        flask_list.append(line)

    # For every next turn after the first tuun
    if not (flask_from == None and flask_to == None):
        for row_no in range(1, len(stacks)+1):
            if row_no == int(flask_from):
                numbers += '  '+ANSI['RED']+str(row_no)+ANSI['RESET']+'   '
            elif row_no == int(flask_to):
                numbers += '  '+ANSI['GREEN']+str(row_no)+ANSI['RESET']+'   '
            else:
                numbers += '  '+str(row_no)+'   '
    else:  # For the first run for the flask where no move has been made yet
        for i in range(1, len(stacks)+1):
            numbers += '  '+str(i)+'   '

    numbers = '\n'+numbers
    # Appends the line above the flask number
    flask_list.append(end_line)
    # Appends the line that contains the flask number
    flask_list.append(numbers)
    for element in flask_list:
        flask += element
    print_location(1, 7, flask)


# def main():
with open('6chemicals.txt') as f:
    # Temporaary variable that stores the first line of the file, removing any whitespaces
    temp = f.readline().split()
    stacks = []
    # Stores the number of flasks to be made for the game
    NUMBER_OF_FLASK = int(temp[0])
    # Stores the number of chemicals there are in the file
    NUMBER_OF_CHEM = int(temp[1].strip())
    data = f.readlines()
    # Creates a bounded queue of 4 to store the chemicals from the file
    file_queue = BoundedQueue(FLASK_SIZE)
    # Creats the amount of necessary flasks  (Bounded stacks)
    for j in range(NUMBER_OF_FLASK):
        stacks.append(BoundedStack(FLASK_SIZE))
    for i in data:
        i = i.strip()
        # When the line contains F, commanding the movement of chemicals from one flask to the other
        if 'F' == i[1] and len(i) == 3:
            move_to = int(i[-1])-1
            for i in range(int(i[0])):
                stacks[move_to].push(file_queue.dequeue())
        else:
            if not file_queue.isFull():
                file_queue.enqueue(i)


def game_logic(fro, to, win_list):
    '''
    Contains the main game logic
    '''
    valid_from = False
    valid_to = False
    # Runs when the fro is 0 ; i.e the first run
    if fro == 0:
        clear_screen()
        print_location(1, 1, 'Magical Flask Game')
        print_flask(stacks, None, None)
    else:
        clear_screen()
        print_location(1, 1, 'Magical Flask Game')
        # print_location(1, 7, print_flask(stacks, flask_from, flask_to))
        print_flask(stacks, fro, to)
    # Printing the seal on the flasks that are full
    for i in range(len(stacks)):
        if CheckIfFull(stacks[i]):
            seal_flask(i)
            win_list.append(i)

    while not valid_from:  # Checks if the source flask input is valid
        print_location(1, 4, 'Select Source flask: ' + ANSI["CLEARLINE"])
        move_cursor(22, 4)
        flask_from = input()
        # Checks if the source flask input is a digit and prints the respective error message if so
        if not flask_from.isdigit():
            print_location(1, 6, 'Invalid Input. Try again.'+ANSI["CLEARLINE"])
        # Checks if the source flask input is an existing flask and prints the respective error message if so
        elif not (0 < int(flask_from) <= len(stacks)):
            print_location(1, 6, 'Invalid Flask'+ANSI['CLEARLINE'])
        # Checks if the source flask input is empty and prints the respective error message if so
        elif stacks[int(flask_from)-1].isEmpty():
            print_location(
                1, 6, 'Cannot move from an empty flask'+ANSI["CLEARLINE"])
        # Checks if the source flask input is full and prints the respective error message if so
        elif CheckIfFull(stacks[int(flask_from)-1]):
            print_location(
                1, 6, 'Cannot pour from a sealed flask'+ANSI["CLEARLINE"])
        # If none of the above are satisfied , the input is valid
        else:
            valid_from = True
            print_location(1, 6, ANSI['CLEARLINE'])

    while not valid_to:  # Checks if the destination flask input is valid
        print_location(1, 5, 'Select destination flask: '+ANSI["CLEARLINE"])
        move_cursor(27, 5)
        flask_to = input()
        # Checks if the destination flask input is a digit and prints the respective error message if so
        if not flask_to.isdigit():
            print_location(1, 6, 'Invalid Input.Try again.'+ANSI["CLEARLINE"])
        # Checks if the destination flask input is an existing flask and prints the respective error message if so
        elif not (0 < int(flask_to) <= len(stacks)):
            print_location(1, 6, 'Invalid Input.Try again.'+ANSI["CLEARLINE"])
        # Checks if the destination flask is sealed and prints the respective error message if so
        elif CheckIfFull(stacks[int(flask_to)-1]):
            print_location(
                1, 6, 'Cannot pour into that flask. Try again.'+ANSI["CLEARLINE"])
        # Checks if the destination flask input is the same as the destination flask and prints the respective error message if so
        elif flask_to == flask_from:
            print(1, 6, 'Cannot pour into the same flask ')
        # Checks if the destination flask is full and prints the respective error message otherwise
        elif len(str(stacks[int(flask_to)-1]).split()) == 4:
            print_location(
                1, 6, 'Cannot move to a sealed flask'+ANSI["CLEARLINE"])
        # If none of the above conditions are True, the input is valid
        else:
            valid_to = True
            print_location(1, 6, ANSI['CLEARLINE'])

    return flask_from, flask_to, stacks


# TEST CODE
def main():
    '''
    Main Funciton containing the main logic for the gameplay
    '''
    win = False
    temp = 0
    fro, to = 0, 0  # For the first run
    # When the player has not won
    while not win:
        win_list = []
        win_count = 0
        if temp == 0:
            fro, to, stacks = game_logic(fro, to, win_list)
        else:
            fro, to, stacks = game_logic(fro, to, win_list)
        temp += 1
        # Moves the chemical from the source flask to the destination flask
        move(int(fro), int(to), stacks)
        # Checks of the player has won
        for i in range(len(stacks)):
            # Incrments win_count if the flask is either sealed or if the flasks are empty
            if CheckIfFull(stacks[i]) or stacks[i].isEmpty():
                win_count += 1
        # If the player has won
        if win_count == NUMBER_OF_FLASK:
            print_location(1, 13, 'You win!')
            win = True
            print_flask(stacks, fro, to)
            # Printing the seal on the flasks that are full
            for i in range(len(stacks)):
                if CheckIfFull(stacks[i]):
                    seal_flask(i)
                    win_list.append(i)
            move_cursor(1, 14)


main()
