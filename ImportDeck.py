from sys import argv
import json

with open("ManaCosts.json") as costs:
    mana_costs = json.load(costs)


try:
    load_path = argv[1]
    with open(load_path) as in_file:
        content = json.load(in_file)
        content = content[0:len(content)-3]
    
    frequencies: dict = {}
    for elem in content:
        file_name: str = elem.split("/")[4]
        short = file_name[:len(file_name)-5]
        short += f" ({mana_costs[short]} Mana)"
        
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
    
    burrowed_cards: list = input("Please enter all card names of burrowed cards\nCards are seperated by a comma. Do not enter the mana cost of the card:\n").split(",")
    top_cards: list = input("Please enter all card names of top cards\nCards are seperated by a comma. Do not enter the mana cost of the card:\n").split(",")

    if burrowed_cards == [""]:
        burrowed_cards = []
    if top_cards == [""]:
        top_cards = []

    idx: int = 0

    while idx < len(burrowed_cards):
        burrowed_cards[idx] = burrowed_cards[idx].strip()
        idx += 1
    
    idx = 0
    while idx < len(top_cards):
        top_cards[idx] = top_cards[idx].strip()
        idx += 1

    if len(burrowed_cards) != 0 or len(top_cards) != 0:
        pos_map: list = [burrowed_cards, top_cards]
        with open(f"Decks/{deck_name}_POSITIONAL.json", "w") as pos_file:
            json.dump(pos_map, pos_file)

    print(f"Saved {deck_name} to Decks/{deck_file}")
        
except IndexError:
    print("Not enough arguments given. Please provide a source file")
except FileNotFoundError:
    print("Provided file does not exist")
except json.JSONDecodeError:
    print("The provided file is not a valid deck")