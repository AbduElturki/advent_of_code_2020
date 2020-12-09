def FindEncodingError(encoded_message, window_size):
    start = 0
    end = window_size + 1
    while end < len(encoded_message):
        window = encoded_message[start:end]
        subtracted_list = [abs(x-window[-1]) for x in window[:-1]]
        if not(any([x in window[:-1] for x in subtracted_list])):
            return window[-1]
        start += + 1
        end += 1
    print("No errors found...")
    return None

def FindContigousError(encoded_message, error_value):
    if not error_value:
        raise Exception("Invalid Error value {}".format(error_value))
    for idx in range(len(encoded_message)):
        contigous_list = []
        tmp_idx = idx
        while sum(contigous_list) < error_value:
            contigous_list.append(encoded_message[tmp_idx])
            tmp_idx += 1
        if sum(contigous_list) > error_value:
            continue
        else:
            return min(contigous_list), max(contigous_list)
    raise Exception("Can't find the contigous set that sums to {}"\
                    .format(error_value))


if __name__ == "__main__":
    with open("input.txt") as f:
        encoded_message = [int(x.strip()) for x in f.readlines()]
    invalid_num = FindEncodingError(encoded_message, 25)
    min_num, max_num = FindContigousError(encoded_message, invalid_num)

    print("Part 1: the first invalid number found", invalid_num)
    print("Part 2: the sum of smallest and largest in contigous range",
          min_num + max_num)
