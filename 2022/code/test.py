from utils import Dir
from day7_part1 import DirSolver
import pytest
from day8_part1 import solver
from utils import adjust_tail
from day9_part2 import Rope
from day10_part2 import cycle_to_position


@pytest.fixture()
def tree() -> Dir:
    t = Dir("/")
    t["file1"] = 1
    t["dir1"]["file2"] = 2

    return t


def test_tree_parent(tree: Dir):

    assert tree["dir1"].parent == tree


def test_tree_type(tree: Dir):

    assert isinstance(tree["dir1"], Dir)


def test_tree_walk(tree: Dir):
    total = 0
    for i in tree.get_files():
        total += i

    assert total == 3


def test_get_size(tree: Dir):

    assert tree.get_size() == 3 and tree["dir1"].size == 2


@pytest.fixture()
def tree2() -> DirSolver:
    t = DirSolver("/")
    t["file1"] = 1
    t["dir1"]["dir11"]["file2"] = 2
    t["dir1"]["dir12"]["file2"] = 3
    t["dir2"]["file3"] = 10**7

    return t


def test_answer(tree2: DirSolver):

    assert tree2.get_answer() == 10


def test_empty_subdir(tree: Dir):
    assert isinstance(tree["new_dir"], Dir)


@pytest.fixture
def dummy_grid():
    return [
        "1231",  # 4 visible from top
        "2141",  # 1 from left, 1 from top, 1 from right
        "1112",  # 4 from bottom
    ]


def test_solver(dummy_grid):
    assert solver(dummy_grid) == 11


test_data_inplace = [
    ((1, 0), (0, 0)),
    ((1, 1), (0, 0)),
    ((1, -1), (0, -1)),
    ((-1, -1), (0, -1)),
    ((-1, -1), (0, 0)),
]


@pytest.mark.parametrize("head,tail", test_data_inplace)
def test_adjust_tail_inplace(head, tail):

    assert tail == adjust_tail(head, tail)


test_data_on_axis = [
    ((2, 0), (0, 0), (1, 0)),
    ((0, -2), (0, 0), (0, -1)),
    ((-1, -5), (-1, -2), (-1, -4)),
]


@pytest.mark.parametrize("head,tail,expected", test_data_on_axis)
def test_adjust_tail_on_axis(head, tail, expected):

    assert expected == adjust_tail(head, tail)


test_data_diag = [
    ((-3, -2), (0, -1), (-2, -2)),
    ((1, 5), (0, 0), (1, 4)),
    ((-3, 1), (0, 0), (-2, 1)),
]


@pytest.mark.parametrize("head,tail,expected", test_data_diag)
def test_adjust_tail_diag(head, tail, expected):

    assert expected == adjust_tail(head, tail)


def test_rope():
    rope = Rope()
    rope.head = (1, 0)

    assert rope.points[0] == rope.head


test_cycles = [(1, 0, 0), (40, 0, 39), (41, 1, 0)]


@pytest.mark.parametrize("cycle,expected_row,expected_col", test_cycles)
def test_cycle_pos(cycle, expected_row, expected_col):
    row, col = cycle_to_position(cycle)

    assert (row == expected_row) and (col == expected_col)
