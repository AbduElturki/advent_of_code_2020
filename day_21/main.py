from collections import defaultdict

if __name__ == "__main__":
    with open("input.txt") as f:
        raw = [x.strip() for x in f.readlines()]
    all_ingreidents = []
    food = defaultdict(list)
    for line in raw:
        food[line[line.find("(contains")+10:-1]].append(set(line[:line.find("(")].split()))
        all_ingreidents += line[:line.find("(")].split()

    #Assign all possible allergies
    allergy_dict = {}
    for allergen in food:
        for sub_allergen in allergen.split(", "):
            if sub_allergen not in allergy_dict:
                allergy_dict[sub_allergen] = set.intersection(*food[allergen])
            else:
                allergy_dict[sub_allergen] = allergy_dict[sub_allergen]\
                        .intersection(*food[allergen])

    # Find the corresponding allergin
    for allergy_1, value_1 in allergy_dict.items():
        for allergy_2, value_2 in allergy_dict.items():
            if diff := allergy_dict[allergy_2].\
                difference(allergy_dict[allergy_1]):
                allergy_dict[allergy_2] = diff

    all_allergy = set.union(*allergy_dict.values())
    num_non_allergy = len(all_ingreidents) - sum(all_ingreidents.count(x)
                                                 for x in all_allergy)

    print("Part 1:", num_non_allergy)
    print("Part 2:", ",".join([list(allergy_dict[allergy])[0]
                               for allergy in sorted(allergy_dict.keys())]))
