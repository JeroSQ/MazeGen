from mazegen import Maze
import exporter

maze = Maze(height=51, width=51, root="top-left", random=True) 
maze.generate(Maze.KRUSKALS)
exporter.export_txt(maze)
exporter.export_png(maze, cell_size=5, cell_border=0, color=False)
exporter.export_gif(maze, cell_size=5, cell_border=0, color=False)
