class Player:
    def __init__(self, name, hand, position, starting_stack_size, stack_size, action):
        self.name = name
        self.hand = hand
        self.position = position
        self.starting_stack_size = starting_stack_size
        self.stack_size = stack_size
        self.action = action


class Game:
    def __init__(self, pot, dealer):
        self.pot = pot
        self.dealer = dealer


def shuffle(cards):
    random.shuffle(cards)
    return cards


def deal(cards):
    card_1_a = cards.pop(0)
    card_1_b = cards.pop(0)
    card_2_a = cards.pop(0)
    card_2_b = cards.pop(0)
    hand_1 = card_1_a + card_2_a
    hand_1 = determine_suited_hands(hand_1)
    hand_2 = card_1_b + card_2_b
    hand_2 = determine_suited_hands(hand_2)
    possible_positions = ['IP', 'OOP']
    random.shuffle(possible_positions)
    stack_1 = random.randint(15, 40)
    stack_2 = random.randint(15, 40)
    player_1 = Player('Daniel Negreanu', hand_1, possible_positions.pop(0), stack_1, stack_1, 'player being dealt...')
    player_2 = Player('Tom Dwan', hand_2, possible_positions.pop(0), stack_2, stack_2, 'player being dealt...')
    # player_1 = Player('Daniel Negreanu', 'AA', 'OOP', 35, 35,
    #                   'player being dealt...')
    # player_2 = Player('Tom Dwan', 'KK', 'IP', 30, 30, 'player being dealt...')
    print('You are {} and you have {}, you are {} and you have a stack of {} BBs'.format(player_1.name, player_1.hand,
                                                                                         player_1.position,
                                                                                         player_1.stack_size))
    print('{} has {}, is {} and has a stack of {} BBs'.format(player_2.name, player_2.hand,
                                                              player_2.position,
                                                              player_2.stack_size))
    if player_1.position == 'IP':
        player_1.stack_size -= small_blind
        player_2.stack_size -= big_blind
        game = Game(small_blind + big_blind, player_1)
        print('{} posts SB, {} posts BB'.format(player_1.name, player_2.name))
    else:
        player_2.stack_size -= small_blind
        player_1.stack_size -= big_blind
        game = Game(small_blind + big_blind, player_2)
        print('{} posts SB, {} posts BB'.format(player_2.name, player_1.name))
    print('Pot is {} BBs'.format(game.pot))
    # print(f'Your player has {player_1.hand}, is {player_1.position} and has a stack of {player_1.stack_size} BBs')
    return game, player_1, player_2, cards


def deal_flop(cards):
    cards.pop(0) # burn
    card_1 = cards.pop(0)
    card_2 = cards.pop(0)
    card_3 = cards.pop(0)
    flop = [card_1, card_2, card_3]
    return flop, cards


def determine_suited_hands(hand):
    hand_array = list(hand)
    if hand_values[hand_array[0]] < hand_values[hand_array[2]]:
        hand_array = [hand_array[2], hand_array[3], hand_array[0], hand_array[1]]
    if hand_array[0] == hand_array[2]:
        hand = hand_array[0] + hand_array[2]
    elif hand_array[1] == hand_array[3]:
        hand = hand_array[0] + hand_array[2] + 's'
    elif hand_array[1] != hand_array[3]:
        hand = hand_array[0] + hand_array[2] + 'o'
    return hand


def deal_turn(board, cards):
    cards.pop(0)  # burn
    board.append(cards.pop(0))
    return board, cards


def deal_river(board, cards):
    cards.pop(0)  # burn
    board.append(cards.pop(0))
    return board


