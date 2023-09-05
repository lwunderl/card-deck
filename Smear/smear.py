#import dependencies
from random import shuffle

#Create number of players
player_count = int(input("How many players? "))

#Create card deck
suits = ["Spades","Hearts","Diamonds","Clubs"]
facecards = ["Ace","King","Queen","Jack"]
deck = [f"{x} of {y}" for x in range(2,11) for y in suits]
deck.extend([f"{x} of {y}" for x in facecards for y in suits])
deck.extend(["Joker","Joker"])

#Shuffle deck
shuffle(deck)

#Create dealing

def deal(deck, player_count):
    hands = []
    cards_per_hand = round(len(deck)/player_count)
    if cards_per_hand > 10:
        cards_per_hand = 10
    cards_dealt = 0
    for player in range(player_count):
        player_number = player + 1
        hand = [deck[x + player + cards_dealt] for x in range(cards_per_hand)]
        cards_dealt += cards_per_hand - 1
        hands.append({f"Player {player_number}'s Hand":hand})
    return hands

#Create bidding

#Create card-play

#Create scoring

def main():
    hands = deal(deck, player_count)
    print(hands[0])

if __name__ == "__main__":
    main()