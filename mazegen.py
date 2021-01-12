import random

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Stack():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        node = self.frontier[-1]
        self.frontier.remove(node)
        return node

    def extend(self, nodes):
        self.frontier.extend(nodes)

    def empty(self):
        return len(self.frontier) == 0

class Maze():
    def __init__(self, height, width, root="top-left", random=True):
        if height < 3 or width < 3:
            raise Exception("Maze too small")
        self.height = round((height + 1) / 2)
        self.width = round((width + 1) / 2)
        self.maze = {}
        self.random = random
        start = [0, 0]
        if root == "top-right":
            start[1] = self.width - 1
        elif root == "bottom-left":
            start[0] = self.height - 1
        elif root == "bottom-right":
            start[0] = self.height - 1
            start[1] = self.width - 1
        elif root == "middle":
            start[0] = int(self.height / 2)
            start[1] = int(self.width / 2)
        self.start = start
        self.DFS = 0
        self.HUNTKILL = 1
        
    def __get_neighbors(self, node, get_unvisited=True, opposite_action=False):
        def is_valid(self, node):
            row, col = node
            return row >= 0 and row < self.height and col >= 0 and col < self.width

        row, col = node.state
        neighbors = [
            ("down" if opposite_action else "up",(row - 1, col)),
            ("up "if opposite_action else "down",(row + 1, col)),
            ("right" if opposite_action else "left",(row, col - 1)),
            ("left" if opposite_action else "right",(row, col + 1))
        ]
        if get_unvisited:
            return [Node(state=n, parent=node, action=action) for action, n in neighbors if is_valid(self, n) and not [i for i in self.maze.keys() if i.state == n]]
        return [Node(state=n, parent=node, action=action) for action, n in neighbors if is_valid(self, n) and [i for i in self.maze.keys() if i.state == n]]

    def generate(self, method):
        if method == self.DFS:
            self.__generateDFS_HUNT(HUNT=False)
        elif method == self.HUNTKILL:
            self.__generateDFS_HUNT(HUNT=True)
        else:
            raise Exception("Wrong Method")
        self.method = method
        self.longest_path = max(l for l in self.maze.values())
        print(f"Furthest away cell from root is {self.longest_path} cells away")
    
    def __generateDFS_HUNT(self, HUNT):
        visited = Stack()
        visited.add(Node(state=(self.start[0], self.start[1]), parent=None, action=None))
        hunt_row = 0
        while not visited.empty():
            node = visited.remove()
            if [n for n in self.maze.keys() if n.state == node.state]:
                continue
            self.maze[node] = self.get_path_length(node)
            neighbors = self.__get_neighbors(node)
            if neighbors:
                if self.random:
                    random.shuffle(neighbors)
                visited.extend(neighbors)
            elif HUNT:
                for row, col in self.get_all_coords(start_row=hunt_row):
                    if not (row, col) in [n.state for n in self.maze.keys()]:
                        neighs = self.__get_neighbors(Node(state=(row, col), parent=None, action=None), get_unvisited=False, opposite_action=True)
                        if neighs:
                            visited.add(Node(state=(row, col), parent=[n for n in self.maze.keys() if n.state == neighs[len(neighs) - 1].state][0], action=neighs[len(neighs) - 1].action))
                            hunt_row = row
                            break             

    def get_path_length(self, node):
        count = 0
        while node.parent:
            count += 1
            node = node.parent
        return count

    def get_all_coords(self, start_row=0):
        coords = []
        for i in range(start_row, self.height - 1):
            for j in range(self.width - 1):
                coords.append((i, j))
        return coords