#import dependencies
from random import shuffle
import playing_cards as pc

#Create number of players
def choose_number_of_players():
    player_count = int(input("How many players? "))
    return player_count

#Create bidding
            
#Create card-play

#Create scoring

#Run game
def main():
    player_count = choose_number_of_players()
    #Create card deck
    deck = pc.CardDeck("smear_deck")
    deck.build_deck("smear")
    #Shuffle deck
    shuffle(deck.cards)
    hand = pc.PlayerHand("player1_hand")
    hand.draw_hand(2, deck)
    print(deck.cards[0].name)
    print(hand.cards[0].name)

if __name__ == "__main__":
    main()