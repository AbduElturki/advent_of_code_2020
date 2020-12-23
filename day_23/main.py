def PlayCrabCups(cups_list, max_round=100):
    #linked list: points to next val
    cups_dict = {}
    max_cup = max(cups_list)
    for i, cup in enumerate(cups_list):
        cups_dict[cup] = cups_list[(i + 1) % len(cups_list)]
    curr_cup = cups_list[0]
    for _ in range(max_round):
        pick_up_1 = cups_dict[curr_cup]
        pick_up_2 = cups_dict[pick_up_1]
        pick_up_3 = cups_dict[pick_up_2]

        pick_up = [curr_cup, pick_up_1, pick_up_2, pick_up_3]

        destination = curr_cup - 1
        if destination == 0:
            destination = max_cup
        while destination in pick_up:
            destination -= 1
            if destination == 0:
                destination = max_cup

        #current cup points to after pick_up_3
        cups_dict[curr_cup] = cups_dict[pick_up_3]
        #current pick_up_3 points to after destination
        cups_dict[pick_up_3] = cups_dict[destination]
        #destination points to pick up 1
        cups_dict[destination] = pick_up_1

        curr_cup = cups_dict[curr_cup]

    return cups_dict

if __name__ == "__main__":
    cups = [int(x) for x in "476138259"]
    cups_ll_100 =  PlayCrabCups(cups, 100)

    RESULT = ""
    curr_cup = cups_ll_100[1]
    while curr_cup != 1:
        RESULT += str(curr_cup)
        curr_cup = cups_ll_100[curr_cup]
    print("Part 1:", RESULT)

    cups_ll_10M = PlayCrabCups(cups + list(range(10,int(1e6)+1)), int(1e7))
    star_1 = cups_ll_10M[1]
    star_2 = cups_ll_10M[star_1]
    print("Part 2:", star_1 * star_2)
