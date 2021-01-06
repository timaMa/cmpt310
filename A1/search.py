# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 20
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>
I like the topic about minimax and Alpha-beta pruning, but I also found this topic is difficult for me 
to understand because I have a poor understanding towards a algorithm when it comes to recursion. 
"""
#####################################################
#####################################################

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Q1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    You will get (5,5)

    print (problem.isGoalState(problem.getStartState()) )
    You will get True

    print ( problem.getSuccessors(problem.getStartState()) )
    You will get [((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"
    # import class stack
    from util import Stack
    fringe = Stack()
    # explored nodes
    explored = []
    # solution
    solution = []
    # initial state
    fringe.push((problem.getStartState(), solution))
    while not fringe.isEmpty():
        state, solution = fringe.pop()
        if problem.isGoalState(state):
            return solution
        explored.append(state)
        # expand
        successors = problem.getSuccessors(state)
        # push node (x, y) into fringe
        for i in successors:
            if i[0] not in explored:
                fringe.push((i[0], solution + [i[1]]))

def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # import class stack
    from util import Queue
    fringe = Queue()
    # explored nodes
    explored = []
    # solution
    solution = []
    # initial state
    fringe.push((problem.getStartState(), solution))
    explored.append(problem.getStartState())
    while not fringe.isEmpty():
        state, solution = fringe.pop()
        if problem.isGoalState(state):
            return solution
        # expand
        successors = problem.getSuccessors(state)
        # push node (x, y) into fringe
        for i in successors:
            if i[0] not in explored:
                explored.append(i[0])
                fringe.push((i[0], solution + [i[1]]))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue
    fringe = PriorityQueue()
    # for checking if in the fringe
    fringe_list = {}
    # explored
    explored = []
    # solution
    solution = []
    # initial state
    fringe.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    fringe_list[problem.getStartState()] = solution
    while not fringe.isEmpty():
        state = fringe.pop()
        if problem.isGoalState(state):
            return fringe_list.get(state)
        explored.append(state)
        solution = fringe_list.get(state)
        fringe_list.pop(state)
        # expand
        successors = problem.getSuccessors(state)
        # push node (x, y) into fringe
        for i in successors:
            if i[0] in explored:
                continue
            g_n = problem.getCostOfActions(solution) + i[2]
            h_n = g_n + heuristic(i[0], problem)

            if i[0] not in fringe_list:
                fringe.push(i[0], h_n)
                fringe_list[i[0]] = solution + [i[1]]
            else:
                if g_n < problem.getCostOfActions(fringe_list.get(i[0])):
                    fringe.update(i[0], h_n)
                    fringe_list[i[0]] = solution + [i[1]]




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
