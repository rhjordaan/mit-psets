################################################################################
# 6.0002 Spring 2020
# Problem Set 1
# Name: Richter Jordaan
# Collaborators: None
# Time: 4:00

from state import *


##########################################################################################################
## Problem 1
##########################################################################################################

def get_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    data = open(filename) #open the file 
    data.readline() #read and skip past the header
    stateList = [] #create list of State instances
    #for every state in file, add State instance to list and then return list
    for line in data:
        line = line.replace("\n", "") #eliminate all "\n" substrings at ends of all but last lines
        stateinfo = line.split("\t") #split on "\t" substrings since that is how line is formatted when read
        stateList.append(State(stateinfo[0], stateinfo[1], stateinfo[2], stateinfo[3]))
        #stateList.append(State(stateinfo[0],stateinfo[1],stateinfo[2]))
    return stateList

##########################################################################################################
## Problem 2: Helper function 
##########################################################################################################

def election_outcome(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances 

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    #count the number of EC votes among all states
    demcount = 0
    gopcount = 0
    #for each state, add the state's EC votes to the winning party's total count
    for state in election:
        ec = state.get_num_ecvotes()
        if state.get_winner() == "dem": #dem win
            demcount += ec
        else: #gop win
            gopcount += ec
    #return tuple with string of winner as first element and string of loser as second
    return ("dem", "gop") if demcount > gopcount else ("gop","dem")


def winning_candidate_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances won by the winning candidate
    """
    #first determine who winner is
    winner = election_outcome(election)[0]
    
    #for every state in election, if the state was won by winner, append to a list and return the list
    return [state for state in election if state.get_winner() == winner]


def reqd_ec_votes(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    #determine total EC votes of loser
    loserECvotes = 0
    #determine who overall loser was
    loser = election_outcome(election)[1]
    
    #get sum of EC votes of states where overall loser won the state
    for state in election:
        if state.get_winner() == loser:
            loserECvotes += state.get_num_ecvotes()
    #return how far away loser was from winning
    return (int)(total/2+1 - loserECvotes)
    

##########################################################################################################
## Problem 3: Greedy approach
##########################################################################################################

def greedy_swing_states(winner_states, reqd_votes):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states, these are our swing states. First choose the states 
    with the smallest win margin, i.e. state that was won by the smallest difference in 
    number of voters. If two states have the same margin, choose the one that appears 
    first alphabetically. Continue to choose other states up until it meets or exceeds the 
    reqd_votes. Should only return states that were originally won by the winner of 
    the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    reqd_votes - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states 
    The empty list, if no possible swing states
    """
    #if no possible swing states, return empty list
    if len(winner_states) ==0:
        return []
    
    #since we want a margin tie to go to alphabet, first sort alphabetically
    #thus if there's a margin tie, the element that appears first in list is selected
    alpha_sorted_winner_states = sorted(winner_states, key = lambda State:State.get_name())
    #sort states based on margin
    sorted_winner_states = sorted(alpha_sorted_winner_states, key = lambda State:State.get_margin())
    #create list of swing states 
    swingStateList = []
    addedECvotes = 0 #number of EC votes added, to know when to stop adding EC votes
    
    i = 0 #index in loop
    while(addedECvotes<reqd_votes):
        swingState = sorted_winner_states[i] #get swing state
        swingStateList.append(swingState) #add to list of swing states
        addedECvotes += swingState.get_num_ecvotes() #add state's EC votes to addedECvotes
        i+=1 #increment i
    return swingStateList #return list of swing states
    

##########################################################################################################
## Problem 4: Dynamic Programming
## In this section we will define two functions, move_max_voters and move_min_voters, that
## together will provide a dynamic programming approach to find swing states. This problem
## is analagous to the complementary knapsack problem, you might find Lecture 1 of 6.0002 useful 
## for this section of the pset. 
##########################################################################################################

def move_max_voters(winner_states, ec_votes, memo=None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. 

    Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin+1),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

    Hint: If using a top-down implementation, it may be helpful to create a helper function

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, the maximum number of EC votes 
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    The empty list, if every state has a # EC votes greater than ec_votes
    """
    if memo == None: #memo is dictionary with key: (len(winner_states),ec_votes) and value: list of optimal states
        memo = {}
    if len(winner_states) == 0:
        result = []
    elif (len(winner_states),ec_votes) in memo: #check if result has already been computed
        result = memo[(len(winner_states),ec_votes)]
    elif winner_states[0].get_num_ecvotes()>ec_votes:#check if current choice would surpass ec_votes limit
        result = move_max_voters(winner_states[1:],ec_votes,memo)
    else:
        #compute result of both selecting and not selecting state and choose optimal
        nextState = winner_states[0]
        
        #left branch
        withState = move_max_voters(winner_states[1:],ec_votes-nextState.get_num_ecvotes(),memo)
        withMovedVoters = nextState.get_margin()+1+sum_moved_voters(withState)
        
        #right branch
        withoutState = move_max_voters(winner_states[1:],ec_votes,memo)
        withoutMovedVoters = sum_moved_voters(withoutState)
        
        #see which branch is better
        if withMovedVoters > withoutMovedVoters: #choose left branch
            result = [nextState]+withState
            
        else:
            result = withoutState
    #always add result to dictionary to avoid recomputing it
    memo[len(winner_states),ec_votes] = result
    return result
    
def sum_moved_voters(stateList):
    """
    finds and returns the sum of the moved voters in a list of states
    
    Parameters:
    stateList: a list of states
    
    Returns:
    the total number of moved voters among all states in list
    """
    #can i use simplified for each loop shown in lecture2?
    moved_voters = 0
    for state in stateList:
        moved_voters+=state.get_margin()+1 #get current state's voters and increment
    return moved_voters #return result


def move_min_voters(winner_states, reqd_votes):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of move_max_voters. You should call 
    move_max_voters with ec_votes set to (#ec votes won by original winner - reqd_votes)

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    reqd_votes - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    winner_total_votes = 0 #total number of winnner votes among all winning states
    for state in winner_states:
        winner_total_votes+=state.get_num_ecvotes()
    #get and return a list of non swing states
    non_swing_states = move_max_voters(winner_states,winner_total_votes-reqd_votes)

    #swing states are states won by original winner not in non_swing_states
    #create and return list of swing states
    return [state for state in winner_states if not state in non_swing_states]

    
    

##########################################################################################################
## Problem 5
##########################################################################################################

def shuffle_voters(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. Moves voters 
    from states that were won by the losing candidate (states not in winning_candidate_states), to 
    each of the states in swing_states. To win a swing state, you must move (margin + 1) 
    new voters into that state. Any state that voters are moved from should still be won 
    by the loser even after voters are moved. Also finds the number of EC votes gained by 
    this rearrangement, as well as the minimum number of voters that need to be moved.
    Note: You cannot move voters out of New York, Washington, Massachusetts, or California. 

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of move_min_voters or greedy_swing_states)

    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple of str, (from_state, to_state), the 2 letter State names
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
    None, if it is not possible to sway the election
    """
    shuffle_dict = {} #dictionary of state voting movements and number of people moved
    total_ec_gain = 0 #total number of EC votes gained
    total_voters_moved = 0 #total number of voters moved
    proud_states = ["NY", "WA", "MA", "CA"] #states that can't move voters from
    
    #first find winning states to determine losing states
    winner_states = winning_candidate_states(election)
    
    #create list of states won by original loser tat are valid to move voters from
    losing_candidate_states = [state for state in election if not state in winner_states and not state.get_name() in proud_states]
            
    if len(losing_candidate_states)==0: #if the winner won all states, this process won't work
        return None

    #for every swing state, move enough voters to win that state
    for swing_state in swing_states:
        votes_needed = swing_state.get_margin()+1 #votes needed to flip state
        losing_state_index = 0 #index of current losing state to move voters from
        while votes_needed>0:
            current_losing_state = losing_candidate_states[losing_state_index] #currrent state to move voters frm
            
            max_voters_to_move = current_losing_state.get_margin()-1 #max voters that can be moved
            
            added_votes = min(max_voters_to_move,votes_needed) #number of voters that can be moved to this swing state
            total_voters_moved+=added_votes #increment total voters moved
            
            current_losing_state.subtract_voters_winning_candidate(added_votes) #update losing state object

            swing_state.add_voters_losing_candidate(added_votes) #update swing state object
            
            shuffle_dict[(current_losing_state.get_name(),swing_state.get_name())] = added_votes #add to dict
            
            votes_needed-=added_votes #update number of votes still needed by swing state
            if current_losing_state.get_margin()==1: #if losing state cannot move more voters, increment losing_state_index
                losing_state_index+=1
        total_ec_gain += swing_state.get_num_ecvotes() #update EC addition

    return (shuffle_dict,total_ec_gain,total_voters_moved) #return tuple

if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

    # # tests Problem 1
    year = 2012
    election = get_election("%s_results.txt" % year)
    print(len(election))
    print(election[0])

    # # tests Problem 2
    winner, loser = election_outcome(election)
    won_states = winning_candidate_states(election)
    names_won_states = [state.get_name() for state in won_states]
    ec_votes_needed = reqd_ec_votes(election)
    print("Winner:", winner, "\nLoser:", loser)
    print("States won by the winner: ", names_won_states)
    print("EC votes needed:",ec_votes_needed, "\n")

    # # tests Problem 3
    print("greedy_swing_states")
    greedy_swing = greedy_swing_states(won_states, ec_votes_needed)
    names_greedy_swing = [state.get_name() for state in greedy_swing]
    voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
    ecvotes_greedy = sum([state.get_num_ecvotes() for state in greedy_swing])
    print("Greedy swing states results:", names_greedy_swing)
    print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.\n")

    # # tests Problem 4: move_max_voters
    print("move_max_voters")
    total_lost = sum(state.get_num_ecvotes() for state in won_states)
    non_swing_states = move_max_voters(won_states, total_lost-ec_votes_needed)
    non_swing_states_names = [state.get_name() for state in non_swing_states]
    max_voters_displaced = sum([state.get_margin()+1 for state in non_swing_states])
    max_ec_votes = sum([state.get_num_ecvotes() for state in non_swing_states])
    print("States with the largest margins (non-swing states):", non_swing_states_names)
    print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # # tests Problem 4: move_min_voters
    print("move_min_voters")
    swing_states = move_min_voters(won_states, ec_votes_needed)
    swing_state_names = [state.get_name() for state in swing_states]
    min_voters_displaced = sum([state.get_margin()+1 for state in swing_states])
    swing_ec_votes = sum([state.get_num_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters_displaced, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # # tests Problem 5: shuffle_voters
    print("shuffle_voters")
    flipped_election = shuffle_voters(election, swing_states)
    print("Flip election mapping:", flipped_election)