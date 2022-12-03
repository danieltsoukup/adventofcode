import pandas as pd
import numpy as np

plays = ["A", "B", "C"]
replies = ["X", "Y", "Z"]
reply_to_score = dict(zip(replies, range(1, 4)))
result_to_score = dict(zip(replies, [0, 3, 6]))

# default score 0 - we lose
game_to_score = pd.DataFrame(
    index=plays, columns=replies, data=np.zeros((len(plays), len(replies)), dtype=int)
)

# we draw
for play, reply in zip(plays, replies):
    game_to_score.loc[play, reply] = 3

# we win
for play, reply in zip(["A", "B", "C"], ["Y", "Z", "X"]):
    game_to_score.loc[play, reply] = 6

def get_reply(play: str, score: int) -> str:
    """
    Find the right reply based on the play and score.
    """
    play_row = game_to_score.loc[play, :]
    idx = np.argmax(play_row == score)

    return replies[idx]

total_score = 0
with open("inputs/day2.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            play, result = line.split(" ")
            score = result_to_score[result]
            reply = get_reply(play, score)

            total_score += score
            total_score += reply_to_score[reply]

print(total_score)
