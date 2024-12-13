"""Module providing a function reading files."""
from pathlib import Path
from functools import cache
import time

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

@cache
def blink(stone, count, cycle, maximum):
    if cycle == maximum:
        return 1
    if stone == '0':
        return blink('1', count, cycle +1, maximum)
    elif len(stone)%2 == 0:
        return blink(str(int(stone[:len(stone)//2])),count, cycle +1, maximum) + blink(str(int(stone[len(stone)//2:])), count+1, cycle +1, maximum)
    else:
        return blink(str(int(stone)*2024), count, cycle +1, maximum)

def blinker(stones, maximum):
    sum_part = 0
    for stone in stones:
        sum_part += (blink(stone, 1, 0, maximum))
    return sum_part

def day11():
    """Day 11 of Advent of code """
    # record start time
    start = time.time()
    
    input_txt = open_file_safely("input.txt")
    stones = input_txt[0].split(' ')
    #part1
    print(blinker(stones, 25))
    #part2
    print(blinker(stones, 75))

    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day11()