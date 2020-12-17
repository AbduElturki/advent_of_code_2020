import re

from functools import reduce

def ParseValidField(raw_data):
    fields = {}
    for data in raw_data:
        field_name = data[:data.index(":")]
        valid_num = re.findall(r"\d+", data)
        fields[field_name] = [range(int(valid_num[0]), int(valid_num[1]) + 1),
                              range(int(valid_num[2]), int(valid_num[3]) + 1)]
    return fields


def GetAllInvalidNumbers(tickets, fields):
    invalid_num = []
    for ticket in tickets:
        for num in ticket:
            if not any([((num in first) or (num in second))
                        for first, second in fields.values()]):
                invalid_num.append(num)
    return invalid_num


def GetValidTickets(tickets, invalid_nums):
    valid_tickets = []
    for ticket in tickets:
        if not any([num in invalid_nums for num in ticket]):
            valid_tickets.append(ticket)
    return valid_tickets


def FindFields(tickets, fields):
    all_possible_fields = []

    for col in range(len(fields.keys())):
        possible_fields = set()
        column_data = [ticket[col] for ticket in tickets]
        for field, ranges in fields.items():
            if all([((num in ranges[0]) or (num in ranges[1])) \
                    for num in column_data]):
                possible_fields.add(field)
        all_possible_fields.append((col, possible_fields))

    all_possible_fields.sort(key=lambda x: len(x[1]),reverse=True)

    for i, order_field_pair in enumerate(all_possible_fields[:-1]):
        all_possible_fields[i] = (order_field_pair[0],
                          order_field_pair[1] - all_possible_fields[i+1][1])

    ordered_fields = [list(field)[0] for _, field in
                      sorted(all_possible_fields, key=lambda x: x[0]) ]
    return ordered_fields


if __name__ == "__main__":
    with open("input.txt") as f:
        raw_data = f.read().split("\n\n")

    raw_fields = raw_data[0].strip().split("\n")

    fields_dict = ParseValidField(raw_fields)
    my_ticket = [int(x) for x in raw_data[1].strip().split("\n")[1].split(",")]
    nearby_ticket = [list(map(int,x.split(","))) for x in
                     raw_data[2].strip().split("\n")[1:]]

    invalid_nums = GetAllInvalidNumbers(nearby_ticket, fields_dict)
    valid_tickets = GetValidTickets(nearby_ticket, invalid_nums)
    field_columns = FindFields(valid_tickets,fields_dict)

    my_ticket_labeled = dict(zip(field_columns, my_ticket))

    mul_depart = reduce(lambda x,y: x*y,[my_ticket_labeled[field]
        for field in list(fields_dict.keys()) if field.startswith("depart")])

    print("Part 1:", sum(invalid_nums))
    print("Part 2:", mul_depart)
