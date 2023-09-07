#import dependencies
from random import shuffle
import playing_cards as pc

#Run game
def main():
    #create number of players
    player_count = int(input("How many players? "))

    #create Deck
    smear_deck = pc.CardDeck("smear_deck")
    smear_deck.build_deck("smear")

    discard_pile = pc.CardDeck("discard_pile")

    #create player hands
    all_hands = [pc.PlayerHand(f"player_{x}") for x in range(1,player_count + 1)]

    #shuffle deck
    shuffle(smear_deck.cards)

    #deal cards from deck to hands
    smear_deck.deal_cards(1, all_hands, 10)

    #create bid
    bid = pc.Bid()
    bid.make_bid(all_hands)
    while True:
        trump = input(f"{bid.winning_bidder}, please select a trump {smear_deck.suits}. ")
        if trump in smear_deck.suits:
            bid.declare_trump(trump)
            break
        else:
            print("please select a trump")
    bid.display_bid()

    all_hands[0].display_cards()
                
    #Create card-play

    #Create scoring

if __name__ == "__main__":
    main()