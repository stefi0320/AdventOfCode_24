"""Module providing a function reading files."""
from pathlib import Path
import time
from recordtype import recordtype
import copy

Point = recordtype ('point', 'X, Y')
Robot = recordtype ('robot', 'p, v')

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
    
def robot_moves(r, max_col, max_row, i):
    r.p.X = (r.p.X  + r.v.X  * i) % max_row
    r.p.Y = (r.p.Y  + r.v.Y  * i) % max_col

def day14():
    """Day 14 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt")
    robots = []
    max_row = 103#7
    max_col = 101#11
    
    for line in input_txt:
        tmp = line.split(' ')
        p = tmp[0].replace('p=','').split(',')
        v = tmp[1].replace('v=','').split(',')
        robots.append(Robot(Point(int(p[1]), int(p[0])), Point(int(v[1]), int(v[0]))))
    robots2 = copy.deepcopy(robots)
    #part1
    sum_pt1 = 0

    for r in robots:
        robot_moves(r, max_col, max_row, 100)    
    i = max_row//2
    j = max_col//2
    tmp1, tmp2, tmp3, tmp4 = 0, 0, 0, 0
    for r in robots:
        if r.p.X < i and r.p.Y < j:
            tmp1 += 1
        if r.p.X < i and r.p.Y > j:
            tmp2 += 1
        if r.p.X > i and r.p.Y < j:
            tmp3 += 1
        if r.p.X > i and r.p.Y > j:
            tmp4 += 1
    sum_pt1 = tmp1 * tmp2 * tmp3 * tmp4

    print(sum_pt1)
    #part2
    for k in range(6500, 7000):
        tmp = copy.deepcopy(robots2)
        print(k)
        for r in tmp:
            robot_moves(r, max_col, max_row, k)
        robots_dict = {(r.p.X, r.p.Y): "#" for r in tmp}
        for x in range(max_row):
            print("".join(robots_dict.get((x, y), ".") for y in range(max_col)))
        print('\n')
                
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day14()
