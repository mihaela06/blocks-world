from math import floor
import time
import random 
from os import sys
import copy

SZ = 1000
SZZ = int((((SZ+2)*(SZ+2)+3)/4))

def allocate(array, size, initVal):
    for i in range(size):
        array.append(copy.deepcopy(initVal))

class TOWER:
    def __init__(self):
        self.top = 0.0
        self.bottom = 0.0


class STATE:
    def __init__(self):
        self.N = 0
        self.S = []
        self.rooted = []
        self.floating = []
        self.nrt = 0
        self.nft = 0
    
    def allocate(self):
        allocate(self.S, self.N, 0)
        allocate(self.rooted, self.N, TOWER())
        allocate(self.floating, self.N, TOWER())

sigma = STATE()
sigma.N = 0
S = 1
seed = 0

def getOptions():
    global sigma
    global S
    global seed
    global SZ
    global SZZ
    if len(sys.argv) < 5:
        print("Incorrect number of parameters")
        sys.exit()

    if sys.argv[1] == '-n':
        sigma.N = int(sys.argv[2], 10)
        SZ = sigma.N
        SZZ = int((((SZ+2)*(SZ+2)+3)/4))
    if sys.argv[3] == '-r':
        S = int(sys.argv[4])
    if len(sys.argv) > 5:
        if sys.argv[5] == '-s':
            seed = int(sys.argv[6])


def pos(N, x, y):
    return int(((x*(N+2-x)) + y))

def makeRatio(N, ratio):
    temp = []
    allocate(temp, SZ + 1, 0)
    
    for k in range(0,N + 1):
        temp[k] = 1.0
    for n in range(0,N + 1):
        for k in range(0,N-n+1):
            if n == 0:
                ratio[pos(N, n, k)] = 1.0
            else:
                temp[k] = (temp[k] * (temp[k+1]+n+k)) / (temp[k]+n+k-1.0)
                if (n % 2) == 0:
                    ratio[pos(N, n/2, k)] = temp[k]

def Ratio(ratio, N, x, y):
    z = pos(N,x/2,y)
    if x % 2:
         return (ratio[z+1]+x+y) / (((1/ratio[z])*(x+y-1))+1)
    else:
         return ratio[z]

def makeState(sigma, ratio):
    for x in range(0, sigma.N):
        sigma.rooted[x].top = sigma.rooted[x].bottom = -1
        sigma.floating[x].top = sigma.floating[x].bottom = x
        sigma.S[x] = -1
    sigma.nrt = 0
    sigma.nft = sigma.N

    while sigma.nft:
        sigma.nft = sigma.nft - 1
        r = random.random()
        choice = sigma.nft + sigma.nrt
        rat = Ratio(ratio,sigma.N,sigma.nft,sigma.nrt)
        p = rat / (rat + choice)

        if r <= p:
            sigma.rooted[sigma.nrt].top = sigma.floating[sigma.nft].top
            sigma.rooted[sigma.nrt].bottom = sigma.floating[sigma.nft].bottom
            sigma.nrt = sigma.nrt + 1
        else:
            b = floor((r-p) / ((1.0 - p) / choice))
            if b < sigma.nrt:
                sigma.S[sigma.floating[sigma.nft].bottom] = sigma.rooted[b].top
                sigma.rooted[b].top = sigma.floating[sigma.nft].top
            else:
                b = b - sigma.nrt
                sigma.S[sigma.floating[sigma.nft].bottom] = sigma.floating[b].top
                sigma.floating[b].top = sigma.floating[sigma.nft].top

def getStringState(state):
    st = ""
    for block in state:
        st += str(block) + " "
    return st

def printState(state):
    print(sigma.N)
    printableState = ""

    for i in range(0,sigma.N):
        printableState += str(sigma.S[i] + 1) + " "
    print(printableState)

def generateStates(nblocks, nstates):
    global sigma
    global SZ
    global SZZ
    global S

    states = []
    seed = time.time()
    ratio = []
    sigma.N = nblocks
    SZ = nblocks
    SZZ = int((((SZ+2)*(SZ+2)+3)/4))
    allocate(ratio, SZZ, 0)
    S = nstates
    sigma.allocate()
    random.seed(seed)

    makeRatio(sigma.N, ratio)
    while (S):
        state = []
        makeState(sigma, ratio)
        for i in range(sigma.N):
            state.append(sigma.S[i] + 1)
        states.append(state)
        S = S-1
    return states

def main():
    global seed
    global S
    global sigma
    seed = time.time()
    getOptions()
    ratio = []
    allocate(ratio, SZZ, 0)
    sigma.allocate()
    random.seed(seed)
    makeRatio(sigma.N, ratio)

    while (S):
        S = S - 1
        makeState(sigma, ratio)
        printState(sigma)

if __name__=="__main__":
    main()