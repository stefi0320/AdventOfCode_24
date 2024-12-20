"""Module providing a function reading files."""
from pathlib import Path
import time
import numpy as np

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

def day20():
    """Day 20 of Advent of code """
    # record start time
    start = time.time()  
    input_txt = open_file_safely("input.txt") 
    racetrack = np.array([list(val.strip()) for val in input_txt])
    distanceMap = np.zeros_like(racetrack,int)
    ds = ((1,0),(-1,0),(0,1),(0,-1))
    i,j = [val[0] for val in np.where(racetrack=='S')]
    racetrack = np.logical_or(racetrack=="E",racetrack==".")
    distanceMap[i,j] = 1
    currVal = 1
    while True:
        for di,dj in ds:
            if racetrack[i+di,j+dj] and not distanceMap[i+di,j+dj]:
                currVal += 1
                distanceMap[i+di,j+dj] = currVal
                i,j = i+di, j+dj
                break
        else:
            break
    iGrid, jGrid = np.ogrid[:racetrack.shape[0],:racetrack.shape[1]]
    i,j = np.where(distanceMap)
    manhattanDistances = np.abs(i-iGrid[:,:,np.newaxis]) + np.abs(j - jGrid[:,:,np.newaxis])
    #part1
    mask1 = manhattanDistances <= 2
    diff = distanceMap[:,:,np.newaxis] - distanceMap[i,j]
    results = diff-manhattanDistances
    print(np.sum(results[mask1]>=100))
    #part2
    mask2 = manhattanDistances <= 20
    print(np.sum(results[mask2]>=100))
    # record end time
    end = time.time()
    print("Runtime :", (end-start) * 10**3, "ms")

day20()
