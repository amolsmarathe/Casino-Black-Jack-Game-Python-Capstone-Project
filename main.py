"""
"Casino Blackjack Game"

This is a simple text-based BlackJack game with following features:
    - Multiple players versus an automated dealer
    - Players can play STAND or HIT or DOUBLE DOWN
    - Players have 4 colored chips: White, Green, Red and Black chips
    - Players can pick their betting amount
    - Each player's total money balance is tracked throughout the game
    - Final results are displayed with cards in the hands, hand value, money balance and winning status Win, Lose or Tie

Structure of the code goes as follows:
It is based on OOP and includes following modules:
    1. player
    2. dealer
    3. deck
    4. game_methods
    5. main

Future enhancements:
    - Create UI for the game
    - Include 'SPLIT' and 'SURRENDER' game moves.
"""

from dealer import *
from game_methods import *


def main():
    player_choice = 'S'
    while player_choice == 'S':     # team starts over new game from very beginning

        # Set default chips balance for all players in the game
        default_chips_balance = {'white': 150, 'red': 100, 'green': 50, 'black': 20}

        # Welcome message
        print("\nWelcome everyone to the Royal Casino! You can play Black Jack and win! \n\tNOTE that every player is "
              "given certain number of chips to play with.\n\tEveryone's default chips balance at the start of the game"
              " is same, which is- \n\t", default_chips_balance)

        # Define number of players and create player objects list:
        print('\nLet us now define the players for the game')
        Player.define_player_list(default_chips_balance)

        player_choice = 'N'
        while player_choice == 'N':         # team chooses to play next round
            # Create Dealer and Deck
            dealer = Dealer()
            deck = Deck()

            # Shuffle Deck for this round
            deck.shuffle()
            print('\nThe deck is now shuffled and ready for the round')

            # Display what is everyone's current chips balance:
            for player in Player.players:
                print(f'\nHey {player.name}, ', player.chips)
            print(f'\nTotal number of players for this round are: {len(Player.players)}. Names are:')
            for player in Player.players:
                print(f'\t{player.name}')

            # Ask and display everyone's initial bet:
            request_bet(Player.players)

            # set the bet for current hand of each player
            for player in Player.players:
                player.hand_list[0].bet = player.initial_bet

            # Dealer distributes cards to each player and himself
            print('\nDistributing 2 cards to everyone...\n')
            dealer.distribute_hand(deck, Player.players)

            # Display everyone's hand and dealer's second card
            Player.show_hand_with_value_all_players()
            dealer.hand.show_cards('one')
            print()

            # Check if any player has Black Jack
            for player in Player.players:
                if player.hand_list[0].value == 21:
                    print(f'Congratulations {player.name}! You won a Black jack, that equals thrice your bet!!!')
                    player.chips.deposit(player.initial_bet)
                    player.chips.deposit(player.initial_bet)

                    # Display current chips balance for blackjack player
                    print(f'{player.name}', player.chips)
                    Player.black_jack_players_list.append(player)

            # Remove blackjack players from current playing list
            remaining_players_list = [i for i in Player.players if i not in Player.black_jack_players_list]

            # Continue game with remaining players:
            for player in remaining_players_list:
                play_game(player, deck)

            # All players played
            print('\nAll players in the round have finished playing.')

            # Show Dealer's hand
            print('Before drawing any additoinal card, ', end='')
            dealer.hand.show_cards('all')
            print(f'Dealer\'s hand value is: {dealer.hand.calculate_value()}')

            # Check who lost before dealer draws any card
            check_lost_before_dealer_draws(dealer, remaining_players_list)

            # If everyone not yet lost
            if len(remaining_players_list) != len(Player.losers_list):

                if dealer.hand.calculate_value() < 17:

                    # Dealer draws till reaches 17
                    dealer.draw_till_17(deck)

                    # Show final dealer's hand and value
                    print('\nAfter drawing till 17, ', end='')
                    dealer.hand.show_cards('all')
                    print(f'Dealer\'s final hand value is: {dealer.hand.calculate_value()}')

                    # Final Results:
                    final_results_calculation(dealer, remaining_players_list)
                    final_results_display(Player.black_jack_players_list, Player.winners_list, Player.losers_list,
                                          Player.tie_players_list, dealer)

                else:
                    # Final results
                    final_results_calculation(dealer, remaining_players_list)
                    final_results_display(Player.black_jack_players_list, Player.winners_list, Player.losers_list,
                                          Player.tie_players_list, dealer)

            else:           # When everyone is already lost

                # Final Results
                for player in Player.losers_list:
                    player.chips.withdraw(player.hand_list[0].bet)
                final_results_display(Player.black_jack_players_list, Player.winners_list, Player.losers_list,
                                      Player.tie_players_list, dealer)

            # Remove the players from the list who do not have minimum chips to bet for next round
            test_list = Player.players.copy()
            for player in test_list:
                if sum(player.chips.chips_balance.values()) < 10:
                    print(f'\n{player.name} does not have minimum chips balance hence out of the game for the'
                          f' next round.')
                    Player.players.remove(player)

            # Clear all lists- winners, losers, etc.
            Player.winners_list.clear()
            Player.losers_list.clear()
            Player.tie_players_list.clear()
            Player.black_jack_players_list.clear()

            # End the game if no player has left with minimum chips balance
            if len(Player.players) == 0:
                print(f'\nGAME OVER! No player has minimum chips balance to play the next round.'
                      f'\n\nStarting a NEW GAME...')
                player_choice = 'S'
                break

            # Ask whether to play next round or start over again with new players or quit the game
            player_choice = ask_to_continue_playing()

            if player_choice == 'N':
                # Clear all cards from all hands. Multiple hands per player is possible when player splits. It is for
                # future enhancements when split method is added to player's move.
                for player in Player.players:
                    for hand in player.hand_list:
                        hand.cards.clear()
                    del player.hand_list[1:]
                continue
            elif player_choice == 'S':
                # Delete all players from the list
                Player.players.clear()
                break
            else:
                break


if __name__ == '__main__':
    main()
