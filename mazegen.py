import random
from collections import OrderedDict

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
        return self.frontier.pop(-1)

    def extend(self, nodes):
        self.frontier.extend(nodes)

    def empty(self):
        return len(self.frontier) == 0

class Maze():
    
    DFS = 0
    HUNTKILL = 1
    ELLERS = 2
    PRIMS = 3

    def __init__(self, height, width, root="top-left", random=True):
      #  if height < 3 or width < 3:
       #     raise Exception("Maze too small")
        self.orig_height = height
        self.orig_width = width
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
        elif method == self.ELLERS:
            self.__generateELLERS()
        elif method == self.PRIMS:
            self.__generatePRIMS()
        else:
            raise Exception("Wrong Method")
        self.method = method
        self.longest_path = max(l for l in self.maze.values())
        if method != self.ELLERS:
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

    def __generateELLERS(self):
        row_sets = dict()
        for row in range(self.height):
            new = []
            cells = [i for j in row_sets.values() for i in j if i[0] == row]
            cells.sort(key=lambda x:x[0])
            for cell in range(self.width):
                # If cell isn't in a set
                if (row, cell) not in cells:
                    new_set = max(i for i in row_sets.keys()) + 1 if row_sets else cell
                    row_sets[new_set] = []
                    row_sets[new_set].append((row, cell))
                    new.append((row, cell))
                    self.maze[Node(state=(row, cell), parent=None, action=None)] = row
                
            # Union sets
            cells = [i for j in row_sets.values() for i in j if i[0] == row]
            cells.sort(key=lambda x:x[0])
            for cell in cells:
                if cell[1]+1 == self.width:
                    continue

                s1 = [s for s in row_sets.keys() if row_sets[s] != 0 and cell in row_sets[s]][0]
                s2 = [s for s in row_sets.keys() if row_sets[s] != 0 and (cell[0], cell[1]+1) in row_sets[s]][0]
                if random.random() < 0.5 or s1 == s2:
                    continue
                else:
                    row_sets[s1].extend(row_sets[s2])
                    row_sets[s2] = 0
                    self.maze[Node(state=(cell[0], cell[1]+1), parent=None, action="right")] = row
            
            # Modify dict
            for key in list(row_sets.keys()):
                if not row_sets[key]:
                    row_sets.pop(key)

            if row == self.height - 1:
                continue

            # Add bottom cells
            for s in list(row_sets.keys()):

                # At least one down-passage per set
                to_choose = [i for i in row_sets[s] if i[0] == row and (i[0]+1, i[1]) not in [i.state for i in self.maze.keys()]]
                r_cell = random.choice(to_choose)
                to_choose.remove(r_cell)
                row_sets[s].append((r_cell[0] + 1, r_cell[1]))
                self.maze[Node(state=(r_cell[0] + 1, r_cell[1]), parent=None, action="down")] = row

                # Other random down-passages
                for c in to_choose:
                    if random.random() < 0.5 and (c[0] + 1, c[1]) not in [i.state for i in self.maze.keys()]:
                        row_sets[s].append((c[0] + 1, c[1]))
                        self.maze[Node(state=row_sets[s][-1], parent=None, action="down")] = row
                        row_sets[s] = list(OrderedDict.fromkeys(row_sets[s]))

            # Forget previous rows
            for s in row_sets.keys():
                for c in row_sets[s]:
                    if c[0] <= row - 1 and row != 0:
                        row_sets[s].remove(c)
        
        # All last-row cells must belong to the same set
        cells = [i for j in row_sets.values() for i in j if i[0] == self.height - 1]
        cells.sort(key=lambda x:x[0])
        for cell in cells:
            if cell[1]+1 == self.width:
                continue

            s1 = [s for s in row_sets.keys() if row_sets[s] != 0 and cell in row_sets[s]][0]
            s2 = [s for s in row_sets.keys() if row_sets[s] != 0 and (cell[0], cell[1]+1) in row_sets[s]][0]

            if s1 != s2:
                row_sets[s1].extend(row_sets[s2])
                row_sets[s2] = 0
                self.maze[Node(state=(cell[0], cell[1]+1), parent=None, action="right")] = self.height - 1

    def __generatePRIMS(self):
        start = (random.randrange(0, self.height), random.randrange(0, self.width))
        node = Node(state=start, parent=None, action=None)
        self.maze[node] = 0
        wall_list = self.__get_neighbors(node)
        while wall_list:
            wall = random.choice(wall_list)
            if not [j for j in self.maze.keys() if j.state == wall.state]:
                self.maze[wall] = self.get_path_length(wall)
                wall_list.extend(self.__get_neighbors(wall))
            wall_list.remove(wall)

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