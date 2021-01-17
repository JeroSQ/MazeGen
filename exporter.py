from PIL import Image, ImageDraw

def export_txt(maze):
    """Exports the maze passed as a .txt file where hashes(#) are the possible paths and whitespaces are walls"""
    height = maze.height * 2 - 1
    width = maze.width * 2 - 1 
    txt_maze = [
        [False for _ in range(width)]
        for _ in range(height)
    ]
    for node in maze.maze: 
        action_coords = get_action_coords(node)
        txt_maze[node.state[0]*2][node.state[1]*2] = True
        txt_maze[action_coords[0]][action_coords[1]] = True
    with open("maze.txt", "w") as f:
        for i in range(height):
            for j in range(width):
                if maze.method == maze.DIVISION:
                    f.write("#" if maze.grid[i][j] else " ")
                else:
                    f.write("#" if txt_maze[i][j] else " ")
            f.write("\n")

def export_png(maze, cell_size=5, cell_border=0, color=False):
    """Exports the maze passed as a .png file where white is the possible paths and black is the walls"""
    height = maze.height * 2 - 1 
    width = maze.width * 2 - 1 
    img = Image.new(
        "RGBA",
        (width * cell_size + 2, height  * cell_size + 2),
        "black"
    )
    draw = ImageDraw.Draw(img)

    if maze.method == maze.DIVISION:
        for i, row in enumerate(maze.grid):
            for j, _ in enumerate(row):
                if maze.grid[i][j]:
                    draw.rectangle(
                        [j * cell_size + cell_border+1, i * cell_size + cell_border+1, (j+1) * cell_size - cell_border, (i+1) * cell_size - cell_border],
                        fill="white")
    else:
        for node, lenpath in maze.maze.items():
            row, col = node.state
            a_row, a_col = get_action_coords(node)
            draw.rectangle(
                [a_col * cell_size + cell_border+1, a_row * cell_size + cell_border+1, (a_col+1) * cell_size - cell_border, (a_row+1) * cell_size - cell_border],
                fill=get_color(height, width, color, lenpath - 1 if lenpath > 0 else 0, maze))

            draw.rectangle(
                [col * 2 * cell_size + cell_border+1, row * 2 * cell_size + cell_border+1, (col*2+1) * cell_size - cell_border, (row*2+1) * cell_size - cell_border],
                fill=get_color(height, width, color, lenpath, maze))

    img.save("maze.png")

def export_gif(maze, cell_size=5, cell_border=0, duration=20, color=False):
    """Exports the maze passed as a .gif file showing the process of generating the maze"""
    height = maze.height * 2 - 1 
    width = maze.width * 2 - 1
    frames = []
    img = Image.new(
        "RGBA",
        (width * cell_size + 2, height * cell_size + 2),
        "black"
    )

    draw = ImageDraw.Draw(img)

    if maze.method == maze.DIVISION:
        record = {}
        for i in range(height):
            for j in range(width):
                draw.rectangle(
                [j * cell_size + cell_border+1, i * cell_size + cell_border+1, (j+1) * cell_size - cell_border, (i+1) * cell_size - cell_border],
                fill="white")
        for wall in maze.walls:
            row, col = wall
            record[wall] = False if wall not in record.keys() else not record[wall]
            draw.rectangle(
            [col * cell_size + cell_border+1, row * cell_size + cell_border+1, (col+1) * cell_size - cell_border, (row+1) * cell_size - cell_border],
            fill="white" if record[wall] else "black")
            frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))
    
    else: 
        count = 1
        for node, lenpath in maze.maze.items():
            row, col = node.state
            a_row, a_col = get_action_coords(node)
            draw.rectangle(
                [a_col * cell_size + cell_border+1, a_row * cell_size + cell_border+1, (a_col+1) * cell_size - cell_border, (a_row+1) * cell_size - cell_border],
                fill=get_color(height, width, color, lenpath, maze))
            if maze.method != maze.KRUSKALS:
                frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))

            draw.rectangle(
                [col * 2 * cell_size + cell_border+1, row * 2 * cell_size + cell_border+1, (col*2+1) * cell_size - cell_border, (row*2+1) * cell_size - cell_border],
                fill=get_color(height, width, color, lenpath, maze))
            if maze.method == maze.KRUSKALS:
                if count == 2:
                    frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))
                    count = 0
                count += 1
            else:
                frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))

    frames[0].save('maze.gif', save_all=True, append_images=frames[1:], duration=duration)

def get_color(height, width, color, path_length, maze):
    """Returns a color for each path_length value"""
    if not color:
        return "white"

    start_color = [0, 255, 255]

    start_color[1] -= int(path_length * 1530 / (maze.longest_path + min([height, width])))

    if start_color[1] < 0:
        start_color[0] += abs(start_color[1])
        start_color[1] = 0
    if start_color[0] > 255:
        start_color[2] -= start_color[0] - 255
        start_color[0] = 255
    if start_color[2] < 0:
        start_color[1] += abs(start_color[2])
        start_color[2] = 0
    if start_color[1] > 255:
        start_color[0] -= start_color[1] - 255
        start_color[1] = 255
    if start_color[0] < 0:
        start_color[0] = 0

    return tuple(start_color)
    
def get_action_coords(node):
    row, col = node.state
    action = node.action
    action_coords = [row*2, col*2]

    if action == "up":
        action_coords[0] = row*2 + 1
    elif action == "down":
        action_coords[0] = row*2 - 1
    elif action == "right":
        action_coords[1] = col*2 - 1
    elif action == "left":
        action_coords[1] = col*2 + 1

    return tuple(action_coords)

