from mazegen import Maze
import exporter

maze = Maze(height=21, width=21, root="top-left", random=True) 
maze.generate(Maze.WILSONS)
exporter.export_txt(maze)
exporter.export_png(maze, cell_size=5, cell_border=0, color=False)
exporter.export_gif(maze, cell_size=5, cell_border=0, color=False)
