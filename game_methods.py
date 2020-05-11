"""
This module defines following methods useful to play the game:
    1. request_bet() - to request bet from all players
    2. ask_move() - to request the player's move: HIT or STAND or DOUBLE DOWN
    3. is_eligible_for_double_down()-to check if the player is eligible to play double down, although he wishes to to so
    4. play_game() - the recursive method to play the game
    5. play_stand() - method for the game move: STAND
    6. play_hit() - method for the game move: HIT
    7. play_double_down() - method for the game move: DOUBLE DOWN
    8. is_bust() - method to check if the hand busted due to its value exceeding 21
    9. check_lost_before_dealer_draws() - method to check who lost the game, before dealer draws next card to reach 17
    10. final_results_calculation() - method to calculate final results of current round of the game
    11. final_results_display() - method to display final results of current round of the game
    12. ask_to_continue_playing() - method to ask user choice, whether to play next round or start over or quit the game
    13. try_input_int() - Error handling method to accept only particular integer as user input
    14. try_input_str() - Error handling method to accept only particular string as user input
"""

from player import *


def request_bet(player_list):
    """
    Method to request bet from all players
    :param player_list: List of the players who are playing this round
    :return: none
    """
    for player in player_list:
        player.enter_bet()
    print('\nEveryone\'s initial bet: ')
    for player in player_list:
        print(f'{player.name}\'s bet is: \n\t', player.initial_bet)


def ask_move(player):
    """
    Method to request the player's move: HIT or STAND or DOUBLE DOWN
    :param player: The Player who is asked to enter the game move
    :return: none
    """
    while True:
        try:
            move = input(f'\n{player.name}, What\'s your move? Hit or Stand or Double Down? H/S/D- ')
        except Exception as e:
            print('Invalid input. Please enter Hit or Stand or Double Down.', e)
        else:
            if move == '':
                print('You must choose a move.')
                continue
            elif move[0].upper() != 'H' and move[0].upper() != 'S' and move[0].upper() != 'D':
                print('Invalid input. Please enter Hit or Stand or Double Down.')
                continue
            elif move[0].upper() == 'D':
                if is_eligible_for_double_down(player):
                    return move
                else:
                    print('You have insufficient chips balance to double your bet. You must have exactly double '
                          '\nthe amount of each color chip in balance to play DOUBLE DOWN.'
                          '\nPlease choose another move')
                    continue
            else:
                return move


def is_eligible_for_double_down(player):
    """
    Method to check if the player is eligible to play double down, although he wishes to to so
    :param player: The player whose chips balance is to be verified for eligibility to play DOUBLE DOWN
    :return: Boolean
    """
    chips_list = list(player.hand_list[0].bet.values())
    bet_list = list(player.hand_list[0].bet.values())
    for i in range(4):
        if chips_list[i] <= bet_list[i]:
            return False
    else:
        return True


def play_game(player, deck):        # Play for single player
    """
    The recursive method to play all game moves
    :param player: The player who is currently playing
    :param deck: The deck in use for the current round
    :return: none
    """
    while True:
        move = ask_move(player)

        # Player Stands
        if move[0].upper() == 'S':
            play_stand(player)
            break

        # Player Hits
        elif move[0].upper() == 'H':
            play_hit(player, deck)

            # Check and display if player busted
            if is_bust(player.hand_list[0]):
                print(f'Oops.. {player.name} busted!')
                Player.losers_list.append(player)
                break
            else:
                continue
            # Even if player is at 21, do nothing till dealer draws

        # Player plays Double down
        else:
            play_double_down(player, deck)

            # Check and display if player busted
            if is_bust(player.hand_list[0]):
                print(f'Oops.. {player.name} busted!')
                Player.losers_list.append(player)
                break
            else:
                continue


def play_stand(player):
    """
    Method for the game move: STAND
    :param player: The player who is currently playing the move
    :return: none
    """
    print(f'{player.name} chooses to STAND with the hand value at {player.hand_list[0].calculate_value()} \n')


def play_hit(player, deck):
    """
    Method for the game move: HIT
    :param player: The player who is currently playing the move
    :param deck: The deck used for drawing a card
    :return: none
    """
    from dealer import Dealer
    # Serve one card and display hand
    Dealer.serve_one_card(player, player.hand_list[0], deck)
    print(f'{player.name}, you played Hit. ', player.hand_list[0])


