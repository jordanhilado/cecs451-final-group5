#!/usr/bin/env python
# coding: utf-8

# In[1]:


def displayMaze(maze, displayState, steps):
    # create a new figure
    plt.figure(figsize=(10, 5))

    # display the maze
    plt.imshow(maze, cmap=plt.cm.viridis, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    # label the graph with the number of steps taken
    if steps > 0:
        plt.title("Steps: " + str(steps))

    if displayState:
        plt.show()

def createMP4(name, imgDirPath):
    # find the number of images in the folder
    numImages = len(os.listdir(imgDirPath))
    
    with imageio.get_writer(name + '.mp4', mode='I') as writer:
        # for each screenshot
        for i in range(1, numImages + 1):
            # read the screenshot
            image = imageio.imread(imgDirPath + "/" + str(i) + ".png")
            # add the screenshot to the video
            writer.append_data(image)
    
    # delete the screenshots
    for i in range(1, numImages + 1):
        os.remove(imgDirPath + "/" + str(i) + ".png")
        
    
    # speed up the video by a factor of 3x speed up
    os.system("ffmpeg -i " + name + ".mp4 -filter:v \"setpts=0.333*PTS\" " + name + "SpedUp.mp4 -y")


# In[3]:




# In[4]:


# import backtracking from mazelib package
from mazelib import Maze
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator

import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time
import sys
import os
import imageio.v2 as imageio

global bfsTime
global dfsTime
global bfsSteps
global dfsSteps
bfsTime = []
dfsTime = []
bfsSteps = []
dfsSteps = []

inputHeight = 0
inputWidth = 0

def generateMaze():
  # get the height and width of the maze from the user
  while True:
      try:
          # inputHeight = int(input("Enter the height of the maze: "))
          # inputWidth = int(input("Enter the width of the maze: "))
          height = (inputHeight + 1) // 2
          width = (inputWidth + 1) // 2
          break
      except ValueError:
          print("Please enter a valid integer.")

  # print the height and width of the maze 
  print("Generating a maze with a height of", height, "and a width of", width)
  # create a maze object
  newMaze = Maze()
  maze_generator = BacktrackingGenerator(width, height)
  newMaze = maze_generator.generate()

  # print the maze
  print(newMaze)

  newHeight = newMaze.shape[0]
  newWidth = newMaze.shape[1]
  print("The height of the maze is", newHeight, "and the width of the maze is", newWidth)

  # ensure that the maze is solvable by creating an entrance and exit in a random location on the top and bottom of the maze which must be connected to a 0 in the maze
  # create a list of all the 0s in the first and last row of the maze
  topRow = []
  bottomRow = []
  for i in range(newWidth):
      if newMaze[1][i] == 0:
          topRow.append(i)
      if newMaze[newHeight - 2][i] == 0:
          bottomRow.append(i)

  # randomly select a 0 from the top1 and bottom row
  top = random.choice(topRow)
  bottom = random.choice(bottomRow)

  # create an entrance and exit in the maze
  newMaze[0][top] = 0
  newMaze[newHeight - 1][bottom] = 0

  displayMaze(newMaze, True, 0)
  return newMaze


# In[5]:


def findNeighbors(node, maze):
    # measure the height and width of the maze
    height = maze.shape[0]
    width = maze.shape[1]

    # create a list to store the neighbors of the node
    neighbors = []

    # if the node is not on the top row
    if node[0] != 0:
        # if the node is not a wall
        if maze[node[0] - 1][node[1]] == 0:
            # add the node above to the neighbors list
            neighbors.append((node[0] - 1, node[1]))

    # if the node is not on the bottom row
    if node[0] != height - 1:
        # if the node is not a wall
        if maze[node[0] + 1][node[1]] == 0:
            # add the node below to the neighbors list
            neighbors.append((node[0] + 1, node[1]))

    # if the node is not on the left side
    if node[1] != 0:
        # if the node is not a wall
        if maze[node[0]][node[1] - 1] == 0:
            # add the node to the left to the neighbors list
            neighbors.append((node[0], node[1] - 1))

    # if the node is not on the right side
    if node[1] != width - 1:
        # if the node is not a wall
        if maze[node[0]][node[1] + 1] == 0:
            # add the node to the right to the neighbors list
            neighbors.append((node[0], node[1] + 1))

    # return the neighbors list
    return neighbors


# In[6]:


# animate the solving of the maze using BFS by taking a screenshot of each step and saving it to a folder and at the end creating a video of the screenshots to show the solving of the maze
def BFS(maze, bfsTime, bfsSteps):
    stepCount = 0

    # used to measure the time it takes to run BFS
    start_time = time.time()

    # measure the height and width of the maze
    height = maze.shape[0]
    width = maze.shape[1]

    # find the entrance and exit of the maze in the first and last row
    for i in range(width):
        if maze[0][i] == 0:
            start = (0, i)
        if maze[height - 1][i] == 0:
            end = (height - 1, i)

    # create a queue to store the nodes to be visited
    queue = []
    # add the start node to the queue
    queue.append(start)

    visited = []
    # create a dictionary to store the parent of each node
    parent = {}
    # set the parent of the start node to None
    parent[start] = None

    stepCount = 0

    # while the queue is not empty
    while queue:
        # increment the step count
        stepCount += 1

        # remove the first node from the queue
        node = queue.pop(0)

        # if the node is the end node
        if node == end:
            # break out of the loop
            break

        # if the node has not been visited
        if node not in visited:
            # add the node to the visited list
            visited.append(node)

            # find the neighbors of the node
            neighbors = findNeighbors(node, maze)

            # for each neighbor of the node
            for neighbor in neighbors:
                # if the neighbor has not been visited
                if neighbor not in visited:
                    # add the neighbor to the queue
                    queue.append(neighbor)
                    # set the parent of the neighbor to the node
                    parent[neighbor] = node

        # create a copy of the maze
        mazeCopy = maze.copy()
        for v in visited:
            mazeCopy[v[0]][v[1]] = 2 

        for q in queue:
            mazeCopy[q[0]][q[1]] = 3 

        displayMaze(mazeCopy, False, stepCount)
        plt.savefig("BFS/" + str(len(visited)) + ".png")
        plt.close()

    # This will be used to store the path from start to end
    path = []

    # Add the end node to the path
    path.append(end)

    # Check if the end node has a parent
    while end in parent:
        # stepCount += 1
        # If the end node has a parent, get the parent
        end = parent[end]
        # Add the parent to the path list
        path.append(end)

    # Reverse the path list
    path.reverse()
    path.pop(0)
    print(path)
    # This code creates a copy of the maze and sets the path to be colored. It then displays the image and saves it in the BFS folder with a name corresponding to the number of nodes visited.

    # measure the time it takes to run BFS
    end_time = time.time()
    elapsed_time = end_time - start_time
    stepCount = len(visited)
    bfsTime.append(elapsed_time)
    bfsSteps.append(stepCount)
    print(f"Elapsed time for Breadth-First Search: {elapsed_time} \| Steps: {stepCount}")

    # Create a copy of the maze
    mazeCopy = maze.copy()

    currentNumFiles = len(os.listdir("BFS"))

    # For each node in the path
    for node in path:
        # If the node is not the start node
        if node != start:
            # Set the node to be colored
            mazeCopy[node[0]][node[1]] = 10 
            # Display the maze in the background and add the screenshot to the BFS folder with a name corresponding to the number of nodes visited plus the initial number of files in the BFS folder
            displayMaze(mazeCopy, False, stepCount)
            plt.savefig("BFS/" + str(currentNumFiles + len(path) - path.index(node)) + ".png")
            plt.close()
    
    # Call the createMP4 function to create a video of the screenshots with the parameters of the name of the file and the folder the screenshots are in
    createMP4("BFS", "BFS")

# BFS(newMaze, bfsTime, bfsSteps)


# In[7]:


# animate the solving of the maze using DFS by taking a screenshot of each step and saving it to a folder and at the end creating a video of the screenshots to show the solving of the maze
def DFS(maze, dfsTime, dfsSteps):
    # used to measure the time it takes to run DFS
    start_time = time.time()
    stepCount = 0

    # measure the height and width of the maze
    height = maze.shape[0]
    width = maze.shape[1]
    # find the entrance and exit of the maze in the first and last row
    for i in range(width):
        if maze[0][i] == 0:
            start = (0, i)
        if maze[height - 1][i] == 0:
            end = (height - 1, i)
    
    # create a stack to store the nodes to be visited
    stack = []
    # add the start node to the stack
    stack.append(start)

    visited = []
    # create a dictionary to store the parent of each node
    parent = {}
    # set the parent of the start node to None
    parent[start] = None
    while stack:
        node = stack.pop()
        if node == end:
            break
        # if the node has not been visited
        if node not in visited:
            # add the node to the visited list
            visited.append(node)

            # find the neighbors of the node
            neighbors = findNeighbors(node, maze)

            # for each neighbor of the node
            for neighbor in neighbors:
                # if the neighbor has not been visited
                if neighbor not in visited:
                    # add the neighbor to the stack
                    stack.append(neighbor)
                    # set the parent of the neighbor to the node
                    parent[neighbor] = node

                # if the neighbor is the end node
                if neighbor == end:
                    # break out of the loop
                    break

        # create a copy of the maze
        mazeCopy = maze.copy()
        # for each node in the maze path
        for v in visited:
            # highlight the node
            mazeCopy[v[0]][v[1]] = 2 
        # for the current node highlight it in a different color to show that it is the current node
        for s in stack:
            mazeCopy[s[0]][s[1]] = 3 

        displayMaze(mazeCopy, False)
        plt.savefig("DFS/" + str(len(visited)) + ".png")
        plt.close()

    path = []
    path.append(end)
    while end in parent:
        # stepCount += 1
        end = parent[end]
        path.append(end)
    path.reverse()
    path.pop(0)

    # measure the time it takes to run DFS
    end_time = time.time()
    elapsed_time = end_time - start_time
    dfsTime.append(elapsed_time)
    stepCount = len(visited)
    dfsSteps.append(stepCount)
    print(f"Elapsed time for Depth-First Search: {elapsed_time} \| Steps: {stepCount}")
    
    mazeCopy = maze.copy()
    currentNumFiles = len(os.listdir("DFS"))
    for node in path:
        if node != start:
            mazeCopy[node[0]][node[1]] = 10 
            displayMaze(mazeCopy, False)
            plt.savefig("DFS/" + str(currentNumFiles + len(path) - path.index(node)) + ".png")
            plt.close()

    createMP4("DFS", "DFS")

# DFS(newMaze, dfsTime, dfsSteps)


# In[8]:




for i in range(5):
  currMaze = generateMaze()
  BFS(currMaze, bfsTime, bfsSteps)
  DFS(currMaze, dfsTime, dfsSteps)


# In[9]:


print("DFS Times:", dfsTime)
print("BFS Times:", bfsTime)

# X-axis labels
labels = ['Maze 1', 'Maze 2', 'Maze 3', 'Maze 4', 'Maze 5']

# Set the width of each bar
barWidth = 0.35

# Set the position of each bar on the X-axis
r1 = np.arange(len(bfsTime))
r2 = [x + barWidth for x in r1]

# Define consistent colors for each search
bfsColor = ['#3366CC', '#3366CC', '#3366CC', '#3366CC', '#3366CC']
dfsColor = ['#109618', '#109618', '#109618', '#109618', '#109618']

# Plotting the bar graph
plt.bar(r1, bfsTime, color=bfsColor, width=barWidth, edgecolor='white', label='BFS')
plt.bar(r2, dfsTime, color=dfsColor, width=barWidth, edgecolor='white', label='DFS')

# Adding labels and title
plt.xlabel('Search Algorithm')
plt.ylabel('Time (in seconds)')
plt.title(f'BFS vs DFS Time Comparison ({heightSize}x{widthSize} maze)')

# Adding X-axis labels
plt.xticks([r + barWidth/2 for r in range(len(bfsTime))], labels)

# Adding legend
plt.legend()

# Displaying the plot
plt.show()


# In[10]:


# X-axis labels
labels = ['Maze 1', 'Maze 2', 'Maze 3', 'Maze 4', 'Maze 5']

# Set the width of each bar
barWidth = 0.35

# Set the position of each bar on the X-axis
r1 = np.arange(len(bfsSteps))
r2 = [x + barWidth for x in r1]

# Define consistent colors for each search
bfsColor = ['#3366CC', '#3366CC', '#3366CC', '#3366CC', '#3366CC']
dfsColor = ['#109618', '#109618', '#109618', '#109618', '#109618']

# Plotting the bar graph
plt.bar(r1, bfsSteps, color=bfsColor, width=barWidth, edgecolor='white', label='BFS')
plt.bar(r2, dfsSteps, color=dfsColor, width=barWidth, edgecolor='white', label='DFS')

# Adding labels and title
plt.xlabel('Search Algorithm')
plt.ylabel('Steps Taken')
plt.title(f'BFS vs DFS Step Comparison ({heightSize}x{widthSize} maze)')

# Adding X-axis labels
plt.xticks([r + barWidth/2 for r in range(len(bfsSteps))], labels)

# Adding legend
plt.legend()

# Displaying the plot
plt.show()

