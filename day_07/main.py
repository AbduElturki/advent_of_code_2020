import re
from collections import defaultdict 

def ParseBags(lines):
    '''
    lines: list

    returns type dictonary

    Parses the lines from the puzzle and converts them to dictonary.
    If the bag contains no other bags it will hold value None.
    Otherwise, it will contain a dictonary that contain sub-bags which mapped
    to their quantity.
    The key is also converted to singular instead of plural so the key/naming
    will consistant.
    '''
    bag_dict = {} 
    for line in lines:
        key_and_items_split = line.split(" contain ")
        key = key_and_items_split[0][:-1]
        if (key_and_items_split[1] == "no other bags."):
            bag_dict[key] = None
        else:
            items = key_and_items_split[1].replace(".","").split(", ")
            bag_dict[key] = {}
            for bag in items:
                sub_bag_key = re.search("[A-z][A-z ]+", bag).group(0)
                sub_bag_item = int(re.search("[0-9]+", bag).group(0))
                if sub_bag_item > 1:
                    sub_bag_key = sub_bag_key[:-1]
                bag_dict[key][sub_bag_key] = sub_bag_item
    return bag_dict

def CountShinyBags(bag_dict, bag):
    if bag_dict[bag] == None:
        return 0
    elif "shiny gold bag" in bag:
        return 1
    else: 
        for sub_bag in bag_dict[bag].keys():
            if CountShinyBags(bag_dict, sub_bag):
                return 1
        return 0

def CountBagsInsideShinyBag(bag_dict, bag):
    num_bags = 0
    for sub_bag, quantity in bag_dict[bag].items():
        if bag_dict[sub_bag] == None:
            num_bags = num_bags + quantity 
        else:
            num_bags = num_bags + quantity + \
                    (quantity * CountBagsInsideShinyBag(bag_dict,sub_bag))
    return num_bags

if __name__ == "__main__":
    with open("example") as f:
        lines = [x.strip() for x in f.readlines()]
    
    bag_dict = ParseBags(lines)
    
    total = 0
    for bag in bag_dict.keys():
        if bag == "shiny gold bag":
            continue
        total = total + CountShinyBags(bag_dict, bag)

    print(total)
    print(CountBagsInsideShinyBag(bag_dict, "shiny gold bag"))

