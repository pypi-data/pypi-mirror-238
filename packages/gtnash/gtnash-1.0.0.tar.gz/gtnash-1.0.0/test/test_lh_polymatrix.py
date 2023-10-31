import numpy as np
import pytest

# from gtnash.game.hypergraphicalgame import HGG
from gtnash.game.polymatrixgame import PMG
from gtnash.solver.lemkehowson_polymatrix import LHpolymatrix
from gtnash.game.bayesian_hypergraphicalgame import BHGG
from fractions import Fraction


@pytest.fixture
def polym_3p():
    utilities = [[[2, 0, 3, 4], [0, 1, 5, 4]], [[3, 5, 1, 4], [4, 1, 1, 2]],
                 [[3, 2, 6, 7], [6, 5, 0, 3]]]
    hypergraph = [[0, 1], [0, 2], [1, 2]]
    players_actions = [[0, 1], [0, 1], [0, 1]]
    return LHpolymatrix(PMG(players_actions, utilities, hypergraph))


@pytest.fixture
def bayesian_polymatrix():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    theta = [[0, 1], [0, 1], [0, 1], [0, 1]]
    same_game = [[[3, 0, 0, 2], [3, 0, 0, 2]], [[3, 0, 0, 2], [1, 0, 0, 2]],
                 [[1, 0, 0, 2], [3, 0, 0, 2]], [[1, 0, 0, 2], [1, 0, 0, 2]]]
    same_p = [4, 1, 1, 4]
    hypergr = [[0, 1], [1, 2], [2, 3], [0, 3]]
    bhgg = BHGG(players_actions, [same_game, same_game, same_game, same_game],
                hypergr, theta, [same_p, same_p, same_p, same_p])
    return LHpolymatrix(bhgg.convert_to_HGG()[0])


@pytest.fixture
def polym_3p3a():
    utilities = [[[8, 2, 5, 5, 1, 7, 1, 5, 1], [4, 1, 4, 5, 6, 2, 4, 7, 3]],
                 [[2, 2, 4, 7, 9, 4, 5, 5, 5], [2, 5, 4, 7, 1, 5, 2, 1, 6]],
                 [[9, 3, 4, 9, 5, 5, 9, 5, 4], [8, 8, 6, 9, 1, 4, 9, 1, 3]]]
    hypergraph = [[0, 1], [0, 2], [1, 2]]
    players_actions = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    return LHpolymatrix(PMG(players_actions, utilities, hypergraph))


@pytest.fixture
def bimat_poly():
    utilities = [[[0, 6, 2, 5, 3, 3],
                  [1, 0, 0, 2, 4, 3]]]
    hypergraph = [[0, 1]]
    players_actions = [[0, 1, 2], [0, 1]]
    return LHpolymatrix(PMG(players_actions, utilities, hypergraph))


# ISSUE WITH INTEGER VALUE, NEED TO BE CONVERTED TO FRACTION
def test_maxu_of_p1(polym_3p):
    assert polym_3p.maxu_of_p == {0: 5, 1: 7, 2: 6}


def test_maxu_of_p2(bayesian_polymatrix):
    assert bayesian_polymatrix.maxu_of_p == {0: 12, 1: 8, 2: 12, 3: 8, 4: 12,
                                             5: 8, 6: 12, 7: 8}


def test_maxu_of_p3(polym_3p3a):
    assert polym_3p3a.maxu_of_p == {0: 9, 1: 9, 2: 9}


def test_maxu_of_p4(bimat_poly):
    assert bimat_poly.maxu_of_p == {0: 6, 1: 4}


def test_all_utilities1(polym_3p):
    assert polym_3p.all_utilities == {
        0: {1: [[2, 0], [3, 4]], 2: [[3, 5], [1, 4]]},
        1: {0: [[0, 5], [1, 4]], 2: [[3, 2], [6, 7]]},
        2: {0: [[4, 1], [1, 2]], 1: [[6, 0], [5, 3]]}}


def test_all_utilities2(polym_3p3a):
    assert polym_3p3a.all_utilities == {
        0: {1: [[8, 2, 5], [5, 1, 7], [1, 5, 1]],
            2: [[2, 2, 4], [7, 9, 4], [5, 5, 5]]},
        1: {0: [[4, 5, 4], [1, 6, 7], [4, 2, 3]],
            2: [[9, 3, 4], [9, 5, 5], [9, 5, 4]]},
        2: {0: [[2, 7, 2], [5, 1, 1], [4, 5, 6]],
            1: [[8, 9, 9], [8, 1, 1], [6, 4, 3]]}}


