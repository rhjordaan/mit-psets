import unittest
import random
import numpy as np
from ps4_classes import CardDecks, BlackJackCard, Busted # remove warnings
from ps4_classes import *
from blackjack import BlackJackHand, play_hand, run_simulation # remove warnings
from blackjack import *

class MockCardDecks(CardDecks):
    """
    Mock representation of CardDecks class used for testing.

    Allows tester to specify which cards to deal.
    """

    def __init__(self, num_decks, card_type, cards_to_deal):
        CardDecks.__init__(self, num_decks, card_type)
        self.cards_to_deal = cards_to_deal

    def deal_card(self):
        return self.cards_to_deal.pop()

    def num_cards_left(self):
        return len(self.cards_to_deal)


def is_within_epsilon(true_value, estimated_value, epsilon):
    return abs(true_value - estimated_value) <= epsilon


def check_within_epsilon(true_values, estimated_values, epsilon):
    """
    Returns True if and only if each value in true_values is within epsilon
    of the corresponding value in estimated_values.
    """
    for i in range(len(true_values)):
        if not is_within_epsilon(true_values[i], estimated_values[i], epsilon):
            return False
    return True


def get_printable_cards(cards):
    """
    Return list of string representations of each card in cards.
    """
    return [str(card) for card in cards]


best_value_error_message = "Your best_val returned %s for cards %s, but it should return %s."
dealer_error_message = "Your copy_dealer_strategy returned %s when player has %s and dealer has %s, but it should return %s."
cheating_error_message = "Your cheating_strategy returned %s when player has %s and dealer has %s, but it should return %s."
simple_error_message = "Your simple_strategy returned %s when player has %s and dealer has %s, but it should return %s."
doubledown_error_message = "Your doubledown_strategy returned %s when player has %s and dealer has %s, but it should return %s."
random_error_message = "Your random strategy returned hit %s percent of the time when player has %s and dealer has %s, that falls" \
                       "outside the correct margins."