def round_half_up(n, decimals=1):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def player_1_decide_preflop(game, player_1, player_2):
    # player_1 IP

    if player_1.position == 'IP' and (player_1.hand in premium_hands or
                                      player_1.hand in strong_kings or
                                      player_1.hand in strong_aces or
                                      player_1.hand in high_pairs or
                                      player_1.hand in middle_pairs) and player_1.stack_size > 25:
        player_1.action = 'raises to'
        raise_amount = random.uniform(2, 3)
        raise_amount = round_half_up(raise_amount)
        player_1.stack_size -= raise_amount - 0.5
        game.pot += raise_amount - 0.5
        print('{} - {} {} BBs with {}'.format(player_1.name, player_1.action, raise_amount, player_1.hand))
        print('Pot is {} BBs'.format(game.pot))
        if player_2.stack_size < 25 and (player_2.hand in premium_hands or
                                         player_2.hand in strong_kings or
                                         player_2.hand in strong_aces or
                                         player_2.hand in high_pairs or
                                         player_2.hand in middle_pairs or
                                         player_2.hand in small_pairs):
            player_2.action = 'goes all-in for'
            player_1.action = 'calls'
            allin_amount = player_2.starting_stack_size
            game.pot = allin_amount * 2
            player_1.stack_size -= allin_amount
            player_2.stack_size = 0
            print('{} - {} {} - with {}'.format(player_2.name, player_2.action, allin_amount, player_2.hand))
            print('{} - {} {} - with {}'.format(player_1.name, player_1.action, allin_amount, player_1.hand))
            print('Pot is {} BBs'.format(game.pot))

        elif player_2.stack_size < 25 and player_2.hand in suited_connectors:
            player_2.action = 'calls'
            game.pot += (raise_amount - 1)
            print(
                '{} - {} - {} BBs - with {}'.format(player_2.name, player_2.action, (raise_amount - 1), player_2.hand))
            print('Pot is {} BBs'.format(game.pot))
            print('To the flop..')
        elif player_2.stack_size >= 25 and (player_2.hand in premium_hands or
                                            player_2.hand in strong_kings or
                                            player_2.hand in strong_aces or
                                            player_2.hand in high_pairs):
            player_2.action = 'raises to'
            raise_amount = raise_amount * 3
            player_2.stack_size -= raise_amount - 1
            game.pot += raise_amount - 1
            print('{} - {} {} BBs - with {}'.format(player_2.name, player_2.action, raise_amount, player_2.hand))
            print('Pot is {} BBs'.format(game.pot))

            if player_1.stack_size < 35 and (player_1.hand in premium_hands or
                                             player_1.hand in strong_aces or
                                             player_1.hand in high_pairs):
                player_1.action = 'goes all-in for'
                allin_amount = player_1.starting_stack_size
                game.pot = allin_amount + raise_amount
                player_1.stack_size = 0
                print('{} - {} {} BBs - with {}'.format(player_1.name, player_1.action, allin_amount, player_1.hand))
                print('Pot is {} BBs'.format(game.pot))

                if player_2.hand in premium_hands or player_2.hand in high_pairs:
                    player_2.action = 'calls'
                    game.pot = 2 * allin_amount
                    player_2.stack_size = 0
                    print('{} - {} {} BBs - with {}'.format(player_2.name, player_2.action, allin_amount,
                                                            player_2.hand))
                    print('Pot is {} BBs'.format(game.pot))
                    print('To the flop..')
                else:
                    player_2.action = 'folds'
                    print('{} {}'.format(player_2.name, player_2.action))
                    print('{} wins pot of {} BBs'.format(player_1.name, game.pot))
                    player_1.stack_size += game.pot
            elif (player_1.hand in premium_hands or
                  player_1.hand in strong_aces or
                  player_1.hand in high_pairs) and (player_1.stack_size - raise_amount * 3) < 15:
                player_1.action = 'goes all-in for'
                allin_amount = player_1.starting_stack_size
                game.pot = allin_amount + raise_amount
                player_1.stack_size = 0
                print('{} - {} {} BBs - with {}'.format(player_1.name, player_1.action, allin_amount, player_1.hand))
                print('Pot is {} BBs'.format(game.pot))

            elif player_1.stack_size >= 35 and (player_1.hand in strong_kings or player_1.hand in middle_pairs or
                                                player_1.hand in small_pairs or
                                                player_1.hand in suited_connectors):
                player_1.action = 'calls'
                call_amount = (raise_amount - raise_amount / 3)
                player_1.action -= call_amount
                game.pot += call_amount
                print('{} - {} {} BBs - with {}'.format(player_2.name, player_2.action, player_2.stack_size,
                                                        player_2.hand))
                print('Pot is {} BBs'.format(game.pot))
                print('To the flop..')

            else:
                player_1.action = 'folds'
                print('{} {}'.format(player_1.name, player_1.action))
                print('{} wins pot of {} BBs'.format(player_2.name, game.pot))
                player_2.stack_size += game.pot
    # player_1 goes allin right away
    elif player_1.position == 'IP' and (player_1.hand in premium_hands or
                                        player_1.hand in strong_kings or
                                        player_1.hand in strong_aces or
                                        player_1.hand in high_pairs or
                                        player_1.hand in middle_pairs) and player_1.stack_size < 25:
        player_1.action = 'goes all-in'
        player_1.stack_size = 0
        game.pot += player_1.starting_stack_size
        print('{} - {} - {} - with {}'.format(player_1.name, player_1.action, player_1.starting_stack_size,
                                              player_1.hand))
        print('Pot is {} BBs'.format(game.pot))
        if player_2.hand in premium_hands or player_2.hand in high_pairs or player_2.hand in middle_pairs:
            player_2.action = 'calls'
            if player_2.starting_stack_size < player_1.starting_stack_size:
                allin_amount = player_2.starting_stack_size
            else:
                allin_amount = player_1.starting_stack_size
            game.pot = 2 * allin_amount
            print('{} - {} - {} - with {}'.format(player_2.name, player_2.action, allin_amount, player_2.hand))
            print('Pot is {} BBs'.format(game.pot))

        else:
            player_2.action = 'folds'
            print('{} {}'.format(player_2.name, player_2.action))
            print('{} wins pot of {} BBs'.format(player_1.name, game.pot))
            player_1.stack_size += game.pot
    else:
        player_1.action = 'folds'
        print('{} {}'.format(player_1.name, player_1.action))
        print('{} wins pot of {} BBs'.format(player_2.name, game.pot))
        player_2.stack_size += game.pot
        return game, player_1, player_2


