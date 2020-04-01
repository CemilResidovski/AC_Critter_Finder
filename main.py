import sys
import Fish

size_commands = ["smallish", "smallest", "small", "medium", "large", "x large" "largest", "largeish"]
loc_commands = ["sea", "pond", "river", "rivermouth", "rivercliff"]
critter_commands = ["bug", "fish"]

def print_list(l):
    string = ""
    for item in l:
        string += item + ", "
    print(string[:-2])

print("Meta commands: quit, help")
while True:
    critter, loc, size = "any", "any", "any"
    cmd = input("Separate words with commas, remember to at least include \"bug\" or \"fish\": ").lower().split(',')
    if "help" in cmd:
        print("Supported animal types: ")
        print_list(critter_commands)
        print("Supported sizes: ")
        print_list(size_commands)
        print("Supported locations: ")
        print_list(loc_commands)
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
        else:
            print(f'Sorry, I don\'t know what "{word}" means. Did you separate commands with a comma?')
            print()
            continue
    
    print(f"Searching for {size} size {critter}-type animal at {loc} location...")
    if critter == "fish":
        print(Fish.get_fish(size, loc))
        print()


