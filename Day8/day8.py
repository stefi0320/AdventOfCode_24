"""Module providing a function reading files."""
from pathlib import Path
import time
import numpy as np

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

def put_antinodes(antenas, antenna_locs, max_range):
    sum_anti = 0
    sum_orig = 0
    antinodes = np.full((antenas.shape[0], antenas.shape[1]), '.')
    for row, line in enumerate(antenas):
        for col, antenna in enumerate(line):
            if antenna != '.':
                if antenna not in antenna_locs:
                    antenna_locs[antenna] = np.char.find(antenas, antenna)
                for n_row, n_line in enumerate(antenna_locs[antenna]):
                    for n_col, pair in enumerate(n_line):
                        if pair == 0 and (n_row != row and n_col != col):
                            step_row = row - n_row
                            step_col = col - n_col
                            for i in range(1, max_range):
                                tmp_row = n_row - (step_row*i)
                                tmp_col = n_col - (step_col*i)
                                if(((tmp_row < antenas.shape[0]) and (tmp_row >= 0)) and ((tmp_col >= 0) and (tmp_col < antenas.shape[1]))):
                                    antinodes[tmp_row, tmp_col] = '#'
                            for i in range(1, max_range):
                                tmp_row = row + (step_row*i)
                                tmp_col = col + (step_col*i)
                                if (((tmp_row < antenas.shape[0]) and (tmp_row >= 0)) and ((tmp_col >= 0) and (tmp_col < antenas.shape[1]))):
                                    antinodes[tmp_row, tmp_col] = '#'
                            
    for row, line in enumerate(antenas):
        for col, antenna in enumerate(line):
            if antinodes[row,col] == '.':
                if antenna != '.':
                    antinodes[row,col] = '#'
                    sum_orig += 1
            else:
                sum_anti += 1
    return sum_anti,sum_orig

def day8():
    """Day 8 of Advent of code """
    # record start time
    start = time.time()

    input_txt = open_file_safely("input.txt")
    antenas = np.array([list(l) for l in input_txt])
    antenna_locs = dict()
    # part1
    sum_part1,_ = put_antinodes(antenas, antenna_locs, 2)                           
    print(sum_part1)

    # part2
    sum_part2,tmp = put_antinodes(antenas, antenna_locs, antenas.shape[0])

    print(sum_part2 + tmp)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day8()