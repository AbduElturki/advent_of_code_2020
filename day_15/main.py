def GetTurn(inital_turns, max_turns):
    memory = inital_turns.copy()
    last_turns = {}

    #The inital puzzle input without the last number
    for turn, num in enumerate(inital_turns[:-1]):
        last_turns[num] = turn + 1

    #Start solving at the last digit.
    for turn in range(len(memory),max_turns):
        last_num = memory[-1]
        if last_num in last_turns:
            memory.append(turn  - last_turns[last_num])
        else:
            memory.append(0)
        last_turns[last_num] = turn

    return memory[-1]


if __name__ == "__main__":
    puzzle = [0,14,1,3,7,9]
    print("Part 1:", GetTurn(puzzle,2020))
    print("Part 2:", GetTurn(puzzle, 30000000))
