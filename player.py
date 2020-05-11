"""
This module consists:
Player class-
    Instance variables:
        1. Name (name of the player)
        2. Chips (object of sub-class Chips())
        3. Hand List (List of hand objects which are instantiated from sub-class Hand())
            This hand list will be useful for the future enhancements in the game when user chose the game move 'SPLIT'
        4. Initial Bet (a dictionary of bet provided by the player)

    Class variables:
        1. players - list of all players who are playing the game
        2. winners_list - the players who have won the game round (except the black jack players)
        3. losers_list - the players who have lost the game round
        4. tie_players_list - the players who had a tie with the dealer
        5. black_jack_players_list - the players who have won the blackjack in the game round

    Static Methods:
        1. show_hand_with_value_all_players() - to display the hand and hand value for all players playing current round
        2. define_player_list() - to create and define all the players who are going to play the game

    Instance Methods:
        1. enter_bet() - to receive initial bet from the player
        2. show_hand_with_value_one_player() - to display

    Inner classes (sub-classes) for Player class-
        1. Chips
            Instance variables: chips_balance- dictionary of chips balance per color of chips for each player
            Instance methods: __str__()- to print current chips balance for a player
                              deposit()- to deposit winning chips into the player's account
                              withdraw()- to withdraw lost chips from the player's account

        2. Hand
            Instance variables: cards- list of Card() objects in a player's hand
                                value- hand value considering adjustment for Ace
                                bet- bet applied on the hand. This is more useful considering the future enhancements in
                                    the game when one player can have multiple hands and each hand will have its bet.
                                    This is when the player choose the game move 'SPLIT'
            Instance methods: __str__()- to print current hand and its value
                              calculate_value()- to calculate latest hand value for the cards in the player's hand
"""

from deck import *


class Player:
    """
    The class for players in the game
    """
    players = []
    winners_list = []
    losers_list = []
    tie_players_list = []
    black_jack_players_list = []

    def __init__(self, name, chips_balance_dictionary):
        self.name = name
        self.chips = Player.Chips(chips_balance_dictionary)
        self.hand_list = [self.Hand()]   # There can be multiple hands per player when player splits. Future enhancement
        self.initial_bet = {'white': 0, 'red': 0, 'green': 0, 'black': 0}
        Player.players.append(self)

    @staticmethod
    def define_player_list(default_chips_balance):
        """
        Method to create and define all the players who are going to play the game
        :param default_chips_balance: Dictionary of default chips balance to be assigned to each new player created
        :return: none
        """
        import game_methods
        while True:         # loop until no. of players <= 0
            count_players = game_methods.try_input_int('How many players would like to play for this round? ')
            if count_players > 0:
                break
            else:
                print('At least one player should play. Please try again.')

        for count in range(count_players):
            name = game_methods.try_input_str(f'Enter the name of player {count + 1}: ')
            Player(name, default_chips_balance)

    @staticmethod
    def show_hand_with_value_all_players():
        """
        Method to display the hand and hand value for all players playing current round
        :return:none
        """
        for player in Player.players:
            print(f'{player.name}\'s hand is: ')
            for card in player.hand_list[0].cards:
                print(f'\t{card}')
            print(f'{player.name}\'s hand value is: {player.hand_list[0].calculate_value()}')

    def show_hand_with_value_one_player(self):
        """
        Method to display the hand and hand value for all players playing current round
        :return: none
        """
        print(f'{self.name}\'s hand is: ')
        for card in self.hand_list[0].cards:
            print(f'\t{card}, ', end='')
        print(f'\n{self.name}\'s hand value is: {self.hand_list[0].calculate_value()}')

    def enter_bet(self):
        """
        Method to receive initial bet from the player
        :return: none
        """
        self.initial_bet = {'white': 0, 'red': 0, 'green': 0, 'black': 0}
        print(f'\n{self.name}, please enter your bet now:')
        while True:             # loop until bet is zero
            for color in Player.Chips.chips_colors:
                while True:     # loop until bet is a valid integer and is <= available chips balance
                    try:
                        chips = int(input(f'How many {color} chips would you like to bet? '))
                    except Exception as e:
                        print('Please enter valid number (only integers)', e)
                    else:
                        if chips < 0:
                            print('Please enter positive numbers only. Try again.')
                            continue
                        elif chips <= self.chips.chips_balance[color]:
                            self.initial_bet[color] = chips
                            break
                        else:
                            print(f'You do not have sufficient {color} chips. You have only '
                                  f'{self.chips.chips_balance[color]}. Try entering correct amount of chips again')
            if set(self.initial_bet.values()) == {0}:
                print('Your bet cannot be zero. Please try again.')
                continue
            elif sum(self.initial_bet.values()) < 10:
                print('You must bet at least 10 chips of any value. Please try again.')
                continue
            else:
                break

    class Chips:
        """
        Class to define the chips balance for each player, deposit and withdraw chips when player wins or loses
        """
        chips_colors = ['white', 'red', 'green', 'black']
        # chips_values = {'white': 25, 'red': 50, 'green': 100, 'black': 500}
        # Above chips values can be used for calculating the actual cost of the chips in dollars, but we have not used
        # these values in the game. Although it can be used to enhance the game experience.

        def __init__(self, chips_balance_dictionary):
            self.chips_balance = {**chips_balance_dictionary}    # This is IMPORTANT. Copy the dictionary do not simply
            #                                              assign it like self.chips_balance = chips_balance_dictionary
            #                                              If done so, it assigns the chips_balance_dictionary directly
            #                                              and causes issues while deposit/withdraw chips.

        def __str__(self):
            """
            Method to print current chips balance for the player
            :return: Strings with chips balance for the player
            """
            white_chips = self.chips_balance["white"]
            red_chips = self.chips_balance["red"]
            green_chips = self.chips_balance["green"]
            black_chips = self.chips_balance["black"]
            x = 'your chips balance is:'
            y = f'\n\tWhite chips: {white_chips}, Red chips: {red_chips}, ' \
                f'\n\tGreen chips: {green_chips}, Black chips: {black_chips}, ' \
                f' \n\t  Total chips = {white_chips + red_chips + green_chips + black_chips}'
            return x + y

        def deposit(self, chips_amount):
            """
            Method to deposit winning chips into the player's account
            :param chips_amount: The dictionary of amount of chips in a bet
            :return: none
            """
            self.chips_balance['white'] += chips_amount['white']
            self.chips_balance['red'] += chips_amount['red']
            self.chips_balance['green'] += chips_amount['green']
            self.chips_balance['black'] += chips_amount['black']

        def withdraw(self, chips_amount):
            """
            Method to withdraw lost chips from the player's account
            :param chips_amount: The dictionary of amount of chips in a bet
            :return: none
            """
            self.chips_balance['white'] -= chips_amount['white']
            self.chips_balance['red'] -= chips_amount['red']
            self.chips_balance['green'] -= chips_amount['green']
            self.chips_balance['black'] -= chips_amount['black']

    class Hand:
        """
        Class to define the hand for each player and calculate the hand value
        """
        def __init__(self):
            self.cards = []
            self.value = 0
            self.bet = {'white': 0, 'red': 0, 'green': 0, 'black': 0}

        def __str__(self):
            """
            Method to print current hand cards and its value
            :return: Strings with cards in a hand and hand value
            """
            x = ''
            for card in self.cards:
                x += f'\n\t{card}'
            hand = 'Your hand is: ' + x
            value = self.calculate_value()
            hand_with_value = hand + '\nand your hand value is: ' + str(value)
            return hand_with_value

        def calculate_value(self):
            """
            Method to calculate latest hand value for the cards in the player's hand
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
