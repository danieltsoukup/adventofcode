import pandas as pd
import numpy as np

plays = ["A", "B", "C"]
replies = ["X", "Y", "Z"]
reply_to_score = dict(zip(replies, range(1, 4)))

# default score 0 - we lose
game_to_score = pd.DataFrame(
    index=plays,
    columns=replies, 
    data=np.zeros((len(plays), len(replies)), dtype=int)
)

# we draw
for play, reply in zip(plays, replies):
    game_to_score.loc[play, reply] = 3 

# we win
for play, reply in zip(["A", "B", "C"], ["Y", "Z", "X"]):
    game_to_score.loc[play, reply] = 6 

total_score = 0
with open("inputs/day2.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            play, reply = line.split(" ")

            total_score += reply_to_score[reply]
            total_score += game_to_score.loc[play, reply]

print(total_score)