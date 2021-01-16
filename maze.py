from mazegen import Maze
import exporter

maze = Maze(height=10, width=10, root="top-left", random=True) 
maze.generate(Maze.BINARY_TREE)
exporter.export_txt(maze)
exporter.export_png(maze, cell_size=5, cell_border=0, color=True)
exporter.export_gif(maze, cell_size=5, cell_border=0, color=False)
