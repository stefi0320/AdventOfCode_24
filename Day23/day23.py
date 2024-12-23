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

def day23():
    """Day 23 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt")
    port_connections = defaultdict(list)
    lan_groups = []
    sum_pt1 = 0
    for line in input_txt:
        line = line.split("-")
        if line[0] not in port_connections:
            port_connections[line[0]] = [line[1]]
        else:
            port_connections[line[0]].append(line[1])
        if line[1] not in port_connections:
            port_connections[line[1]] = [line[0]]
        else:
            port_connections[line[1]].append(line[0])
    #part1
    for port in sorted(port_connections.keys()):
        for item in port_connections[port]:
            for port2 in port_connections[item]:
                if (port2 in port_connections[port]):
                    if sorted([port, item, port2]) not in lan_groups:
                        lan_groups.append(sorted([port, item, port2]))
                        if port[0] == 't' or item[0] == 't' or port2[0] == 't':
                            sum_pt1 += 1
    
    print("Part1: ", sum_pt1)
    #part2
    lan = {}
    for key in sorted(port_connections):
        tmp = [key]
        common_items = [key]
        for item in sorted(port_connections[key]):
            temp = [ e for e in port_connections[key] if e in port_connections[item] ]
            if temp:
                for i in [ e for e in port_connections[key] if e in port_connections[item] ]:
                    if i not in common_items:
                        common_items.append(i)
                tmp.append(item)
        if sorted(tmp) == sorted(common_items):
            if ','.join(sorted(common_items)) not in lan:
                lan[','.join(sorted(common_items))] = 1
            else:
                lan[','.join(sorted(common_items))] += 1
      
    for key, value in lan.items():
        if value == len(key.split(',')):
            print("Part2: ", key)
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day23()
