import random

# numbers
VALUES = sorted(list(range(1, 13)) * 2)
# add the wilds
VALUES += ["W"] * 2
# and the skip
VALUES += ["S"]

COLORS = ["R", "G", "B", "Y"]


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
    def __repr__(self):
        return f"<{self.color}{self.value}>"
    def __str__(self):
        return f"<{self.color}{self.value}>"
    def __lt__(self, other):
        value_order = list(range(1, 13)) + ["W", "S"]
        color_order = COLORS
        def ltHelper(card):
            return value_order.index(card.value), color_order.index(card.color)
        return ltHelper(self) < ltHelper(other)
    

class Deck:
    def __init__(self, num_decks = 1):
        # Create full deck
        self.full_deck = []
        for _ in range(num_decks):
            for val in VALUES:
                for color in COLORS:
                    self.full_deck.append(Card(val, color))

        # Create discard pile
        self.discard_pile = []

        # Create "current" deck (where you draw from)
        self.current_deck = self.full_deck.copy()
        self.shuffle()

    def shuffle(self):
        if len(self.discard_pile) > 1:
            self.current_deck += self.discard_pile[:-1]
            self.discard_pile = self.discard_pile[-1:]
        random.shuffle(self.current_deck)

    def draw(self):
        if not self.is_empty():
            return self.current_deck.pop()
        else:
            self.shuffle()
            return self.current_deck.pop()

    def is_empty(self):
        return len(self.current_deck) == 0
    
    def discard(self, card):
        if type(card) is not Card:
            print("That wasn't a card!")
            return
        self.discard_pile.append(card)