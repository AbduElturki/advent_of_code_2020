import time

def isValidRepeats(minimum, maximum, char, password):
    return int(minimum) <= password.count(char) <= int(maximum)

def isValidPosition(x, y, char, password):
    return (char is password[int(x)-1])^(char is password[int(y)-1])

if __name__ == "__main__":
    start_time = time.time()

    with open("input.txt") as f:
        text = f.readlines()
    text = [x.strip().replace(':','').replace('-',' ').split() for x in text]

    num_valid_repeats = sum([isValidRepeats(*x) for x in text])
    print("Part 1 answer: {}".format(num_valid_repeats))
    num_valid_pos = sum([isValidPosition(*x) for x in text])
    print("Part 2 answer: {}".format(num_valid_pos))

    print("--- {} seconds ---".format(round(time.time() - start_time,4)))
