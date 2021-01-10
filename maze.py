import mazegen
import exporter

maze = mazegen.Maze(height=30, width=30, root="middle", random=True) 
maze.generate()
exporter.export_txt(maze)
exporter.export_png(maze, cell_size=5, cell_border=0, color=False)
# WARNING - Creating a GIF of a big maze and/or big cell_size can lead to Memory Error or even crash your PC
exporter.export_gif(maze, cell_size=5, cell_border=0, color=False)
