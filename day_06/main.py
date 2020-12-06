import time

if __name__ == "__main__":
    start_time = time.time()

    with open("input.txt") as f:
        raw_data = f.read().rstrip()

    #Split groups by "\n\n" and split each person by "\n"
    data_per_group = [x.split("\n") for x in raw_data.split("\n\n")]

    #Combine each person with its group and cast set. get len of each set.
    unique_ans = sum([len(set("".join(x))) for x in data_per_group])
    #Cast set to each person and find intersect of each group.
    common_ans = sum([len(set.intersection(*map(set,x)))
                      for x in data_per_group])

    print("Part 1: number of unique answers per group:", unique_ans)
    print("Part 2: number of common answers per group:", common_ans)

    print("--- {} seconds ---".format(round(time.time() - start_time,4)))