def play_double_down(player, deck):
    """
    Method for the game move: DOUBLE DOWN
    :param player: The player who is currently playing the move
    :param deck: The deck used for drawing a card
    :return: none
    """
    from dealer import Dealer

    # Make the bet double
    player.hand_list[0].bet['white'] *= 2
    player.hand_list[0].bet['red'] *= 2
    player.hand_list[0].bet['green'] *= 2
    player.hand_list[0].bet['black'] *= 2
    print(f'{player.name}, you played Double down. Your bet has been doubled now.'
          f'\nYour new bet is: \n\t', player.initial_bet)

    # Serve 1 card and display hand
    Dealer.serve_one_card(player, player.hand_list[0], deck)
    player.show_hand_with_value_one_player()
    print('You have been served a new card, let us see your current position- \n', player.hand)


def is_bust(hand):
    """
    Method to check if the hand busted due to its value exceeding 21
    :param hand: The player's hand to be checked
    :return: Boolean
    """
    return hand.calculate_value() > 21


def check_lost_before_dealer_draws(dealer, player_list):
    """
    Method to check who lost the game, before dealer draws next card to reach 17
    :param dealer: The dealer
    :param player_list: List of players currently playing the game
    :return: none
    """
    for player in player_list:
        if player not in Player.losers_list:
            if player.hand_list[0].calculate_value() < dealer.hand.calculate_value():
                Player.losers_list.append(player)


def final_results_calculation(dealer, player_list):
    """
    Method to calculate final results of current round of the game
    :param dealer: The dealer
    :param player_list: List of players currently playing the game
    :return: none
    """
    if dealer.hand.calculate_value() > 21:
        print('\nDealer busted!\n')

        # Update winners list
        for player in player_list:
            if player not in Player.losers_list:
                Player.winners_list.append(player)
    else:
        # Update winners and losers BOTH lists
        for player in player_list:
            if (player not in Player.losers_list) and (player not in Player.winners_list) and \
                    (player not in Player.tie_players_list):
                if player.hand_list[0].calculate_value() > dealer.hand.calculate_value():
                    Player.winners_list.append(player)
                elif player.hand_list[0].calculate_value() < dealer.hand.calculate_value():
                    Player.losers_list.append(player)
                else:
                    Player.tie_players_list.append(player)
    for player in Player.winners_list:
        player.chips.deposit(player.hand_list[0].bet)

    for player in Player.losers_list:
        player.chips.withdraw(player.hand_list[0].bet)


def final_results_display(blackjack_list, winners, losers, tie_list, dealer):
    """
    Method to display final results of current round of the game
    :param blackjack_list: List of players who won a blackjack
    :param winners: List of other winning players except the blackjack
    :param losers: List of players who lost
    :param tie_list: List of players who had a tie
    :param dealer: The dealer
    :return: none
    """
    print('\nFinal hand status for all:')
    Player.show_hand_with_value_all_players()
    dealer.hand.show_cards('all')
    print(f'Dealer\'s final hand value is: {dealer.hand.calculate_value()}')

    print('\nFinal RESULTS are:')
    for player in Player.players:
        if player in blackjack_list:
            print(f'{player.name} is a BLACK JACK!!!')
            print(f'{player.name}, ', player.chips, '\n')
        elif player in winners:
            print(f'{player.name} is a Winner!')
            print(f'{player.name}, ', player.chips, '\n')
        elif player in losers:
            print(f'{player.name} Lost. Better Luck Next Time!')
            print(f'{player.name}, ', player.chips, '\n')
        elif player in tie_list:
            print(f'{player.name} had a tie.')
            print(f'{player.name}, ', player.chips, '\n')


def ask_to_continue_playing():
    """
    Method to ask user choice, whether to play NEXT round or START OVER AGAIN or QUIT the game
    :return: The team's choice 'N' or 'S' or 'Q'
    """
    while True:
        try:
            x = input('\nWould you like to play next round or start over a new game or quit playing? \nEnter "N" for'
                      ' next round or "S" to start over a new game or "Q" to quit playing: ')
        except Exception as e:
            print('Please enter a string. It cannot be empty.', e)
        else:
            if x[0].upper() != 'S' and x[0].upper() != 'N' and x[0].upper() != 'Q':
                print('Please enter a valid choice')
                continue
            else:
                return x[0].upper()


def try_input_int(input_message):
    """
    Error handling method to accept only particular integer as user input
    :param input_message: The message to be displayed to take user input
    :return: The input message
    """
    while True:
        try:
            x = int(input(f'{input_message} '))
        except Exception as e:
            print('Please enter a valid integer.', e)
        else:
            # Place for checking condition on x
            # Can leave blank if no check required for x
            return x


def try_input_str(input_message):
    """
    Error handling method to accept only particular string as user input
    :param input_message: The message to be displayed to take user input
    :return: The input message
    """
    while True:
        try:
            x = input(f'{input_message} ')
        except Exception as e:
            print('Please enter a string. It cannot be empty.', e)
        else:
            # Place for checking condition on x
            # Can leave blank if no check required for x
            return x
