import time
from functools import reduce

def CountTrees(puzzle: list, right: int, down: int):
    num_tress = 0
    width = len(puzzle[0])
    position = right
    for row in range(down, len(puzzle), down):
        if puzzle[row][position] == '#': num_tress = num_tress + 1
        position = (position + right) % width
    return num_tress

if __name__ == "__main__":
    start_time = time.time()

    with open("input.txt") as f:
        text = f.readlines()
    text = [x.strip() for x in text]

    part_1 = CountTrees(text, 3, 1)
    print("Part 1: {}".format(part_1))
    
    paths = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    part_2 = reduce((lambda x,y: x*y), [CountTrees(text, x[0], x[1]) 
                                       for x in paths])
    print("Part 2: {}".format(part_2))

    print("--- {} seconds ---".format(round(time.time() - start_time,4)))
