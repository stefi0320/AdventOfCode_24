"""Module providing a function reading files."""
from pathlib import Path
import time
from more_itertools import locate

def open_file_safely(file_name):
    """ File open """
    try:
        script_dir = Path(__file__).resolve().parent
        file_path = script_dir / file_name

        with open(file_path, 'r', encoding="utf-8") as file:
            content = list(line for line in (l.strip() for l in file) if line)
        return content

    except FileNotFoundError:
        print(
            "The file '{file_name}' was not found in the same directory as the script.")
        return None
    
def dfs(grid, start, visited, part2 ) :
    n = len(grid)
    m = len(grid[0])
    point_stack = []
    point_stack.append(start)
    path = 0
    while len(point_stack) != 0:
        current = point_stack.pop()
        i = current[0]
        j = current[1]
        if (grid[i][j] == 9):
            path += 1
            if part2:
                visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
                continue 

        if visited[i][j]:
            continue
       
        visited[i][j] = True
        
        if i < n-1 and grid[i+1][j] - 1 == grid[i][j] and visited[i+1][j] is False:
            point_stack.append([i+1, j]) # Move bottom
        if i > 0  and grid[i-1][j] - 1 == grid[i][j] and visited[i-1][j] is False:
            point_stack.append([i-1, j]) # Move top
        if j > 0 and grid[i][j-1] - 1 == grid[i][j] and visited[i][j-1] is False:
            point_stack.append([i, j-1]) # Move left
        if j < m-1 and grid[i][j+1] - 1 == grid[i][j] and visited[i][j+1] is False:
            point_stack.append([i, j+1]) # Move right   
    
    return path 

def has_path_dfs(grid, start, part2) :
    sum_path = 0
    for s in start:
        visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
        sum_path += dfs(grid, s, visited, part2)   
    return sum_path


def day9():
    """Day 9 of Advent of code """
    # record start time
    start = time.time()
    
    input_txt = open_file_safely("input.txt")
    input_seq = []
    start_point = []
    for i, line in enumerate(input_txt):
        tmp = [int(x) for x in line.strip()]
        row = list(locate(tmp, lambda x: x == 0))
        for r in row:
            start_point.append([i, r])
        input_seq.append(tmp)

    #part1
    print(has_path_dfs(input_seq, start_point, False))

    # part2
    print(has_path_dfs(input_seq, start_point, True))
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day9()