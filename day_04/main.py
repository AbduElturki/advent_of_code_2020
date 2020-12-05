import time
from string import hexdigits

def CleanDataToDict(raw_data):
    data_dict = []
    current_data = {}
    for data_line in raw_data:
        for entry in data_line.split():
            key, item = entry.split(":")
            current_data[key] = item
        data_dict.append(current_data)
        current_data = {}
    return data_dict

def IsValidEntries(data_dict, required=["byr", "iyr", "eyr", "hgt", 
                                         "hcl", "ecl", "pid"]):
    difference = list(set(data_dict.keys()) ^ set(required))
    return ((len(difference) == 1) and "cid" in difference) \
            or (len(difference) == 0)

def IsValidBirthYear(data_dict):
    return int(data_dict["byr"]) in range(1920,2003)

def IsValidIssueYear(data_dict):
    return int(data_dict["iyr"]) in range(2010,2021)

def IsValidExpiryYear(data_dict):
    return int(data_dict["eyr"]) in range(2020,2031)

def IsValidHeight(data_dict):
    if data_dict["hgt"][-2:] == "cm":
        return int(data_dict["hgt"][:-2]) in range(150,194)
    elif data_dict["hgt"][-2:] == "in":
        return int(data_dict["hgt"][:-2]) in range(59,77)
    else:
        return False

def IsValidHairColour(data_dict):
    if (data_dict["hcl"][0] == "#") and (len(data_dict["hcl"]) == 7):
        return all([x in hexdigits for x in data_dict["hcl"][1:]])
    else:
        return False

def IsValidEyeColour(data_dict):
    valid_clr = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    return data_dict["ecl"] in valid_clr

def IsValidPassportID(data_dict):
    return len(data_dict["pid"]) == 9

def DeleteInvalidPassports(data):
    functions = [IsValidEntries, IsValidBirthYear, IsValidIssueYear,
                 IsValidExpiryYear, IsValidHeight, IsValidHairColour, 
                 IsValidEyeColour, IsValidPassportID]
    valid_data = data.copy()

    for function in functions:
        valid_data = [x for x in valid_data if function(x)]

    return valid_data



if __name__ == "__main__":
    start_time = time.time()

    with open("input.txt") as f:
        raw = f.read()
    raw_data = [x.strip().replace("\n", " ") for x in raw.split("\n\n")]
    data = CleanDataToDict(raw_data)

    print("Part 1: {}".format(sum(map(IsValidEntries,data))))
    print("Part 2: {}".format(len(DeleteInvalidPassports(data))))

    print("--- {} seconds ---".format(round(time.time() - start_time,4)))
