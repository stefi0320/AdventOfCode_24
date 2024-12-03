import std/strutils
import std/times
import std/sugar
import sequtils

proc checkNums(nums: seq[int]): bool =
    var diff: seq[int] = @[]
    for i in 0 ..< nums.len-1:
        diff.add(nums[i+1] - nums[i])
    let monotonic = (diff.allIt(it > 0) or diff.allIt(it < 0))
    return diff.allIt(it >= -3 and it <= 3 and abs(it) >= 1) and monotonic

proc customCheck(nums: seq[int]): bool =
  for i in 0 ..< nums.len:
    let subNums = nums[0..i-1] & nums[i+1..^1] # Create a new sequence excluding the i-th element
    if checkNums(subNums):
      return true
  return false

proc Day2() =
    let time = cpuTime()
    var safe = 0
    var unsafe = 0
    var safe2 = 0
    var unsafe2 = 0
    for line in lines "H:/AdventOfCode_24/Day2/input.txt":
        let temp = collect(newseq):
            for val in split(line):
                parseInt(val)
        # Part  1
        if checkNums(temp) == true:
            safe += 1
        else:
            unsafe += 1       
        #Part 2
        if customCheck(temp) == true:
            safe2 += 1
        else:
            unsafe2 += 1

    echo "safe: ", safe, ", unsafe: ", unsafe
    echo "dampened safe: ", safe2, ", unsafe: ", unsafe2
    echo "Time taken: ", cpuTime() - time, " seconds"

Day2() 