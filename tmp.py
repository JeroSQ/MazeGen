explored = set()
row_sets = dict()
for row in range(self.orig_height):
    cells = [i for j in row_sets.values() for i in j if i[0] == row]
    cells.sort(key=lambda x:x[0])
    for cell in range(self.width):
        # If cell isn't in a set
        if (row, cell) not in cells:
            new_set = max(i for i in row_sets.keys()) + 1 if row_sets else cell
            row_sets[new_set] = []
            row_sets[new_set].append((row, cell))
            explored.add((row, cell))
            # self.maze[Node(state=(row, cell), parent=None, action=None)] = new_set * 5
        
    # Union sets
    cells = [i for j in row_sets.values() for i in j if i[0] == row]
    cells.sort(key=lambda x:x[0])
    for i, cell in enumerate(cells):
        if i == len(cells) - 1:
            continue

        s1 = [s for s in row_sets.keys() if row_sets[s] != 0 and cell in row_sets[s]][0]
        s2 = [s for s in row_sets.keys() if row_sets[s] != 0 and cells[i + 1] in row_sets[s]][0]
        if random.random() < 0.5 or s1 == s2:
            continue
        else:
            row_sets[s1].extend(row_sets[s2])
            row_sets[s2] = 0
            #   self.maze[Node(state=cells[i+1], parent=None, action="right")] = s1*5
    
    # Modify dict
    for key in list(row_sets.keys()):
        if not row_sets[key]:
            row_sets.pop(key)

    # Draw cells
    print(row_sets)
    for s in row_sets.keys():
        for i, cell in enumerate(row_sets[s]):
            if cell not in explored:
                explored.add(cell)
                # self.maze[Node(state=cell, parent=None, action="right" if not i == 0 else None)] = s*5

    # Add bottom cells
    for s in list(row_sets.keys()):

        # At least one down-passage per set
        to_choose = [i for i in row_sets[s] if i[0] == row and (i[0]+1, i[1]) not in [i.state for i in self.maze.keys()]]
        r_cell = random.choice(to_choose)
        to_choose.remove(r_cell)
        row_sets[s].append((r_cell[0] + 1, r_cell[1]))
        explored.add((r_cell[0] + 1, r_cell[1]))
        #self.maze[Node(state=(r_cell[0] + 1, r_cell[1]), parent=None, action="down")] = s*5

        # Other random down-passages
        for c in to_choose:
            if random.random() < 0.5 and (c[0] + 1, c[1]) not in [i.state for i in self.maze.keys()]:
                row_sets[s].append((c[0] + 1, c[1]))
                explored.add((c[0] + 1, c[1]))
                # self.maze[Node(state=row_sets[s][-1], parent=None, action="down")] = s*5
                row_sets[s] = list(OrderedDict.fromkeys(row_sets[s]))

for s in row_sets.keys():
    for c in row_sets[s]:
        self.maze[Node(c,None,None)] = s*5

for n, l in self.maze.items():
    print(n.state, n.action, l)

#   print(row_sets)