from collections import deque
from os import sys

from Utils import generateStatesFromB, planFromSolution, printMoves, printSolution, read

"""
From https://github.com/kouzapo/blocks-world
"""


def __astar_heuristic(F, goal_layout, blocks_keys):
    """
    The __astar_heuristic is a private heuristic function that
    is used in the A* Search algorithm.

    It takes as arguments a search frontier F containing State objects,
    a dict object (goal_layout), containing the layout of the goal state,
    and a list object (blocks_keys), containing the names/keys of the blocks.

    The function is a variation of the __out_of_place_heuristic function,
    with the addition of the distance attribute in the calculation of the scores.
    It counts how many blocks are not in the final position and adds the total number
    of steps from the root. So between two states with equal out of place blocks,
    the heuristic function chooses the one with the smallest distance from the root.
    """
    scores = []  # A list object containing the score of each state.

    for state in F:
        score = 0  # Initialize each score to 0.

        for key in blocks_keys:  # For each block...
            # If it is not in its final position...
            if state.layout[key] != goal_layout[key]:
                score += 1  # Add 1 to score.

        score += state.distance  # Add the distance from the root to score.

        scores.append(score)

    # Return the index of the state with the minimun score.
    return scores.index(min(scores))


def heuristic_search(current_state, goal_state):
    """
    This function implements a heuristic search algorithm. Essensialy, the implementation is the
    same with BFS but the structure for storing the nodes/states is now a list and the choice of the
    node to be examined is made by a heuristic function.
    """

    F = []  # A list fot storing the nodes/states.
    discovered = set()  # A set for keeping the ids of the discovered states.
    # A list with the names/keys of the blocks.
    blocks_keys = list(current_state.layout.keys())

    F.append(current_state)  # Add the current/initial state to the list.
    discovered.add(current_state.id)  # Add the id of the state to the set.


    while F:  # While F is not empty...

        # Return the index of the state with the minimum score in F.
        i = __astar_heuristic(F, goal_state.layout, blocks_keys)
        state = F.pop(i)  # Pop the state with the minimum score.

        if state == goal_state:  # If the state is the goal state, return it and break.
            return state

        # Else, calculate the children of this state.
        children = state.calcChildren()

        for child in children:  # For each child...
            if child.id not in discovered:  # If this child has not been discovered...
                discovered.add(child.id)  # Mark it as discovered.
                # Set the parent attribute of the child to be the state that has been poped.
                child.parent = state

                F.append(child)  # Append the child to F.


def ASTAR(B):
    initial_state, goal_state = generateStatesFromB(B)
    solution = heuristic_search(initial_state, goal_state)
    return planFromSolution(solution)


def main():
    B = read(sys.argv[1])
    plan = ASTAR(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)
    return


if __name__ == "__main__":
    main()
