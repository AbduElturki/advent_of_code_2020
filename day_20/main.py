from functools import reduce
from math import sqrt

import re
import numpy as np

def GetEdges(tile):
    edges = []
    edges.append(tile[:,0])
    edges.append(tile[0,:])
    edges.append(tile[:,-1])
    edges.append(tile[-1,:])
    return edges

def AllPossibleEdges(tile):
    edges = GetEdges(tile)
    filped_edges = [edge[::-1] for edge in edges]
    return edges + filped_edges

def FindCornersAndEdges(tile_dict):
    corners = []
    corner_orientation = []
    all_possible_edges = []
    for possible_edges in map(AllPossibleEdges, tile_dict.values()):
        all_possible_edges += possible_edges
    for tile_id, tile in tile_dict.items():
        matching = 0
        orientation = [0, 0, 0, 0]
        for or_idx, edge in enumerate(GetEdges(tile)):
            for possible_edge in all_possible_edges:
                if np.array_equal(edge, possible_edge):
                    matching += 1
                    orientation[or_idx] += 1
        # 4 edges match with the tile itself
        # 2 edges match with other tiles if it is a corner
        # 4 + 2 = 6 matches to be a corner
        if matching == 6:
            corners.append(tile_id)

            # if any of the values is True that means in that edge
            # there is another tile edge that match it.
            corner_orientation.append({"left": orientation[0] == 2,
                                       "top": orientation[1] == 2,
                                       "right": orientation[2] == 2,
                                       "bottom": orientation[3] == 2})
    return corners, corner_orientation

def MatchNextTile(tile_dict, starting_tile_id,
                  candidate_ids, bottom=False):
    if bottom:
        col = (slice(None,None,None), slice(None,None,None))
        row = (-1,0)
    else:
        col = (-1,0)
        row = (slice(None,None,None), slice(None,None,None))
    to_match = tile_dict[starting_tile_id][row[0],col[0]]
    for candidate_id in candidate_ids:
        tile_candidate = tile_dict[candidate_id]
        for _ in range(2):
            for _ in range(4):
                if np.array_equal(tile_candidate[row[1],col[1]], to_match):
                    tile_dict[candidate_id] = tile_candidate
                    return candidate_id
                tile_candidate = np.rot90(tile_candidate)
            tile_candidate = np.fliplr(tile_candidate)
    return None

def OrderTiles(tile_dict, corner_id, corner_orientation):
    width = int(sqrt(len(tile_dict)))
    image_ids = np.zeros((width, width),np.int32)
    image = [[] for _ in range(width)]

    #force this corner to become the top left corner.
    top_left = tile_dict[corner_id]

    # Adjust the corner orientation
    if corner_orientation["left"]:
        top_left = np.fliplr(top_left)
    if corner_orientation["top"]:
        top_left = np.flipud(top_left)

    image_ids[0,0] = corner_id
    image[0].append(top_left[1:-1,1:-1])
    candidate_ids = list(tile_dict.keys())
    candidate_ids.remove(corner_id)
    for i in range(width-1):
        image_ids[i+1,0] = MatchNextTile(tile_dict, image_ids[i,0],
                                        candidate_ids, bottom=True)
        candidate_ids.remove(image_ids[i+1,0])
        image[i+1].append(tile_dict[image_ids[i+1,0]][1:-1,1:-1])
    for i in range(width):
        for j in range(width-1):
            image_ids[i,j+1] = MatchNextTile(tile_dict, image_ids[i,j],
                                            candidate_ids)
            candidate_ids.remove(image_ids[i,j+1])
            image[i].append(tile_dict[image_ids[i,j+1]][1:-1,1:-1])
    constructed_image = np.concatenate([np.concatenate((x),axis=1)
                                        for x in image])
    return image_ids, constructed_image

def FindSeaMonsters(image):
    sea_mon = [list("                  # "),
               list("#    ##    ##    ###"),
               list(" #  #  #  #  #  #   ")]

    sea_mon_idx = [[i for i,x in enumerate(part) if x=="#"]
                       for part in sea_mon]
    sea_mon_width = len(sea_mon[0])
    sea_mon_height = len(sea_mon)
    sea_mon_blocks = sum(len(x) for x in sea_mon_idx)
    sea_mon_count = 0

    for _ in range(2):
        for _ in range(4):
            for i in range(image.shape[0] - sea_mon_height):
                for j in range(image.shape[1]-sea_mon_width):
                    matches = []
                    for k in range(sea_mon_height):
                        matches.append(all([x=="#" for x in
                          image[i+k,j:j+sea_mon_width][sea_mon_idx[k]]]))
                    if all(matches):
                        sea_mon_count += 1
            if sea_mon_count:
                return sea_mon_count, sea_mon_blocks * sea_mon_count
            image = np.rot90(image)
        image = np.fliplr(image)
    return sea_mon_count, None


if __name__ == "__main__":
    with open("input.txt") as f:
        raw = f.read().rstrip().split("\n\n")

    tiles = {}
    for raw_tile_data in raw:
        tile_data = raw_tile_data.split("\n")
        tile_num =  int(re.findall(r"\d+", tile_data[0])[0])
        tile = np.array([list(row_tile) for row_tile in tile_data[1:]])
        tiles[tile_num] = tile

    img_corners, img_corner_orientation = FindCornersAndEdges(tiles)
    print("Part 1:", reduce(lambda x,y: x*y, img_corners))

    _, fixed_image = OrderTiles(tiles, img_corners[0], img_corner_orientation[0])
    _, num_sea_dragon_blk = FindSeaMonsters(fixed_image)

    block, counts = np.unique(fixed_image, return_counts=True)
    block_dict = dict(zip(block, counts))

    print("Part 2:",  block_dict["#"] - num_sea_dragon_blk)
