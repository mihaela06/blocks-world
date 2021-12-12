from Utils import STATE, Block, Move, printSolution, read, printMoves
import GN1H
from itertools import combinations
from copy import deepcopy
from os import sys


Bcopy = None

def initialiseK(B):
    K = []
    for b in B[1:]:
        Bwithoutb = [x for x in Bcopy if x.name != b.name]
        res = GN1H.returnPlan(deepcopy(Bcopy), Bwithoutb)
        if len(res) == 0:
            K.append({b.name})
    return K


def checkHittingSet(currentSet, K):
    hit = True
    for deadlock in K:
        if(len(currentSet.intersection(deadlock)) == 0):
            hit = False
            break
    if hit == True:
        return True
    return False


def generateMinimalHittingSet(blocks, K):
    blockList = list(blocks)
    for r in range(1, len(blockList) + 1):
        setList = list(combinations(blockList, r))
        for currentSet in setList:
            currentSet = set(currentSet)
            if checkHittingSet(currentSet, K):
                return currentSet


def generateH(K):
    blocks = set()
    for deadlock in K:
        for block in deadlock:
            blocks.add(block)
    return [Block(i) for i in generateMinimalHittingSet(blocks, K)]


def generateDeadlock(B, H, K):
    for b in B[1:]:
        Hcopy = [deepcopy(x) for x in H]
        Hcopy.append(b)
        res = GN1H.returnPlan(deepcopy(Bcopy), list(Hcopy))
        if len(res) == 0:
            H.append(b)

    D = []
    for c in B[1:]:
        if c not in H:
            D.append(c.name)
    K.append(set(D))

    return


def PERFECT(B):
    global Bcopy
    Bcopy = deepcopy(B)
    K = initialiseK(B)
    if len(K) == 0:
        return GN1H.returnPlan(deepcopy(Bcopy), deepcopy(Bcopy))
    while True:
        H = generateH(K)
        print(K)
        print([x.name for x in H])
        plan = GN1H.returnPlan(deepcopy(Bcopy), list(H))  # testing H
        if len(plan) > 0:
            return plan
        else:
            generateDeadlock(B, H, K)


def main():
    B = read(sys.argv[1])
    plan = PERFECT(B)
    printMoves(plan)
    B = read(sys.argv[1])
    printSolution(B[1:], plan)


if __name__ == "__main__":
    main()