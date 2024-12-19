"""Module providing a function reading files."""
from pathlib import Path
import time
from functools import cache

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

def recreate_string(s, words, memo):
    if s == "":
        return True
    if s in memo:
        return memo[s]

    memo[s] = False

    for word in words:
        length = len(word)
        start = s[:length]
        rest = s[length:]
        if start == word and recreate_string(rest, words, memo):
            memo[s] = True
            break
    return memo[s]

def get_all_recreations(s, words):
    memo = {}
    def helper(s):
        if s == "":
            yield 1
        elif s in memo:
            yield memo[s]
        else:
            total_count = 0
            for word in words:
                if s.startswith(word):
                    rest = s[len(word):]
                    for sub_count in helper(rest):
                        total_count += sub_count
            memo[s] = total_count
            yield total_count

    return sum(helper(s))

def day19():
    """Day 19 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt") 
    towels = set()
    designs = []
    
    for line in input_txt:
        tmp = line.replace(' ','').split(',') 
        if len(tmp) == 1:
            designs.append(line)
        else:
            towels.update(tmp)

    #part1
    sum_pt1 = 0
    sum_pt2 = 0
    for design in designs:
        possible_towels = [towel for towel in towels if towel in design]
        #part1
        recreated_string = recreate_string(design, possible_towels, {})
        if recreated_string:
            sum_pt1 += 1
            #part2
            sum_pt2 += get_all_recreations(design,possible_towels)
    print("Part1: ", sum_pt1)
    print("Part2: ", sum_pt2)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day19()
