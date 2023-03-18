from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        
        def MinimaxFunction(gameState,agt,depth):
            ans = []
            
            # If the game is ended (win or lose)
            if gameState.isWin():
                return self.evaluationFunction(gameState),0
            if gameState.isLose():
                return self.evaluationFunction(gameState),0
            
            # If it arrive max depth
            if depth == self.depth:
                return self.evaluationFunction(gameState),0
            if agt == gameState.getNumAgents() - 1:
                depth += 1
            if agt == gameState.getNumAgents() - 1:
                nxt_agt = self.index
            else:
                nxt_agt = agt + 1
            
            # The function that fix the answer with minimax value
            def FixingFunction():
                nxt_val = MinimaxFunction(gameState.getNextState(agt,action),nxt_agt,depth)
                ans.append(nxt_val[0])
                ans.append(action)
            
            # The function that check the minimax value
            def CheckingFunction():
                prvs_val = ans[0]
                nxt_val = MinimaxFunction(gameState.getNextState(agt,action),nxt_agt,depth)
                if agt == self.index and nxt_val[0] > prvs_val:
                     ans[0] = nxt_val[0]
                     ans[1] = action
                elif agt != self.index and nxt_val[0] <= prvs_val:    
                     ans[0] = nxt_val[0]
                     ans[1] = action
               
            # Find every minimax value 
            for action in gameState.getLegalActions(agt):
                if len(ans) == 0: 
                   FixingFunction()
                else:
                   CheckingFunction()
                                     
            return ans

        return MinimaxFunction(gameState,self.index,0)[1]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        def AlphaBetaPruning(gameState,agt,depth,alpha,beta):
            ans = []
            
            # If the game is ended (win or lose)
            if gameState.isWin():
                return self.evaluationFunction(gameState),0
            if gameState.isLose():
                return self.evaluationFunction(gameState),0
            
            # If it arrive max depth
            if depth == self.depth:
                return self.evaluationFunction(gameState),0
            if agt == gameState.getNumAgents() - 1:
                depth += 1
            if agt == gameState.getNumAgents() - 1:
                nxt_agt = self.index
            else:
                nxt_agt = agt + 1
        

            for action in gameState.getLegalActions(agt):
                if  len(ans) == 0 :
                    nxt_val = AlphaBetaPruning(gameState.getNextState(agt,action),nxt_agt,depth,alpha,beta)


                    ans.append(nxt_val[0])
                    ans.append(action)
                
                # Modified the initial value of alpha and beta 
                    if agt == self.index:
                        if ans[0] > alpha:
                            alpha = ans[0]
                    else:
                        if ans[0] < beta:
                            beta = ans[0]
             
                else:
                # If the alpha-beta pruning is correct           
                    if ans[0] > beta:
                      if agt == self.index:
                        return ans

                    if ans[0] < alpha :
                     if agt != self.index:
                        return ans

                    prvs_val = ans[0] 
                    nxt_val = AlphaBetaPruning(gameState.getNextState(agt,action),nxt_agt,depth,alpha,beta)

                # Max agent
                    if agt == self.index:
                        if nxt_val[0] > prvs_val:
                            ans[0] = nxt_val[0]
                            ans[1] = action
                            if ans[0] > alpha:
                                alpha = ans[0]
                # Min agent
                    else:
                        if nxt_val[0] < prvs_val:
                            ans[0] = nxt_val[0]
                            ans[1] = action
                            if ans[0] < beta:
                                beta = ans[0]
                           
            return ans

        return AlphaBetaPruning(gameState,self.index,0,-float("inf"),float("inf"))[1]
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        def ExpectivemaxFunction(gameState,agt,depth):
            ans = []
           
            # If the game is ended (win or lose)
            if gameState.isWin():
                return self.evaluationFunction(gameState),0
            if gameState.isLose():
                return self.evaluationFunction(gameState),0
           
            # If it arrive max depth
            if depth == self.depth:
                return self.evaluationFunction(gameState),0
            if agt == gameState.getNumAgents() - 1:
                depth += 1
            if agt == gameState.getNumAgents() - 1:
                nxt_agt = self.index
            else:
                nxt_agt = agt + 1
            
            # The function that fix chance node 
            # p = 1 / total legal actions
            def FixingFunction():
               
                    nxt_val = ExpectivemaxFunction(gameState.getNextState(agt,action),nxt_agt,depth)
                  
                    if(agt != self.index):
                        ans.append((1.0 / len(gameState.getLegalActions(agt))) * nxt_val[0])
                        ans.append(action)
                    else:
                        ans.append(nxt_val[0])
                        ans.append(action)
            
            # The function that check the minimax value
            def CheckingFunction():
                prvs_val = ans[0] 
                nxt_val = ExpectivemaxFunction(gameState.getNextState(agt,action),nxt_agt,depth)
            
                if agt == self.index:
                    if nxt_val[0] > prvs_val:
                       ans[0] = nxt_val[0]
                       ans[1] = action
                else:
                    ans[0] = ans[0] + (1.0 / len(gameState.getLegalActions(agt))) * nxt_val[0]
                    ans[1] = action
            
            for action in gameState.getLegalActions(agt):
               
                if len(ans) == 0 : 
                  FixingFunction()
                            
                else:
                  CheckingFunction()
                    
            return ans

        return ExpectivemaxFunction(gameState,self.index,0)[1]
        
    # End your code (Part 3)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    
    # Get the list of the food
    food_list = currentGameState.getFood().asList()
    
    # Get the total number of the food
    Num_of_food = len(food_list)
    
    # Get the total number of capsules
    Num_of_cap = len(currentGameState.getCapsules())
    
    # Get the position of pacman 
    pacman_pos = currentGameState.getPacmanPosition()
   
    # Get the position of ghosts
    ghost_pos = currentGameState.getGhostPositions()
    
    # Get the state of the ghosts
    ghost_state= currentGameState.getGhostStates()
    
    # Initialize the distance of the nearest food
    nearest_food = 1
    
    # The lists of normal ghosts and those can be eaten. 
    normal_ghost = [] 
    weak_ghost = []
    
    # The lists of distances to normal ghosts and those can be eaten. 
    normal_ghost_distance = []
    weak_ghost_distance = []
    
    # Get the score
    score = currentGameState.getScore()
    
    # Initialize the evaluation value
    Evaluation_Value = 0
    
    # Add those scared ghost into the weak ghost list and 
    # the other to the normal ghost list 
    for ghost in ghost_state:
       if ghost.scaredTimer: 
           weak_ghost.append(ghost)
       else:
           normal_ghost.append(ghost)
   
   # The list of distances of pacman to the food
    food_distances = [manhattanDistance(pacman_pos, food_position) for food_position in food_list]

   # There always be a nearest food while there is food have not been eaten
    if Num_of_food > 0:
      nearest_food = min(food_distances)

   # The list of the distances of pacman and ghosts
    for ghost_position in ghost_pos:
       ghost_distance = manhattanDistance(pacman_pos, ghost_position)

   # If the ghost is too close to the nearest food,
   # set the distance of the nearest food a bigger value
       
       if ghost_distance <= 1:
           nearest_food = 10000 # Set the value very big if the ghost is super close
                                # because I don't want it to lose
       elif ghost_distance <= 2:
           nearest_food = 3       
  
   # Get manhattan distance
    for ghost in normal_ghost:
        weak_ghost_distance.append(manhattanDistance(pacman_pos,ghost.getPosition()))

    for ghost in weak_ghost:
        weak_ghost_distance.append(manhattanDistance(pacman_pos,ghost.getPosition()))
   
   # Give value to ghosts that can be eaten 
    for i in weak_ghost_distance:
        if i < 3:
            Evaluation_Value += -30 * i
        else :
            Evaluation_Value += -10 * i
   
   # Give value to ghosts that are normal
    for i in normal_ghost_distance:
        if i <= 1:
            Evaluation_Value += 20 * i
        elif i <= 3:
            Evaluation_Value += 10 * i
        elif i <= 5:
            Evaluation_Value += 5 * i
        else:
            Evaluation_Value += 1 * i
   
   # Add the value of each weights * features 
    Evaluation_Value += 20 / nearest_food
    Evaluation_Value += 100 * score
    Evaluation_Value += (-150) * Num_of_food
    Evaluation_Value += (-30) * Num_of_cap
    
    return Evaluation_Value
    # End your code (Part 4)

better = betterEvaluationFunction
