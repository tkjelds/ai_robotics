bounds_y = 4
bounds_x = 4
goalStates = [[0,1],[1,0]]
exploredStates = []

class state:
    def __init__(self, position, direction, cans):
        self.position = position
        self.direction = direction
        self.cans = cans
        

class Directions:
    NORTH = [1,0]
    SOUTH = [0,-1]
    EAST = [0,1]
    WEST = [-1,0]
    
class Actions:
    FORWARD = 0
    LEFT = 1
    RIGHT = 2
    
    
class Node: 
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


def isGoalState(state):
    return state.cans == goalStates

def returnPath(node):
    path = []
    while node.parent != None:
        path.append(node.action)
        node = node.parent
    return path[::-1]

def isOutOfBounds(position):
    return position[0] < 0 or position[0] >= bounds_x-1 or position[1] < 0 or position[1] >= bounds_y-1

def isInfront(position_1, position_2, direction):
    return position_1[0] + direction[0] == position_2[0] and position_1[1] + direction[1] == position_2[1]

def expand(node):
    newNodes = []
    for action in [Actions.FORWARD, Actions.LEFT, Actions.RIGHT]:
        newState = apply(node.state, action)
        if newState != None:
            newNodes.append(Node(newState, node, action))
    return newNodes

def apply(state, action):
    newPosition = [state.position[0] + state.direction[0], state.position[1] + state.direction[1]]
    if action == Actions.FORWARD:
        for can in state.cans:
            if isInfront(state.position, can, state.direction):
                newCans = state.cans.copy()
                newCans.remove(can)
                newCan = [can[0] + state.direction[0], can[1] + state.direction[1]]
                if not isOutOfBounds(newCan):
                    newCans.append(newCan)
                    return state(newPosition, state.direction, newCans)
                else: 
                    return None

        if isOutOfBounds(newPosition):
            return None
        else:
            return state(newPosition, state.direction, state.cans)
    elif action == Actions.LEFT:
        # TODO
    elif action == Actions.RIGHT:
        # TODO
        
InitialNode = Node(state([0,0], Directions.NORTH, [[0,1],[1,0]]), None, None)
while True: