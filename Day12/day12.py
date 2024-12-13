"""Module providing a function reading files."""
from pathlib import Path
import time
import numpy as np
from typing import TypeAlias
from collections.abc import Iterable, Iterator

Vector: TypeAlias = tuple[int, int]
OFFSETS: tuple[Vector, ...] = ((0, -1), (0, 1), (-1, 0), (1, 0))

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

def side_counter(region):
    """
    Calculate the side-count of this region.
    """
    side_count = 0
    for dr, dc in OFFSETS:
        analyzed: set[Vector] = set()
        for plot in region:
            if plot in analyzed:
                continue
            pr, pc = plot
            if (pr + dr, pc + dc) in region:
                continue
            side_count += 1

            for scan_delta in (-1, 1):
                r, c = plot
                while (r, c) in region and (r + dr, c + dc) not in region:
                    analyzed.add((r, c))
                    r += dc * scan_delta
                    c += dr * scan_delta
    return side_count

def is_safe(M, r, c, visited):
    ROW = len(M)
    COL = len(M[0])

    return (r >= 0) and (r < ROW) and (c >= 0) and (c < COL) and \
           (M[r][c] == 0 and not visited[r][c])

def dfs(grid, i, j, visited,points):
    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] == -1:
        return 1
    if visited[i][j] == 1:  # Already visited
        return 0
    visited[i][j] = 1  # Mark as visited
    points.append((i,j))
    return dfs(grid, i-1, j, visited,points) + dfs(grid, i+1, j, visited,points) + dfs(grid, i, j-1, visited,points) + dfs(grid, i, j+1, visited,points)

def count_islands(M):
    ROW = len(M)
    COL = len(M[0])
    visited =  np.array([[0 for _ in range(COL)] for _ in range(ROW)])
    count, count2 = 0, 0
    peri, area = 0, 0
    prev_area = 0
    for r in range(ROW):
        for c in range(COL):
            if M[r][c] == 0 and visited[r][c] == 0:
                points = []
                peri = dfs(M, r, c, visited, points)
                area = np.count_nonzero(visited == 1) - prev_area
                prev_area += area
                count += area*peri
                count2 += area* side_counter(points)
    return count, count2

def day12():
    """Day 12 of Advent of code """
    # record start time
    start = time.time()
    
    input_txt = open_file_safely("input.txt")
    garden = []
    types = []
    for line in input_txt:
        tmp = []
        for r in line:
            if r not in types:
                types.append(r)
            tmp.append(r)
        garden.append(tmp)

    #part1
    sum_pt1, sum_pt2 = 0, 0
    for t in types:
        type_garden = np.char.find(garden, t)
        i,j = count_islands(type_garden)
        sum_pt1 += i
        sum_pt2 += j
    print(sum_pt1)
    #part2
    print(sum_pt2)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day12()