def ParseDockingData(raw_lines):
    docking_data = []
    for line in raw_lines:
        docking_data.append(line.replace("["," ").replace("]","")\
                            .replace("= ", "").split())
    return docking_data

def FloatingMask(xs, num):
    rtn_addresses = []
    num_xs = xs.count('X')
    find_char = lambda s, ch: [i for i, ltr in enumerate(s) if ltr == ch]
    idx_to_replace = find_char(xs, "X")
    for floating_digits in range(2**num_xs):
        base2_digits = "{0:0{1}b}".format(floating_digits, num_xs)
        temp_num = list("{0:0{1}b}".format(num,36))
        for i, j in enumerate(idx_to_replace):
            temp_num[j] = base2_digits[i]
        rtn_addresses.append(int("".join(temp_num),2))
    return rtn_addresses


def ExecuteDockingProgam(docking_data):
    # 0: Normal, 1: Floating
    mem = [{}, {}]
    mask_x = "0" * 36
    mask_0 = int("1" * 36,2)
    mask_1 = 0
    for instruction in docking_data:
        if instruction[0] == "mem":
            # Normal
            value_masked_by_1 = mask_1 | int(instruction[2])
            value_masked_by_0 = mask_0 & value_masked_by_1
            mem[0][instruction[1]] = mask_1 | value_masked_by_0
            
            #Floating
            address_masked_by_1 = mask_1 | int(instruction[1])
            write_addresses = FloatingMask(mask_x, address_masked_by_1)
            for address in write_addresses:
                mem[1][address] = int(instruction[2])
        elif instruction[0] == "mask":
            mask_x = instruction[1]
            mask_0 = int(instruction[1].replace("X","1"),2)
            mask_1 = int(instruction[1].replace("X","0"),2)
    return mem


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [x.strip() for x in f.readlines()]
    data = ParseDockingData(lines)
    normal, floating = ExecuteDockingProgam(data)
    print("Part 1:", sum(normal.values()))
    print("Part 2:", sum(floating.values()))
