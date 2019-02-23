from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        peg1 = []
        peg2 = []
        peg3 = []
        for i in self.kb.kb_ask(parse_input('fact: (on ?d ?p)')):
            for j in i.bindings_dict['?d']:
                if j.isdigit():
                    d = int(j) 
            p = int(i.bindings_dict['?p'][3])
            if p == 1:
                peg1.append(d)
            elif p == 2:
                peg2.append(d)
            elif p == 3:
                peg3.append(d)
        peg1.sort()
        peg2.sort()
        peg3.sort()
        return tuple((tuple(peg1),tuple(peg2),tuple(peg3)))

                    

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        
        disk = str(movable_statement.terms[0])
        pegfrom = str(movable_statement.terms[1])
        pegto = str(movable_statement.terms[2])

        oldmoving = self.kb.kb_ask(parse_input("fact: (above " + disk + " ?d)"))
        if oldmoving:
            new_top = oldmoving[0]
            self.kb.kb_retract(parse_input("fact: (above " + disk + " " + new_top['?d'] + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + new_top['?d'] + " " + pegfrom + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + pegfrom + ")"))

        newmoving = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pegto + ")"))
        if newmoving:
            new_top1 = newmoving[0]
            self.kb.kb_retract(parse_input("fact: (top " + new_top1['?x'] + " " + pegto + ")"))
            self.kb.kb_assert(parse_input("fact: (above " + disk + " " + new_top1['?x'] + ")"))
        else:
            self.kb.kb_retract(parse_input("fact: (empty " + pegto + ")"))
    
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + pegfrom + ")"))
        self.kb.kb_assert(parse_input("fact: (top " + disk + " " + pegto + ")"))

        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + pegfrom + ")"))
        self.kb.kb_assert(parse_input("fact: (on " + disk + " " + pegto + ")"))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = [-1, -1, -1]
        row2 = [-1, -1, -1]
        row3 = [-1, -1, -1]
        for i in self.kb.kb_ask(parse_input("fact: (pos ?t ?px ?py")):
            if str(i.bindings_dict['?t'])=='empty':
                t = -1
            else:
                t = int(i.bindings_dict['?t'][4])
            xpx = int(i.bindings_dict['?px'][3])
            xpy = int(i.bindings_dict['?py'][3])
            if xpy == 1:
                row1[xpx-1] = t
            elif xpy == 2:
                row2[xpx-1] = t
            elif xpy == 3:
                row3[xpx-1] = t
        return tuple((tuple(row1),tuple(row2),tuple(row3)))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = str(movable_statement.terms[0])
        fromx = str(movable_statement.terms[1])
        fromy = str(movable_statement.terms[2])
        tox = str(movable_statement.terms[3])
        toy = str(movable_statement.terms[4])
        self.kb.kb_retract(parse_input('fact: (pos ' + tile + ' ' + fromx + ' ' + fromy + ')'))
        self.kb.kb_retract(parse_input('fact: (pos empty ' + tox + ' ' + toy + ')'))
        self.kb.kb_assert(parse_input('fact: (pos ' + tile + ' ' + tox + ' ' + toy + ')'))
        self.kb.kb_assert(parse_input('fact: (pos empty ' + fromx + ' ' + fromy + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
