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


def search(tmp_array, row, col, i, step_row, step_col):
    symbols = ['M','A','S']
    sum_part = 0
    if i < 3:
        if ((row + step_row < tmp_array.shape[0]) and (row + step_row >= 0)) and ((col + step_col >= 0) and (col + step_col < tmp_array.shape[1])):
            if tmp_array[row + step_row, col + step_col] == symbols[i]:
                sum_part += search(tmp_array, row + step_row, col + step_col, i+1, step_row, step_col)
    else:
        sum_part += 1
                
    return sum_part

def search2(tmp_array, row, col):
    sum_part = 0
    if ((row < tmp_array.shape[0]-1) and (row  > 0)) and ((col  > 0) and (col < tmp_array.shape[1]-1)):
        if (((tmp_array[row + 1, col + 1] == 'M' and tmp_array[row - 1, col - 1] == 'S') or
            (tmp_array[row + 1, col + 1] == 'S' and tmp_array[row - 1, col - 1] == 'M')) and
            ((tmp_array[row - 1, col + 1] == 'M' and tmp_array[row + 1, col - 1] == 'S') or
            (tmp_array[row - 1, col + 1] == 'S' and tmp_array[row + 1, col - 1] == 'M'))):
            sum_part += 1            
    return sum_part

def day4():
    """Day 4 of Advent of code """
    # record start time
    start = time.time()

    input_txt = open_file_safely("input.txt")
    input_array = np.array([list(l) for l in input_txt])
    indexer = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, +1], [1, -1], [1, 0], [1, 1]]
    # part1
    sum_part1 = 0
    specials = np.char.find(input_array, 'X')
    for row in enumerate(specials):
        for column in enumerate(row[1]):
            if specials[row[0]][column[0]] == 0:
                for idx in indexer:
                    sum_part1 += search(input_array, row[0], column[0], 0, idx[0], idx[1])
    print(sum_part1)

    # part2
    sum_part2 = 0
    specials2 = np.char.find(input_array, 'A')
    for row in enumerate(specials2):
        for column in enumerate(row[1]):
            if specials2[row[0]][column[0]] == 0:            
                    sum_part2 += search2(input_array, row[0], column[0])
    print(sum_part2)
    
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day4()
