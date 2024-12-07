"""Module providing a function reading files."""
from pathlib import Path
import time
import copy

stepmap = {'^':[-1, 0, '|'],
           '<':[0, -1, '-'],
           '>':[0, 1, '-'],
           'v':[1, 0, '|']}

turnmap = {'^':'>',
           '<':'^',
           '>':'v',
           'v':'<'}
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

def move(guard, lab, step_row, step_col, step):
    temp_guard = copy.deepcopy(guard)
    turn = False
    temp = ''
    while ((temp_guard[0] < len(lab)-1) and (temp_guard[0] > 0)) and ((temp_guard[1] > 0) and (temp_guard[1] < len(lab)-1)):
        if lab[temp_guard[0]][temp_guard[1]] == lab[temp_guard[0]+step_row][temp_guard[1]+step_col] or temp == lab[temp_guard[0]+step_row][temp_guard[1]+step_col]:
            return lab, True
        else:
            if lab[temp_guard[0]+step_row][temp_guard[1]+step_col] != '#':   
                if turn:
                    lab[temp_guard[0]+step_row][temp_guard[1]+step_col] = temp
                else:
                    lab[temp_guard[0]+step_row][temp_guard[1]+step_col],  lab[temp_guard[0]][temp_guard[1]] = lab[temp_guard[0]][temp_guard[1]], step
                temp_guard[0] += step_row
                temp_guard[1] += step_col
                turn =  False
            else:
                if turn:
                    temp = turnmap[temp]
                else:
                    temp = turnmap[lab[temp_guard[0]][temp_guard[1]]]
                step_row = stepmap[temp][0]
                step_col = stepmap[temp][1]  
                step = stepmap[temp][2]
                turn = True
    return lab, False

def day6():
    """Day 6 of Advent of code """
    # record start time
    start = time.time()

    input_txt = open_file_safely("input.txt")
    lab = []
    guard = [0, 0]
    for line in input_txt:
        lab.append(list(x for x in line))

    for idx, lst in enumerate(lab):
        if '^' in lst:
            guard[0] = idx
            guard[1] = lst.index('^')
    lab2 = copy.deepcopy(lab)
    guard2 = copy.deepcopy(guard)
    
    # part1
    sum_part1 = 0
    lab,_ = move(guard, lab, stepmap[lab[guard[0]][guard[1]]][0], stepmap[lab[guard[0]][guard[1]]][1], stepmap[lab[guard[0]][guard[1]]][2])  
    for line in lab:
        sum_part1 += sum([i.count('.') for i in line])
        sum_part1 += sum([i.count('#') for i in line])
    print(len(lab)*len(lab)-sum_part1)

    # part2
    sum_part2 = 0
    for i, line in enumerate(lab2):
        for j,_ in enumerate(lab2):
            temp_lab = copy.deepcopy(lab2)
            loop = False
            if [i, j] != guard2 and temp_lab[i][j] != '#' and lab[i][j] != '.':
                temp_lab[i][j] = '#'
                _,loop = move(guard2, temp_lab, stepmap[temp_lab[guard2[0]][guard2[1]]][0], stepmap[temp_lab[guard2[0]][guard2[1]]][1], stepmap[temp_lab[guard2[0]][guard2[1]]][2])  
                if loop:
                    sum_part2 += 1
                    
    print(sum_part2)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day6()