def test_all_utilities3(bayesian_polymatrix):
    assert bayesian_polymatrix.all_utilities == {
        0: {2: [[12, 0], [0, 8]], 3: [[3, 0], [0, 2]],
            6: [[12, 0], [0, 8]], 7: [[3, 0], [0, 2]]},
        1: {2: [[1, 0], [0, 2]], 3: [[4, 0], [0, 8]],
            6: [[1, 0], [0, 2]], 7: [[4, 0], [0, 8]]},
        2: {0: [[12, 0], [0, 8]], 1: [[3, 0], [0, 2]],
            4: [[12, 0], [0, 8]], 5: [[3, 0], [0, 2]]},
        3: {0: [[1, 0], [0, 2]], 1: [[4, 0], [0, 8]],
            4: [[1, 0], [0, 2]], 5: [[4, 0], [0, 8]]},
        4: {2: [[12, 0], [0, 8]], 3: [[3, 0], [0, 2]],
            6: [[12, 0], [0, 8]], 7: [[3, 0], [0, 2]]},
        5: {2: [[1, 0], [0, 2]], 3: [[4, 0], [0, 8]],
            6: [[1, 0], [0, 2]], 7: [[4, 0], [0, 8]]},
        6: {0: [[12, 0], [0, 8]], 1: [[3, 0], [0, 2]],
            4: [[12, 0], [0, 8]], 5: [[3, 0], [0, 2]]},
        7: {0: [[1, 0], [0, 2]], 1: [[4, 0], [0, 8]],
            4: [[1, 0], [0, 2]], 5: [[4, 0], [0, 8]]}}


def test_all_utilities4(bimat_poly):
    assert bimat_poly.all_utilities == {0: {1: [[0, 6], [2, 5], [3, 3]]},
                                        1: {0: [[1, 0, 4], [0, 2, 3]]}}


# def test_inverse_utilities(polym_3p):
#     assert polym_3p.inverse_utilities == {}

def test_tucker_schema0(polym_3p):
    assert (polym_3p.tucker == np.zeros((9, 10))).all()


def test_tucker_schema1(bayesian_polymatrix):
    assert (bayesian_polymatrix.tucker == np.zeros((24, 25))).all()


def test_tucker_schema2(polym_3p3a):
    assert (polym_3p3a.tucker == np.zeros((12, 13))).all()


def test_tucker_schema3(bimat_poly):
    assert (bimat_poly.tucker == np.zeros((7, 8))).all()


def test_tucker_schema_meth1(polym_3p):
    polym_3p.tucker_schema()
    assert (polym_3p.tucker == np.mat(
        [[0, 0, 0, 4, 6, 3, 1, -1, 0, 0], [0, 0, 0, 3, 2, 5, 2, -1, 0, 0],
         [0, 8, 3, 0, 0, 5, 6, 0, -1, 0], [0, 7, 4, 0, 0, 2, 1, 0, -1, 0],
         [0, 3, 6, 1, 7, 0, 0, 0, 0, -1], [0, 6, 5, 2, 4, 0, 0, 0, 0, -1],
         [-1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 1, 1, 0, 0, 0]], dtype=float)).all()


def test_tucker_schema_meth2(polym_3p3a):
    polym_3p3a.tucker_schema()
    assert (polym_3p3a.tucker == np.mat(
        [[0, 0, 0, 0, 2, 8, 5, 8, 8, 6, -1, 0, 0],
         [0, 0, 0, 0, 5, 9, 3, 3, 1, 6, -1, 0, 0],
         [0, 0, 0, 0, 9, 5, 9, 5, 5, 5, -1, 0, 0],
         [0, 6, 5, 6, 0, 0, 0, 1, 7, 6, 0, -1, 0],
         [0, 9, 4, 3, 0, 0, 0, 1, 5, 5, 0, -1, 0],
         [0, 6, 8, 7, 0, 0, 0, 1, 5, 6, 0, -1, 0],
         [0, 8, 3, 8, 2, 1, 1, 0, 0, 0, 0, 0, -1],
         [0, 5, 9, 9, 2, 9, 9, 0, 0, 0, 0, 0, -1],
         [0, 6, 5, 4, 4, 6, 7, 0, 0, 0, 0, 0, -1],
         [-1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], ])).all()


def test_tucker_schema_meth3(bimat_poly):
    bimat_poly.tucker_schema()
    assert (bimat_poly.tucker == np.mat([[0, 0, 0, 0, 7, 1, -1, 0],
                                         [0, 0, 0, 0, 5, 2, -1, 0],
                                         [0, 0, 0, 0, 4, 4, -1, 0],
                                         [0, 4, 5, 1, 0, 0, 0, -1],
                                         [0, 5, 3, 2, 0, 0, 0, -1],
                                         [-1, 1, 1, 1, 0, 0, 0, 0],
                                         [-1, 0, 0, 0, 1, 1, 0, 0], ])).all()


def test_launch_solver1(bimat_poly):
    sol = bimat_poly.launch_solver([0, 0])
    assert sol == {0: [0, 0, 1], 1: [1, 0]}
    assert bimat_poly.currentgame.is_equilibrium(sol)


def test_launch_solver2(bimat_poly):
    sol = bimat_poly.launch_solver([0, 1])
    assert sol == {0: [Fraction(2, 3), Fraction(1, 3), 0],
                   1: [Fraction(1, 3), Fraction(2, 3)]}
    assert bimat_poly.currentgame.is_equilibrium(sol)


def test_launch_solver3(polym_3p):
    sol = polym_3p.launch_solver([0, 0, 0])
    assert sol == {0: [0, 1], 1: [0, 1], 2: [0, 1]}
    assert polym_3p.currentgame.is_equilibrium(sol)


def test_launch_solver4(polym_3p):
    sol = polym_3p.launch_solver([1, 1, 1])
    assert sol == {0: [0, 1], 1: [0, 1], 2: [0, 1]}
    assert polym_3p.currentgame.is_equilibrium(sol)
