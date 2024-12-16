"""Module providing a function reading files."""
from pathlib import Path
import time
import collections

step_dict = {'>': (0,1), '<': (0,-1), 'v': (1,0), '^': (-1,0)}

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

def check_range(step,robot, row, col, i):
    return (0 < i*(step_dict[step][0])+robot[0] < row) and (0 < i*(step_dict[step][1])+robot[1] < col)

def robot_step(robot, warehouse, step):
    warehouse[robot[0]][robot[1]] = '.'
    robot[0] += step_dict[step][0]
    robot[1] += step_dict[step][1]
    warehouse[robot[0]][robot[1]] = '@'

def check_further(robot, warehouse, step):
    i = 2
    not_found = True
    while check_range(step, robot, len(warehouse)-1, len(warehouse[0])-1, i) and not_found:
        if warehouse[i*step_dict[step][0]+robot[0]][i*step_dict[step][1]+robot[1]] == '.':
            for k in range(i, 0, -1):
                warehouse[(k*step_dict[step][0])+robot[0]][(k*step_dict[step][1])+robot[1]] = warehouse[((k-1)*step_dict[step][0])+robot[0]][((k-1)*step_dict[step][1])+robot[1]]
                not_found = False
            robot_step(robot, warehouse, step)
            break
        if warehouse[i*step_dict[step][0]+robot[0]][i*step_dict[step][1]+robot[1]] == '#':
            not_found = True
            break
        i += 1

def part1(input_txt):
    warehouse = []
    steps = []
    robot = []
    for i, line in enumerate(input_txt):
        tmp = list(line)
        if None is not tmp.index('@') if '@' in tmp else None:
            robot = [i, tmp.index('@')]
        if tmp[0] == '#':
            warehouse.append(tmp)
        else:
            for t in tmp:
                steps.append(t)
    sum_pt = 0 
    for step in steps:
        if check_range(step, robot, len(warehouse)-1, len(warehouse[0])-1, 1):
            if warehouse[step_dict[step][0]+robot[0]][step_dict[step][1]+robot[1]] == '.':
                robot_step(robot, warehouse, step)
            elif warehouse[step_dict[step][0]+robot[0]][step_dict[step][1]+robot[1]] == 'O':
                check_further(robot, warehouse, step)
    for i, line in enumerate(warehouse):
        if 'O' in line:
            ids = [i for i, x in enumerate(line) if x == 'O']
            for id0 in ids:
                sum_pt += 100 * i + id0
    print(sum_pt)

def check_up_down(warehouse, step, robot, pair):
    queue = []
    queue.append([step+robot[0], robot[1], step+robot[0], robot[1]+pair, pair])
    row = len(warehouse)
    col = len(warehouse[0])-1
    points = []
    boxes = []
    while queue:
        x,y, z,v, cur_pair = queue.pop()
        if warehouse[x][y] == '#' or warehouse[z][v] == '#':
            return 0
        if warehouse[x][y] == '.' and warehouse[z][v] == '.':
            points.append([x,y])
            points.append([z,v])
        else:
            if [x,y] not in boxes:
                boxes.append([x,y])
            else:
                continue
            if [z,v] not in boxes:
                boxes.append([z,v])
            else:
                continue
            if (0 < step + z < row ) and (0 < v + cur_pair < col):
                if cur_pair == -1: #left
                        if  warehouse[step+x][y] == '[' and warehouse[step+z][v] == ']':
                            queue.append([step+z, v, step+z, v+cur_pair, cur_pair])
                            queue.append([step+x, y, step+x, y+1, 1])
                        elif warehouse[step+z][v] == '[' and warehouse[step+x][y] == ']':
                            queue.append([step+z, v, step+z, v+1, 1])
                            queue.append([step+x, y, step+x, v, cur_pair])
                        elif warehouse[step+z][v] == ']' and warehouse[step+x][y] == '.':
                            queue.append([step+z, v, step+z, v+cur_pair, cur_pair])
                            points.append([step+x,y])
                        elif warehouse[step+x][y] == '[' and warehouse[step+z][v] == '.':
                            queue.append([step+x, y, step+x, y+1, 1])
                            points.append([step+z,v])
                        else:
                            queue.append([step+x, y, step+z, v, cur_pair])                 
                else: #right
                    if  warehouse[step+x][y] == ']' and warehouse[step+z][v] == '[':
                        queue.append([step+z, v, step+z, v+cur_pair, cur_pair])
                        queue.append([step+x, y, step+x, y-1, -1])
                    elif warehouse[step+z][v] == ']' and warehouse[step+x][y] == '[':
                        queue.append([step+z, v, step+z, v-1, -1])
                        queue.append([step+x, y, step+x, v, cur_pair])
                    elif warehouse[step+x][y] == ']' and warehouse[step+z][v] == '.':
                        queue.append([step+x, y, step+x, y-1, -1])
                        points.append([step+z,v])
                    elif warehouse[step+z][v] == '[' and warehouse[step+x][y] == '.':
                        queue.append([step+z, v, step+z, v+1, 1])
                        points.append([step+x,y])
                    else:
                        queue.append([step+x, y, step+z, v, cur_pair])  
    return [points, boxes]

def part2(input_txt):
    warehouse = []
    steps = []
    robot = []
    for i, line in enumerate(input_txt):
        tmp = list(line)
        if tmp[0] == '#':
            temp = []
            idx = 0
            for t in tmp:
                if t == '#':
                    temp.append(t)
                    temp.append(t)
                elif t == 'O':
                    temp.append('[')
                    temp.append(']')
                elif t == '.':
                    temp.append('.')
                    temp.append('.')
                else:
                    temp.append('@')
                    temp.append('.')
                    robot = [i, idx]
                idx += 2
            warehouse.append(temp)    
        else:
            for t in tmp:
                steps.append(t)
    sum_pt = 0 
    for step in steps:
        if check_range(step, robot, len(warehouse)-1, len(warehouse[0])-2, 1):
            if warehouse[step_dict[step][0]+robot[0]][step_dict[step][1]+robot[1]] == '.':
                robot_step(robot, warehouse, step)
            elif warehouse[step_dict[step][0]+robot[0]][step_dict[step][1]+robot[1]] != '#':
                if step == '<' or step == '>':
                    check_further(robot, warehouse, step)
                else:
                    if warehouse[step_dict[step][0]+robot[0]][step_dict[step][1]+robot[1]] == ']':
                        tmp = check_up_down(warehouse, step_dict[step][0], robot, -1)
                    else:
                        tmp = check_up_down(warehouse, step_dict[step][0], robot, 1)
                    if tmp:
                        points = tmp[0]
                        boxes = tmp[1]
                        if len(points) > 1 and boxes:
                            while(boxes):
                                for p in points:
                                    if [p[0]-step_dict[step][0], p[1]] in boxes:
                                        idx = boxes.index([p[0]-step_dict[step][0], p[1]])
                                        if idx is not None:
                                            warehouse[boxes[idx][0]][boxes[idx][1]], warehouse[p[0]][p[1]] = warehouse[p[0]][p[1]], warehouse[boxes[idx][0]][boxes[idx][1]]
                                            p[0] -= step_dict[step][0]
                                            boxes.pop(idx)
                            robot_step(robot, warehouse, step)                  
    for i, line in enumerate(warehouse):
        if '[' in line:
            ids = [i for i, x in enumerate(line) if x == '[']
            for id0 in ids:
                sum_pt += 100 * i + id0
    print(sum_pt)

def day14():
    """Day 14 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt")
    #part1
    part1(input_txt)   
    #part2  
    part2(input_txt)        
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day14()
