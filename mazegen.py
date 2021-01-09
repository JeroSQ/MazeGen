import copy
import random
import time
from PIL import Image, ImageDraw, ImageFile
import glob

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
        self.maze = []
        self.order = {}
        self.random= random
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
        for row in range(self.height):
            self.maze.append([])
            for col in range(self.width):
                self.maze[row].append(False)
        self.maze_export = []
        for row in range((self.height * 2) - 1):
            self.maze_export.append([])
            for col in range((self.width * 2) - 1):
                self.maze_export[row].append(False)
        
    def __get_unvisited_neighbors(self, coords, node):
        def is_valid(self, coords):
            row, col = coords
            return row >= 0 and row < self.height and col >= 0 and col < self.width

        row, col = coords
        neighbors = [
            ("up",(row - 1, col)),
            ("down",(row + 1, col)),
            ("left",(row, col - 1)),
            ("right",(row, col + 1))
        ]
        return [Node(state=n, parent=node, action=action) for action, n in neighbors if is_valid(self, n) and not self.maze[n[0]][n[1]]]

    def __draw_cell(self, node):
        row, col = node.state
        export_coords = [row * 2, col * 2]
        action = node.action
        if action == "up":
            export_coords[0] = row * 2 + 1
        elif action == "down":
            export_coords[0] = row * 2 - 1
        elif action == "right":
            export_coords[1] = col * 2 - 1
        elif action == "left":
            export_coords[1] = col * 2 + 1

        path_length = self.get_path_length(node)
       
        self.maze_export[row * 2][col * 2] = True
        self.maze_export[export_coords[0]][export_coords[1]] = True

        self.order[(export_coords[0], export_coords[1])] = path_length - 1
        self.order[(row * 2, col * 2)] = path_length

    def generate(self):
        visited = Stack()
        visited.add(Node(state=(self.start[0], self.start[1]), parent=None, action=None))
        self.count = 0
        while not visited.empty():
            node = visited.remove()
            coords = node.state
            if self.maze[coords[0]][coords[1]]:
                continue
            self.maze[coords[0]][coords[1]] = True
            self.count += 1
            #print(self.count)
            neighbors = self.__get_unvisited_neighbors(coords, node)
            self.__draw_cell(node)
            if neighbors:
                if self.random:
                    r = random.choice(neighbors)
                    copy_n = [n for n in neighbors]
                    copy_n.remove(r)
                    visited.extend(copy_n)
                    visited.add(r)
                else:
                    visited.extend(neighbors)

    def get_path_length(self, node):
        count = 0
        while node.parent:
            count += 1
            node = node.parent
        return count
                       
