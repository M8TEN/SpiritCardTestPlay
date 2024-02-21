from random import shuffle, randint
import json

'''Replace the elements in BURROWED_CARDS and TOP_CARDS to contain the cards that go at the bottom and top of the deck respectively.
Make sure to always write out the Mana cost after the card's name, otherwise an error will occur.'''

BURROWED_CARDS: list = ["Pa'sschat (8 Mana)", "Ravages of War (9 Mana)"]
TOP_CARDS: list = ["Allegiance (2 Mana)"]
POSITIONAL_CARDS: list = BURROWED_CARDS+TOP_CARDS

def get_deck() -> list:
    # Insert your file name here
    with open("Flame Deck.txt") as file:
        deck: list = []
        for line in file:
            end_idx: int = line.index(")")
            if (end_idx != len(line)-1) and (line[end_idx+1] != "\n"):
                count: int = int(line[end_idx+3])
            else:
                count: int = 1
            
            for i in range(count):
                deck.append(line[2:end_idx+1])
    
    shuffle(deck)
    shuffle(BURROWED_CARDS)
    shuffle(TOP_CARDS)
    
    for burrowed in BURROWED_CARDS:
        index: int = deck.index(burrowed)
        deck.insert(len(deck)-1, deck.pop(index))
    
    for top in TOP_CARDS:
        deck.insert(0, deck.pop(deck.index(top)))
    return deck

def mulligan(deck: list) -> list:
    temp_hand: list = []
    i: int = 0
    while i < 4:
        idx: int = randint(0,len(deck)-1)
        if not deck[idx] in POSITIONAL_CARDS:
            temp_hand.append(deck.pop(idx))
            i += 1
    
    print(temp_hand)
    invalid: bool = True
    while invalid:
        mull: list = input("Which cards do you want to swap? ").split(",")
        for i in range(len(mull)):
            mull[i] = mull[i].strip()

        if len(mull) == 1 and mull[0] == "":
            return temp_hand
        if len(mull) > len(temp_hand):
            print("Too many cards!")
            continue
        for card in mull:
            check: bool = (card in temp_hand)
            invalid = invalid and check
        invalid = not invalid
    
    i = 0
    while i < len(mull):
        from_deck: int = randint(0,len(deck)-1)
        if deck[from_deck] in POSITIONAL_CARDS:
            continue
        replace_card: str = mull[i]
        temp_card: str = temp_hand.pop(temp_hand.index(replace_card))
        deck.insert(from_deck, temp_card)
        temp_hand.append(deck.pop(randint(0,len(deck)-1)))
        i += 1

    return temp_hand

def discard(hand: list) -> None:
    discarding: bool = True
    display_game_state("Too many cards in hand")
    while discarding:
        display_game_state(f"Hand: {hand}")
        display_game_state("Which hand card should be discarded? ", False)
        card_name: str = input("Which hand card should be discarded? ").strip()
        display_game_state(">> "+card_name, False)
        if card_name in hand:
            hand.pop(hand.index(card_name))
            discarding = False
        else:
            print(f"Card '{card_name}' not in hand!")

def draw(deck: list, hand: list) -> str:
    while len(hand) > 9:
        discard(hand)
    if len(deck) > 0:
        return deck.pop(0)
    return None

def get_mana_cost(card: str) -> int:
    return int(card[card.index("(")+1])

def display_game_state(message: str, to_console: bool = True) -> None:
    try:
        with open("GameLog.txt") as file:
            content: str = file.read()
    except FileNotFoundError:
        content: str = ""
    
    with open("GameLog.txt", "w") as file:
        content += message+"\n"
        file.write(content)

    if to_console:
        print(message)

def average_mana_cost(deck) -> float:
    total: int = 0
    for card in deck:
        total += get_mana_cost(card)
    
    return total/len(deck)

new_game: bool = input("Dou you want to load a previous game? (y/n) ").lower() == "n"

if new_game:
    with open("GameLog.txt", "w") as file:
        file.write("")
    
    deck: list = get_deck()
    assert len(deck) == 45, "Invalid amount of cards!"

    hand: list = mulligan(deck)
    hand.append(draw(deck, hand))
    turn: int = 1
    mana: int = 1
    tamer_mana: int = 0
    attack_token: bool = (randint(0,1) == 0)
    core_hp: int = 30

else:
    with open("GameState.json") as state_file:
        content: list = json.load(state_file)
        deck: list = content[0]
        hand: list = content[1]
        turn: int = content[2]
        mana: int = content[3]
        tamer_mana: int = content[4]
        attack_token: bool = content[5]
        core_hp: int = content[6]

