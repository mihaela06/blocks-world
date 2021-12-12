from Utils import STATE, Block, Move, printSolution, read, printMoves, DLL
from os import sys

def inPosition(block):
    if block == TABLE:
        return True
    if block == SKY:
        return True
    if not block.examined:
        block.examined = True
        if block.currentlyBelow != block.goalBelow:
            block.inPosition = False
        else:
            block.inPosition = inPosition(block.currentlyBelow)
    return block.inPosition


def init(B, readyList, stuckList):
    global SKY
    SKY = Block(len(B))
    global TABLE
    TABLE = B[0]
    for block in B[1:]:
        block.clear = True
        block.examined = False
        block.status = STATE.OTHER
        block.currentlyOn = SKY
        block.goalOn = SKY
    for block in B[1:]:
        inPosition(block)
        if block.currentlyBelow != TABLE:
            block.currentlyBelow.clear = False
            block.currentlyBelow.currentlyOn = block
        if block.goalBelow != TABLE:
            block.goalBelow.goalOn = block
    for block in B[1:]:
        status(block, readyList, stuckList)
    return


def status(block, readyList, stuckList):
    if (not block.inPosition) and block.clear:
        if block.goalBelow == TABLE:
            stat(block, STATE.READY, readyList, stuckList)
        elif block.goalBelow.inPosition and block.goalBelow.clear:
            stat(block, STATE.READY, readyList, stuckList)
        elif block.currentlyBelow == TABLE:
            stat(block, STATE.OTHER, readyList, stuckList)
        else:
            stat(block, STATE.STUCK, readyList, stuckList)
    else:
        stat(block, STATE.OTHER, readyList, stuckList)


def stat(block, status, readyList, stuckList):
    if block.status == STATE.READY:
        readyList.remove(block)
    elif block.status == STATE.STUCK:
        stuckList.remove(block)
    if status == STATE.READY:
        readyList.append(block)
    elif status == STATE.STUCK:
        stuckList.append(block)
    block.status = status


def move(currentMove, plan, readyList, stuckList):
    plan.append(currentMove)
    a = currentMove.a
    b = currentMove.b
    c1 = a.currentlyBelow
    c2 = a.goalOn
    if a.currentlyBelow != TABLE:
        c3 = a.currentlyBelow.goalOn
    else:
        c3 = TABLE
    if a.currentlyBelow != TABLE:
        a.currentlyBelow.clear = True
        a.currentlyBelow.currentlyOn = SKY
    if b != TABLE:
        b.clear = False
        b.currentlyOn = a
        a.inPosition = ((a.goalBelow == b) and b.inPosition)
    else:
        a.inPosition = (a.goalBelow == TABLE)
    a.currentlyBelow = b
    status(a, readyList, stuckList)
    if c1 != TABLE:
        status(c1, readyList, stuckList)
    if c2 != SKY:
        status(c2, readyList, stuckList)
    if c3 != TABLE and c3 != SKY:
        status(c3, readyList, stuckList)


def GN1(B):
    plan = []
    stuckList = DLL()
    readyList = DLL()
    init(B, readyList, stuckList)
    while not (readyList.empty() and stuckList.empty()):
        if not readyList.empty():
            b = readyList.head
            move(Move(b, b.goalBelow), plan, readyList, stuckList)
        else:
            b = stuckList.head
            move(Move(b, TABLE), plan, readyList, stuckList)
    return plan


def main():
    B = read(sys.argv[1])
    plan = GN1(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)
    return


if __name__ == "__main__":
    main()
