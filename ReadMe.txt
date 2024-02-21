This program uses commands to interact with the user. All arguments for a command are seperated by a comma.
(e.g. burrow, Pa'sschat (8 Mana), 3)

Whenever a card is used as an argument, always add the mana cost in brackets to the end of the name.

Command list:
() round brackets means optional parameter, [] square brackets means required parameter

- play, [card_name]
    Removes the card from your hand if you have enough mana. Subtracts how much mana you have left after playing the card.

- draw, (amount)
    draws as many cards as 'amount'. If no amount is provided, 1 card will be drawn

- burrow, [card_name], [places]
    Moves the card 'card_name' up in the deck by 'places'

- level up
    Checks if you have enough Tamer Mana and subtracts 6 if you have enough

- damage core, [amount]
    Subtracts 'amount' from your Core HP. If you have 0 or less HP, the game will tell you that you lost and ends

- add, [card_name], [to]
    Adds 'card_name' to 'to'. 'to' can either be 'deck' or 'hand'

- transform, [replace_card], [transform_card]
    Transforms 'replace_card' into 'transform_card' in your hand

- spend mana, [to_spend]
    Spends [to_spend] mana. If [to_spend] is higher than the mana you have left, a warning will appear. If [to_spend] is negative, fills up mana

- random, [from], [to], [iterations], [max_repeats], (...map)
    Outputs [iterations] random numbers in the range from [from] to [to]. If a number would be rolled more than [max_repeats], a new number will be rolled.
    Aditionally, a number of targets can be defined as optional parameters, which has the effect of printing the name of the target rather than just the number.
    The range can start at the lowest of 1. Inputting anything below 1 will be set to 1.

- remove, [card], [from]:
    Removes a card from [from]. [from] can either be 'hand' or 'deck'. The card is deleted without spending it's mana cost.

- end
    Ends the current turn. Adds one max mana, fills up max mana, fills up Tamer Mana accordingly, switches Attack Token, and draws a card

- save
    Saves the current game state

- win
    Use when you won the game. The game will tell you that you won and end.

- exit
    close the game


Almost all interactions are logged to the file "GameLog.txt" located in the same directory as the program.
Please provide a deck in form of a .txt file in the same directory. Change the file name in the code at the correct place.