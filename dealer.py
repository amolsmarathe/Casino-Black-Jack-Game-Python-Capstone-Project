"""
Dealer class-
Instance variables:
    1. Hand- Object of sub class Hand()

Instance Methods:
    1. distribute_hand() - to distribute cards to start the game (2 cards per player and 2 cards to the dealer)
    2. draw_till_17() - to draw new cards one by one to dealer until his hand reaches the value 17

Static methods:
    1. serve_one_card() - to serve one card to the given player from the deck

Inner classes for Dealer class-
    1. Hand
        Instance variables: cards- list of Card() objects
                            value- hand value considering adjustment for Ace
        Instance methods: show_cards()- to show the cards of dealer, either single in the beginning or all cards at end
                          calculate_value()- to calculate latest hand value for the cards in the Dealer's hand
"""

from player import *


class Dealer:
    """
    Class to define the Dealer, serve cards and calculate the Dealer's hand value
    """
    def __init__(self):
        self.hand = self.Hand()

    def distribute_hand(self, deck, players_list):
        """
        Method to distribute cards to start the game (2 cards per player and 2 cards to the dealer)
        :param deck: The deck of cards
        :param players_list: List of players currently playing the round
        :return: none
        """
        for i in range(2):
            for player in players_list:
                card = deck.draw_card()     # 1 card for 1 player
                player.hand_list[0].cards.append(card)
            card = deck.draw_card()         # 1 card for dealer
            self.hand.cards.append(card)

    def draw_till_17(self, deck):
        """
        Method to draw new cards one by one to dealer until his hand reaches the value 17
        :param deck: The deck of cards
        :return: none
        """
        while self.hand.calculate_value() < 17:
            self.hand.cards.append(deck.draw_card())

    @staticmethod
    def serve_one_card(player, hand, deck):
        """
        Method to serve one card to the given player from the deck
        :param player: The player to who the card is to be served
        :param hand: The hand into which the card is to be added
        :param deck: The deck of cards
        :return: none
        """
        print(f'\nServing one card to {player.name}...')
        card = deck.draw_card()
        hand.cards.append(card)

    class Hand:
        """
        Class to define the Dealer's hand, its hand value and the cards in it.
        """
        def __init__(self):
            self.cards = []
            self.value = 0

        def show_cards(self, count='one'):
            """
            Method to show the cards of dealer, either single in the beginning or all cards at end
            :param count: The number of cards to be displayed in dealer's hand, 'one' or 'all'
            :return: none
            """
            if count == 'one':
                print(f'\nDealer\'s second card is: {self.cards[1]}')
            elif count == 'all':
                print(f'\nDealer\'s hand is: ')
                for card in self.cards:
                    print(f'\t{card}')

        def calculate_value(self):
            """
            Method to calculate latest hand value for the cards in the Dealer's hand
            :return: Integer of hand value
            """
            self.value = 0
            for card in self.cards:
                self.value += Deck.card_values[card.rank]
            for card in self.cards:
                if card.rank == 'Ace':
                    if self.value + 11 > 21:
                        self.value += 1
                    else:
                        self.value += 11
            return self.value
