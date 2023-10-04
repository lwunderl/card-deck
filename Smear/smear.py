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
    
    #Create teams
    number_of_teams = 2
    teams = []
    for team in range(1, number_of_teams + 1):
        teams.append(pc.Team(f"Team_{team}"))

    #add players to teams
    i = 0
    for player in players:
        if i % 2 == 0:
            teams[0].add_player(player)
        else:
            teams[1].add_player(player)
        i += 1

    #Create hands
    hands = []
    for hand in range(1,number_of_players + 1):
        hands.append(pc.Hand(f"Hand_{hand}"))

    #Players pick up hands
    i = 0
    for player in players:
        player.get_hand(hands[i])
        i += 1
        
#start loop for game
        
    #Create card deck
    deck = pc.CardDeck("Smear Deck")
    deck.build_deck("smear")
    
    #Create card deck for discard pile
    discard_pile = pc.CardDeck("Discard Pile")

    #Deal hands
    shuffle(deck.cards)
    deck.deal_cards(1, hands, 10)

    #Make bids
    bid = pc.Bid()
    for player in players:
        bid.make_bid(player)
    
    #declare trump of the deck
    bid.declare_trump(deck)

    #winning bidder gets to go first
    players = pc.winner_leads(bid.winning_bidder, players)
    
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

    #draw to fill 7 cards in hand
    for player in players:
        while True:
            if len(player.hand.cards) < 7 and len(deck.cards) > 0:
                player.hand.draw_hand(1,deck)
            elif len(player.hand.cards) < 7 and len(discard_pile.cards) > 0:
                player.hand.draw_hand(1,discard_pile)  
            else:
                break
    
    #set trick number for naming purposes
    t = 1
    #Store tricks for data collection purposes
    game_data = []

    #Card-play
    #One round for each card in hand
    for _ in range(7):
        #Create trick
        trick = pc.Trick(f"trick_{t}")
        #variable to store current winning card in trick
        winning_card = pc.PlayingCard("Winning_Card")
        #variable to store current winning player for trick
        current_winner = pc.Player("Winning_Player")
        #loop through each player to play a card object from hand and store in trick
        for player in players:
            #variable to store names of card objects
            current_hand = [x.name for x in player.hand.cards]
            #loop through trick and hand to make sure card selected follows criteria and to determine if card and player is new winner
            while True:
                #visual for bid
                print(bid)
                #visual for trick
                trick.display_cards()
                #choose card to play by index number
                card_played_index = int(input(f"{player.name}, please choose a card {current_hand} "))
                #variable for card name
                card_played = current_hand[card_played_index]
                #bool to verify card chosen follows playing rules
                good_card = True
                #loop through hand to find card_played
                for hand_card in player.hand.cards:
                    #find chosen card in hand
                    if hand_card.name == card_played:
                        #card needs to follow lead suit or be trump to be valid
                        if hand_card.is_follow_suit(trick) or hand_card.is_trump(bid.trump):
                            #if trump is played, check if it's the highest trump
                            if hand_card.is_trump(bid.trump):
                                #set highest trick trump card variable to card played
                                highest_trump = hand_card
                                #loop through trick to check for higher trick trump card
                                for trick_card in trick.cards:
                                    if trick_card.is_trump(bid.trump) and trick_card.order > highest_trump.order:
                                        highest_trump = trick_card
                                    elif trick_card.id == "Jack" and trick_card.suit == bid.trump and hand_card.id == "Jack":
                                        highest_trump = trick_card
                                #award card played as the current winning player and winning card if valid
                                if hand_card == highest_trump:
                                    winning_card = hand_card
                                    current_winner = player
                                    player.hand.discard_cards([hand_card], trick)
                                else:
                                    player.hand.discard_cards([hand_card], trick)
                            #if trump is not played, check to see if the winning card is already trump
                            elif winning_card.is_trump(bid.trump):
                                player.hand.discard_cards([hand_card], trick)
                            #if trump is not played, and the winning card is not trump, is the card played higher than the winning card
                            elif hand_card.order > winning_card.order:
                                winning_card = hand_card
                                current_winner = player
                                player.hand.discard_cards([hand_card], trick)
                            #if trump is not played, and the winning card is not trump, and the card played is lower than the winning card
                            else:
                                player.hand.discard_cards([hand_card], trick)
                            good_card = True
                        #there must be no lead suit in hand in order to play off-suit
                        elif hand_card.is_renege(trick, player.hand, bid.trump):
                            good_card = False
                            print("renege, choose suit card")
                        #assuming validation criteria cannot be met, any card may be played in place of valid card.
                        else:
                            player.hand.discard_cards([hand_card], trick)
                            good_card = True
                        break
                    #card in hand loop does not equal chosen card
                    else:
                        good_card = False
                #Card chosen is valid
                if good_card == True:
                    break
        
        #check if winning player is in team and attach trick to winning player's team
        for team in teams:
            if current_winner in team.players:
                team.get_trick(trick)
        
        #log trick for game data
        game_data.append(trick)

        #next trick number
        t += 1
    
        #change players order of play to winner of last trick goes first
        players = pc.winner_leads(current_winner, players)

    #score tricks
    pc.score_smear(teams, bid)

    #clear hands and tricks and re-deal
    for team in teams:
        team.clear_all_tricks()
    
    print(teams[0], teams[1])

    #log moves

if __name__ == "__main__":
    main()