def GetNumAdapters(jolts):
    current_output = 0
    one_jolt_diff, two_jolt_diff, three_jolt_diff = 0, 0, 0
    for adapter in jolts:
        difference = adapter - current_output
        if difference == 0:
            # This case doesn't really exist but feels right...
            continue
        elif difference == 1:
            one_jolt_diff += 1
        elif difference == 2:
            two_jolt_diff += 1
        elif difference == 3:
            three_jolt_diff += 1
        else:
            break
        current_output = adapter
    return one_jolt_diff, two_jolt_diff, three_jolt_diff


def GetNumArrangements(jolts,idx, his_dict=None):
    if his_dict == None:
        his_dict = {}
    if idx == len(jolts) - 1:
        return 1
    if jolts[idx] in his_dict:
        return his_dict[jolts[idx]]
    num_arrangements = 0
    for j in range(idx+1, min(idx+4,len(jolts))): 
        if jolts[j]-jolts[idx]<=3:
            num_arrangements += GetNumArrangements(jolts,j,his_dict)
    his_dict[jolts[idx]] = num_arrangements
    return num_arrangements


if __name__ == "__main__":
    #with open("example") as f:
    with open("input.txt") as f:
        jolts = [int(x.strip()) for x in f.readlines()]

    jolts.append(0)
    jolts.append(max(jolts)+3)
    jolts.sort()

    one, _, three = GetNumAdapters(jolts)
    num_arrangements = GetNumArrangements(jolts, 0)

    print("Part 1:", one * three)
    print("Part 2:", num_arrangements)
