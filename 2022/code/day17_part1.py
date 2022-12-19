import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = "2022/inputs/day17.txt"


class Piece:
    def __init__(self, array: np.ndarray) -> None:
        self.array = array
        self.shape = self.array.shape
        self.position = None  # current board position

    def draw(self):
        plt.imshow(self.array)
        plt.show()


BOARD_WIDTH = 7
APPEAR_ABOVE = 3
NUM_PIECES_DROPPED = 2022


class Tetris:
    def __init__(self, moves: list[str]) -> None:
        self.board = None
        self.moves = moves
        self.jet_move_counter = 0

    def _put_piece_at_initial_position(self, piece: Piece) -> Piece:
        """
        Pad piece and add 3 empty rows before stacking on the board.
        """
        self._pad_board(piece)
        piece.position = (piece.shape[0] - 1, 2)

        return piece

    def _pad_board(self, piece: Piece) -> None:
        padding = np.zeros((APPEAR_ABOVE + piece.shape[0], BOARD_WIDTH))
        if self.board is None:  # first piece
            self.board = padding
        else:
            self.board = np.concatenate([padding, self.board], axis=0)

    def _move_down(self, piece: Piece) -> Piece:
        new_position = (piece.position[0] + 1, piece.position[1])
        if self._is_valid_position(new_position, piece):
            piece.position = new_position
            return piece
        else:
            return False

    def _move_left(self, piece: Piece) -> Piece:
        new_position = (piece.position[0], piece.position[1] - 1)
        if self._is_valid_position(new_position, piece):
            piece.position = new_position

        return piece

    def _move_right(self, piece: Piece) -> Piece:
        new_position = (piece.position[0], piece.position[1] + 1)
        if self._is_valid_position(new_position, piece):
            piece.position = new_position

        return piece

    def _is_valid_position(self, new_position: tuple[int], piece: Piece) -> bool:
        # floor
        if new_position[0] > self.board.shape[0] - 1:
            return False

        # sides
        if (new_position[1] < 0) or (
            new_position[1] > self.board.shape[1] - piece.shape[1]
        ):
            return False

        board_state = self.board[
            new_position[0] - piece.shape[0] + 1 : new_position[0] + 1,
            new_position[1] : new_position[1] + piece.shape[1],
        ]

        return np.sum(board_state * piece.array) == 0

    def _update_counter(self) -> None:
        self.jet_move_counter = (self.jet_move_counter + 1) % len(self.moves)

    def drop_piece_to_board(self, piece: Piece) -> None:
        piece = self._put_piece_at_initial_position(piece)
        move_count = 0
        while True:
            # jet move
            if move_count % 2 == 0:
                move = self._get_next_jet_move()
                if move == ">":
                    move_result = self._move_right(piece)
                elif move == "<":
                    move_result = self._move_left(piece)

                if move_result:  # successful move
                    piece = move_result

                self.jet_move_counter += 1

            # move down
            else:
                move_result = self._move_down(piece)
                if move_result:  # successful move
                    piece = move_result
                else:
                    break

            move_count += 1

        self._add_piece_to_board_at_position(piece)
        self._cut_board()

    def _add_piece_to_board_at_position(self, piece: Piece) -> None:
        self.board[
            piece.position[0] - piece.shape[0] + 1 : piece.position[0] + 1,
            piece.position[1] : piece.position[1] + piece.shape[1],
        ] += piece.array

    def _get_next_jet_move(self) -> str:
        return self.moves[self.jet_move_counter % len(self.moves)]

    def _cut_board(self) -> None:
        while self.board[0, :].sum() == 0:
            self.board = self.board[1:, :]

    def draw(self):
        plt.imshow(self.board)
        plt.show()


def load_pieces():
    ## setup pieces ##
    flat_piece = Piece(np.ones((1, 4)))
    tall_piece = Piece(np.ones((4, 1)))
    square_piece = Piece(np.ones((2, 2)))

    corner_array = np.zeros((3, 3))
    corner_array[:, 2] = 1
    corner_array[2, :] = 1
    corner_piece = Piece(corner_array)

    cross_array = np.zeros((3, 3))
    cross_array[:, 1] = 1
    cross_array[1, :] = 1
    cross_piece = Piece(cross_array)

    return [flat_piece, cross_piece, corner_piece, tall_piece, square_piece]


if __name__ == "__main__":
    # read input moves
    with open(INPUT_FILE, "r") as file:
        for line in file:
            moves = list(line.strip())

    pieces = load_pieces()
    num_pieces_dropped = 2022

    tetris = Tetris(moves)

    for i in range(num_pieces_dropped):
        next_piece = pieces[i % len(pieces)]
        tetris.drop_piece_to_board(next_piece)

    print(tetris.board.shape[0])
