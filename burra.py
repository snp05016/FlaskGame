import os
from bqueue import BoundedQueue
from bstack import BoundedStack

MAX = 3
flask_size = 4
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

COLORS = {'AA': ANSI['HRED'], 'BB': ANSI['HBLUE'], 'CC': ANSI['HGREEN'],
          'DD': ANSI['HORANGE'], 'EE': ANSI['HYELLOW'], 'FF': ANSI['HMAGENTA']}

with open('6chemicals.txt', 'r') as file:
    firstline = file.readline()
    firstline = firstline.strip()
    num_flask = int(firstline[0])
    num_chemicals = int(firstline[2])
    chemical_data = file.readlines()
    queue = BoundedQueue(flask_size)
    stacks = [BoundedStack(flask_size) for i in range(num_flask)]
    
    for line in chemical_data:
        line = line.strip()
        if 'F' in line and len(line) >= 3:
            flask_number_to_dequeue = int(line[0])
            from_flask = int(line[len(line)-1])
            dequeue_into = from_flask - 1
            
            for j in range(flask_number_to_dequeue):
                stacks[dequeue_into].push(queue.dequeue())
        else:
            if not queue.isFull():
                queue.enqueue(line)
                
def print_location(x, y, text):
    print("\033[{1};{0}H{2}".format(x, y, text))
    
def move_cursor(x, y):
    print("\033[{1};{0}H".format(x, y), end='')

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def check_full(stack):
    return True if stack.with_same_letter() and stack.len() == MAX else False

def string_stacks(stacks,source_flask = None, destination_flask = None):
    result = ""
    for i in range(flask_size - 1, -1, -1):
        for stack_index, stack in enumerate(stacks):
            try:
                if not stack.isEmpty():
                    item = stack.items()[i]
                    result += f"|{COLORS[item]}{item:^2}{ANSI['RESET']}|  "
                else:
                    result += "|  |  "
            except IndexError:
                if check_full(stack):
                    if i == flask_size - 1:
                        result += "+--+  "
                    else:
                        result += "|  |  "
                else:
                    result += "|  |  "
            if stack_index == len(stacks) - 1:
                result += "\n"

    result += "+--+  " * len(stacks) + "\n"
    return result

def print_stacks(stacks, source_flask=None, dest_flask=None):
    if len(stacks) <= 4:
        result = string_stacks(stacks, source_flask, dest_flask)
        for i in range(len(stacks)):
            flask_number = i + 1
            if flask_number == source_flask:
                result += f"{ANSI['RED']}{flask_number:^5}{ANSI['RESET']} "
            elif flask_number == dest_flask:
                result += f"{ANSI['GREEN']}{flask_number:^5}{ANSI['RESET']} "
            else:
                result += f"{flask_number:^5} "
        return result
    else:
        chunks = [stacks[i:i+4] for i in range(0, len(stacks), 4)]
        output = ""
        for index, chunk in enumerate(chunks):
            output += string_stacks(chunk, source_flask, dest_flask)
            output += ""
            for i in range(len(chunk)):
                flask_number = (index * 4) + i + 1
                if flask_number == source_flask:
                    output += f"{ANSI['RED']}{flask_number:^5}{ANSI['RESET']} "
                elif flask_number == dest_flask:
                    output += f"{ANSI['GREEN']}{flask_number:^5}{ANSI['RESET']} "
                else:
                    output += f"{flask_number:^5} "
            output += "\n\n"
        return output

def win_condition(stacks):
    win_no = 0
    for stack in stacks:
        if check_full(stack)==True:
            win_no += 1
    if win_no == len(stacks) - (num_flask - num_chemicals):
        return True
    else:
        return False
    
def move_stack(stacks, source_input, destination_input):
    item = stacks[int(source_input) - 1].pop()
    stacks[int(destination_input) - 1].push(item)

def main():
    source_input_constant = 0
    dest_input_constant = 0
    while True:
        clear_screen()
        print_location(0, 2, 'Magical Flask Game')
        
        source_flag = True
        destination_flag = True
        print_location(1, 4, 'Select source flask:')
        print_location(1, 5, 'Select destination flask:')
        print_location(1, 3+(flask_size), print_stacks(stacks,int(source_input_constant),int(dest_input_constant)))
        while source_flag:
            move_cursor(22, 4)
            source_input = input()

            if source_input.lower() == 'exit':
                if len(stacks) <= 4 : 
                    print_location(1, 6, ANSI["CLEARLINE"])
                    move_cursor(1,15)
                    exit()
                else:
                    print_location(1, 6, ANSI["CLEARLINE"])
                    move_cursor(1, 21)
                    exit()
                
            elif not source_input.isdigit():
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            elif not (0 <= int(source_input) - 1 < len(stacks)):
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            elif stacks[int(source_input) - 1].len() == 0:
                print_location(0, 6, "Cannot pour from that flask. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            elif check_full(stacks[int(source_input) - 1]):
                print_location(0, 6, "Cannot pour from that flask. Try again." + ANSI["CLEARLINE"])
                print_location(21,4,ANSI["CLEARLINE"])

            else:
                source_flag = False
                print_location(1, 6, ANSI['CLEARLINE'])
                source_input_constant = source_input
        print_location(1, 3+flask_size, print_stacks(stacks,int(source_input),None))
        while destination_flag:
            move_cursor(27, 5)
            dest_input = input()
    
            if dest_input.lower() == 'exit':
                if len(stacks) <= 4 : 
                    print_location(1, 6, ANSI["CLEARLINE"])
                    print_location(1, 15, 'Thank you for playing!')
                    exit()
                else:
                    print_location(1, 6, ANSI["CLEARLINE"])
                    print_location(1, 21, 'Thank you for playing!')
                    exit()
                
            elif not dest_input.isdigit():
                print_location(0, 6, "Invalid input. Try Again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])
                
            elif not (0 <= int(dest_input) - 1 < len(stacks)):
                print_location(0, 6, "Invalid input. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            elif stacks[int(dest_input) - 1].len() == flask_size:
                print_location(0, 6, "Cannot pour into that flask. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            elif check_full(stacks[int(dest_input) - 1]):   
                print_location(0, 6, "Cannot pour into that flask. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            elif source_input == dest_input:
                print_location(0, 6, "Cannot pour into the same flask. Try again." + ANSI["CLEARLINE"])
                print_location(27,5,ANSI["CLEARLINE"])

            else:
                destination_flag = False
                move_stack(stacks,source_input,dest_input)
                dest_input_constant  = dest_input

        if win_condition(stacks):
            print_location(27, 5, dest_input) 
            print_location(1, 7, print_stacks(stacks, int(source_input), int(dest_input)))
            if len(stacks) <= 4:
                print_location(0, 15, "You win!")
            else:
                print_location(0, 21, "You win!")
            exit()               
if __name__ == "__main__":
    main()
