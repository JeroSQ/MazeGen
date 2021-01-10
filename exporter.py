from PIL import Image, ImageDraw

def export_txt(maze):
    "Exports the maze passed as a .txt file where hashes(#) are the possible paths and whitespaces are walls"
    with open("maze.txt", "w") as f:
        height = len(maze.maze_export)
        width = max(len(row) for row in maze.maze_export)
        for i in range(height):
            for j in range(width):
                f.write(" " if maze.maze_export[i][j] else "#")
            f.write("\n")

def export_png(maze, cell_size=5, cell_border=0, color=False):
    "Exports the maze passed as a .png file where white is the possible paths and black is the walls"
    height = len(maze.maze_export)
    width = max(len(row) for row in maze.maze_export)
    img = Image.new(
        "RGBA",
        (width * cell_size, height  * cell_size),
        "black"
    )
    draw = ImageDraw.Draw(img)

    for (i, j), lenpath in maze.order.items():
        draw.rectangle(
            [j * cell_size + cell_border, i * cell_size + cell_border, (j+1) * cell_size - cell_border, (i+1) * cell_size - cell_border],
            fill=get_color(height, width, color, lenpath, maze.random))

    img.save("maze.png")

def export_gif(maze, cell_size=5, cell_border=0, duration=20, color=False):
    "Exports the maze passed as a .gif file showing the process of generating the maze"
    height = len(maze.maze_export)
    width = max(len(row) for row in maze.maze_export)
    frames = []
    img = Image.new(
        "RGBA",
        (width * cell_size, height  * cell_size),
        "black"
    )

    draw = ImageDraw.Draw(img)

    for (i, j), lenpath in maze.order.items():
        draw.rectangle(
            [j * cell_size + cell_border, i * cell_size + cell_border, (j+1) * cell_size - cell_border, (i+1) * cell_size - cell_border],
            fill=get_color(height, width, color, lenpath, maze.random))
        frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))

    frames[0].save('maze.gif', save_all=True, append_images=frames[1:], duration=duration)

def get_color(height, width, color, path_length, random):
    "Returns a color for each path_length value"
    if not color:
        return "white"

    # Calculate approximate longest possible path
    longest_path = int((height * width) / 10) + max([height, width]) * 2 if random else (height * width) / 4

    start_color = [0, 255, 255]

    start_color[1] -= int(path_length * 1530 / longest_path)

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


