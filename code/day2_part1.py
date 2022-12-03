from collections import defaultdict

reply_to_score = {"X": 1, "Y": 2, "Z": 3}

# we lose
game_to_score = defaultdict(int)

# we draw
for game in zip(["A", "B", "C"], ["X", "Y", "Z"]):
    game_to_score[game] = 3

# we win
for game in zip(["A", "B", "C"], ["Y", "Z", "X"]):
    game_to_score[game] = 6

total_score = 0
with open("inputs/day2.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            play, reply = line.split(" ")
            total_score += reply_to_score[reply]
            total_score += game_to_score[(play, reply)]

print(total_score)
