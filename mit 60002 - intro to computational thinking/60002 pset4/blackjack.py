# Problem Set 4
# Name: Richter Jordaan
# Collaborators:None
# Time Spent: 5:00
# Late Days Used: 0

import random
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import random
from ps4_classes import BlackJackCard, CardDecks, Busted


#############
# PROBLEM 1 #
#############
class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """

    # Do not modify these three lines, they provide an interface for the tester!
    HIT = 'hit'
    STAND = 'stand'
    DD = 'DD'
    #########################

    def __init__(self, deck, initial_bet=1.0):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
               card deck (this deck itself contains one or more standard card decks)
        initial_bet - float, represents the initial bet/wager of the hand

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.current_bet - float, represents the current bet/wager of the hand
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck

        Important: You MUST deal out the first four cards in the following order:
            player, dealer, player, dealer
            
            You may find the deal_card function (and others) in ps4_classes.py helpful.
        """
        self.deck=deck
        self.current_bet=initial_bet #current bet is initially just initial bet
        
        #player and dealer hand lists
        self.player = []
        self.dealer = []
        
        #deal cards
        self.player.append(self.deck.deal_card())
        self.dealer.append(self.deck.deal_card())
        self.player.append(self.deck.deal_card())
        self.dealer.append(self.deck.deal_card())
        

    # Do not modify!
    def set_bet(self, new_bet):
        """
        Sets the player's current wager in the game.

        Parameters:
        new_bet - the floating point number representing the new wager for the game.

        Do not modify!
        """
        self.current_bet = new_bet

    # Do not modify!
    def get_bet(self):
        """
        Returns the player's current wager in the game.

        Returns:
        self.current_bet, the floating point number representing the current wager for the game

        Do not modify!
        """
        return self.current_bet
        
    # Do not modify this function!
    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        used for testing, DO NOT MODIFY
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    # You can call the method below like this:
    #   BlackJackHand.best_value(cards)
    @staticmethod
    def best_value(cards):
        """
        Finds the total value of the cards. All cards must contribute to the
        best sum; however, an Ace may contribute a value of 1 or 11.

        The best sum is the highest point total not exceeding 21 if possible.
        If it is not possible to keep the total value from exceeding 21, then
        the best sum is the lowest total value of the cards.

        Hint: If you have one Ace, give it a value of 11 by default. If the sum
        point total exceeds 21, then give it a value of 1. What should you do
        if cards has more than one Ace?

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        best_val = 0
        remaining_aces = 0 #number of aces, used for changing from 11 to 1 if bust
        #start off adding Aces as 11, face cards as 10, others as their value
        for card in cards:
            if card.get_val() == 11:
                remaining_aces+=1
            best_val+=card.get_val()
        
        #now see if bust, then try to change ace values
        while best_val>21 and remaining_aces>0:
            best_val-=10
            remaining_aces-=1
        return best_val

    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player.copy()

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer.copy()

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.dealer[0]

    # Strategy 1
    def copy_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        return "hit" if self.best_value(self.player) < 17 else "stand"

    # Strategy 2
    def cheating_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        return "hit" if self.best_value(self.player)<self.best_value(self.dealer) else "stand"

    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        case1 = self.best_value(self.player)>=17
        case2 = 12<=self.best_value(self.player)<=16 and 2<=self.get_dealer_upcard().get_val()<=6
        return "stand" if case1 or case2 else "hit"
    
    # Strategy 4
    def DD_strategy(self):
        """
        A playing strategy in which the player will
            - doubledown (DD) if the following is true:
                - the best value of the player's cards is 11
            - else they will fall back to using simple_strategy

        In our game, we allow "doubling down" (DD) on any turn, rather than just the first turn.

        The double down action indicates a special, somewhat risky, but possibly rewarding player
        action. It means the player wishes to double the current bet of the hand, hit one more time,
        and then immediately stand, ending their turn with whatever cards result. 

        This strategy simply consists of siginaling to that the calling function with the action
        BlackJackHand.DD when the sum of the players cards is 11, which is a very good 
        position in which to try to double one's bet while getting only one more card. Otherwise,
        the strategy falls back to using the simple_strategy to play normally.

        Returns:
        str, "DD" if player_best_score == 11,
             otherwise the return value of calling simple_strategy to play in the default way
        """
        if self.best_value(self.player)==11:
            return "DD"
        return self.simple_strategy()

    # Strategy 5
    def random_strategy(self):
        """
        A playing strategy in which the player will
            - stand if the following is true:
                - the best value of player's hand is greater than or equal to 16
            - hit if the following is true:
                - the best value of player's hand is less than or equal to 12
            - otherwise:
                - toss a coin and hit if the result of the coin toss is a head, stand otherwise
                  (the 'random' library is already imported for you - think of ways to mimic a coin toss through it).

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        val = self.best_value(self.player)
        if val > 15:
            return "stand"
        elif val <13:
            return "hit"
        return "hit" if random.random()<0.5 else "stand"

    def play_player_turn(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player (a hit). The player
        will be dealt a new card until they stand, bust, or doubledown. 

        When doubling down, the player doubles their bet, receive one final hit, and 
        then they stand. The hit when doubling down (like any hit) can cause the player to 
        go bust.

        The following will guide you through some design requirements for this function. 

        This function must _repeatedly_ query the strategy for the next action, until the action
        is to stand, or until their hand's best value is over 21, which should then raise a Busted
        exception (imported from ps4_classes.py) to signal this sad outcome to the caller.

        Remember, receiving the doubledown action from a strategy indicates: 
            - the player wishes to double their current bet,
            - the player receives one last hit,
            - the player then immediately stands, ending their turn

        Remember, 
            - Whenever hitting, always signal to the caller if the best value of the 
              player's hand becomes greater than 21 (because the player has busted).

        Parameter:
        strategy - function, one of the the 4 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.copy_dealer_strategy, BlackJackHand.double_down_strategy)

        Returns:          
        This function does not return anything.

        """
        current_move = strategy(self) #will be either hit, stand, or dd

        
        while current_move == "hit" and self.best_value(self.player)<21:
            self.player.append(self.deck.deal_card())
            current_move = strategy(self)
        if current_move == "DD": #DD
            #double bet and get last hit
            self.set_bet(2*self.current_bet) 
            self.player.append(self.deck.deal_card())
        if self.best_value(self.player)>21: #busted
            raise Busted()   
            
        

    def play_dealer_turn(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17. If they go over 21, they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the dealer's hand is greater than 21.
        """
        while self.best_value(self.dealer) < 17:
            self.dealer.append(self.deck.deal_card())
        if self.best_value(self.dealer)>21:
            raise Busted()

    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.

        Useful for debugging. DO NOT MODIFY. 
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

