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
            "The file '{file_name}' was not found in the same directory as the script.")
        return None
    
def check_pages(pages_coll, ruleset):
    incorrect = []
    sum_part = 0
    for j, pages in enumerate(pages_coll):
        tmp_incorrect, sum_part = check_page(j, pages, ruleset, sum_part)
        if tmp_incorrect:
            incorrect.append(tmp_incorrect)
    return sum_part, incorrect
    
def check_page(j, pages, ruleset, sum_part):
    length = 0
    temp = []
    incorrect = []
    for i, page in enumerate(pages):
        value_found = 0
        if page in ruleset.keys():
            temp_length = 0
            for value in ruleset[page]:
                if value in pages:
                    value_found += 1
                    value_index = pages.index(value)
                    if i < value_index:
                        temp_length += 1
                    else:
                        temp.append((page,value))
            if value_found == temp_length:
                length += 1
        else:
            length += 1
    if length == len(pages):
        sum_part += int(pages[int(length/2)])
    else:
        incorrect.append((j, temp))
    return incorrect, sum_part
        
def day5():
    """Day 5 of Advent of code """
    # record start time
    start = time.time()

    input_txt = open_file_safely("input.txt")
    ruleset = dict()
    pages_coll = []
    for line in input_txt:
        if line == '':    
            break
        else:
            tmp = line.split('|')
            if len(tmp) == 2:
                if tmp[0] in ruleset:
                    ruleset[tmp[0]].append(tmp[1])
                else:
                    ruleset[tmp[0]] = [tmp[1]]
            else:
                pages_coll.append(line.split(','))
 
    # part1
    sum_part1 = 0
    incorrect_pages = []
    sum_part1, incorrect_pages = check_pages(pages_coll, ruleset)
                
    print(sum_part1)
    
    # part2
    sum_part2 = 0
    for page in  incorrect_pages:
        temp_page = page[0]
        while temp_page:
            for incorrect in temp_page[1]:
                id1 = pages_coll[temp_page[0]].index(incorrect[0])
                id2 = pages_coll[temp_page[0]].index(incorrect[1])
                pages_coll[temp_page[0]][id1], pages_coll[temp_page[0]][id2] =  pages_coll[temp_page[0]][id2], pages_coll[temp_page[0]][id1]
            temp, _ = check_page(temp_page[0],  pages_coll[temp_page[0]], ruleset, 0)
            if temp:
                temp_page = temp[0]
            else:
                temp_page = temp
        sum_part2 += int(pages_coll[page[0][0]][int(len(pages_coll[page[0][0]])/2)])
 
    print(sum_part2)
    
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day5()