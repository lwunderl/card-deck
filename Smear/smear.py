#import dependencies
from random import shuffle
import playing_cards as pc

#Run game
def main():
    #Create players and teams, there are always 2 teams in smear
    number_of_players = int(input("How many players? "))
    players = []
    for player in range(1,number_of_players + 1):
        players.append(pc.Player(f"Player_{player}"))
    
    team_1 = pc.Team("Team_1")
    team_2 = pc.Team("Team_2")
    i = 0
    for player in players:
        if i % 2 == 0:
            team_1.add_player(player)
        else:
            team_2.add_player(player)
        i += 1

    #Create card deck
    deck = pc.CardDeck("Smear Deck")
    deck.build_deck("smear")
    
    discard_pile = pc.CardDeck("Discard Pile")

    #Create hands
    hands = []
    for hand in range(1,number_of_players + 1):
        hands.append(pc.Hand(f"Hand_{hand}"))

    #Deal hands
    shuffle(deck.cards)
    deck.deal_cards(1, hands, 10)

    #Players pick up hands
    i = 0
    for player in players:
        player.get_hand(hands[i])
        i += 1

    #Make bids
    bid = pc.Bid()
    for player in players:
        bid.make_bid(player)
    
    #declare trump of the deck
    bid.declare_trump(deck)
    
    #discard non-trump cards
    for player in players:
        non_trump = []
        for card in player.hand.cards:
            if card.is_trump(bid.trump):
                continue
            else:
                non_trump.append(card)
        player.hand.discard_cards(non_trump, discard_pile)
    
    #shuffle discard pile
    shuffle(discard_pile.cards)

    #draw to 7 cards in hand
    for player in players:
        while True:
            if len(player.hand.cards) < 7 and len(deck.cards) > 0:
                player.hand.draw_hand(1,deck)
            elif len(player.hand.cards) < 7 and len(discard_pile.cards) > 0:
                player.hand.draw_hand(1,discard_pile)  
            else:
                break
                
    #Create card-play
    #Store tricks

    #Score tricks
    #Tally team scores
    #clear hands and tricks and re-deal

    #log moves

if __name__ == "__main__":
    main()