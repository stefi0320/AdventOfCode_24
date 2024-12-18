"""Module providing a function reading files."""
from pathlib import Path
import time
import heapq

class Node:
    def __init__(
        self,
        pos: tuple[int, int],
        direction: str,
        cost: int,
    ):
        self.pos = pos
        self.direction = direction
        self.cost = cost

    def to_hashable(self) -> tuple[tuple[int, int], int]:
        return (self.pos, self.cost)

    # For visited
    def __hash__(self):
        return hash(self.to_hashable())
    
    def __lt__(self, other):
        return self.cost < other.cost  # For heapq to prioritize by cost

    def __eq__(self, other):
        return self.to_hashable() == other.to_hashable()

    def __repr__(self):
        return f"Node(pos={self.pos}, direction={self.direction}, cost={self.cost})"
    
    def get_neighbours(self, m, n) -> list[tuple[int, int, str, int]]:
        neighbours = []
        rotation_map = [(0, -1, 'L'), (0, 1, 'R'), (-1, 0, 'U'),(1, 0, 'D')]
        for di, dj, new_direction in rotation_map:
            ni, nj = self.pos[0] + di, self.pos[1] + dj
            if 0 <= ni < m and 0 <= nj < n:
                new_cost = self.cost + 1
                neighbours.append((ni, nj, new_direction, new_cost))
        return neighbours
class Grid:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.queue = []
        
    def get_char(self, position: tuple[int, int]) -> str:
        x, y = position
        return self.grid[x][y]

    def shortest_path(self, start) -> list[tuple[int, int]]:
        visited = set()
        heapq.heappush(self.queue,Node(pos=start, direction='R', cost = 0))
        # Locate the goal ('E') in the grid
        goal = (self.height-1, self.width-1)

        while self.queue:
            current_node = heapq.heappop(self.queue)
            retval = current_node.cost
            if current_node.pos == goal:
                return retval

            if (current_node.pos,current_node.direction) in visited:
                continue
            visited.add((current_node.pos, current_node.direction))

            for ni, nj, new_direction, new_cost in current_node.get_neighbours(self.height, self.width):
                if ((ni, nj), new_direction) not in visited and self.get_char((ni, nj)) != '#':
                    heapq.heappush(self.queue, Node((ni, nj), new_direction, new_cost))
                 
        return None

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

def day18():
    """Day 18 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt") 
    mem_map = [['.' for _ in range(71)] for i in range(71)]
    start_p = (0,0)
    
    for i in range(1024):
        tmp = list(int(x) for x in input_txt[i].split(','))
        mem_map[tmp[1]][tmp[0]] = '#'

    #part1
    maze = Grid(mem_map)
    print(maze.shortest_path(start_p))
    #part2  
    for i in range(1024, len(input_txt)):
        tmp = list(int(x) for x in input_txt[i].split(','))
        mem_map[tmp[1]][tmp[0]] = '#'
        maze = Grid(mem_map)
        if maze.shortest_path(start_p) is None:
            print(tmp)
            break
    
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day18()
