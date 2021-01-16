from mazegen import Maze
import exporter

maze = Maze(height=51, width=51, root="top3-left", random=True) 
maze.generate(Maze.GROWING_TREE)
exporter.export_txt(maze)
exporter.export_png(maze, cell_size=5, cell_border=0, color=True)
exporter.export_gif(maze, cell_size=5, cell_border=0, color=True)
