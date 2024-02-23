from sys import argv
import json

try:
    load_path = argv[1]
    with open(load_path) as in_file:
        content = json.load(in_file)
        content = content[0:len(content)-3]
    
    frequencies: dict = {}
    for elem in content:
        file_name: str = elem.split("/")[4]
        short = file_name[:len(file_name)-5]
        
        if not short in frequencies:
            frequencies[short] = 1
        else:
            frequencies[short] += 1
    
    out = ""

    for key in frequencies:
        if frequencies[key] == 1:
            out += f"- {key}\n"
        else:
            out += f"- {key} x{frequencies[key]}\n"
    
    json_name = load_path.split("\\")[-1]
    deck_name = json_name[0:len(json_name)-5]
    deck_file = deck_name+".txt"
    
    with open(f"Decks/{deck_file}", "w") as out_file:
        out_file.write(out)
    
    print(f"Saved {deck_name} to Decks/{deck_file}")
        

except IndexError:
    print("Not enough arguments given. Please provide a source file")
except FileNotFoundError:
    print("Provided file does not exist")
except json.JSONDecodeError:
    print("The provided file is not a valid deck")