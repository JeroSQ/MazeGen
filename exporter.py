from PIL import Image, ImageDraw

def export_txt(maze):
    with open("maze.txt", "w") as f:
        height = len(maze)
        width = max(len(row) for row in maze)
        for i in range(height):
            for j in range(width):
                f.write(" " if maze[i][j] else "#")
            f.write("\n")

def export_png(maze, cell_size=5):
    height = len(maze)
    width = max(len(row) for row in maze)
    img = Image.new(
        "RGBA",
        (width * cell_size, height  * cell_size),
        "black"
    )
    draw = ImageDraw.Draw(img)

    for i in range(height):
        for j in range(width):
            if maze[i][j]:
                draw.rectangle([i * cell_size, j * cell_size, i * cell_size + cell_size, j * cell_size + cell_size],fill="white")

    img.save("maze.png")

def export_gif(maze, order, cell_size=5):
    height = len(maze)
    width = max(len(row) for row in maze)
    frames = []
    img = Image.new(
        "RGBA",
        (width * cell_size, height  * cell_size),
        "black"
    )

    draw = ImageDraw.Draw(img)

    for i, j in order:
        draw.rectangle([i * cell_size, j * cell_size, i * cell_size + cell_size, j * cell_size + cell_size],fill="white")
        frames.append(Image.frombytes(img.mode, img.size, img.tobytes()))

    frames[0].save('maze.gif', save_all=True, append_images=frames[1:], duration=20)