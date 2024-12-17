"""Module providing a function reading files."""
from pathlib import Path
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
            f"The file '{file_name}' was not found in the same directory as the script.")
        return None

def operation(reg_a, reg_b, reg_c, operation_list):
    combo_op = {'0': 0, '1': 1, '2': 2, '3': 3, '4': reg_a, '5': reg_b, '6': reg_c, '7': None}
    inst_pointer = 0
    retval = ""
    while inst_pointer < len(operation_list)-1:
        if operation_list[inst_pointer] =='0':
            reg_a = reg_a // pow(2, combo_op[operation_list[inst_pointer+1]])
            combo_op['4'] = reg_a
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '1':
            reg_b = reg_b ^ int(operation_list[inst_pointer+1])
            combo_op['5'] = reg_b
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '2':
            reg_b = (combo_op[operation_list[inst_pointer+1]] % 8)
            combo_op['5'] = reg_b
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '3':
            if reg_a != 0:
                inst_pointer = int(operation_list[inst_pointer+1])
                continue
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '4':
            reg_b = reg_b ^ reg_c
            combo_op['5'] = reg_b
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '5':
            retval += str(combo_op[operation_list[inst_pointer+1]] % 8)
            retval += ','
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '6':
            reg_b = reg_a // pow(2, combo_op[operation_list[inst_pointer+1]])
            combo_op['5'] = reg_b
            inst_pointer += 2
            continue
        if operation_list[inst_pointer] == '7':
            reg_c = reg_a // pow(2, combo_op[operation_list[inst_pointer+1]])
            combo_op['6'] = reg_c
            inst_pointer += 2
            continue
    return retval[:-1]

def possible_a(operation_list):
    possibilities = {0: [x for x in range(8)]}
    for exponent in range(1, len(operation_list)):
        possibilities[exponent] = []
        for p in possibilities[exponent - 1]:
            for q in range(8):
                if p == 0:
                    continue
                ra = 8 * p + q
                out = operation(ra, 0, 0, operation_list)
                out = list(out.split(','))
                l = len(out)
                if out == operation_list[len(operation_list) - l:]:
                    possibilities[exponent].append(ra)
                if out == operation_list:
                    return ra

def day17():
    """Day 17 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt")
    reg_a, reg_b, reg_c = 0, 0, 0
    reg_a = int(input_txt[0].replace('Register A: ', ''))
    reg_b = int(input_txt[1].replace('Register B: ', ''))
    reg_c = int(input_txt[2].replace('Register C: ', ''))
    operation_list = list(x for x in list(input_txt[3].replace('Program: ', '').split(',')))
    #part1
    print("Part1: ", operation(reg_a, reg_b, reg_c, operation_list))
    #part2
    print("Part2: ",possible_a(operation_list))

    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day17()

