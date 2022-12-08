from utils import Dir
from day7_part1 import DirSolver
from pytest import fixture


@fixture()
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


@fixture()
def tree2() -> Dir:
    t = Dir("/")
    t["file1"] = 1
    t["dir1"]["dir11"]["file2"] = 2
    t["dir1"]["dir12"]["file2"] = 3
    t["dir2"]["file3"] = 10**7

    return t


def test_answer(tree2: DirSolver):

    assert tree2.get_answer() == 10


def test_empty_subdir(tree: Dir):
    assert isinstance(tree["new_dir"], Dir)
