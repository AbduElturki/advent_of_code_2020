import time

def DecodePosition(encoded_position):
    #Decoding Rows
    encoded_row = encoded_position[:7]
    possible_rows = list(range(128)) 
    for symbol in encoded_row:
        if symbol == "F":
            possible_rows = possible_rows[:len(possible_rows)//2] 
        elif symbol == "B":
            possible_rows = possible_rows[len(possible_rows)//2:] 
        else:
            raise Exception("Unexpected Symbol {}".format(symbol))
    decoded_row = possible_rows[0]

    #Decoding Columns 
    encoded_column = encoded_position[7:]
    possible_columns = list(range(8)) 
    for symbol in encoded_column:
        if symbol == "L":
            possible_columns = possible_columns[:len(possible_columns)//2] 
        elif symbol == "R":
            possible_columns = possible_columns[len(possible_columns)//2:] 
        else:
            raise Exception("Unexpected Symbol {}".format(symbol))
    decoded_column = possible_columns[0]
    
    return (decoded_row,decoded_column)


def FindGapSeat(seat_ids):
    sorted_ids = sorted(seat_ids)
    for idx in range(len(sorted_ids)-1):
        if (sorted_ids[idx+1] - sorted_ids[idx]) == 2:
            return sorted_ids[idx]+1
    raise Exception("There are no empty seat")

if __name__ == "__main__":
    start_time = time.time()

    with open("input.txt") as f:
        encoded_positions = [x.strip() for x in f.readlines()]

    decoded_positions = [position for position in 
                         map(DecodePosition, encoded_positions)]
    seat_ids = [row * 8 + column for row, column 
                           in decoded_positions]

    print("Part 1: highest seat ID {}".format(max(seat_ids)))
    print("Part 2: the missing seat ID {}".format(FindGapSeat(seat_ids)))

    print("--- {} seconds ---".format(round(time.time() - start_time,4)))
