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
        rotation_map = {
            'U': [(0, -1, 'L'), (0, 1, 'R'), (-1, 0, 'U')],
            'D': [(0, -1, 'L'), (0, 1, 'R'), (1, 0, 'D')],
            'L': [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L')],
            'R': [(-1, 0, 'U'), (1, 0, 'D'), (0, 1, 'R')],
        }
        for di, dj, new_direction in rotation_map[self.direction]:
            ni, nj = self.pos[0] + di, self.pos[1] + dj
            if 0 <= ni < m and 0 <= nj < n:
                new_cost = self.cost + (1001 if new_direction != self.direction else 1)
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
        heapq.heappush(self.queue,Node(pos=start, direction='U', cost = 1000))
        heapq.heappush(self.queue,Node(pos=start, direction='R', cost = 0))
        # Locate the goal ('E') in the grid
        goal = None
        for i in range(self.height):
            for j in range(self.width):
                if self.get_char((i, j)) == 'E':
                    goal = (i, j)
                    break
            if goal:
                break

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
                 
        raise ValueError("No path found")
    
    
    def find_all_shortest_paths(self, start) -> list[list[tuple[int, int]]]:
        work = [(0, (start,), 1, 0)]        
        goal = None
        for i in range(self.height):
            for j in range(self.width):
                if self.get_char((i, j)) == 'E':
                    goal = (i, j)
                    break
            if goal:
                break

        best_costs = {(*start, 1, 0): 0}
        best_end_cost = 0
        best_seats = set()
        
        while work:
            cost, path, dx, dy = heapq.heappop(work)
            x, y = pos = path[-1]
            if pos == goal:
                best_seats |= {*path}
                best_end_cost = cost
            elif not best_end_cost or cost < best_end_cost:
                for cost, x, y, dx, dy in (
                    (cost + 1, x + dx, y + dy, dx, dy),  # straight
                    (cost + 1000, x, y, dy, -dx),        # left
                    (cost + 1000, x, y, -dy, dx),        # right
                ):
                    pos = x, y, dx, dy
                    if self.grid[y][x] != '#' and best_costs.get(pos, cost + 1) >= cost:
                        best_costs[pos] = cost
                        heapq.heappush(work, (cost, path + ((x, y),), dx, dy))
        return len(best_seats)


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

def day16():
    """Day 16 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt")
    tmp_grid = []
    for line in input_txt:
        tmp = [x for x in line]
        tmp_grid.append(tmp)
    
    start_p = set()
    for i,line in enumerate(tmp_grid):
        for j,char in enumerate(line):
            if char == 'S':
                start_p = (i, j)
                break
        if start_p:
            break

    #part1
    maze = Grid(tmp_grid)
    min_coast = maze.shortest_path(start_p)
    print(min_coast)
    #part2  
    print(maze.find_all_shortest_paths(start_p))
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day16()
