import enum
from copy import deepcopy

"""
Class State taken from https://github.com/kouzapo/blocks-world
"""


class Node:
    def __init__(self):
        self.next = None
        self.previous = None


class Block(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Move:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class State:
    """
    The State class. Each State object represents a possible arrangement of the blocks on the table.

    Attributes:

        layout: 
        A dict structure with keys the names of the blocks and values a list with two items.
        The first item is the name of a block on which the block stands on. If the blocks is on the table,
        the '-' character represents this possibility. The second item is a character 
        indicating whether or not the block if free to move. 'c' for clear, 'u' for unclear.

            example:                                    |A|
            For a state with an arrangement like this:  |B|C|

            The layout attribute is {'A': ['B', 'c'], 'B': ['-', 'u'], 'C': ['-', 'c']}.

        The dictionary data structure in Python has constant access time complexity O(1).

        parent: 
        A State object indicating the parent of the current state. Basically, it is a pointer
        to another state object. The initial state has parent = None.

        move:
        A list with 3 items which represents the move from which the current state is created.
        The first item is the block that has benn moved. The second item is the block that
        has been released and the third item is the destination block.

            example:
            |A|           |A| 
            |B|C| ----> |B|C|   The move attribute is ['A', 'B', 'C']

        The inital state has move = [].

        distance:
        An integer indicating the distance from the root - inital state.
        Basically counts how many moves have been done to get to this state.
        The initial state has distance = 0.

        id:
        A string which is unique for each state. Each state hash an is which is constructed
        using the items of the layout attribute so two states have the same id if and only if
        they have the same items in their layout attributes. The id is used by the searching
        algorithms in order to check whether or not a state has been discoverd.

            example:                                      |A|
            For a state with an arrangement like this:  |B|C|
            and layout {'A': ['B', 'c'], 'B': ['-', 'u'], 'C': ['-', 'c']},
            the id is 'Bc-u-c'.
    """

    def __init__(self, layout, parent=None, move=[], distance=0):
        self.layout = layout
        self.parent = parent
        self.move = move
        self.distance = distance

        # A list of the names of the blocks.
        values = list(self.layout.values())

        # Create the id attribute.
        self.id = ''.join([str(i) for s in values for i in s])

    def __eq__(self, other_state):
        """
        Override the build-in __eq__ method. Two states are equal if and only if they have
        the same id.
        """
        if other_state != None:
            return self.id == other_state.id
        else:
            return False

    def calcChildren(self):
        """
        The method creates a list of all the states that can be produced from a given state.
        It moves all the clear blocks to all available destinations and creates a new state 
        for each alteration.

        example:                                      |A|
        For a state with an arrangement like this:  |B|C|
        the free blocks are |A| and |B|. The children that can be created are:

                        |B|
        |A|             |A|
        |B|C|, |A|B|C|, |C|.
        """
        layout = self.layout
        children = []

        # The blocks that can be moved.
        free_blocks = [key for key in layout if layout[key][1] == 'c']

        for moving_block in free_blocks:  # For each free block that will be moved...
            for target_block in free_blocks:
                if moving_block != target_block:
                    # Copy the current layout in order to alter it.
                    temp = deepcopy(layout)
                    move = []
                    distance = 0

                    # The 'released_block' is the first item of the list in layout with key == moving_block.
                    released_block = temp[moving_block][0]

                    # The 'moving block' now is on top of the 'target_block'.
                    temp[moving_block][0] = target_block
                    # And the 'target_block' is now unclear.
                    temp[target_block][1] = 'u'

                    # Add the 'moving_block' to 'move' list.
                    move.append(moving_block)

                    # If the 'released_block" is not '-' i.e. is not on the table...
                    if released_block != '-':
                        temp[released_block][1] = 'c'  # Set the block clear.

                        # Add the 'released_block' to 'move' list.
                        move.append(released_block)
                    else:
                        move.append('table')

                    # Add the 'target_block' to 'move' list.
                    move.append(target_block)
                    # The distance of the child is the distance of the parent plus 1.
                    distance = self.distance + 1

                    # Add to 'children' list a new State object.
                    children.append(
                        State(layout=temp, parent=self, move=move, distance=distance))

            # If the 'moving_block' is not currently on the table, create a state that it is.
            if layout[moving_block][0] != '-':
                temp = deepcopy(layout)
                move = []
                distance = 0

                # The 'released_block' is the first item of the list in layout with key == moving_block.
                released_block = temp[moving_block][0]

                temp[moving_block][0] = '-'
                temp[released_block][1] = 'c'  # Set the block clear.

                # Add the 'moving_block' to 'move' list.
                move.append(moving_block)
                # Add the 'released_block' to 'move' list.
                move.append(released_block)
                move.append('table')

                # The distance of the child is the distance of the parent plus 1.
                distance = self.distance + 1

                # Add to 'children' list a new State object.
                children.append(State(layout=temp, parent=self,
                                move=move, distance=distance))

        return children  # Return the children list.


class STATE(enum.Enum):
    READY = 1
    STUCK = 2
    OTHER = 3


class DLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def __repr__(self):
        string = ""

        if(self.head == None):
            string += "Empty"
            return string

        string += f"{self.head.name}"
        start = self.head.next
        while(start != None):
            string += f" -> {start.name}"
            start = start.next
        return string

    def append(self, node):
        if self.head is None:
            self.head = node
            self.tail = self.head
            self.count += 1
            return

        self.tail.next = node
        self.tail.next.previous = self.tail
        self.tail = self.tail.next
        self.count += 1

    def insert(self, node, index):
        if (index > self.count) | (index < 0):
            raise ValueError(
                f"Index out of range: {index}, size: {self.count}")

        if(index == self.count):
            self.append(node)
            return

        if(index == 0):
            self.head.previous = node
            self.head.previous.next = self.head
            self.head = self.head.previous
            self.count += 1
            return

        start = self.head
        for _ in range(index):
            start = start.next
        start.previous.next = node
        start.previous.next.previous = start.previous
        start.previous.next.next = start
        start.previous = start.previous.next
        self.count += 1
        return

    def removeAtIndex(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(
                f"Index out of range: {index}, size: {self.count}")

        if index == 0:
            self.head = self.head.next
            self.head.previous = None
            self.count -= 1
            return

        if index == (self.count - 1):
            self.tail = self.tail.previous
            self.tail.next = None
            self.count -= 1
            return

        start = self.head
        for i in range(index):
            start = start.next
        start.previous.next, start.next.previous = start.next, start.previous
        self.count -= 1

        return

    def remove(self, node):
        if self.count == 0:
            raise ValueError("Empty list, can't remove")

        if self.count == 1:
            self.head = None
            self.tail = None
            self.count = 0
            return

        nextNode, prevNode = node.next, node.previous

        if node == self.head:
            self.head = nextNode
            nextNode.previous = None
        else:
            prevNode.next = nextNode

        if node == self.tail:
            self.tail = prevNode
            prevNode.next = None
        else:
            nextNode.previous = prevNode
        self.count -= 1
        node.next = None
        node.prev = None
        return

    def index(self, node):
        start = self.head
        for i in range(self.count):
            if(start == node):
                return i
            start = start.next
        return None

    def size(self):
        return self.count

    def display(self):
        if self.head is None:
            print("The list is empty")
            return
        else:
            n = self.head
            while n is not None:
                print(n.name)
                n = n.next
        print("\n")

    def getNodeByName(self, name):
        n = self.head
        while n is not None:
            if n.name == name:
                return n
            n = n.next
        return n

    def empty(self):
        return self.size() == 0

    def __eq__(self, other):
        n1 = self.head
        while n1 is not None:
            if not other.getNodeByName(n1.name):
                return False
            n1 = n1.next
        n1 = other.head
        while n1 is not None:
            if not self.getNodeByName(n1.name):
                return False
            n1 = n1.next
        return True


def parse(blockBelowListInit, blockBelowListGoal):
    B = [Block(0)]
    TABLE = B[0]
    for block in range(1, len(blockBelowListInit) + 1):
        B.append(Block(block))
    for block in range(1, len(blockBelowListInit) + 1):
        index = int(blockBelowListInit[block - 1])
        if index == 0:
            B[block].currentlyBelow = TABLE
        else:
            B[block].currentlyBelow = B[int(blockBelowListInit[block - 1])]
    for block in range(1, len(blockBelowListGoal) + 1):
        index = int(blockBelowListGoal[block - 1])
        if index == 0:
            B[block].goalBelow = TABLE
        else:
            B[block].goalBelow = B[int(blockBelowListGoal[block - 1])]
    return B


def read(infile):
    statesList = open(infile, "rt").read().split("\n")
    blockBelowListInit = statesList[0].split()
    blockBelowListGoal = statesList[1].split()
    return parse(blockBelowListInit, blockBelowListGoal)


def printMoves(plan):
    for move in plan:
        print("{" + str(move.a.name) + "} -> {" + str(move.b.name) + "}")
    print(len(plan))
    print()


def BtoStacks(B):
    stacks = []
    added = []
    while len(added) < len(B):
        for b in B:
            if b.name not in added:
                if b.currentlyBelow.name == 0:
                    stacks.append([b.name])
                    added.append(b.name)
                else:
                    for s in stacks:
                        if s[-1] == b.currentlyBelow.name:
                            s.append(b.name)
                            added.append(b.name)
    return stacks


def BtoStacksGoal(B):
    stacks = []
    added = []
    while len(added) < len(B):
        for b in B:
            if b.name not in added:
                if b.goalBelow.name == 0:
                    stacks.append([b.name])
                    added.append(b.name)
                else:
                    for s in stacks:
                        if s[-1] == b.goalBelow.name:
                            s.append(b.name)
                            added.append(b.name)
    return stacks


def printState(B):
    noDigitsMax = len(str(B[-1].name))
    stacks = BtoStacks(B)
    heightMax = 0
    formatStr = "{0: >" + str(noDigitsMax) + "}"
    for stack in stacks:
        if len(stack) > heightMax:
            heightMax = len(stack)
    for i in range(heightMax - 1, -1, -1):
        for s in stacks:
            if len(s) <= i:
                print(" " * noDigitsMax, end=" ")
            else:
                print(formatStr.format(str(s[i])), end=" ")
        print()
    print()


def printSolution(B, plan):
    # Initial configuration
    printState(B)
    for move in plan:
        B[move.a.name - 1].currentlyBelow = move.b
        printState(B)


def generateStatesFromB(B):
    noBlocks = len(B) - 1
    blocks_names = [i + 1 for i in range(noBlocks)]

    # Construct the inital layout.
    initial_layout = {key: ['-', 'c'] for key in blocks_names}
    # Construct the goal layout.
    goal_layout = {key: ['-', 'c'] for key in blocks_names}

    for block in B[1:]:
        if block.currentlyBelow.name != 0:
            initial_layout[block.name][0] = block.currentlyBelow.name
        for b in B[1:]:
            if b.currentlyBelow.name == block.name:
                initial_layout[block.name][1] = 'u'
                break

    for block in B[1:]:
        if block.goalBelow.name != 0:
            goal_layout[block.name][0] = block.goalBelow.name
        for b in B[1:]:
            if b.goalBelow.name == block.name:
                goal_layout[block.name][1] = 'u'
                break

    # Return two state objects.
    return State(layout=initial_layout), State(layout=goal_layout)


def planFromSolution(solution):
    # The state we start, which is the last i.e. the solution.
    current_state = solution
    path = []  # The path from the solution towards the intial state.
    i = 1
    plan = []
    while True:
        # Add the current state i.e. solution, in the list.
        path.append(current_state)

        # The current state now becomes the parent of it.
        current_state = current_state.parent

        if current_state.parent == None:  # If the current state has no parent...
            path.append(current_state)  # Add the current state in the list.
            break

    path.reverse()  # Reverse the list.

    for state in path[1:]:
        move = state.move  # Get the move.
        a = Block(int(move[0]))
        b = Block(0)
        if move[2] != "table":
            b = Block(int(move[2]))
        plan.append(Move(a, b))
        i += 1  # Increment the counter.

    return plan
