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
                
    #set trick number for naming purposes
    t = 1
    #Store tricks for data collection purposes
    tricks = []

    #Card-play
    for _ in range(7):
        trick = pc.Trick(f"trick_{t}")
        winning_card = pc.PlayingCard("Winning_Card")
        current_winner = pc.Player("Winning_Player")
        for player in players:
            current_hand = [x.name for x in player.hand.cards]
            while True:
                print(bid)
                trick.display_cards()
                card_played = input(f"{player.name}, please choose a card {current_hand} ")
                good_card = True
                for hand_card in player.hand.cards:
                    #find chosen card in hand
                    if hand_card.name == card_played:
                        #card needs to follow lead suit or be trump to be valid
                        if hand_card.is_follow_suit(trick) or hand_card.is_trump(bid.trump):
                            #if trump is played, check if it's the highest trump
                            if hand_card.is_trump(bid.trump):
                                highest_trump = hand_card
                                for trick_card in trick.cards:
                                    if trick_card.is_trump(bid.trump) and trick_card.order > highest_trump.order:
                                        highest_trump = trick_card
                                    elif trick_card.id == "Jack" and trick_card.suit == bid.trump and hand_card.id == "Jack":
                                        highest_trump = trick_card
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
                    else:
                        good_card = False
                if good_card == True:
                    break
        
        #attach trick to winning team
        if current_winner in team_1.players:
            team_1.tricks.append(trick)
        elif current_winner in team_2.players:
            team_2.tricks.append(trick)
        
        #log tricks for history
        tricks.append(trick)

        print(team_1, team_2)
        #next trick number
        t += 1
        #winner leads next trick
        cw_index = players.index(current_winner)
        next_player = players[:cw_index]
        start_player = players[cw_index:]
        players = start_player + next_player

    #Score tricks
    team_1_high = 0
    team_1_low = 20
    team_1_jjj = 0
    team_1_game = 0

    team_2_high = 0
    team_2_low = 20
    team_2_jjj = 0
    team_2_game = 0

    for trick in team_1.tricks:
        print(trick)
        print("game",trick.game_points())
        print("high",trick.high(bid.trump))
        print("low",trick.low(bid.trump))
        print("jjj",trick.jjj(bid.trump))

        if trick.high(bid.trump) > team_1_high:
            team_1_high = trick.high(bid.trump)
        if trick.low(bid.trump) < team_1_low:
            team_1_low = trick.low(bid.trump)
        team_1_jjj += trick.jjj(bid.trump)
        team_1_game += trick.game_points()
    
    print(team_1)
    
    for trick in team_2.tricks:
        print(trick)
        print("game",trick.game_points())
        print("high",trick.high(bid.trump))
        print("low",trick.low(bid.trump))
        print("jjj",trick.jjj(bid.trump))

        if trick.high(bid.trump) > team_2_high:
            team_2_high = trick.high(bid.trump)
        if trick.low(bid.trump) < team_2_low:
            team_2_low = trick.low(bid.trump)
        team_2_jjj += trick.jjj(bid.trump)
        team_2_game += trick.game_points()
    
    print(team_2)
    
    team_1.add_score(team_1_jjj)
    team_2.add_score(team_2_jjj)

    if team_1_high > team_2_high:
        team_1.add_score(1)
    else:
        team_2.add_score(1)

    if team_1_low < team_2_low:
        team_1.add_score(1)
    else:
        team_2.add_score(1)
    
    if team_1_game > team_2_game:
        team_1.add_score(1)
    else:
        team_2.add_score(1)

    print(team_1, team_2)

    #Tally team scores
    #clear hands and tricks and re-deal

    #log moves

if __name__ == "__main__":
    main()