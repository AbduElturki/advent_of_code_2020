import time

def TwoSum(numbers: list, value: int):
    l = 0
    r = len(numbers) - 1
    numbers.sort()
    while l != r:
        if ((numbers[l] + numbers[r]) > value):
            r = r-1
        elif ((numbers[l] + numbers[r]) < value):
            l = l+1
        else:
            return numbers[l],numbers[r]
    return None,None

def ThreeSum(numbers: list, value: int):
    for i in range(len(numbers)):
        x = numbers[i]
        temp_value = value - numbers[i]
        y,k = TwoSum(numbers[i:], temp_value)
        if (y is not None) and (k is not None):
            return x,y,k
    return None, None, None


if __name__ == "__main__":
    start_time = time.time()
    with open("input.txt") as f:
        numbers = f.readlines()
    numbers = [int(x.strip()) for x in numbers]

    x1,y1 = TwoSum(numbers, 2020)
    print("Part 1: x: {}, y: {}, x+y: {}, x*y: {}"
          .format(x1,y1,(x1+y1),(x1*y1)))

    x2,y2,k2 = ThreeSum(numbers,2020)
    print("Part 2: x: {}, y: {}, k:{}, x+y+k: {}, x*y*k: {}"
          .format(x2,y2,k2,(x2+y2+k2),(x2*y2*k2)))

    print("--- {} seconds ---".format(round(time.time() - start_time,4)))
