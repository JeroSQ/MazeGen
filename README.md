# MazeGen
A Python program that generates mazes using randomized Depth-First-Search

mazegen.py contains the code that ultimately generates the maze. 

exporter.py contains the code to export the generated maze as .txt, .png or .gif

maze.py is used as a bridge between those two modules

How to Use
----------

Using the mazegen.Maze() consctructor, create your maze with your desired height and width as keyword arguments.
To generate your random maze, simply call generate() on your maze object.

exporter.py functions:

export_txt(maze) -> exports the maze passed as a .txt file where hashes(#) are the possible paths and whitespaces are walls 

export_img(maze, cell_size=5, cell_border=0, color=False) -> exports the maze passed as a .png file where white is the possible paths and black is the walls. In case you want to color the maze according to the path's distance to the root, set the color argument to True

export_gif(maze, cell_size=5, duration=20, cell_border=0, color=False) -> exports the maze passed as a .gif file showing the process of generating the maze. In case you want to color the maze according to the path's distance to the root, set the color argument to True
