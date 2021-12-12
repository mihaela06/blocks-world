from collections import deque
from os import sys

from Utils import generateStatesFromB, planFromSolution, printMoves, printSolution, read

"""
From https://github.com/kouzapo/blocks-world
"""

def depth_first_search(current_state, goal_state):
    """
    An implementation of the DFS algorithm, taking as arguments a current_state
    i.e. initial state, a goal state and an optional argument timeout (default 60)
    indicating the time before the algorithm stops if no solution is found.

    A stack is used as a structure for storing the nodes/states and a set for keeping the 
    ids of the discovered states in order to check quicker whether a node has been discovered.
    """
    S = []  # A stack fot storing the nodes/states.
    discovered = set()  # A set for keeping the ids of the discovered states.

    S.append(current_state)  # Add the current/initial state to the stack.


    while S:  # While S is not empty...

        state = S.pop()  # Pop an element from the top of S.

        if state == goal_state:  # If the state is the goal state, return it and break.
            return state

        if state.id in discovered:  # If the state has been discovered, do nothing.
            continue

        # Else, calculate the children of this state.
        children = state.calcChildren()

        for child in children:  # For each child...
            S.append(child)  # Append the child to S.

        discovered.add(state.id)  # Mark state as discovered.


def DFS(B):
    initial_state, goal_state = generateStatesFromB(B)
    solution = depth_first_search(initial_state, goal_state)
    return planFromSolution(solution)


def main():
    B = read(sys.argv[1])
    plan = DFS(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)
    return


if __name__ == "__main__":
    main()
