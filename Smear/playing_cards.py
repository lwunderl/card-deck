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

    def __str__(self):
        return f"Playing card named {self.name}"
    
    def is_trump(self, trump):
        black = ["Spades", "Clubs"]
        red = ["Hearts", "Diamonds"]
        if self.suit == trump:
            return True
        elif self.id == "Jack" and self.suit in black and trump in black:
            return True
        elif self.id == "Jack" and self.suit in red and trump in red:
            return True
        elif self.id == "Joker":
            return True
        else:
            return False

#create playing card deck object class
class CardDeck:
    def __init__(self, name):
        self.name = name
        self.suits = []
        self.cards = []
    
    def __str__(self):
        return f"Card deck named {self.name}"

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
    def deal_cards(self, n, hands, passes=1):
        for _ in range(passes):
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
    #n must be integer, deck must be card deck object or subclass
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
    
    def __str__(self):
        return f"Trick Name: {self.name}, Trick Cards: {self.cards}"

    #search through the trick to add up the card values for the "game" score point in smear
    def game_points(self):
        for card in self.cards:
            if card.id in ["Ace","King","Queen","Jack","10"]:
                self.game_points += card.value
    
    #search through the trick to find the highest trump card for the "high" score point in smear based on playing card object self.order
    def high(self):
        order = 0
        for card in self.cards:
            if card.suit == self.trump and card.order > order:
                self.high = card.order
    
    #search through the trick to find the lowest trump card for the "low" score point in smear based on playing card object self.order
    def low(self):
        order = 0
        for card in self.cards:
            if card.suit == self.trump and card.order < order:
                self.low = card.order
    
    #search through the trick to find the "Jack", "Jick", and "Jokers" for smear
    def jjj(self):
        for card in self.cards:
            if card.id == "Jack" and card.is_trump(self.trump):
                self.score_cards.append(card.name)
            elif card.id == "Joker":
                self.score_cards.append(card.name)

#create a player class object
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = ""
        self.npc = False
    
    def __str__(self):
        return f"{self.name}"
    
    def get_hand(self, hand):
        self.hand = hand

#create a team class object which will contain player objects and trick objects, players will not have a score, they must be placed on a team even if it is a team of 1 player.
class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.tricks = []
        self.score = 0
    
    def __str__(self):
        return f"Team Name: {self.name}, Players: {[x.name for x in self.players]}, Tricks: {[x.name for x in self.tricks]}, Score: {self.score}"
    
    #attach trick to team
    def get_trick(self, trick):
        self.trick.append(trick)

    #attach player to team
    def add_player(self, player):
        self.players.append(player)

    #add score
    def add_score(self, n):
        self.score += n
    
    #subtract score
    def subract_score(self, n):
        self.score -= n

    def score_tricks(self):
        for trick in self.tricks:
            print(len(trick.score_cards), trick.game_points, trick.high, trick.low)

#create bidding object class 
class Bid:
    def __init__(self):
        self.highest_bid = 0
        self.trump = ""
        self.winning_bidder = ""

    def __str__(self):
        return f"Winning Bidder: {self.winning_bidder}, Bid: {self.highest_bid}, Trump: {self.trump}"

    #make a bid using player object, and maximum bid allowed
    def make_bid(self, player, max=7):
        while True:
            try:
                bid = int(input(f"{player.name}'s bid? "))
                if bid > self.highest_bid and bid <= max:
                    self.highest_bid = bid
                    self.winning_bidder = player
                    break
                elif bid <= self.highest_bid:
                    print("Bid not high enough, next!")
                    break
                else:
                    print(f"{max} is the maximum allowable bid!")
            except ValueError:
                print("Bid needs to be an integer!")

    #declare trump using deck suits
    def declare_trump(self, deck):
        while True:
            trump = input(f"{self.winning_bidder}, declare trump suit {deck.suits}: ")
            if trump in deck.suits:
                self.trump = trump
                break
            else:
                print("Trump must be a suit in the deck!")

#main script
def main():
    ...

if __name__ == "__main__":
    main()