def player_2_decide_preflop(game, player_1, player_2):
    print('Players are deciding preflop..')
    # player_2 IP
    if player_2.position == 'IP' and (player_2.hand in premium_hands or
                                      player_2.hand in strong_kings or
                                      player_2.hand in strong_aces or
                                      player_2.hand in high_pairs or
                                      player_2.hand in middle_pairs) and player_2.stack_size > 25:
        player_2.action = 'raises to'
        raise_amount = random.uniform(2, 3)
        raise_amount = round_half_up(raise_amount)
        player_2.stack_size -= raise_amount - 0.5
        game.pot += raise_amount - 0.5
        print('{} - {} {} BBs with {}'.format(player_2.name, player_2.action, raise_amount, player_2.hand))
        print('Pot is {} BBs'.format(game.pot))
        if player_1.stack_size < 25 and (player_1.hand in premium_hands or
                                         player_1.hand in strong_kings or
                                         player_1.hand in strong_aces or
                                         player_1.hand in high_pairs or
                                         player_1.hand in middle_pairs or
                                         player_1.hand in small_pairs):
            player_1.action = 'goes all-in for'
            player_2.action = 'calls'
            allin_amount = player_1.starting_stack_size
            game.pot = allin_amount*2
            player_2.stack_size -= allin_amount
            player_1.stack_size = 0

            print('{} - {} {} - with {}'.format(player_1.name, player_1.action, allin_amount, player_1.hand))
            print('{} - {} {} - with {}'.format(player_2.name, player_2.action, allin_amount, player_2.hand))
            print('Pot is {} BBs'.format(game.pot))

        elif player_1.stack_size < 25 and player_1.hand in suited_connectors:
            player_1.action = 'calls'
            game.pot += (raise_amount - 1)
            print('{} - {} - {} BBs - with {}'.format(player_1.name, player_1.action, (raise_amount - 1), player_1.hand))
            print('Pot is {} BBs'.format(game.pot))
            print('To the flop..')
        elif player_1.stack_size >= 25 and (player_1.hand in premium_hands or
                                            player_1.hand in strong_kings or
                                            player_1.hand in strong_aces or
                                            player_1.hand in high_pairs):
            player_1.action = 'raises to'
            raise_amount = raise_amount*3
            player_1.stack_size -= raise_amount - 1
            game.pot += raise_amount - 1
            print('{} - {} {} BBs - with {}'.format(player_1.name, player_1.action, raise_amount, player_1.hand))
            print('Pot is {} BBs'.format(game.pot))

            if player_2.stack_size < 35 and (player_2.hand in premium_hands or
                                             player_2.hand in strong_aces or
                                             player_2.hand in high_pairs):
                player_2.action = 'goes all-in for'
                allin_amount = player_2.starting_stack_size
                game.pot = allin_amount + raise_amount
                player_2.stack_size = 0
                print('{} - {} {} BBs - with {}'.format(player_2.name, player_2.action, allin_amount, player_2.hand))
                print('Pot is {} BBs'.format(game.pot))

                if player_1.hand in premium_hands or player_1.hand in high_pairs:
                    player_1.action = 'calls'
                    game.pot = 2*allin_amount
                    player_1.stack_size = 0
                    print('{} - {} {} BBs - with {}'.format(player_1.name, player_1.action, allin_amount,
                                                          player_1.hand))
                    print('Pot is {} BBs'.format(game.pot))
                    print('To the flop..')
                else:
                    player_1.action = 'folds'
                    print('{} {}'.format(player_1.name, player_2.action))
                    print('{} wins pot of {} BBs'.format(player_2.name, game.pot))
                    player_2.stack_size += game.pot
            elif (player_2.hand in premium_hands or
                  player_2.hand in strong_aces or
                  player_2.hand in high_pairs) and (player_2.stack_size - raise_amount*3) < 15:
                player_2.action = 'goes all-in for'
                allin_amount = player_2.starting_stack_size
                game.pot = allin_amount + raise_amount
                player_2.stack_size = 0
                print('{} - {} {} BBs - with {}'.format(player_2.name, player_2.action, allin_amount, player_2.hand))
                print('Pot is {} BBs'.format(game.pot))

            elif player_2.stack_size >= 35 and (player_2.hand in strong_kings or player_2.hand in middle_pairs or player_2.hand in small_pairs or
                                                player_2.hand in suited_connectors):
                player_2.action = 'calls'
                call_amount = (raise_amount - raise_amount/3)
                player_2.action -= call_amount
                game.pot += call_amount
                print('{} - {} {} BBs - with {}'.format(player_2.name, player_2.action, player_2.stack_size, player_2.hand))
                print('Pot is {} BBs'.format(game.pot))
                print('To the flop..')

            else:
                player_2.action = 'folds'
                print('{} {}'.format(player_2.name, player_2.action))
                print('{} wins pot of {} BBs'.format(player_1.name, game.pot))
                player_1.stack_size += game.pot

    # player_2 goes allin right away
    elif player_2.position == 'IP' and (player_2.hand in premium_hands or
                                        player_2.hand in strong_kings or
                                        player_2.hand in strong_aces or
                                        player_2.hand in high_pairs or
                                        player_2.hand in middle_pairs) and player_2.stack_size < 25:
        player_2.action = 'goes all-in'
        player_2.stack_size = 0
        game.pot += player_2.starting_stack_size
        print('{} - {} - {} - with {}'.format(player_2.name, player_2.action, player_2.starting_stack_size, player_2.hand))
        print('Pot is {} BBs'.format(game.pot))
        if player_1.hand in premium_hands or player_1.hand in high_pairs or player_1.hand in middle_pairs:
            player_1.action = 'calls'
            if player_1.starting_stack_size < player_2.starting_stack_size:
                allin_amount = player_1.starting_stack_size
            else:
                allin_amount = player_2.starting_stack_size
            game.pot = 2*allin_amount
            print('{} - {} - {} - with {}'.format(player_1.name, player_1.action, allin_amount, player_1.hand))
            print('Pot is {} BBs'.format(game.pot))

        else:
            player_1.action = 'folds'
            print('{} {}'.format(player_1.name, player_1.action))
            print('{} wins pot of {} BBs'.format(player_2.name, game.pot))
            player_2.stack_size += game.pot
    else:
        player_2.action = 'folds'
        print('{} {}'.format(player_2.name, player_2.action))
        print('{} wins pot pot of {} BBs'.format(player_1.name, game.pot))
        player_1.stack_size += game.pot

    return game, player_1, player_2


