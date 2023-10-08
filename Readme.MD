This is the Readme.MD file for the LMRE-AI-Pathfinder repository:

# LMRE-AI-Pathfinder

This repository contains the code and data for the LMRE-AI-Pathfinder project, which is a Python application that uses artificial intelligence to find the shortest path between two points in a given image. The image can be a maze, a street map, or any other type of graph.

## Features

- The application can load an image from the source_images folder or from a URL.
- The application can detect the nodes and edges in the image using OpenCV and networkx libraries.
- The application can find the shortest path between two user-specified points using A* algorithm.
- The application can render the solution path on the image and save it to the output folder.

## Requirements

- Python 3.8 or higher
- OpenCV 4.5.3 or higher
- networkx 2.6.2 or higher
- numpy 1.21.2 or higher
- matplotlib 3.4.3 or higher

## Usage

- Run the main.py file in the code directory using `python main.py`.
- Set the start and end coordinates in the code (an interface is not available yet, but in progress)
- Wait for the application to process the image and find the solution path.
- Check the output folder for the rendered image.

## Examples

Here are some examples of input images and output images:

Path from top-left to bottom-right
![Maze input](source_images/stock_maze.jpg)
![Maze output](Maze.jpg)

Path from top to bottom
![Street map input](source_images/city.jpg)
![Street map output](Street Map.png)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, please feel free to contact me at apps247@gmail.com.
