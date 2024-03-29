# MazeGen
A Python program that generates perfect mazes using different algorithms and shows visualizations of how the mazes are created. 
You can check out some examples in the example folder called mazegen_algorithms

### Files
mazegen.py contains the code that ultimately generates the maze. 

exporter.py contains the code to export the generated maze as .txt, .png or .gif

maze.py is an example for you to see how to use the program.

How to Use
----------

Using the ```mazegen.Maze()``` consctructor, create your maze with your desired height and width as keyword arguments.
To generate your random maze, simply call ```generate(*method*)``` on your maze object passing as an argument the method you'd like to use.
Supported methods are:

-DFS(recursive back-tracker)

-Hunt and Kill

-Eller's 

-Prim's 

-Kruskal's 

-Aldous-Broder 

-Wilson's 

-Binary Tree

-Growing Tree

-Sidewinder

-Recursive Division

To select a method use this notation:

```Maze.method``` 

where *method* is *DFS* or *HUNT_KILL* or *ELLERS* or *PRIMS* or *KRUSKALS* or *ALDOUS_BRODER* or *WILSONS* or *BINARY_TREE* or *GROWING_TREE* or *SIDEWINDER* or *DIVISION*

## exporter.py functions:

```export_txt(maze)``` -> exports the maze passed as a .txt file where hashes(#) are the possible paths and whitespaces are walls 

```export_img(maze, cell_size=5, cell_border=0, color=False)``` -> exports the maze passed as a .png file where white is the possible paths and black is the walls. In case you want to color the maze according to the path's distance to the root, set the color argument to True

```export_gif(maze, cell_size=5, duration=20, cell_border=0, color=False)``` -> exports the maze passed as a .gif file showing the process of generating the maze. In case you want to color the maze according to the path's distance to the root, set the color argument to True
###### WARNING: Creating a GIF of a big maze and/or big cell_size can lead to Memory Error or even crash your PC!
