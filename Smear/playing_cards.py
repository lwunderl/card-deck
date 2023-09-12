#classes to create card games with

#create playing card object class
class PlayingCard:
    def __init__(self, name, id="", suit="", value=0, color="", order=0):
        self.name = str(name)
        self.id = str(id)
        self.suit = str(suit)
        self.value = int(value)
        self.color = str(color)
        self.order = int(order)

#create playing card deck object class
class CardDeck:
    def __init__(self, name):
        self.name = name
        self.suits = []
        self.cards = []

    #create a card deck object full of playing card objects
    #game is a string
    def build_deck(self, game):
        self.game = game

        #smear deck
        if game == "smear":
            self.suits = ["Spades","Hearts","Diamonds","Clubs"]
            facecards = ["Jack","Queen","King","Ace"]
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0, order=x) for x in range(2,11) for y in self.suits])
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in facecards for y in self.suits])
            self.cards.extend([PlayingCard("Joker", "Joker", "Joker", 0, order=11), PlayingCard("Joker", "Joker", "Joker", 0, order=11)])
            for card in self.cards:
                if card.suit in ["Spades","Clubs"]:
                    card.color = "Black"
                elif card.suit in ["Hearts","Diamonds"]:
                    card.color = "Red"
            for card in self.cards:
                if card.id == "10":
                    card.value = 10
                    card.order = 10
                elif card.id == "Jack":
                    card.value = 1
                    card.order = 13
                elif card.id == "Queen":
                    card.value = 2
                    card.order = 14
                elif card.id == "King":
                    card.value = 3
                    card.order = 15
                elif card.id == "Ace":
                    card.value = 4
                    card.order = 16

        #euchre deck
        elif self.game == "euchre":
            self.suits = ["Spades","Hearts","Diamonds","Clubs"]
            facecards = ["Ace","King","Queen","Jack"]
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in range(9,11) for y in self.suits])
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in facecards for y in self.suits])
            for card in self.cards:
                if card.suit in ["Spades","Clubs"]:
                    card.color = "Black"
                elif card.suit in ["Hearts","Diamonds"]:
                    card.color = "Red"
        
        #standard deck
        elif self.game == "standard":
            self.suits = ["Spades","Hearts","Diamonds","Clubs"]
            facecards = ["Ace","King","Queen","Jack"]
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in range(2,11) for y in self.suits])
            self.cards.extend([PlayingCard(f"{x} of {y}", x, y, 0) for x in facecards for y in self.suits])
            for card in self.cards:
                if card.suit in ["Spades","Clubs"]:
                    card.color = "Black"
                elif card.suit in ["Hearts","Diamonds"]:
                    card.color = "Red"
    
    #create draw card method to remove playing card objects from card deck object and return drawn cards
    #n is an integer
    def draw_cards(self, n):
        draw = self.cards[:n]
        self.cards = self.cards[n:len(self.cards)]
        return draw
    
    #create discard card method to remove specific playing card objects from card deck object and place into separate card deck object
    #cards must be a list of playing card objects example: [player_hand.cards[2]] or player_hand.cards[0:], deck must be a card deck object in which to discard to.
    def discard_cards(self, cards, deck):
        deck.cards.extend(cards)
        for card in cards:
            self.cards.remove(card)
    
    #create a method to deal player card objects from card deck object to player hand objects
    #n is an integer and the number of cards you would like to deal in each pass, hands is a list of player hand objects, p is an integer for the number of dealing passes to make
    def deal_cards(self, n, hands, p=1):
        for _ in range(p):
            for hand in hands:
                hand.draw_hand(n, self)
    
    #display card deck information
    def display_cards(self):
        print(self.name, [self.cards[x].name for x in range(len(self.cards))])

#create player hand object subclass of card deck class
class Hand(CardDeck):
    def __init__(self, name):
        super().__init__(name)
        self.cards = []
    
    #create method to draw playing card objects from card deck object and place into player hand object
    #n must be integer, deck must be card deck object
    def draw_hand(self, n, deck):
        draw = deck.draw_cards(n)
        self.cards.extend(draw)

#create a trick object subclass of card deck class
class Trick(CardDeck):
    def __init__(self, name, bid):
        super().__init__(name)
        self.cards = []
        self.trump = bid.trump
        self.score_cards = []
        self.game_points = 0
        self.high = 0
        self.low = 0

    #search through the trick to add up the card values for the "game" score point
    def game_points(self):
        for card in self.cards:
            if card.id in ["Ace","King","Queen","Jack","10"]:
                self.game_points += card.value
    
    #search through the trick to find the highest trump card for the "high" score point
    def high(self):
        order = 0
        for card in self.cards:
            if card.suit == self.trump and card.order > order:
                self.high = card.order
    
    #search through the trick to find the lowest trump card for the "low" score point
    def low(self):
        order = 0
        for card in self.cards:
            if card.suit == self.trump and card.order < order:
                self.low = card.order
    
    #search through the trick to find the "Jack", "Jick", and "Jokers" score points
    def jjj(self):
        black = ["Spades", "Clubs"]
        red = ["Hearts", "Diamonds"]
        for card in self.cards:
            if card.id == "Jack" and card.suit in black and self.trump in black:
                self.score_cards.extend(card.name)
            elif card.id == "Jack" and card.suit in red and self.trump in red:
                self.score_cards.extend(card.name)
            elif card.id == "Joker":
                self.score_cards.extend(card.name)

#create a player class object
class Player:
    def __init__(self, name):
        self.name = name

#create a team class object which will contain player objects and trick objects
class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.tricks = []
        self.score = 0
    
    #attach trick to team
    def get_trick(self, trick):
        self.trick.extend(trick)

    #attach player to team
    def get_player(self, player):
        self.player.extend(player)

class Score:
    def __init__(self):
        self.score = 0
    
    def score_tricks():
        ...

#create bidding object class 
class Bid:
    def __init__(self):
        self.highest_bid = 0
        self.trump = ""
        self.winning_bidder = ""

    #make a bid using player object
    def make_bid(self, player):
        while True:
            try:
                bid = int(input(f"{player.name}'s bid? "))
                if bid > self.highest_bid:
                    self.highest_bid = bid
                    self.winning_bidder = player.name
                break
            except ValueError:
                print("Bid needs to be a number")

    #declare trump with suit as string
    def declare_trump(self, suit):
        self.trump = suit
        print(f"Trump is {suit}!")
    
    #display the bid information
    def display_bid(self):
        print(f"Winning Bidder: {self.winning_bidder}, Bid: {self.highest_bid}, Trump: {self.trump}")

#main script
def main():
    smear_deck = CardDeck("smear")
    smear_deck.build_deck("smear")
    player_hand = Hand("player_hand")
    player_hand.draw_hand(50,smear_deck)
    player_hand.display_cards()

    bid = Bid()
    bid.declare_trump("Hearts")

    trick = Trick("trick_1", bid)
    player_hand.discard_cards(player_hand.cards[:40], trick)
    trick.display_cards()


if __name__ == "__main__":
    main()