from collections import deque
from os import sys

from Utils import generateStatesFromB, planFromSolution, printMoves, printSolution, read

"""
From https://github.com/kouzapo/blocks-world
"""

def breadth_first_search(current_state, goal_state):
    """
    An implementation of the BFS algorithm, taking as arguments a current_state
    i.e. initial state, a goal state and an optional argument timeout (default 60)
    indicating the time before the algorithm stops if no solution is found.

    A queue is used as a structure for storing the nodes/states and a set for keeping the 
    ids of the discovered states in order to check quicker whether a node has been discovered.
    """
    Q = deque([])  # A queue for storing the nodes/states.
    discovered = set()  # A set for keeping the ids of the discovered states.

    Q.append(current_state)  # Add the current/initial state to the queue.
    discovered.add(current_state.id)  # Add the id of the state to the set.

    while Q:  # While Q is not empty...

        state = Q.popleft()  # Dequeue an element from the left of Q.

        if state == goal_state:  # If the state is the goal state, return it and break.
            return state

        # Else, calculate the children of this state.
        children = state.calcChildren()

        for child in children:  # For each child...
            if child.id not in discovered:  # If this child has not been discovered...
                discovered.add(child.id)  # Mark it as discovered.
                # Set the parent attribute of the child to be the state that has been dequeued.
                child.parent = state

                Q.append(child)  # Append the child to Q.


def BFS(B):
    initial_state, goal_state = generateStatesFromB(B)
    solution = breadth_first_search(initial_state, goal_state)
    return planFromSolution(solution)


def main():
    B = read(sys.argv[1])
    plan = BFS(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)
    return


if __name__ == "__main__":
    main()
