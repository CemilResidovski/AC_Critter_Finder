from sys import exit
from Critter import Fish, Bug

size_commands = ["smallish", "smallest", "small", "medium", "large", "x large", "largest", "largeish"]
loc_commands = ["sea", "pond", "rivers", "river", "rivermouth", "rivercliff"]
critter_commands = ["bug", "bugs", "fish"]
info_commands = ["new", "expiring", "find", "info"]

def print_list(l):
    print(", ".join(l))

print("Meta commands: quit, help")
while True:
    critter, loc, size, info, to_find = "any", "any", "any", "any", "any"
    print()
    cmd = input("Remember to at least include \"bug\" or \"fish\": ").lower()
    if "quit" in cmd:
        exit()
    elif "help" in cmd:
        print("Supported animal types: ")
        print_list(critter_commands)
        print("Supported sizes: ")
        print_list(size_commands)
        print("Supported locations: ")
        print_list(loc_commands)
        print("Supported actions: ")
        print_list(info_commands)
        print("To search for eg. a fish: write fish find \"sea bass\"")
        continue
    elif "info" in cmd or "find" in cmd:
        start_index = cmd.find('"')
        if (start_index == -1):
            print("Please write in the critter name you want to find within quotation signs (\")")
            continue
        end_index = cmd.find('"', start_index + 1)
        first_half = cmd[:start_index]
        second_half = cmd[end_index + 1:]
        critter_to_find = cmd[start_index + 1:end_index].title()
        cmd = (first_half + second_half)
    cmd = cmd.split()
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
    
    '''TODO: what do you mean, I'm sorry?'''
    """ I'm sorry """
    if critter == "fish":
        f = Fish()
        if info == "any":
            print(f"Searching for currently available {size} size fish at {loc} location...")
            print_list(f.get_fish(size, loc))
        elif info == "new":
            print(f"Searching for new fish this month...")
            print_list(f.new_fish())
        elif info == "expiring":
            print(f"Searching for fish that will be unavailable next month...")
            print_list(f.expiring_fish())
        elif info == "find":
            print(f"Searching for fish called {critter_to_find}...")
            print(f.get_fish_info(critter_to_find))

    elif critter in ["bug", "bugs"]:
        b = Bug()
        if info == "any":
            print(f"Searching for currently available bugs...")
            print_list(b.get_bugs())
        elif info == "new":
            print(f"Searching for new bugs this month...")
            print_list(b.new_bugs())
        elif info == "expiring":
            print(f"Searching for bugs that will be unavailable next month...")
            print_list(b.expiring_bugs())
        elif info == "find" or info == "info":
            print(f"Searching for bugs called {critter_to_find}...")
            print(b.get_bug_info(critter_to_find))