class TestPS4(unittest.TestCase):
    #######################
    # BlackJackHand Tests #
    #######################

    def test_01_best_value_no_aces_1(self):
        # no cards
        cards = []
        self.assertEqual(BlackJackHand.best_value(cards), 0, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 0))

    def test_02_best_value_no_aces_2(self):
        # less than 21
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            '3', 'C'), BlackJackCard('K', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 15, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 15))

    def test_03_best_value_one_ace_1(self):
        # less than 21, A with value 11
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('7', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 20, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 20))

    def test_04_best_value_one_ace_2(self):
        # less than 21, A with value 1
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('K', 'S')]
        self.assertEqual(BlackJackHand.best_value(cards), 13, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 13))

    def test_05_best_value_multiple_aces_1(self):
        # one A with value 1, one A with value 11
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('A', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 14, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 14))

    def test_06_best_value_multiple_aces_2(self):
        # two A with value 1
        cards = [BlackJackCard('2', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            'A', 'S'), BlackJackCard('8', 'H'), BlackJackCard('K', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 22, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 22))
    
    def test_06_best_value_multiple_aces_3(self):
        cards = [BlackJackCard('A', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            '3', 'S'), BlackJackCard('7', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 12, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 12))
    
    def test_06_best_value_multiple_aces_4(self):
        cards = [BlackJackCard('A', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            '3', 'S'), BlackJackCard('A', 'H'), BlackJackCard('5', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 21, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 21))

    def test_07_copy_dealer_strategy_1(self):
        # less than 17, hit
        player_cards = [BlackJackCard('5', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('6', 'C'), BlackJackCard('3', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.copy_dealer_strategy(), BlackJackHand.HIT, dealer_error_message % (
            hand.copy_dealer_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.HIT))

    def test_08_copy_dealer_strategy_2(self):
        # 17, stand
        player_cards = [BlackJackCard('7', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('6', 'C'), BlackJackCard('3', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.copy_dealer_strategy(), BlackJackHand.STAND, dealer_error_message % (
            hand.copy_dealer_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.STAND))

    def test_09_cheating_strategy_1(self):
        # player < dealer, hit
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('K', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.cheating_strategy(), BlackJackHand.HIT, cheating_error_message % (
            hand.cheating_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.HIT))

    def test_10_cheating_strategy_2(self):
        # player == dealer, stand
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('K', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.cheating_strategy(), BlackJackHand.STAND, cheating_error_message % (
            hand.cheating_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.STAND))

    def test_11_cheating_strategy_3(self):
        # player > dealer, stand
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.cheating_strategy(), BlackJackHand.STAND, cheating_error_message % (
            hand.cheating_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.STAND))

    def test_12_simple_strategy_1(self):
        # player > 17
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.simple_strategy(), BlackJackHand.STAND, simple_error_message % (
            hand.simple_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.STAND))

    def test_13_simple_strategy_2(self):
        # player == 17
        player_cards = [BlackJackCard('7', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.simple_strategy(), BlackJackHand.STAND, simple_error_message % (
            hand.simple_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.STAND))

    def test_14_doubledown_strategy_1(self):
        # player < 11 (has 10)
        player_cards = [BlackJackCard('2', 'C'), BlackJackCard('8', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.DD_strategy(), BlackJackHand.HIT, doubledown_error_message % (
            hand.DD_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.HIT))
    
    def test_15_doubledown_strategy_2(self):
        # player > 11 (has 17)
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('8', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.DD_strategy(), BlackJackHand.STAND, doubledown_error_message % (
            hand.DD_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.STAND))
    
    def test_16_doubledown_strategy_3(self):
        # player == 11
        player_cards = [BlackJackCard('2', 'C'), BlackJackCard('9', 'H')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.DD_strategy(), BlackJackHand.DD, doubledown_error_message % (
            hand.DD_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.DD))
        
        # make sure the bet doubles when doubling down
        cards_to_deal = [BlackJackCard('9', 'D'), BlackJackCard('9', 'S'), *dealer_cards, *player_cards]
        mockdeck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(mockdeck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        initial_bet = hand.get_bet()
        self.assertEqual(initial_bet, 2.0, "Inaccurate initial bet, found %s, expected %s" % (initial_bet, 2.0))
        def strategy(hand):
            if hand.deck.num_cards_left() == 2:
                return BlackJackHand.DD # trigger play_player_turn to double the bet
            else:
                return BlackJackHand.STAND
        hand.play_player_turn(strategy)
        new_bet = hand.get_bet()
        self.assertEqual(new_bet, 4.0, "Your doubledown strategy did not double the current bet to %s, found %s" %
                         (4.0, new_bet))

    def test_17_random_strategy_1(self):
        # player < 12 (has 5)
        player_cards = [BlackJackCard('2', 'C'), BlackJackCard('3', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        counter, n = 0.0, 10
        for _ in range(n):
            if hand.random_strategy() == BlackJackHand.HIT:
                counter += 1
        percentage_hit = counter/n
        within_margins = False
        if percentage_hit == 1: within_margins = True
        self.assertTrue(within_margins, random_error_message % (
            counter*100, get_printable_cards(player_cards), get_printable_cards(dealer_cards)))

    def test_18_random_strategy_2(self):
        # player > 16 (has 17)
        player_cards = [BlackJackCard('8', 'C'), BlackJackCard('9', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        counter, n = 0.0, 10
        for _ in range(n):
            if hand.random_strategy() == BlackJackHand.HIT:
                counter += 1
        percentage_hit = counter/n
        within_margins = False
        if percentage_hit == 0.0: within_margins = True
        self.assertTrue(within_margins, random_error_message % (
            counter*100, get_printable_cards(player_cards), get_printable_cards(dealer_cards)))

    def test_19_random_strategy_3(self):
        # 12 < player < 16 (has 13)
        player_cards = [BlackJackCard('5', 'C'), BlackJackCard('8', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        counter, n = 0.0, 5000
        for _ in range(n):
            if hand.random_strategy() == BlackJackHand.HIT:
                counter += 1
        percentage_hit = counter/n
        within_margins = False
        if 0.4 < percentage_hit < 0.6: within_margins = True
        self.assertTrue(within_margins, random_error_message % (
            counter*100, get_printable_cards(player_cards), get_printable_cards(dealer_cards)))

    def test_20_play_player_turn_1(self):
        # player busts
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('K', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        def strategy(hand):
            if hand.deck.num_cards_left() > 0:
                return BlackJackHand.HIT
            return BlackJackHand.STAND

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        self.assertRaises(Busted, hand.play_player_turn, strategy)
        

    def test_21_play_player_turn_2(self):
        # player does not bust
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('3', 'S'), BlackJackCard(
            '3', 'S'), *dealer_hand, *player_hand]

        def strategy(hand):
            if hand.deck.num_cards_left() > 0:
                return BlackJackHand.HIT
            return BlackJackHand.STAND

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        try:
            hand.play_player_turn(strategy)
        except:
            self.fail('Your play_player_turn busted when it should not have.')

    def test_22_play_dealer_turn_1(self):
        # dealer busts
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('K', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        self.assertRaises(Busted, hand.play_dealer_turn)

    def test_23_play_dealer_turn_2(self):
        # dealer does not bust
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('3', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        try:
            hand.play_dealer_turn()
        except:
            self.fail('Your play_dealer_turn busted when it should not have.')

    ###################
    # play_hand Tests #
    ###################

    def test_24_play_hand_copy_dealer_strategy_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.copy_dealer_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with dealer strategy.')

    def test_25_play_hand_copy_dealer_strategy_2(self):
        random.seed(5)
        correct_return = 2
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.copy_dealer_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with dealer_dealer strategy.')

    def test_26_play_hand_cheating_strategy_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.cheating_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with cheating strategy.')

    def test_27_play_hand_cheating_strategy_2(self):
        random.seed(5)
        correct_return = 2.0
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.cheating_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    def test_28_play_hand_simple_strategy_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.simple_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    def test_29_play_hand_simple_strategy_2(self):
        random.seed(5)
        correct_return = 2.0
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.simple_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')
        
    def test_30_play_hand_doubledown_strategy_1(self):
        random.seed(6)
        correct_return = 1.0
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.DD_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from doubledown strategy actual (%f) differs from expected (%f) too much' %
                        (player_return, correct_return))
                
    def test_31_play_hand_doubledown_strategy_2(self):
        random.seed(7)
        correct_return = 0.0 #@TODO give a mock deck to see return be 4x initial bet
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.DD_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from doubledown strategy actual (%f) differs from expected (%f) too much' %
                        (player_return, correct_return))

    def test_32_play_hand_random_strategy_1(self):
        random.seed(8)
        n = 5000
        amount_bet, player_return = 0.0, 0.0
        for _ in range(n):
            deck = CardDecks(8, BlackJackCard)
            player_return += play_hand(deck, BlackJackHand.random_strategy)[1]
        correct_return = False
        if player_return > 0.9: correct_return = True
        self.assertTrue(correct_return,
                        'Average return from playing hand in random strategy 5000 times differs from allowed return')

    ########################
    # run_simulation Tests #
    ########################
    
    # helper function to run a simulation and test the resulting (returns, mean, and std) against
    # the supplied expected values
    #
    # this function currently must use the random number generator seed of 0 to match with 
    # the hardcoded expected values in the tests.
    #
    def sim_run_check(self, correct_mean, correct_std, strategy, strategy_str, 
                                        bet, num_decks, num_hands, num_trials, show_plot):
        random.seed(0) # Must be zero for deterministically producing expected vals!
        returns, mean, std = run_simulation(strategy, bet, num_decks, num_hands, num_trials, show_plot)
        self.assertTrue(is_within_epsilon(np.mean(returns), correct_mean, 0.0001),
                        'Mean of %s simulation returns (%f) not within tolerance of correct val (%f)' % \
                        (strategy_str, np.mean(returns), correct_mean))
        self.assertTrue(is_within_epsilon(np.std(returns), correct_std, 0.0001),
                        'Std. dev. of %s simulation returns (%f) not within tolerance of correct val (%f)' % \
                        (strategy_str, np.std(returns), correct_std))
        self.assertTrue(
            is_within_epsilon(correct_mean, mean, 0.0001),
            'Mean of %s simulation (%s) not within tolerance of correct val (%s)' % \
            (strategy_str, mean, correct_mean))
        self.assertTrue(
            is_within_epsilon(correct_std, std, 0.0001),
            'Std. dev. of %s simulation (%s) not within tolerance of correct val (%s)' % \
            (strategy_str, std, correct_std))

    def test_33_run_simulation_copy_dealer(self):
        correct_mean = -6.044375
        correct_std = 22.19167002186575
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.copy_dealer_strategy,
                           "copy_dealer", 2, 8, 20, 4000, False)

    def test_34_run_simulation_cheating(self):
        correct_mean = -0.1825
        correct_std = 21.89051892372586
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.cheating_strategy,
                           "cheating", 2, 8, 20, 4000, False)

    def test_35_run_simulation_simple(self):
        correct_mean = -3.3925
        correct_std = 21.8872895478
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.simple_strategy,
                           "simple", 2, 8, 20, 4000, False)
        
    def test_36_run_simulation_doubledown(self):
        #correct_mean = 3.072500
        #correct_std = 24.547602
        correct_mean = -2.540875
        correct_std = 22.238588
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.DD_strategy,
                           "doubledown", 2, 8, 20, 4000, False)

# Dictionary mapping function names from the above TestCase class to
# the point value each test is worth.
point_values = {
    'test_01_best_value_no_aces_1': 0.15,
    'test_02_best_value_no_aces_2': 0.15,
    'test_03_best_value_one_ace_1': 0.15,
    'test_04_best_value_one_ace_2': 0.15,
    'test_05_best_value_multiple_aces_1': 0.15,
    'test_06_best_value_multiple_aces_2': 0.15,
    'test_06_best_value_multiple_aces_3': 0.15,
    'test_06_best_value_multiple_aces_4': 0.15,
    'test_07_copy_dealer_strategy_1': 0.25,
    'test_08_copy_dealer_strategy_2': 0.25,
    'test_09_cheating_strategy_1': 0.25,
    'test_10_cheating_strategy_2': 0.25,
    'test_11_cheating_strategy_3': 0.25,
    'test_12_simple_strategy_1':0.25,
    'test_13_simple_strategy_2':0.25,
    'test_14_doubledown_strategy_1':0.25,
    'test_15_doubledown_strategy_2':0.25,
    'test_16_doubledown_strategy_3':0.25,
    'test_17_random_strategy_1': 0.25,
    'test_18_random_strategy_2': 0.25,
    'test_19_random_strategy_3': 0.25,
    'test_20_play_player_turn_1': 0.40,
    'test_21_play_player_turn_2': 0.40,
    'test_22_play_dealer_turn_1': 0.40,
    'test_23_play_dealer_turn_2': 0.40,
    'test_24_play_hand_copy_dealer_strategy_1': 0.30,
    'test_25_play_hand_copy_dealer_strategy_2': 0.30,
    'test_26_play_hand_cheating_strategy_1': 0.30,
    'test_27_play_hand_cheating_strategy_2': 0.30,
    'test_28_play_hand_simple_strategy_1': 0.30,
    'test_29_play_hand_simple_strategy_2': 0.30,
    'test_30_play_hand_doubledown_strategy_1': 0.30,
    'test_31_play_hand_doubledown_strategy_2': 0.30,
    'test_32_play_hand_random_strategy_1': 0.30,
    'test_33_run_simulation_copy_dealer': 0.31,
    'test_34_run_simulation_cheating': 0.31,
    'test_35_run_simulation_simple': 0.31,
    'test_36_run_simulation_doubledown': 0.32
}


# Subclass to track a point score and appropriate
# grade comment for a suit of unit tests
class Results_600(unittest.TextTestResult):

    # We override the init method so that the Result object
    # can store the score and appropriate test output.
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 8

    def addFailure(self, test, err):
        test_name = test._testMethodName
        msg = str(err[1])
        self.handleDeduction(test_name, msg)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, None)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, message):
        point_value = point_values[test_name]
        if message is None:
            message = 'Your code produced an error on test %s.' % test_name
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= point_value

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS4))
    result = unittest.TextTestRunner(
        verbosity=2, resultclass=Results_600).run(suite)

    output = result.getOutput()
    points = result.getPoints()

    # weird bug with rounding
    if points < .1:
        points = 0

    print("\nProblem Set 4 Unit Test Results:")
    print(output)
    print("Points: %s/8\n" % points)
