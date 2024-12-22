from pathlib import Path
import time
from collections import defaultdict

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

def mix(result, secret):
    return result ^ secret

def prune(secret):
    return secret % 16777216

def evolve_secret(secret):
    tmp = secret*64
    secret = prune(mix(secret, tmp))
    tmp = secret//32
    secret = prune(mix(secret, tmp))
    tmp = secret*2048
    secret = prune(mix(secret, tmp))
    return secret

def day22():
    """Day 22 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt") 
    secret_nums = list(int(x) for x in input_txt) 
    banana_list = []
    change_list = []
    #part1
    sum_pt1 = 0
    for num in secret_nums:
        tmp_banana_list = []
        tmp_banana_list.append(int(str(num)[-1]))
        for _ in range(2000):
            num = evolve_secret(num)
            tmp_banana_list.append(int(str(num)[-1]))
        sum_pt1 += num
        change_list.append(list(tmp_banana_list[i+1]-tmp_banana_list[i] for i in range(len(tmp_banana_list)-1)))
        banana_list.append(tmp_banana_list)
    print("Part1: ", sum_pt1)
    #part2
    sequences = defaultdict(int)
    for i in range(len(secret_nums)):
        seen = set()
        for j in range(len(banana_list[i]) - 4):
            cur = tuple(change_list[i][j : j + 4])
            if cur in seen:
                continue
            seen.add(cur)
            sequences[cur] += banana_list[i][j + 4]
    print(max(sequences.values()))

    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day22()
