from copy import deepcopy

class SimpleSeatingPlan:

    def __init__(self, seating_input):
        self.seating = seating_input

    def __iter__(self):
        return self

    def __next__(self):
        temp_seating = deepcopy(self.seating)
        for row_idx in range(len(self.seating)):
            for column_idx in range(len(self.seating[0])):
                if self.seating[row_idx][column_idx] == "L":
                    if self.GetSurrounding(row_idx, column_idx) == 0:
                        temp_seating[row_idx][column_idx] = "#"
                elif self.seating[row_idx][column_idx] == "#":
                    if self.GetSurrounding(row_idx, column_idx) >= 4:
                        temp_seating[row_idx][column_idx] = "L"
        self.seating = temp_seating

    def __str__(self):
        return '\n'.join(' '.join(str(x) for x in row)  \
                          for row in self.seating)

    def Count(self):
        num_seats = 0
        for row in self.seating:
            for seat in row:
                if seat == "#":
                    num_seats += 1
        return num_seats

    def GetSurrounding(self, row_idx, column_idx):
        directions = [-1,0,1]
        num_surrounding_seat = 0
        for row_direction in directions:
            row = row_idx + row_direction
            if not 0<=row<len(self.seating):
                continue
            for column_direction in directions:
                column = column_idx + column_direction
                if ((column_direction == 0) and (row_direction == 0)) or \
                   (not 0<=column<len(self.seating[0])):
                    continue
                if self.seating[row][column] == "#":
                    num_surrounding_seat += 1
        return num_surrounding_seat

class LongSightSeatingPlan(SimpleSeatingPlan):
    def __next__(self):
        temp_seating = deepcopy(self.seating)
        for row_idx in range(len(self.seating)):
            for column_idx in range(len(self.seating[0])):
                if self.seating[row_idx][column_idx] == "L":
                    if self.GetSurrounding(row_idx, column_idx) == 0:
                        temp_seating[row_idx][column_idx] = "#"
                elif self.seating[row_idx][column_idx] == "#":
                    if self.GetSurrounding(row_idx, column_idx) >= 5:
                        temp_seating[row_idx][column_idx] = "L"
        self.seating = temp_seating

    def GetSurrounding(self, row_idx, column_idx):
        num_surrounding_seat = 0
        directions = [-1,0,1]
        for row_direction in directions:
            for column_direction in directions:
                if (row_direction == 0) and (column_direction == 0):
                    continue
                row_dir = row_idx + row_direction
                column_dir = column_idx + column_direction
                while (0<=row_dir<len(self.seating)) and \
                      (0<=column_dir<len(self.seating[0])):
                    if self.seating[row_dir][column_dir] == "#":
                        num_surrounding_seat += 1
                        break
                    if self.seating[row_dir][column_dir] == "L":
                        break
                    row_dir = row_dir + row_direction
                    column_dir = column_dir + column_direction


        return num_surrounding_seat


if __name__ == "__main__":
    with open("input.txt") as f:
        seating = [list(x.strip()) for x in f.readlines()]

    seat_plan = SimpleSeatingPlan(seating)
    prev_plan = ""
    while prev_plan != str(seat_plan):
        prev_plan = str(seat_plan)
        next(seat_plan)

    print("Part 1:", seat_plan.Count())

    long_sight_seat_plan = LongSightSeatingPlan(seating)
    prev_plan = ""
    while prev_plan != str(long_sight_seat_plan):
        prev_plan = str(long_sight_seat_plan)
        next(long_sight_seat_plan)

    print("Part 2:", long_sight_seat_plan.Count())