if __name__ == '__main__':
    import random
    import math
    small_blind = 0.5
    big_blind = 1
    premium_hands = ['AA', 'KK', 'QQ', 'JJ', 'AKs', 'AKo', 'AQs', 'AQo', 'KQs']
    suited_connectors = ['76s',
                         '86s', '87s',
                         '97s', '98s',
                         'T7s', 'T8s', 'T9s',
                         'J8s', 'J9s', 'JTs',
                         'Q9s', 'QTs', 'QJs']
    connectors = ['76o', '87o', '98o', 'T9o', 'JTo', 'QJo']
    strong_kings = ['KQo', 'KJo', 'KT0', 'K9s', 'KTs', 'KJs']
    strong_aces = ['A2s', 'A3s', 'A4s', 'A5s', 'A6s', 'A7s', 'A8s', 'A9s', 'ATs', 'AJs',
                   'A2o', 'A3o', 'A4o', 'A5o', 'ATo', 'AJo', 'AQo']
    high_pairs = ['TT', '99', '88']
    middle_pairs = ['77', '66', '55']
    small_pairs = ['44', '33', '22']

    suits = ['h', 'c', 'd', 's'] # hearts, clubs, diamonds, spades

    hand_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                   'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    deck = ['Ah', 'Ac', 'Ad', 'As',
             '2h', '2c', '2d', '2s',
             '3h', '3c', '3d', '3s',
             '4h', '4c', '4d', '4s',
             '5h', '5c', '5d', '5s',
             '6h', '6c', '6d', '6s',
             '7h', '7c', '7d', '7s',
             '8h', '8c', '8d', '8s',
             '9h', '9c', '9d', '9s',
             'Th', 'Tc', 'Td', 'Ts',
             'Jh', 'Jc', 'Jd', 'Js',
             'Qh', 'Qc', 'Qd', 'Qs',
             'Kh', 'Kc', 'Kd', 'Ks']
    shuffled_deck = shuffle(deck)
    game, player_1, player_2, shuffled_deck = deal(shuffled_deck)
    if player_1.position == 'IP':
        player_1_decide_preflop(game, player_1, player_2)
    else:
        player_2_decide_preflop(game, player_1, player_2)
    board_flop, deck_after_flop = deal_flop(shuffled_deck)
    board_turn, deck_after_turn = deal_turn(board_flop, deck_after_flop)
    board_river = deal_river(board_turn, deck_after_turn)
    print('Board after the river is: ')
    print(board_river)

