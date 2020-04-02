import sys
import Fish, Bugs

size_commands = ["smallish", "smallest", "small", "medium", "large", "x large" "largest", "largeish"]
loc_commands = ["sea", "pond", "river", "rivermouth", "rivercliff"]
critter_commands = ["bug", "bugs", "fish"]
info_commands = ["new", "expiring", "find", "info"]

def print_list(l):
    string = ""
    for item in l:
        string += item + ", "
    print(string[:-2])

print("Meta commands: quit, help")
while True:
    critter, loc, size, info = "any", "any", "any", "any"
    print()
    cmd = input("Separate words with commas, remember to at least include \"bug\" or \"fish\": ").lower().split(',')
    if "help" in cmd:
        print("Supported animal types: ")
        print_list(critter_commands)
        print("Supported sizes: ")
        print_list(size_commands)
        print("Supported locations: ")
        print_list(loc_commands)
        print("Supported actions: ")
        print_list(info_commands)
        continue
    elif "quit" in cmd:
        sys.exit()
    for word in cmd: 
        word = word.strip()
        if word in critter_commands:
            critter = word
        elif word in loc_commands:
            loc = word
        elif word in size_commands:
            size = word
        elif word in info_commands:
            info = word
        else:
            print(f'Sorry, I don\'t know what "{word}" means. Did you separate commands with a comma?')
            continue
    
    """ I'm sorry """
    if critter == "fish":
        if info == "any":
            print(f"Searching for currently available {size} size fish at {loc} location...")
            print_list(Fish.get_fish(size, loc))
        elif info == "new":
            print(f"Searching for new fish this month...")
            print_list(Fish.new_fish())
        elif info == "expiring":
            print(f"Searching for fish that will be unavailable next month...")
            print_list(Fish.expiring_fish())
    elif critter == "bug" or critter == "bugs":
        if info == "any":
            print(f"Searching for currently available bugs...")
            print_list(Bugs.get_bugs())
        elif info == "new":
            print(f"Searching for new bugs this month...")
            print_list(Bugs.new_bugs())
        elif info == "expiring":
            print(f"Searching for bugs that will be unavailable next month...")
            print_list(Bugs.expiring_bugs())