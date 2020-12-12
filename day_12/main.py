def GetFinalLocation(instructions):
    direction = 0 # east
    current_x = 0
    current_y = 0
    for instruction in instructions:
        action = instruction[0]
        units = instruction[1]

        if action == "N":
            current_y += units
        elif action == "S":
            current_y -= units
        elif action == "E":
            current_x += units
        elif action == "W":
            current_x -= units

        elif action == "F":
            if direction == 0: # east
                current_x += units
            elif direction == 90: # north
                current_y += units
            elif direction == 180: # west
                current_x -= units
            elif direction == 270: # south
                current_y -= units
            else:
                raise Exception("This angle isn't implemented {}"\
                                .format(direction))

        elif action == "R":
            direction = (direction - units) % 360
        elif action == "L":
            direction = (direction + units) % 360
        else:
            raise Exception("This action isn't implemented: {}".format(action))

    return current_x, current_y

def GetFinalRelativeLocation(instructions):
    current_x = 0
    current_y = 0
    waypoint_x = 10
    waypoint_y = 1

    for instruction in instructions:
        action = instruction[0]
        units = instruction[1]

        if action == "N":
            waypoint_y += units
        elif action == "S":
            waypoint_y -= units
        elif action == "E":
            waypoint_x += units
        elif action == "W":
            waypoint_x -= units

        elif action == "R":
            if units == 90:
                temp = waypoint_x
                waypoint_x = waypoint_y
                waypoint_y = -1 * temp
            elif units == 180:
                waypoint_x *= -1
                waypoint_y *= -1
            elif units == 270:
                temp = waypoint_x
                waypoint_x = -1 * waypoint_y
                waypoint_y = temp

        elif action == "L":
            if units == 90:
                temp = waypoint_x
                waypoint_x = -1 * waypoint_y
                waypoint_y = temp
            elif units == 180:
                waypoint_x *= -1
                waypoint_y *= -1
            elif units == 270:
                temp = waypoint_x
                waypoint_x = waypoint_y
                waypoint_y = -1 * temp

        elif action == "F":
            current_x += (units * waypoint_x)
            current_y += (units * waypoint_y)

    return current_x, current_y


if __name__ == "__main__":
    with open("input.txt") as f:
        instructions = [(x[0], int(x.strip()[1:])) for x in f.readlines()]
    x, y = GetFinalLocation(instructions)
    print("Part 1:", abs(x) + abs(y))
    x, y = GetFinalRelativeLocation(instructions)
    print("Part 2:", abs(x) + abs(y))
