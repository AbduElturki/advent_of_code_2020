from collections import deque

def PlayRegularCombat(p1, p2):
    while (len(p1) != 0) and (len(p2) != 0):
        p1_card = p1.popleft()
        p2_card = p2.popleft()
        if p1_card > p2_card:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])

    if p1: return "Player 1", p1
    return "Player 2", p2

def PlayRecursiveCombat(p1, p2):
    p1_past = []
    p2_past = []

    while (len(p1) != 0) and (len(p2) != 0):
        if (p1 in p1_past) and (p2 in p2_past):
            return "Player 1", p1

        p1_past.append(p1.copy())
        p2_past.append(p2.copy())

        p1_card = p1.popleft()
        p2_card = p2.popleft()

        if (p1_card <= len(p1)) and (p2_card <= len(p2)):
            p1_copy = deque([p1[x] for x in range(p1_card)])
            p2_copy = deque([p2[x] for x in range(p2_card)])
            sub_winner, _ = PlayRecursiveCombat(p1_copy, p2_copy)
            if sub_winner == "Player 1":
                p1.extend([p1_card, p2_card])
            else:
                p2.extend([p2_card, p1_card])
        else:
            if p1_card > p2_card:
                p1.extend([p1_card, p2_card])
            else:
                p2.extend([p2_card, p1_card])

    if p1: return "Player 1", p1
    return "Player 2", p2

if __name__ == "__main__":
    with open("input.txt") as f:
        raw = f.read().rstrip().split("\n\n")
    player_1 = deque([int(x.strip()) for x in raw[0].split("\n")[1:]])
    player_2 = deque([int(x.strip()) for x in raw[1].split("\n")[1:]])

    winner, deck = PlayRegularCombat(player_1.copy(), player_2.copy())
    result = sum( x * (len(deck) - i) for i, x in enumerate(deck))
    print("Part 1: {} won! socre".format(winner), result)

    winner, deck = PlayRecursiveCombat(player_1.copy(), player_2.copy())
    result = sum( x * (len(deck) - i) for i, x in enumerate(deck))
    print("Part 2: {} won! socre".format(winner), result)
