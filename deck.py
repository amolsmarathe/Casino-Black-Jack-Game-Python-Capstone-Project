"""
Deck class-
Instance variables:
    1. cards- list of object of sub class Card()

Class variables:
    1. card_ranks- list of all ranks of a card
    2. card_suits- list of all suits of a card
    3. card_values- dictionary of card values for hand calculation purposes

Instance Methods:
    1. __str__()- to print all cards in the deck
    2. shuffle()- to shuffle the cards in the deck
    3. draw_card()- to draw one card from the deck
    4. show_count()- to show the current count of cards available in the deck

Inner classes for Dealer class-
    1. Card
        Instance variables: suit- suit of the card
                            rank- rank of the card
        Instance methods: __str__()- to print the rank and suit of the card
"""

import random


class Deck:
    card_ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Ace', 'King', 'Queen',
                  'Jack']
    card_suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    card_values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
                   'Ace': 0, 'King': 10, 'Queen': 10, 'Jack': 10}

    def __init__(self):
        self.cards = []
        for suit in Deck.card_suits:
            for rank in Deck.card_ranks:
                self.cards.append(self.Card(suit, rank))

    def __str__(self):
        """
        Method to print all cards currently available in the deck
        :return: none
        """
        print('\n')
        for card in self.cards:
            return card

    def shuffle(self):
        """
        Method to shuffle the cards in the deck
        :return: none
        """
        random.shuffle(self.cards)

    def draw_card(self):
        """
        Method to draw one card from the deck
        :return: Card
        """
        card = self.cards[0]
        self.cards.pop(0)
        return card

    def show_count(self):
        """
        Method to show the current count of cards available in the deck
        :return: none
        """
        print(f'\nNumber of cards remaining in deck now: {len(self.cards)}')

    class Card:
        """
        Class to define the Card in a deck
        """
        def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank

        def __str__(self):
            """
            Method to print the rank and suit of the card
            :return: none
            """
            return f'{self.suit} of {self.rank}'
