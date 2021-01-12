import mazegen
import exporter

maze = mazegen.Maze(height=30, width=30, root="top-left", random=True) 
maze.generate(maze.DFS)
exporter.export_txt(maze)
exporter.export_png(maze, cell_size=5, cell_border=0, color=True)
# WARNING - Creating a GIF of a big maze and/or big cell_size can lead to Memory Error or even crash your PC
exporter.export_gif(maze, cell_size=5, cell_border=0, color=True)