# Main Game loop
while True:
    if attack_token:
        player: str = "Bastion B-56"
    else:
        player: str = "M8TEN"
    
    out: str = f"Turn: {turn}\nMana: {mana}\nTamer Mana: {tamer_mana}\nAttack Token: {player}\nCore HP: {core_hp}"
    display_game_state(out)
    display_game_state(str(hand))
    command = input("Enter command: ")
    display_game_state(">> "+command, False)
    command = command.split(",")

    for i in range(len(command)):
        command[i] = command[i].strip()

    match command[0]:

        case "play":
            try:
                index: int = hand.index(command[1])
                if index == -1:
                    display_game_state(f"{command[1]} not in hand!")
                    continue
                mana_cost = get_mana_cost(hand[index])
                if mana-mana_cost >= 0:
                    hand.pop(index)
                    mana -= mana_cost
                else:
                    display_game_state(f"Not enough Mana to play {hand[index]}")
            except IndexError:
                display_game_state("Index out of bounds")
            except ValueError:
                display_game_state(f"{command[1]} is not in hand")
        
        case "draw":
            if len(command) == 2:
                count: int = int(command[1])
            else:
                count: int = 1
            
            for i in range(count):
                card = draw(deck, hand)
                if card == None:
                    display_game_state("You can't draw any more cards!")
                    break
                hand.append(card)
        
        case "burrow":
            try:
                idx: int = deck.index(command[1])
                at: int = max(0, idx-int(command[2]))
                deck.insert(at, deck.pop(idx))
                display_game_state(f"Moved {command[1]} from position {idx} to {at}")
            except IndexError:
                display_game_state("Invalid number of arguments!")
        
        case "level up":
            if tamer_mana >= 6:
                tamer_mana -= 6
                display_game_state(f"Tamer Mana now at {tamer_mana}")
            else:
                display_game_state("Not enough Tamer Mana to level up Tamer!")

        case "end":
            turn += 1
            tamer_mana += mana
            mana = min(turn, 10)
            attack_token = not attack_token
            next_card = draw(deck, hand)
            if next_card == None:
                display_game_state("You can't draw a card")
            else:
                hand.append(next_card)
        
        case "damage core":
            try:
                core_hp -= int(command[1])
                display_game_state(f"Core HP is now {core_hp}")
                if core_hp <= 0:
                    display_game_state("You lose!")
                    break
            except IndexError:
                print("Not enough parameters")
            except ValueError:
                print(f"Couldn't convert from {command[1]} of type {type(command[1])} to integer")

        case "add":
            try:
                card_name: str = command[1]
                to: str = command[2]

                if to == "deck":
                    deck.insert(randint(0,len(deck)-1), card_name)
                elif to == "hand" and len(hand) < 10:
                    hand.append(card_name)
                elif to == "hand" and len(hand) >= 10:
                    display_game_state(f"Couldn't add '{card_name}' to hand. Discarding '{card_name}'")
            except IndexError:
                display_game_state("Invalid number of parameters")
        
        case "transform":
            try:
                replace_card: str = command[1]
                transform_card: str = command[2]
                replace_idx: int = hand.index(replace_card)
                hand[replace_idx] = transform_card
                display_game_state(f"Transformed '{replace_card}' into '{transform_card}'")
            except IndexError:
                display_game_state("Invalid number of parameters")
            except ValueError:
                display_game_state(f"'{replace_card}' not in hand!")
        
        case "spend mana":
            try:
                to_spend = int(command[1])
                if mana - to_spend < 0:
                    display_game_state("You don't have enough mana!")
                else:
                    mana = min(mana-to_spend, 10)
                    display_game_state(f"Spent {to_spend} Mana, Mana now at {mana}")
            except IndexError:
                display_game_state("Invalid number of parameters")
        
        case "random":
            try:
                begin: int = int(command[1])
                end: int = int(command[2])
                iterations: int = int(command[3])
                max_repeats: int = int(command[4])
                frequencies: dict = {}
                if len(command) > 5:
                    target_map: list = []
                    idx: int = 5
                    while idx < len(command):
                        target_map.append(command[idx])
                        idx += 1
                    
                    successful: int = 0
                    while successful < iterations:
                        res: int = randint(begin, end)
                        if not res in frequencies:
                            frequencies[res] = 1
                            successful += 1
                            display_game_state(f"Hit target '{target_map[res]}'")
                        elif res in frequencies and frequencies[res] < max_repeats:
                            frequencies[res] += 1
                            successful += 1
                            display_game_state(f"Hit target '{target_map[res]}'")
                
                else:
                    successful: int = 0
                    while successful < iterations:
                        res: int = randint(begin, end)
                        if not res in frequencies:
                            frequencies[res] = 1
                            successful += 1
                            display_game_state(f"Hit target {res}")
                        elif res in frequencies and frequencies[res] < max_repeats:
                            frequencies[res] += 1
                            successful += 1
                            display_game_state(f"Hit target {res}")
            except IndexError:
                display_game_state("Invalid number of parameters")
        
        case "remove":
            try:
                card: str = command[1]
                place: str = command[2]

                if place == "hand":
                    hand.remove(card)
                elif place == "deck":
                    deck.remove(card)
                else:
                    display_game_state(f"Card Location {place} unknown. Use 'hand' or 'deck' instead")
            
            except IndexError:
                display_game_state("Invalid number of parameters")
            except ValueError:
                display_game_state(f"Couldn't find card '{card}' in '{place}'")

        case "save":
            with open("GameState.json", "w") as state_file:
                game_state: list = [deck, hand, turn, mana, tamer_mana, attack_token, core_hp]
                json.dump(game_state, state_file)
            
            print("Game state saved")
        
        case "win":
            display_game_state("You won!")
            break

        case "exit":
            break
        
        case _:
            display_game_state(f"Command '{command[0]}' is unknown")