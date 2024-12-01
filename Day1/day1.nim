import std/algorithm
import std/strutils
import std/times

proc Day1() =
    let time = cpuTime()
    var all_distance = 0
    var id_left = newSeq[int]()
    var id_right = newSeq[int]()
    for line in lines "H:/AdventOfCode_24/Day1/input.txt":
        var temp = newSeq[string]()
        temp = split(line)     
        id_left.add(parseInt(temp[0]))
        id_right.add(parseInt(temp[^1]))

# Part  1
    id_left.sort()
    id_right.sort()

    for i,_ in id_left:
        all_distance += abs(id_left[i]-id_right[i])

    echo all_distance,'\n'

#Part 2
    var sim_score = 0
    for id in id_left:
        var match = 0
        for id_r in id_right:
            if id == id_r:
                match += 1

        sim_score += id * match
    
    echo sim_score

    echo "Time taken: ", cpuTime() - time, " seconds"

Day1()