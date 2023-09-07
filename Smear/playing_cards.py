#classes to create card games with

#create playing card object class
class PlayingCard:
    def __init__(self, name, number, suit, value):
        self.name = str(name)
        self.number = str(number)
        self.suit = str(suit)
        self.value = int(value)

#create playing card deck object class
class CardDeck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    #create a deck of cards
    #game is a string
    def build_deck(self, game):
        self.game = game

        #smear deck
        if game == "smear":
            suits = ["Spades","Hearts","Diamonds","Clubs"]
            facecards = ["Ace","King","Queen","Jack"]
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in range(2,11) for y in suits])
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in facecards for y in suits])
            self.cards.extend([PlayingCard("Joker", "Joker", "Joker", 0), PlayingCard("Joker", "Joker", "Joker", 0)])
            for card in self.cards:
                if card.number == "10":
                    card.value = 10
                elif card.number == "Ace":
                    card.value = 4
                elif card.number == "King":
                    card.value = 3
                elif card.number == "Queen":
                    card.value = 2
                elif card.number == "Jack":
                    card.value = 1
        #euchre deck
        elif self.game == "euchre":
            suits = ["Spades","Hearts","Diamonds","Clubs"]
            facecards = ["Ace","King","Queen","Jack"]
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in range(9,11) for y in suits])
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in facecards for y in suits])
        
        #standard deck
        elif self.game == "standard":
            suits = ["Spades","Hearts","Diamonds","Clubs"]
            facecards = ["Ace","King","Queen","Jack"]
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in range(2,11) for y in suits])
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in facecards for y in suits])
    
    #create draw card method to remove playing card objects from card deck object and return drawn cards
    #n is an integer
    def draw_cards(self, n):
        draw = self.cards[:n]
        self.cards = self.cards[n:len(self.cards)]
        return draw
    
    #create discard card method to remove specific playing card objects from card deck object and place into separate card deck object
    #cards must be a list of playing card objects example: [player_hand.cards[2]] or player_hand.cards, deck must be a card deck object in which to discard to.
    def discard_cards(self, cards, deck):
        for card in cards:
            self.cards.remove(card)
        deck.cards.extend(cards)
    
    #create a method to deal player card objects from card deck object to player hand objects
    #n is an integer and the number of cards you would like to deal in each pass, hands is a list of player hand objects, p is an integer for the number of dealing passes to make
    def deal_cards(self, n, hands, p=1):
        for _ in range(p):
            for hand in hands:
                hand.draw_hand(n, self)

#create player hand object subclass of card deck class
class PlayerHand(CardDeck):
    def __init__(self, name):
        super().__init__(name)
        self.cards = []
    
    #create method to draw playing card objects from card deck object and place into player hand object
    #n must be integer, deck must be card deck object
    def draw_hand(self, n, deck):
        draw = deck.draw_cards(n)
        self.cards.extend(draw)

#create bidding mechanic class 
class Bid:
    def __init__(self):
        self.highest_bid = 0
        self.trump = ""
        self.winning_bidder = ""

    def bid(self, hands):
        for hand in hands:
            bid = int(input(f"{hand.name}'s bid? "))
            if bid > self.highest_bid:
                self.highest_bid = bid
                self.winning_bidder = hand.name

    def declare_trump(self, suit):
        self.trump = suit

#main script
def main():
    smear_deck = CardDeck("smear_deck")
    smear_deck.build_deck("smear")
    # print([smear_deck.cards[x].name for x in range(len(smear_deck.cards))],"\n")

    discard_pile = CardDeck("discard_pile")
    # print([discard_pile.cards[x].name for x in range(len(discard_pile.cards))],"\n")

    player1_hand = PlayerHand("player_1")
    player2_hand = PlayerHand("player_2")
    player3_hand = PlayerHand("player_3")

    all_hands = [player1_hand, player2_hand, player3_hand]

    bid = Bid()
    bid.bid(all_hands)
    bid.declare_trump(input(f"{bid.winning_bidder}, please select a trump. "))
    print(bid.winning_bidder, bid.trump)

    # smear_deck.deal_cards(2, all_hands, 2)
    # player_hand.draw_hand(10, smear_deck)
    # print([player1_hand.cards[x].name for x in range(len(player1_hand.cards))],"\n")
    # print([smear_deck.cards[x].name for x in range(len(smear_deck.cards))],"\n")

    # player_hand.discard_cards([player_hand.cards[1]], discard_pile)
    # print([player_hand.cards[x].name for x in range(len(player_hand.cards))],"\n")
    # print([smear_deck.cards[x].name for x in range(len(smear_deck.cards))],"\n")
    # print([discard_pile.cards[x].name for x in range(len(discard_pile.cards))],"\n")

if __name__ == "__main__":
    main()