from day7_part1 import Dir
from day7_part1 import DirSolver
import pytest
from day8_part1 import solver
from day9_part1 import adjust_tail
from day9_part2 import Rope
from day10_part2 import cycle_to_position
from day11_part1 import operation_factory
from day12_part1 import condition
from day13_part1 import compare_packets
import re
from day14_part1 import get_line_segment
from day15_part1 import find_overlap_interval, interval_union_size
import networkx as nx
import matplotlib.pyplot as plt
from day16_part1 import graph_to_flow_digraph, optimize_flow


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


def test_op_factory():
    op = operation_factory("new = old + 3")

    assert op(3) == 6


##############
### DAY 12 ###
##############


@pytest.fixture
def grid():
    return [["a", "b"], ["c", "d"]]


def test_condition_true(grid):
    assert condition((0, 0), (0, 1), grid)


def test_condition_false(grid):
    assert not condition((0, 0), (1, 0), grid)


test_packets = [
    ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], True),
    ([1, 1, 5, 1, 1], [1, 1, 3, 1, 1], False),
    ([[1], [2, 3, 4]], [[1], 4], True),
    ([[1], 4], [[1], [2, 3, 4]], False),
    ([9], [[8, 7, 6]], False),
    ([[4, 4], 4, 4], [[4, 4], 4, 4, 4], True),
    ([7, 7, 7, 7], [7, 7, 7], False),
    ([7, 7], [7, 7, 7], True),
    ([], [3], True),
    ([[[]]], [[]], False),
    ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9], False),
    ([1, 2, 3], [1, 2, 3], None),
    ([[[]]], [[[]]], None),
    ([], [], None),
    ([5, 3], [[5], 4], True),
]


@pytest.mark.parametrize("left,right,expected", test_packets)
def test_compare_packets(left, right, expected):

    assert compare_packets(left, right) == expected


def test_eval():
    string_list = "[1,[2,[3,[4,[5,6,7]]]],8,9]"

    assert eval(string_list) == [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]


def test_regex_for_rocks():
    string_ = "502,34 -> 502,33 -> 502,34"

    tuples = re.findall(r"(\d+),(\d+)", string_)
    tuples = [(int(x), int(y)) for x, y in tuples]

    assert tuples == [(502, 34), (502, 33), (502, 34)]


def test_line_segment():
    point1 = (0, -1)
    point2 = (0, 1)
    points = get_line_segment(point1, point2)

    assert points == {(0, -1), (0, 0), (0, 1)}


def test_line_segment2():
    point1 = (2, -1)
    point2 = (5, -1)
    points = get_line_segment(point1, point2)

    assert points == {(2, -1), (3, -1), (4, -1), (5, -1)}


def test_parse_coords():
    string_ = "Sensor at x=-12, y=23: closest beacon is at x=45, y=-67"
    expected = [("-12", "23"), ("45", "-67")]

    assert expected == re.findall(r"x=(-?\d+), y=(-?\d+)", string_)


### DAY 15 ###


def test_overlap():
    height = 10
    point = (8, 7)
    distance = 9

    assert (2, 14) == find_overlap_interval(point, distance, height)


def test_overlap_edge():
    height = 1
    point = (0, 0)
    distance = 1

    assert (0, 0) == find_overlap_interval(point, distance, height)


def test_overlap_edge2():
    height = 1
    point = (0, 0)
    distance = 2

    assert (-1, 1) == find_overlap_interval(point, distance, height)


def test_no_overlap():
    height = 2
    point = (0, 0)
    distance = 1

    assert None is find_overlap_interval(point, distance, height)


intervals = [
    ([(1, 1)], 1),
    ([(1, 2), (3, 4)], 4),
    ([(1, 2), (2, 3)], 3),
    ([(1, 2), (1, 4)], 4),
    ([(1, 4), (2, 5)], 5),
    ([(1, 5), (-5, 10)], 16),
    ([(1, 2), (2, 3), (-7, -5), (-8, -6)], 7),
]


@pytest.mark.parametrize("intervals,expected", intervals)
def test_interval_union_size(intervals, expected):
    assert interval_union_size(intervals) == expected


############
## DAY 16 ##
############


def test_extract_nodes():
    string_ = "Valve XN has flow rate=7; tunnels lead to valves DG, UJ, VD, VI, OU"
    expected = ["XN", "DG", "UJ", "VD", "VI", "OU"]

    assert expected == re.findall(r"([A-Z]+\b)+", string_)


def test_optimizer():
    graph = nx.Graph()
    graph.add_node("a")
    graph.nodes["a"]["flow"] = 1
    graph.add_node("b")
    graph.nodes["b"]["flow"] = 0
    graph.add_edge("a", "b")

    digraph = graph_to_flow_digraph(graph)

    # nx.draw(digraph, labels={node: node + " " + str(digraph.nodes[node]["flow"]) for node in digraph.nodes})
    # plt.show()

    assert optimize_flow(digraph, "a", 20) == 19
