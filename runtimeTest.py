import time
from bwstates import generateStates
from os import sys
import os
from US import US
from GN1 import GN1
from GN2 import GN2
from Utils import parse
import csv
import matplotlib.pyplot as plt
import pandas as pd
from BFS import BFS
from DFS import DFS
from BEST import BEST
from ASTAR import ASTAR
from PERFECT import PERFECT

def getFiles():
    files = os.listdir('.\\States')
    return files

def readStates(nstates, file):
    path = "States\\" + file
    readed = open(path, "rt").read()
    statesList = readed.split('\n')
    stateInitialList = []
    stateGoalList = []
    for i in range(0, nstates - 1, 2):
        stateInitialList.append(statesList[i].split())
        stateGoalList.append(statesList[i+1].split())
    return stateInitialList, stateGoalList

def runOnceUS(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = US(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'US' , "Plan length" : len(plan)})

def runOnceGN1(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = GN1(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'GN1', "Plan length" : len(plan)})

def runOnceGN2(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = GN2(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'GN2', "Plan length" : len(plan)})

def runOnceBFS(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = BFS(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'BFS', "Plan length" : len(plan)})

def runOnceDFS(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = DFS(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'DFS', "Plan length" : len(plan)})

def runOnceBEST(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = BEST(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'BEST', "Plan length" : len(plan)})

def runOnceASTAR(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = ASTAR(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'ASTAR', "Plan length" : len(plan)})

def runOncePERFECT(writer, initialState, goalState):
    B = parse(initialState, goalState)
    start = time.time()
    plan = PERFECT(B)
    end = time.time()
    writer.writerow({'Number of blocks': str(len(initialState)), 'Time': str(((end-start) * 1000.0)), "Algorithm": 'PERFECT', "Plan length" : len(plan)})


def runtimeTestUS(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        runOnceUS(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestGN1(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        runOnceGN1(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestGN2(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        runOnceGN2(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestBFS(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        if (len(stateInitialList[i]) < 10):
            runOnceBFS(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestDFS(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        if (len(stateInitialList[i]) < 7):
            runOnceDFS(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestBEST(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        runOnceBEST(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestASTAR(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        runOnceASTAR(writer, stateInitialList[i], stateGoalList[i])

def runtimeTestPERFECT(writer, file):
    nstates = 20
    sys.setrecursionlimit(10000)
    stateInitialList, stateGoalList = readStates(nstates, file)
    for i in range(len(stateInitialList)):
        runOncePERFECT(writer, stateInitialList[i], stateGoalList[i])

def getNumberBlocks(files):
    nblocks = []
    for file in files:
        nblocks.append(int(file.replace('.txt', ''), 10))
    return nblocks

def getAverage(alg, nblocks, dataframe, column):
    list = []
    for blocks in nblocks:
        if alg == "BFS" and blocks < 8:
            list.append(dataframe.loc[dataframe[column] == blocks].mean())
        if alg == "DFS" and blocks < 8:
            list.append(dataframe.loc[dataframe[column] == blocks].mean())
        elif alg != 'BFS' and alg != 'DFS':
            list.append(dataframe.loc[dataframe[column] == blocks].mean())
    return list

def createUSTimegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('US', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    print(sorted)
    plt.plot(x, y, 'r', label="US")
    plt.legend()

def createGN1Timegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('GN1', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    plt.plot(x, y, 'g', label="GN1")
    plt.legend()

def createGN2Timegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('GN2', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    plt.plot(x, y, 'y', label="GN2")
    plt.legend()

def createBFSTimegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('BFS', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    plt.plot(x, y, 'b', label="BFS")
    plt.legend()

def createDFSTimegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('DFS', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    plt.plot(x, y, 'c', label="DFS")
    plt.legend()

def createBESTTimegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('BEST', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    plt.plot(x, y, 'c', label="BEST")
    plt.legend()

def createASTARTimegraph(filename, nblocks):
    data = pd.read_csv(filename)
    avg = getAverage('ASTAR', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Time']
    plt.plot(x, y, 'c', label="ASTAR")
    plt.legend()

def generateUScsv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('us.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestUS(writer, file)

def generateGN1csv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('gn1.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestGN1(writer, file)

def generateGN2csv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('gn2.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestGN2(writer, file)

def generateBFScsv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('bfs.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestBFS(writer, file)

def generateDFScsv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('dfs.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestDFS(writer, file)

def generateBESTcsv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('best.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestBEST(writer, file)

def generateASTARcsv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('astar.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestASTAR(writer, file)

def generatePERFECTcsv():
    files = getFiles()
    nblocks = getNumberBlocks(files)
    with open('perfect.csv', "w") as csvfile:
        fieldnames = ['Number of blocks', 'Time', 'Algorithm', 'Plan length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in files:
            runtimeTestPERFECT(writer, file)

def createTimeGraphs():
    createUSTimegraph('us.csv', getNumberBlocks(getFiles()))
    createGN1Timegraph('gn1.csv', getNumberBlocks(getFiles()))
    createGN2Timegraph('gn2.csv', getNumberBlocks(getFiles()))
    createBFSTimegraph('bfs.csv', getNumberBlocks(getFiles()))
    createDFSTimegraph('dfs.csv', getNumberBlocks(getFiles()))
    plt.show()


def createUSplangraph(nblocks):
    data = pd.read_csv('us.csv')
    avg = getAverage('US', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Plan length']
    plt.plot(x, y, 'c', label="US")
    plt.legend()

def createGN1plangraph(nblocks):
    data = pd.read_csv('gn1.csv')
    avg = getAverage('GN1', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Plan length']
    plt.plot(x, y, 'r', label="GN1")
    plt.legend()

def createGN2plangraph(nblocks):
    data = pd.read_csv('gn2.csv')
    print(data)
    avg = getAverage('GN2', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=False)
    print(sorted)
    x = sorted['Plan length']
    y = sorted['Number of blocks']
    plt.plot(x, y, 'g', label="GN2")
    plt.legend()

def createBFSplangraph(nblocks):
    data = pd.read_csv('bfs.csv')
    avg = getAverage('BFS', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Plan length']
    plt.plot(x, y, 'r', label="BFS")
    plt.legend()

def createDFSplangraph(nblocks):
    data = pd.read_csv('dfs.csv')
    avg = getAverage('DFS', nblocks, data, 'Number of blocks')
    averaged = pd.DataFrame(avg)
    sorted = averaged.sort_values(by='Number of blocks', ascending=True)
    x = sorted['Number of blocks']
    y = sorted['Plan length']
    plt.plot(x, y, 'r', label="DFS")
    plt.legend()

def createPlanGraph():
    createUSplangraph(getNumberBlocks(getFiles()))
    createGN1plangraph(getNumberBlocks(getFiles()))
    createGN2plangraph(getNumberBlocks(getFiles()))
    createBFSplangraph(getNumberBlocks(getFiles()))
    createDFSplangraph(getNumberBlocks(getFiles()))
    plt.show()

def main():
    generatePERFECTcsv()
   
    return


if __name__=="__main__":
    main()