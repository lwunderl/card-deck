#import dependencies
from random import shuffle

#Create number of players
def choose_number_of_players():
    player_count = int(input("How many players? "))
    return player_count

#Create card deck
def create_deck():
    suits = ["Spades","Hearts","Diamonds","Clubs"]
    facecards = ["Ace","King","Queen","Jack"]
    deck = [{"card_name": f"{x} of {y}", "card_number": x, "card_suit": y, "card_value": 0} for x in range(2,11) for y in suits]
    deck.extend([{"card_name": f"{x} of {y}", "card_number": x, "card_suit": y, "card_value": 0} for x in facecards for y in suits])
    deck.extend([{"card_name": "Joker", "card_number": "Joker", "card_suit": "Joker", "card_value": 0}, {"card_name": "Joker", "card_number": "Joker", "card_suit": "Joker", "card_value": 0}])
    for card in deck:
        if card["card_number"] == 10:
            card["card_value"] = 10
        if card["card_number"] == "Ace":
            card["card_value"] = 4
        if card["card_number"] == "King":
            card["card_value"] = 3
        if card["card_number"] == "Queen":
            card["card_value"] = 2
        if card["card_number"] == "Jack":
            card["card_value"] = 1
    return deck

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
def bid(player_count):
    winning_bidder = ""
    high_bid = 0
    for _ in range(player_count):
        bid = int(input(f"Player {_ + 1}'s bid? "))
        if bid > high_bid:
            high_bid = bid
            winning_bidder = f"Player {_ + 1}"
    return {"winning_bidder": winning_bidder, "winning_bid": high_bid}

def declare_trump(winning_bid):
    trump = input(f"What suit is trump? ")
    winning_bid["trump_suit"] = trump
    return winning_bid

def discard(hands, winning_bid):
    trump = winning_bid["trump_suit"]
    for hand in hands:
        cards = list(hand.values())[0]
        for card in cards:
            print(card)
            

#Create card-play


#Create scoring


#Run game
def main():
    player_count = choose_number_of_players()
    deck = create_deck()
    #Shuffle deck
    shuffle(deck)
    hands = deal(deck, player_count)
    print(hands[0])

if __name__ == "__main__":
    main()