#############
# PROBLEM 2 #
#############


def play_hand(deck, strategy, initial_bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on the bet/wager of the hand.

    The player will get:

        - 2.5 times the bet of the hand if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.

        - 2 times the bet of the hand if the player wins by having a higher best value than 
          the dealer after the dealer's turn concludes

        - 2 times the bet of the hand if the dealer busts

        - the exact bet amount of the hand if the game ends in a tie. 
          If the player and dealer both get blackjack from their first two cards, 
          this is also a tie.

        - 0 if the dealer wins with a higher best value, or the player busts.

        Remember, the doubledown strategy doubles the current bet under certain conditions. 
        You do not have to worry about doubling the bet here for any doubledowns if 
        your doubledown strategy properly signals to alter the bet of the hand during the
        player's turn.

        Reminder of how the game flow works:

        1. Deal cards to player, then dealer, then player, then dealer.

        2. Check for initial blackjacks from either player. If at least one person has 
           blackjack, the game is over. Calculate how much the player receives.

        3. If no one has blackjack, then deal the player until they stand or bust 
           (use your play_player_turn function).

           If you catch a Busted exception from the player playing their turn,
           the player busted, and the game is over. Calculate how much the player receives.

        4. If the player has not bust, then deal the dealer until they stand or bust.
           (use your play_dealer_turn function).
           If the dealer busts, the game is over. Calculate how much the player receives.

        5. If no one has bust, determine the outcome of the game based on the
            best value of the player's cards and the dealer's cards.

    Parameters:
        deck - an instance of CardDeck
        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.copy_dealer_strategy)
        initial_bet - float, the amount that the player initially bets (default=1.0)

    Returns:
        tuple (float, float): (amount_wagered, amount_won)
               amount_wagered, the current bet of the hand. Should use hand.get_bet().
               amount_won, the amount of money the player gets back. Should be 0 if they busted and lost.
    """
    #first player does a round
    hand = BlackJackHand(deck,initial_bet)
    
    #check if iniital blackjack
    player_start_val = hand.best_value(hand.get_player_cards())
    dealer_start_val = hand.best_value(hand.get_dealer_cards())
    if player_start_val == 21 and dealer_start_val != 21: #player wins 2.5 bet
        return (initial_bet,2.5*initial_bet)
    elif dealer_start_val == 21 and player_start_val != 21: #dealer wins
        return (initial_bet,0)
    elif player_start_val == 21 and dealer_start_val == 21: #hand is over, tie
        return (initial_bet,initial_bet)
    
    #game continues
    try: 
        hand.play_player_turn(strategy)#player turn
    except Busted:
        #game is over 
        return (hand.get_bet(),0)
    
    try:
        hand.play_dealer_turn()#dealer turn
    except Busted:
        return (hand.get_bet(),2*hand.get_bet())
    
    #nobody has busted, so determine winner
    player_final_val = hand.best_value(hand.get_player_cards())
    dealer_final_val = hand.best_value(hand.get_dealer_cards())
    
    if player_final_val > dealer_final_val:
        return (hand.get_bet(),2*hand.get_bet())
    elif player_final_val < dealer_final_val:
        return (hand.get_bet(),0)
    return (hand.get_bet(),hand.get_bet())

    


#############
# PROBLEM 3 #
#############


def run_simulation(strategy, initial_bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False):
    """
    Runs a simulation and generates a normal distribution reflecting 
    the distribution of player's rates of return across all trials.

    The normal distribution is based on the mean and standard deviation of 
    the player's rates of return across all trials. 
    You should also plot the histogram of player's rates of return that 
    underlies the normal distribution. 
    For hints on how to do this, consider looking at 
        matplotlib.pyplot
        scipy.stats.norm.pdf

    For each trial:

        - instantiate a new CardDeck with the num_decks and type BlackJackCard
        - for each hand in the trial, call play_hand and keep track of how
          much money the player receives across all the hands in the trial
        - calculate the player's rate of return, which is
            100*(total money received-total money bet)/(total money bet)

    Parameters:

        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.copy_dealer_strategy)
        initial_bet - float, the amount that the player initially bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials


    MORE PLOTTING HINTS:

    y_values = stats.norm.pdf(x_values, avg, std), This function returns the y-values of the normal distribution
    make sure x_values passed in are sorted. avg and std can be calculated using some numpy functions. 


    """
    rates_of_return = [] #list of various rates of returns for each trial
    for trial in range(num_trials):
        decks = CardDecks(num_decks,BlackJackCard) #new deck
        
        total_return = 0
        total_bet = 0
        for hand in range(num_hands):#for each hand, add the bet and return to that trial's sum
            amt_bet,amt_return = play_hand(decks,strategy,initial_bet)
            total_bet += amt_bet
            total_return += amt_return
        rates_of_return.append(100*(total_return-total_bet)/total_bet)#return rate of return and append 
        
    #get avg and std using numpy
    avg = np.mean(rates_of_return)
    std = np.std(rates_of_return)
    
    if show_plot:#plot graph
        x_values = sorted(rates_of_return) #sort rates of return
        y_values = stats.norm.pdf(x_values, avg, std)#get normal distribution
        plt.plot(x_values,y_values)#plot normal dist
        
        #make and plot histogram
        hist_vals = np.array(x_values)
        plt.hist(hist_vals,density=True)#plot and normalize y values to fit in 0 to 1 range with normal dist
         
        #edit graph to fit specifications
        
        #get title 
        title_text = "Player ROI on playing " + str(num_hands) + " Hands (" + strategy.__name__ +  ")"
        plt.suptitle(title_text)
        
        #get subtitle and round floats to 2 decimal places
        subtitle_text = "(Mean = " + str(round(avg, 2)) + "%, SD = " + str(round(std, 2)) + "%)"
        plt.title(subtitle_text)
        plt.yticks([])#remove y axis ticks
        
        plt.xlabel("% Return")#add x label
        
        plt.show()#show graph
    
    return (rates_of_return, avg, std)#return tuple
        


def run_all_simulations(strategies):
    """
    Runs a simulation for each strategy in strategies and generates a single graph with normal 
    distribution plot for each strategy. No need to graph the underlying histogram. Each guassian 
    (another name for normal) distribution should reflect the distribution of rates of return 
    for each strategy.

    You might find scypi.stats (imported as stats) helpful.

    You might find matplotlib.pyplot (imported as plt) helpful.

    Make sure to label each plot with the name of the strategy and the x axis label.

    Parameters:

        strategies - list of strategies to simulate
    """
    strategies_strings = []#list of names of strategies in order that parameter has them
    for strategy in strategies:
        results = run_simulation(strategy)#get tuple of results
        strategies_strings.append(strategy.__name__)#add strategy name to list
        x_values = sorted(results[0])#sort rate of returns
        y_values = stats.norm.pdf(x_values, results[1], results[2])#make normal dist

        plt.plot(x_values,y_values)#plot this strategy's normal dist
        
    #add title
    plt.title("Player ROIs for Different Strategies")
    
    #add legend
    plt.legend(strategies_strings)
    plt.xlabel("% Return") #add x label
    plt.show()#show graph
    


if __name__ == '__main__':
    #
    # You can uncomment pieces of the following to test each strategy separately.
    #
    # Default plots:
    #
#    run_simulation(BlackJackHand.copy_dealer_strategy, show_plot=True)
#    run_simulation(BlackJackHand.cheating_strategy, show_plot=True)
#    run_simulation(BlackJackHand.simple_strategy, show_plot=True)
#    run_simulation(BlackJackHand.DD_strategy, show_plot=True)
#
     #Uncomment to run all simulations:
#
#    run_all_simulations([BlackJackHand.copy_dealer_strategy,
#                         BlackJackHand.cheating_strategy,
#                         BlackJackHand.simple_strategy,
#                         BlackJackHand.DD_strategy])
#
    pass
