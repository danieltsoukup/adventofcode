from day17_part1 import load_pieces, Tetris
from tqdm import tqdm
import numpy as np

INPUT_FILE = "2022/inputs/day17.txt"


if __name__ == "__main__":
    # read input moves
    with open(INPUT_FILE, "r") as file:
        for line in file:
            moves = list(line.strip())

    pieces = load_pieces()

    num_pieces_dropped = 10_000

    tetris = Tetris(moves)
    heights = [0]
    for i in range(num_pieces_dropped):
        next_piece = pieces[i % len(pieces)]
        tetris.drop_piece_to_board(next_piece)
        heights.append(tetris.board.shape[0])

    deltas = np.array(
        [next_ - current for next_, current in zip(heights[1:], heights[:-1])]
    )

    for p in range(10_000):
        if np.all(deltas[-p:] == deltas[-2 * p : -p]):
            print(f"{p} works as period")
            break

    # p = 1755
    initial_deltas = deltas[:-p]
    periodic_increment = deltas[-p:].sum()

    large_number = 1000000000000

    num_blocks = (large_number - initial_deltas.shape[0]) // p
    remainder = (large_number - initial_deltas.shape[0]) % p

    total = (
        initial_deltas.sum()
        + num_blocks * periodic_increment
        + deltas[-p : -p + remainder].sum()
    )

    print(total)

    # print("---- Verify ----")
    # tetris = Tetris(moves)
    # heights = [0]
    # for i in range(large_number):
    #     next_piece = pieces[i % len(pieces)]
    #     tetris.drop_piece_to_board(next_piece)
    #     heights.append(tetris.board.shape[0])

    # print(tetris.board.shape[0])
