# Copyright 2020.

import std/times
import std/re
import std/strutils
from std/sequtils import map

proc Day3() =
    let time = cpuTime()
    var safe = newseq[string]()
    var result = 0
    # Part  1
    for line in lines "H:/AdventOfCode_24/Day3/input.txt":
        safe = findAll(line, re"mul\(\d*,\d*\)", 0)
    for item in safe:
        let temp = item.replace(re"mul\(").replace(re"\)").split(',').map(parseInt)
        result += temp[0] * temp[1]
    echo result 
      
    #Part 2
    result = 0
    for line in lines "H:/AdventOfCode_24/Day3/input.txt":
        let donts = line.split(re"don\'t\(\)")
        safe = findAll(donts[0], re"mul\(\d*,\d*\)", 0)
        for item in safe:
            let temp = item.replace(re"mul\(").replace(re"\)").split(',').map(parseInt)
            result += temp[0] * temp[1]

        for j in 1 ..< donts.len:
            let dos = donts[j].split(re"do\(\)")
            for i in 1 ..< dos.len:
                safe = findAll(dos[i], re"mul\(\d*,\d*\)", 0)
                for item in safe:
                    let temp = item.replace(re"mul\(").replace(re"\)").split(',').map(parseInt)
                    result += temp[0] * temp[1]
        echo result 
    echo "Time taken: ", cpuTime() - time, " seconds"

Day3() 