import numpy as np

def attack_pairs(queens):

    """
    computes number of pairs of attacking queens
    Args:
      queens (ndarray (n, ))  : represents the assignment of queens on the board.  n = 8 for the 8-queens problem.
    Returns
      attack_pairs scaler     : number of pairs of attacking queens for the given queens assignment on the board.
    """
    attack_pairs = 0
    ### START CODE HERE
    for i in range(len(queens)):
        index = queens[i]
        for j in range(i + 1, len(queens)):
            if index == queens[j] or abs(queens[i] - queens[j]) == abs(i - j):
                attack_pairs += 1   
    ### END CODE HERE
                
    return attack_pairs

def attack_pairs_board(queens):
    n = len(queens)
    ### START CODE HERE
    counts = np.zeros((n,n))
    
    for column in range(n):
        for row in range(n):
            queens_temp = queens.copy()
            queens_temp[column] = row # Move queen to the new row
            counts[row][column] = attack_pairs(queens_temp) # For each row and column in the array, we calculate attack_pairs and place that value inside its corrseponding spot
    ### END CODE HERE
    return counts 

def steepest_ascent_hill_climb(n):
    """
    Performs a steepest ascent hill climb toward a goal state of a queens assignment (represented in the form of a 
    Numpy array of size (n, )) in which there are no pairs of queens attacking each other. Not every execution
    of this function will result in success - often a local optimum will be reached (i.e., a local minimum in which
    the number of attacking pairs is > 0, but no neighbors offer any improvement).
     
    Args:
      n (scalar)                    : Dimension of the board. For 8-queens, n = 8 (but we could use this to 
                                      solve say, 10-queens).
    Returns:
      current_attack_pairs (scalar) : Count of attacking pairs of the local optimum it found (0 if goal state found).
      queens (ndarray (n, ))        : Locally optimum queens assignment, or, if attack pairs = 0, a globally optimum 
                                      assignment.
    """
    
    # Start with a random assignment of queens on the board.
    queens = np.random.randint(n, size=n)
 
    while True:
        # Calculate the current number of attacking pairs
        current_attack_pairs = attack_pairs(queens)
        
        # If there are no attacking pairs, we've reached the global optimum
        if current_attack_pairs == 0:
            return current_attack_pairs, queens
        
        # Initialize variables to keep track of the best move and its attack pairs
        best_move = None
        best_attack_pairs = current_attack_pairs
        
        # Iterate over all possible moves
        for column in range(n):
            for row in range(n):
                if queens[column] != row:
                    queens_temp = queens.copy()
                    queens_temp[column] = row  # Move queen to the new row
                    attack_pairs_temp = attack_pairs(queens_temp)
                    
                    # Check if this move results in fewer attacking pairs
                    if attack_pairs_temp < best_attack_pairs:
                        best_attack_pairs = attack_pairs_temp
                        best_move = (column, row)
        
        # If no better move was found, we're at a local minimum
        if best_move is None:
            return current_attack_pairs, queens
        
        # Make the best move
        column, row = best_move
        queens[column] = row

# UNIT TEST 1 - steepest_ascent_hill_climb()

# This test runs steepest ascent 100 times, giving us the chance to to observe the frequency with which 
# it arrives at a solution for 100 randomly chosen starting queen assignments.  We know from the literature 
# that the overall average is about 14%.

np.random.seed(0)  # reset seed to produce the same set of starting queen assignments with every execution

num_successes = 0
for i in range(100):
    attack_pairs_count, queens = steepest_ascent_hill_climb(8)
    if attack_pairs_count == 0:
        print(f'Success: {queens}')
        num_successes += 1
        
print(f'\nNumber of successes: {num_successes}')

def successors_probs(queens, k):
    """
    returns a probability distribution whose values correspond to the attack pair counts for a queens arrangement
    that is passed in as an input argument.  That is, cells with lower attack pair counts are assigned higher 
    probabilities and those with higher counts are assigned lower probabilities.
     
    Args:
      queens ((n, ) ndarray)         : queens assignment on a board
      k (scalar)                     : scaling factor for probabilities.  (max_prob = k x min_prob - see above)
                                        
    Returns
      probs ((n**2, ) ndarray)         : 1D array of probs whose length is n**2, giving a probability for each cell 
                                       in the n x n grid of successors.  
    """
    n = len(queens)
    
    ### BEGIN CODE HERE
    max_attack_pairs = (n * (n - 1)) / 2
    
    successors_fitness = max_attack_pairs - np.array(attack_pairs_board(queens)).flatten()
    
    x_1 = min(successors_fitness) 
    x_2 = max(successors_fitness) 
    
    scaled_successors_fitness = (((successors_fitness * (k - 1)) / (x_2 - x_1))) + (x_2 - (k * x_1)) / (x_2 - x_1)
    
    probs = scaled_successors_fitness / scaled_successors_fitness.sum()

    ### END CODE HERE
    
    return probs        

def stochastic_hill_climb(n, k):
    queens = np.random.randint(n, size=n)
    max_iterations = 1000  # You can adjust this as needed
    
    for _ in range(max_iterations):
        current_attack_pairs = attack_pairs(queens)
        
        if current_attack_pairs == 0:
            # Found a solution with no attacking queens
            return attack_pairs(queens), queens

        successors = []
        probs = successors_probs(queens, k)
        
        # Generate a random index according to the probability distribution
        index = np.random.choice(np.arange(n * n), p=probs)
        
        # Calculate the column and row based on the flattened index
        column = index % n
        row = index // n
        
        queens_temp = queens.copy()
        queens_temp[column] = row
        new_attack_pairs = attack_pairs(queens_temp)

        if new_attack_pairs < current_attack_pairs:
            queens = queens_temp.copy()

    return attack_pairs(queens), queens
