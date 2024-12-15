"""Module providing a function reading files."""
from pathlib import Path
import time
from collections import namedtuple
    
Point = namedtuple('point', 'X, Y')
Machine = namedtuple('machine', 'A, B, res')
    
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
    
def solve_coast(machine):
    res_a = ((machine.res.X * machine.B.Y) - (machine.res.Y * machine.B.X)) / ((machine.A.X * machine.B.Y)- (machine.A.Y * machine.B.X))
    res_b = ((machine.res.Y * machine.A.X) - (machine.res.X * machine.A.Y)) / ((machine.A.X * machine.B.Y)- (machine.A.Y * machine.B.X))
    if res_a.is_integer() and res_b.is_integer():
        return int(res_a) * 3 + int(res_b) * 1
    else:
        return 0

def day13():
    """Day 13 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt")
    slot_machine = []
    i = 0
    while i < len(input_txt):
        tmp = input_txt[i].replace(',', '').split(' ')
        tmp2 = input_txt[i+1].replace(',', '').split(' ')
        tmp3 = input_txt[i+2].replace(',', '').split(' ')        
        slot_machine.append(Machine(A=Point(int(tmp[2].replace('X+','')),int(tmp[3].replace('Y+',''))), B=Point(int(tmp2[2].replace('X+','')),int(tmp2[3].replace('Y+',''))), res=Point(int(tmp3[1].replace('X=', '')), int(tmp3[2].replace('Y=', '')))))
        i+= 3
    #part1
    sum_pt1, sum_pt2 = 0, 0
    
    for machine in slot_machine: 
        sum_pt1 += solve_coast(machine)
    
    print(sum_pt1)
    #part2
    for machine in slot_machine: 
        sum_pt2 += solve_coast(Machine(machine.A, machine.B, Point(machine.res.X+ 10000000000000,  machine.res.Y+10000000000000)))
    
    print(sum_pt2)
    
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day13()
