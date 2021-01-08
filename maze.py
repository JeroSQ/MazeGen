import mazegen
import exporter

maze = mazegen.Maze(height=50, width=50) 
maze.generate()
exporter.export_txt(maze.maze_export)
exporter.export_png(maze.maze_export)
# WARNING - Creating a GIF of a big maze and/or big cell_size can lead to Memory Error or even crash your PC
exporter.export_gif(maze.maze_export, maze.order)
