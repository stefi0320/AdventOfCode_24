"""Module providing a function reading files."""
from pathlib import Path
import time
import sys

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
def part1(disk_map):
    sum_part1 = 0
    j = len(disk_map) - 1
    i = 0
    while i < j:
        if disk_map[i] == '.':
            if disk_map[j] == '.':
                j -= 1
            else:
                disk_map[i], disk_map[j] = disk_map[j], disk_map[i]
                j -= 1
                i += 1
        else:
            i += 1
    for k, char in enumerate(disk_map):
        if char != '.':
            sum_part1 += k * int(char)
    return sum_part1

def day9():
    """Day 9 of Advent of code """
    # record start time
    start = time.time()

    sys.set_int_max_str_digits(0)
    input_txt = open_file_safely("input.txt")

    disk_map = []
    disk_map2 = []
    eid = 0
    fid = 0
    for i, char in enumerate(input_txt[0]):
        if char != '0':
            if i%2 == 0:
                for _ in range(int(char)):
                    disk_map.append(str(fid))
                disk_map2.append([str(fid), int(char)])
                fid += 1
            else:
                for _ in range(int(char)):
                    disk_map.append('.')
                disk_map2.append(['.', int(char)])
            eid += 1
    #part1
    print(part1(disk_map))

    # part2
    sum_part2 = 0
    visited = []
    j = next((k for k in range(len(disk_map2)-1, -1, -1) if disk_map2[k][0] != '.'), None)
    i = next((l for l, item in enumerate(disk_map2) if item[0] == '.'), None)
    while j > 0:
        if i < j:
            if disk_map2[i][1] == disk_map2[j][1]:
                visited.append(disk_map2[j][0])
                disk_map2[i], disk_map2[j] = disk_map2[j], disk_map2[i]
                j = next((k for k in range(j-1, 0, -1) if disk_map2[k][0] != '.' and disk_map2[k][0] not in visited), 0)
                if j != 0:
                    i = next((l for l in range(0, j) if disk_map2[l][0] == '.'), j)
            elif disk_map2[i][1] > disk_map2[j][1]:
                visited.append(disk_map2[j][0])
                diff = disk_map2[i][1]-disk_map2[j][1]
                disk_map2[i] = disk_map2[j]
                disk_map2[j] = ['.', disk_map2[j][1]]
                disk_map2.insert(i+1, ['.', diff])
                j = next((k for k in range(j, 0, -1) if disk_map2[k][0] != '.' and disk_map2[k][0] not in visited), 0)
                if j != 0:
                    i = next((l for l in range(0, j) if disk_map2[l][0] == '.'), j)
            else:
                i = next((l for l in range(i+1 , j) if disk_map2[l][0] == '.'), j)
        else:
            visited.append(disk_map2[j][0])
            j = next((k for k in range(j-1, 0, -1) if disk_map2[k][0] != '.' and disk_map2[k][0] not in visited), 0)
            if j != 0:
                i = next((l for l in range(0, j) if disk_map2[l][0] == '.'), j)
    idx = 0
    for item in disk_map2:
        if item[0] != '.':
            for i in range(item[1]):
                sum_part2 += idx * int(item[0])
                idx += 1
        else:
            idx += item[1] 
    print(sum_part2)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day9()