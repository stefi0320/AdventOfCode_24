"""Module providing a function reading files."""
from pathlib import Path
import time

switch_op = {'+': '*', "*" : "+"}
switch_op2 = {'+': ['*', '|'], "*" : ["+", '|'], '|': ['+', "*"] }

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

def operator_combiner(inp, result, operator, idx, res):
    retval = False
    returned = False

    if operator == '+':
        result += int(inp[idx])
    else:
        result *= int(inp[idx])
    if result == res and idx == len(inp) -1:
        return True, True
    else: 
        if result <= res:
            if idx + 1 < len(inp):
                retval, returned = operator_combiner(inp, result, operator, idx+1, res)
                if retval:
                    return True, True
            else:
                return False, True
        if returned and idx + 1 < len(inp):
            retval, returned = operator_combiner(inp, result, switch_op[operator], idx+1, res)
            if retval:
                return True, True
        else:
            return False, True
    
    return retval, returned

def operator_combiner2(inp, result, operator, idx, res):
    retval = False
    returned = False

    if operator == '+':
        result += int(inp[idx])
    elif operator == '*':
        result *= int(inp[idx])
    else:
        result = int(str(result) + inp[idx])
    if result == res and idx == len(inp) -1:
        return True, True
    else: 
        if result <= res:
            if idx + 1 < len(inp):
                retval, returned = operator_combiner2(inp, result, operator, idx+1, res)
                if retval:
                    return True, True
            else:
                return False, True
        if returned and idx + 1 < len(inp):
            retval, returned = operator_combiner2(inp, result, switch_op2[operator][0], idx+1, res)
            if retval:
                return True, True
            retval, returned = operator_combiner2(inp, result, switch_op2[operator][1], idx+1, res)
            if retval:
                return True, True
        else:
            return False, True
    
    return retval, returned

def day7():
    """Day 7 of Advent of code """
    # record start time
    start = time.time()

    input_txt = open_file_safely("input.txt")
    input_list = []
    input_wrong = []
    for line in input_txt:
        tmp = line.split(': ')
        input_list.append([int(tmp[0]), list(x for x in tmp[1].split(' '))])

    # part1
    sum_part1 = 0
    for i in input_list:
        good = False
        good, _ = operator_combiner(i[1], 0, '+', 0, i[0])
        if good:
            sum_part1 += i[0]
        else:
            input_wrong.append(i)

    print(sum_part1)

    # part2
    sum_part2 = 0
    for i in input_wrong:
        good = False
        good, _ = operator_combiner2(i[1], 0, '+', 0, i[0])
        if good:
            sum_part2 += i[0]

    print(sum_part1+sum_part2)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day7()