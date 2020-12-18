import itertools

from collections import deque
from copy import deepcopy

class ConwayCubes:
    def __init__(self, inital_cubes: deque):
        self.world = deque()
        self.world.append(deque())
        self.world[0].append(inital_cubes)
        self.middle_z = 0
        self.middle_w = 0

    def __str__(self):
        conway_cubes_string = ""
        for w, plane_3d in enumerate(self.world):
            for i, cubes in enumerate(plane_3d):
                conway_cubes_string += "Z = {}   W = {}\n\n"\
                        .format(i-self.middle_z, w-self.middle_w)
                for plane_2d_row in cubes:
                    conway_cubes_string += ("".join(plane_2d_row)+"\n")
                conway_cubes_string += "\n"
        return conway_cubes_string

    def expand_dimensions_vertical(self):
        for w, plane_3d in enumerate(self.world):
            for plane_2d in plane_3d:
                new_rows  = "." * len(plane_2d[0])
                plane_2d.append(deque(new_rows))
                plane_2d.appendleft(deque(new_rows))
                for plane_2d_row in plane_2d:
                    plane_2d_row.append(".")
                    plane_2d_row.appendleft(".")

            new_plane = deque(deque("." * len(self.world[w][0][0]))
                              for _ in range(len(self.world[w][0])))

            self.world[w].append(deepcopy(new_plane))
            self.world[w].appendleft(deepcopy(new_plane))
        self.middle_z += 1

    def expand_dimensions_horizontal(self):
        new_plane = deque(deque("." * len(self.world[0][0][0]))
                          for _ in range(len(self.world[0][0])))
        new_line = deque([deepcopy(new_plane) for _ in range(len(self.world[0]))])
        self.world.appendleft(deepcopy(new_line))
        self.world.append(deepcopy(new_line))
        self.middle_w += 1


    def get_surrounding_active_cubes(self, x, y, z, w):
        num_active = 0
        directions = list(itertools.product((-1,0,1), repeat=4))

        for direction in directions:
            if all([x == 0 for x in direction]) :
                continue
            # the order is z,y,x not x,y,z
            near_coor = [k + j for j,k in zip(direction, [w, z, y, x])]

            if (0 <= near_coor[0] < len(self.world)) and \
               (0 <= near_coor[1] < len(self.world[0])) and \
               (0 <= near_coor[2] < len(self.world[0][0])) and \
               (0 <= near_coor[3] < len(self.world[0][0][0])) and \
               (self.world[near_coor[0]][near_coor[1]][near_coor[2]][near_coor[3]] == "#"):
                num_active += 1

        return num_active

    def Step3D(self, dimension_w=None):
        if dimension_w is None:
            dimension_w = self.middle_w
        self.expand_dimensions_vertical()
        new_plane = deepcopy(self.world[dimension_w])
        for z, plane in enumerate(self.world[dimension_w]):
            for y, plane_row in enumerate(plane):
                for x, cube in enumerate(plane_row):
                    num_active = self.get_surrounding_active_cubes(x, y, z, dimension_w)
                    if (cube == "#") and (num_active != 2) and (num_active != 3):
                        new_plane[z][y][x] = "."
                    elif (cube == ".") and (num_active == 3):
                        new_plane[z][y][x] = "#"
        self.world[dimension_w] = new_plane

    def Step4D(self):
        self.expand_dimensions_vertical()
        self.expand_dimensions_horizontal()
        new_world = deque()
        for w, plane_3d in enumerate(self.world):
            new_plane = deepcopy(plane_3d)
            for z, plane in enumerate(plane_3d):
                for y, plane_row in enumerate(plane):
                    for x, cube in enumerate(plane_row):
                        num_active = self.get_surrounding_active_cubes(x, y, z, w)
                        if (cube == "#") and (num_active != 2) and (num_active != 3):
                            new_plane[z][y][x] = "."
                        elif (cube == ".") and (num_active == 3):
                            new_plane[z][y][x] = "#"
            new_world.append(new_plane)
        self.world = new_world

    def GetActiveCubesTotal(self):
        total_active_cubes = 0
        for plane_3d in self.world:
            for plane in plane_3d:
                for plane_row in plane:
                    total_active_cubes += plane_row.count("#")
        return total_active_cubes


if __name__ == "__main__":
    with open("input.txt") as f:
        inital_cubes_state = deque(deque(x.strip()) for x in f.readlines())

    conway_3d = ConwayCubes(inital_cubes_state)
    for _ in range(6):
        conway_3d.Step3D()
    print("Part 1:",conway_3d.GetActiveCubesTotal())

    conway_4d = ConwayCubes(inital_cubes_state)
    for _ in range(6):
        conway_4d.Step4D()
    print("Part 2:",conway_4d.GetActiveCubesTotal())
