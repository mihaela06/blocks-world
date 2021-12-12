from bwstates import generateStates

def createStatesFile(filename, nrStates, N):
    file = open(filename, "wt")
    states = generateStates(N, nrStates)
    for state in states:
        for i in state:
            file.write(str(i) + " ")
        file.write("\n")

def generateFiles():
    path = "States\\"

    for i in range(4, 50 + 1):
        fpath = path + str(i) + ".txt"
        createStatesFile(fpath, 20, i)

def main():
    generateFiles()
    return

if __name__=="__main__":
    main()