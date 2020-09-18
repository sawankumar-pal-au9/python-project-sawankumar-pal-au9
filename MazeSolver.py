import argparse
import copy

# This is class object Maze.
class Maze:
    def __init__(self, maze):
        self.maze = maze

    # This is method of class Maze.
    def findPath(self, source_x, source_y, destination_x, destination_y):
        global res, min_steps, directions

        col = len(self.maze[0])
        row = len(self.maze)
        min_steps = 1000000000000

        # Checking is Source or Destination co-ordinates are out of range if yes then print alert message and return -1.
        if destination_x >= row or destination_y >= col or source_x < 0 or source_y < 0:
            print("------------------------------")
            print("No such Source or Destination exist.")
            print("Enter valid Source or Destination")
            print("------------------------------")
            return -1

        # Checking is Source or Destination is a blocked cell if yes then print alert message and return -1.
        if self.maze[destination_x][destination_y] == 0 or self.maze[source_x][source_y] == 0:
            print("------------------------------")
            print("Source or Destination is Blocked.")
            print("Enter valid Source or Destination")
            print("------------------------------")
            return -1

        visited = [[0 for i in range(col)] for j in range(row)]
        # Using depth first search algorithm to traverse throught all possible directions to reach to the destination.
        dfs(self.maze, source_x, source_y, destination_x, destination_y, visited, steps = 0, dir = '')
        
        if min_steps != 1000000000000:
            print("------------------------------")
            print("Minimum Steps taken to reach the destination is", min_steps)
            print("Directions followed to reach the destination are ", directions)
            print("------------------------------")
            return res
        else:
            print("No Path exist from source to destination")
            return -1


def dfs(maze, x, y, n, m, visited, steps, dir):
    global res, min_steps, directions

    # If co-ordinates are out of maze return.
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]):
        return

    # If cell is already visited or a blocked cell return.
    if visited[x][y] == 1 or maze[x][y] == 0:
        return

    # If reached to destination store the directions, steps and path in visited matrix and look for another shorter path than this.
    if x == n and y == m:
        visited[x][y] = 1
        if (min_steps > steps):
            min_steps = steps
            directions = dir
            res = copy.deepcopy(visited)

    # Marking visites cell as 1 so that program will not compute for that cell again and again.
    visited[x][y] = 1
    
    # Checking for path in Right, Down, Left anf Up directons.
    dfs(maze, x, y + 1, n, m, visited, steps + 1, dir + '->' + 'R')
    dfs(maze, x + 1, y, n, m, visited, steps + 1, dir + '->' + 'D')
    dfs(maze, x, y - 1, n, m, visited, steps + 1, dir + '->' + 'L')
    dfs(maze, x - 1, y, n, m, visited, steps + 1, dir + '->' + 'U')  

    # If choosen path results in a blocked cells marking travelled cell as 0 which means not visited and Backtracking.
    visited[x][y] = 0


# This is main driver code.
if __name__ == '__main__':   
    
    # Adding Arguments and setting default values for CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='input.txt', help='What is your input file name?')
    parser.add_argument('--output_file', type=str, default='output.txt', help='What is your output file name?')
    parser.add_argument('--x', type=int, default=0, help='What is your Source Row?')
    parser.add_argument('--y', type=int, default=0, help='What is your Source Column?')
    parser.add_argument('--dx', type=int, default=None, help='What is your Destination Row?')
    parser.add_argument('--dy', type=int, default=None, help='What is your Destination Column?')
    args = parser.parse_args()

    # To check if default input file is not present it will show the message to provide input file name through CLI.
    try:
        input = open(args.input_file, 'r')                   # Method to open and read file.
        error = False
    except:
        error = True
        print("Please provide input file name")

    # If program do not find any input file it will stop execution of further code.
    if not error:
        maze = list()
        for data in input:
            maze.append(list(map(int, data.split())))       # Fetching data from file and convert it into 2D matrix. 
        input.close()
        
        # Setting default destination as Bottom right cell.
        if args.dx == None:
            args.dx = len(maze) - 1
        if args.dy == None:
            args.dy = len(maze[0]) - 1
        
        # Making an instance of class Maze.
        maze = Maze(maze)

        x, y, dx, dy = args.x, args.y, args.dx, args.dy

        # Calling findPath Method to check for the path from Source to Destination.
        path = maze.findPath(x, y, dx, dy)

        # Creating output file and if path exist writes path data on output file else writes -1 on output file.
        output = open(args.output_file, 'w')               # Method to open and write into file.
        if path == -1:
            output.write("-1")
            output.close()
        else:
            path[x][y], path[dx][dy] = 'S', 'D'
            for data in path:
                append = " ".join(map(str, data))
                output.write(append)
                output.write("\n")
            output.close()         