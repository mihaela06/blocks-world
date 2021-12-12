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
        block.highestInPosition = TABLE
    for block in B[1:]:
        inPosition(block)
        if block.currentlyBelow != TABLE:
            block.currentlyBelow.clear = False
            block.currentlyBelow.currentlyOn = block
        if block.goalBelow != TABLE:
            block.goalBelow.goalOn = block
    for block in B[1:]:
        status(block, readyList, stuckList)
    for block in B[1:]:
        block.examined = False
    for block in B[1:]:
        getCurrentlyConcierge(block)
    for block in B[1:]:
        block.examined = False
    for block in B[1:]:
        getGoalConcierge(block)
    for block in B[1:]:
        block.examined = False
    return


def getCurrentlyConcierge(block):
    if not block.examined:
        block.examined = True
        if block.currentlyBelow != TABLE:
            block.currentlyConcierge = getCurrentlyConcierge(
                block.currentlyBelow)
        else:
            block.currentlyConcierge = block
        block.currentlyConcierge.top = block
    return block.currentlyConcierge


def getGoalConcierge(block):
    if not block.examined:
        block.examined = True
        if block.goalBelow != TABLE:
            block.goalConcierge = getGoalConcierge(block.goalBelow)
        else:
            block.goalConcierge = block
        if block.inPosition:
            block.goalConcierge.highestInPosition = block
    return block.goalConcierge


def beta(BETA, stuckList):
    f = False
    while not (f or len(BETA) == 0):
        block = BETA[-1]
        if block.status != STATE.STUCK:
            BETA.pop()
        else:
            f = True
    if len(BETA) == 0:
        block = stuckList.head
        BETA.append(block)
        block.examined = True
    f = False
    while not f:
        block = delta(BETA[-1])
        if block is None:
            break
        if block.examined:
            f = True
        else:
            block.examined = True
            BETA.append(block)
    return BETA[-1]


def delta(block):
    if block.status != STATE.STUCK:
        return block
    c = block.goalConcierge.highestInPosition
    if c != TABLE:
        d = c.goalOn
    else:
        d = block.goalConcierge
    if c == TABLE:
        return d.currentlyConcierge.top
    if c.clear:
        return d.currentlyConcierge.top
    return c.currentlyConcierge.top


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
        a.currentlyConcierge.top = a.currentlyBelow
    if b != TABLE:
        b.clear = False
        b.currentlyOn = a
        a.currentlyConcierge = b.currentlyConcierge
        a.inPosition = ((a.goalBelow == b) and b.inPosition)
    else:
        a.currentlyConcierge = a
        a.inPosition = (a.goalBelow == TABLE)
    a.currentlyConcierge.top = a
    if a.inPosition:
        a.goalConcierge.highestInPosition = a
    a.currentlyBelow = b
    status(a, readyList, stuckList)
    if c1 != TABLE:
        status(c1, readyList, stuckList)
    if c2 != SKY:
        status(c2, readyList, stuckList)
    if c3 != TABLE and c3 != SKY:
        status(c3, readyList, stuckList)


def GN2(B):
    plan = []
    stuckList = DLL()
    readyList = DLL()
    BETA = []
    init(B, readyList, stuckList)
    while not (readyList.empty() and stuckList.empty()):
        if not readyList.empty():
            b = readyList.head
            move(Move(b, b.goalBelow), plan, readyList, stuckList)
        else:
            b = beta(BETA, stuckList)
            move(Move(b, TABLE), plan, readyList, stuckList)
    return plan


def main():
    B = read(sys.argv[1])
    plan = GN2(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)
    return


if __name__ == "__main__":
    main()
