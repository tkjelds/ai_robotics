from collections import deque
q = deque()

bounds_x = 4
bounds_y = 4
goalStates = [[0,3],[3,0]]
exploredStates = []


def printState(state):
    worldMap = [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]
    for can in state.cans:
        worldMap[can[0]][can[1]] = "C"
    for goal in goalStates:
        worldMap[goal[0]][goal[1]] = "G"
    worldMap[state.position[0]][state.position[1]] = printDirection(state.direction)
    for row in worldMap:
        print(row)
    print("\n")

class State:
    def __init__(self, position, direction, cans):
        self.position = position
        self.direction = direction
        self.cans = cans
        
class Directions:
    NORTH = [-1,0]
    SOUTH = [1,0]
    EAST = [0,1]
    WEST = [0,-1]
    
def printDirection(direction):
    if direction == Directions.NORTH:
        return "^"
    elif direction == Directions.SOUTH:
        return "v"
    elif direction == Directions.EAST:
        return ">"
    elif direction == Directions.WEST:
        return "<"
    

def turnLeft(direction):
    if direction == Directions.NORTH:
        return Directions.WEST
    elif direction == Directions.WEST:
        return Directions.SOUTH
    elif direction == Directions.SOUTH:
        return Directions.EAST
    elif direction == Directions.EAST:
        return Directions.NORTH
        
def turnRight(direction):
    if direction == Directions.NORTH:
        return Directions.EAST
    elif direction == Directions.EAST:
        return Directions.SOUTH
    elif direction    == Directions.SOUTH:
        return Directions.WEST
    elif direction == Directions.WEST:
        return Directions.NORTH
    
class Actions:
    FORWARD = 0
    LEFT = 1
    RIGHT = 2
    PUSH = 3
    
class Node: 
    def __init__(self, state, parent, action, children = []):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = children
        
def actionPrint(action):
    if action == Actions.FORWARD:
        return "FORWARD"
    elif action == Actions.LEFT:
        return "LEFT"
    elif action == Actions.RIGHT:
        return "RIGHT"
    elif action == Actions.PUSH:
        return "PUSH"
        
def isGoalState(state):
    return state.cans == goalStates

def returnPath(node):
    path = []
    while node.parent != None:
        path.append(actionPrint(node.action))
        node = node.parent
    return path[::-1]

def isOutOfBounds(position):
    return position[0] < 0 or position[0] >= bounds_x or position[1] < 0 or position[1] >= bounds_y

def expand(node):
    newNodes = []
    for action in [Actions.FORWARD, Actions.LEFT, Actions.RIGHT]:
        newState = apply(node.state, action)
        if newState != None:
            if node.state.cans != newState.cans: # If the can position has changed, the robot has pushed a can
                action = Actions.PUSH
            newNode = Node(newState, node, action)
            newNodes.append(newNode)
            q.append(newNode)
        node.children = newNodes
    return newNodes

def explored(state):
    for exploredState in exploredStates:
        if state.position == exploredState.position and state.direction == exploredState.direction and state.cans == exploredState.cans:
            return True
    return False

def printSolution(node):
    currentNode = node
    while currentNode.parent != None:
        printState(currentNode.state)
        currentNode = currentNode.parent

def getSolution(node):
    solution = []
    currentNode = node
    while currentNode.parent != None:
        solution.append(currentNode.action)
        currentNode = currentNode.parent
    return solution[::-1]
        
# Takes a state and an action, returns the new state if the action is valid, else returns None
def apply(state, action):
    newPosition = [state.position[0] + state.direction[0], state.position[1] + state.direction[1]]
    if action == Actions.FORWARD:
        for can in state.cans:
            if can == newPosition: # If there is a can in front of the robot, try to push it
                newCans = state.cans.copy()
                newCans.remove(can)
                newCan = [can[0] + state.direction[0], can[1] + state.direction[1]] # Update can position 
                if not isOutOfBounds(newCan) and newCan not in state.cans: # Don't push can out of bounds or into another can
                    newCans.append(newCan)
                    newState = State(newPosition, state.direction, newCans)
                    if explored(newState):
                        return None
                    else:
                        exploredStates.append(newState)
                        return newState
                else: 
                    return None

        if isOutOfBounds(newPosition): # Don't return state to move out of bounds
            return None
        else: # Move forward without pushing a can
            newState = State(newPosition, state.direction, state.cans)
            if explored(newState):
                return None
            else:            
                exploredStates.append(newState)
                return newState
    elif action == Actions.LEFT:
        newState = State(state.position, turnLeft(state.direction), state.cans)
        if explored(newState):
            return None
        else:            
            exploredStates.append(newState)
            return newState
    elif action == Actions.RIGHT:
        newState = State(state.position, turnRight(state.direction), state.cans)
        if explored(newState):
            return None
        else:            
            exploredStates.append(newState)
            return newState
        
InitialNode = Node(State([0,0], Directions.NORTH, [[3,1],[0,1]]), None, None)
q.append(InitialNode)

while q:
    node = q.popleft()
    if isGoalState(node.state):
        printSolution(node)
        print("Goal state found!")
        print("Path to goal: ", returnPath(node))
        print("Explored states: ", len(exploredStates))
        break
    expand(node)
    
print("No solution found. Explored states: ", len(exploredStates))