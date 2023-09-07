#import dependencies
from random import shuffle
from playing_cards import CardDeck

#Create number of players
def choose_number_of_players():
    player_count = int(input("How many players? "))
    return player_count

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
        hands.append({f"Player {player_number} Hand":hand})
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
    discard_pile = []
    for hand in hands:
        cards = list(hand.values())[0]
        for card in cards:
            if card["card_suit"] == winning_bid["trump_suit"]:
                print(card)
            else:
                discard_pile.append(card)
        print(discard_pile)
            
#Create card-play


#Create scoring


#Run game
def main():
    player_count = choose_number_of_players()
    #Create card deck
    deck = CardDeck("smear")
    deck.build_deck()
    #Shuffle deck
    shuffle(deck.cards)
    print(deck.cards[0].name)

if __name__ == "__main__":
    main()