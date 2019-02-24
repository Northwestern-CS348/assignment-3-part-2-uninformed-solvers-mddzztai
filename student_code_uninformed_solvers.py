
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states rea1chable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        self.visited[self.currentState] = True
        if self.gm.getGameState() == self.victoryCondition: 
            return True

        moves = self.gm.getMovables()
        if moves:
            visitallstate = True
            for i in moves:
                self.gm.makeMove(i)
                currentGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, i)
                
                if not self.visited.get(currentGameState, False) and not currentGameState in self.currentState.children:
                    self.currentState.children.append(currentGameState)
                    currentGameState.parent = self.currentState
                self.gm.reverseMove(i)

            for child in self.currentState.children:
                move = child.requiredMovable
                self.gm.makeMove(move)

                if self.visited.get(child, False):
                    self.gm.reverseMove(move)
                    continue

                self.visited[child] = True
                self.currentState = child
                visitallstate = False
                break

            if visitallstate:
                self.currentState = self.currentState.parent
                
            
            
            
        else:
            self.currentState = self.currentState.parent
            
        
        if self.gm.getGameState() == self.victoryCondition:
            return True

        return False
                

        



        


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visited[self.currentState] = True
        if self.gm.getGameState() == self.victoryCondition: 
            return True

        moves = self.gm.getMovables()
        curr = self.currentState
        if moves and not curr.children:
            for i in moves:
                self.gm.makeMove(i)
                newstate = GameState(self.gm.getGameState(), curr.depth + 1, i)
                newstate.parent = curr
                curr.children.append(newstate)
                self.gm.reverseMove(i)
        self.bfsHelp()
        return False
    
    
    def bfsHelp(self):
        while self.currentState.parent and len(self.currentState.parent.children)-1 == self.getIndex(self.currentState):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            next_index = self.getIndex(self.currentState)+1
            self.currentState = self.currentState.parent.children[next_index]
            self.gm.makeMove(self.currentState.requiredMovable)
        while self.visited.get(self.currentState,False) and self.currentState.children:
            index = 0
            self.currentState = self.currentState.children[index]
            self.gm.makeMove(self.currentState.requiredMovable)
        if self.visited.get(self.currentState,False):
            self.bfsHelp()
        return True
            
    def getIndex(self, state):
        return state.parent.children.index(state)


