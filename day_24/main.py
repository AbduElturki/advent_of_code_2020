def GetNeighbours(cor_pair, tile_layout):
    directions = [(1,-1),(0,-1),(-1,0),(-1,1),(0,1),(1,0)]
    black_neighbours = set()
    white_neighbours = set()
    for direction in directions:
        col = cor_pair[0] + direction[0]
        row = cor_pair[1] + direction[1]
        if (col,row) in tile_layout:
            black_neighbours.add((col,row))
        else:
            white_neighbours.add((col,row))
    return black_neighbours, white_neighbours

def TilesGameOfLife(tile_layout, rounds):
    for _ in range(rounds):
        next_day = tile_layout.copy()
        for tile in tile_layout:
            b_set, w_set = GetNeighbours(tile, tile_layout)
            if (len(b_set) > 2) or (len(b_set) == 0):
                next_day.remove(tile)
            for w_tile in w_set:
                b_set, _ = GetNeighbours(w_tile, tile_layout)
                if len(b_set) == 2:
                    next_day.add(w_tile)
        tile_layout = next_day
    return tile_layout

def FlipTiles(steps, tile_layout):
    col, row = 0, 0
    s = 0

    while s < len(steps):
        if steps[s] == "e":
            col += 1
        elif steps[s] == "w":
            col -= 1
        elif steps[s] == "n":
            row -= 1
            s += 1
            if steps[s] == "e":
                col += 1
        elif steps[s] == "s":
            row += 1
            s += 1
            if steps[s] == "w":
                col -= 1
        s += 1

    if (col,row) not in tile_layout:
        tile_layout.add((col,row))
    else:
        tile_layout.remove((col,row))
    return tile_layout


if __name__ == "__main__":
    with open("input.txt") as f:
        instructions = [x.rstrip() for x in f.readlines()]
    tiles = set()

    for instruction in instructions:
        tiles = FlipTiles(instruction, tiles)

    print("Part 1:", len(tiles))

    tiles = TilesGameOfLife(tiles,100)
    print("Part 2:", len(tiles))
