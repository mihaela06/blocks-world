from Utils import Move, printSolution, read, printMoves
from os import sys


def inPosition(block):
    if block == TABLE:
        return True
    if not block.examined:
        block.examined = True
        if block.currentlyBelow != block.goalBelow:
            block.inPosition = False
        else:
            block.inPosition = inPosition(block.currentlyBelow)
    return block.inPosition


def init(B):
    global TABLE
    TABLE = B[0]
    for block in B[1:]:
        block.clear = True
        block.examined = False
    for block in B[1:]:
        inPosition(block)
        if block.currentlyBelow != TABLE:
            block.currentlyBelow.clear = False
    return


def move(currentlyMove, plan):
    plan.append(currentlyMove)
    if currentlyMove.a.currentlyBelow != TABLE:
        currentlyMove.a.currentlyBelow = True
    if currentlyMove.b != TABLE:
        currentlyMove.b.clear = False
        currentlyMove.a.inPosition = (
            currentlyMove.a.goalBelow == currentlyMove.b) and currentlyMove.b.inPosition
    else:
        currentlyMove.a.inPosition = (currentlyMove.a.goalBelow == TABLE)
    currentlyMove.a.currentlyBelow = currentlyMove.b


def unstack(block, plan):
    if not block.inPosition and block.currentlyBelow != TABLE:
        c = block.currentlyBelow
        move(Move(block, TABLE), plan)
        unstack(c, plan)


def stack(block, plan):
    if not block.inPosition:
        stack(block.goalBelow, plan)
        move(Move(block, block.goalBelow), plan)


def US(B):
    plan = []
    init(B)
    for block in B[1:]:
        if block.clear:
            unstack(block, plan)
    for block in B[1:]:
        stack(block, plan)
    return plan


def main():
    B = read(sys.argv[1])
    plan = US(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)
    return


if __name__ == "__main__":
    main()
