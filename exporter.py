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

def export_png(maze, cell_size=5, cell_border=0):
    "Exports the maze passed as a .png file where white is the possible paths and black is the walls"
    height = len(maze.maze_export)
    width = max(len(row) for row in maze.maze_export)
    img = Image.new(
        "RGBA",
        (width * cell_size, height  * cell_size),
        "black"
    )
    draw = ImageDraw.Draw(img)

    for i in range(height):
        for j in range(width):
            if maze.maze_export[i][j]:
                draw.rectangle([i * cell_size + cell_border, j * cell_size + cell_border, (i+1) * cell_size - cell_border, (j+1) * cell_size - cell_border],fill="white")

    img.save("maze.png")

def export_gif(maze, cell_size=5, cell_border=0, duration=20):
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

    for i, j in maze.order:
        draw.rectangle([i * cell_size + cell_border, j * cell_size + cell_border, (i+1) * cell_size - cell_border, (j+1) * cell_size - cell_border],fill="white")
        frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))

    frames[0].save('maze.gif', save_all=True, append_images=frames[1:], duration=duration)