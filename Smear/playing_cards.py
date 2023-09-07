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
    def __init__(self):
        self.cards = []

    #create a deck of cards
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
    
    #create draw card method to remove playing card objects from card deck object
    def draw_cards(self, n):
        draw = self.cards[:n]
        self.cards = self.cards[n:len(self.cards)]
        return draw
    
    #create discard card method to add playing card objects do a card deck object
    def discard_cards(self, cards):
        discard = cards
        self.cards = self.cards.extend(cards)
        return discard

#create player hand object class
class PlayerHand(CardDeck):
    def __init__(self):
        super().__init__()
        self.cards = []
    
    #create method to draw playing card objects from card deck object
    def draw_hand(self, n, deck):
        draw = deck.draw_cards(n)
        self.cards.extend(draw)
    
    def discard_hand(self, cards):
        ...

#create bidding mechanic class 
class Bid:
    def __init__(self, game):
        self.game = game

    def declare_trump(self):
        ...

#main script
def main():
    smear_deck = CardDeck()
    smear_deck.build_deck("smear")
    print([smear_deck.cards[x].name for x in range(len(smear_deck.cards))],"\n")
    player_hand = PlayerHand()
    player_hand.draw_hand(10, smear_deck)
    #draw = smear_deck.draw_cards(5)
    #player_hand.build_hand(draw)
    print([player_hand.cards[x].name for x in range(len(player_hand.cards))],"\n")
    print([smear_deck.cards[x].name for x in range(len(smear_deck.cards))],"\n")


if __name__ == "__main__":
    main()