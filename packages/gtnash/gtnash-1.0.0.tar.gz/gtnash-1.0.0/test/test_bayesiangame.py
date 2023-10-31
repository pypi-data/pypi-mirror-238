import numpy as np
import pytest

from gtnash.game.bayesiangame import BG
from fractions import Fraction


@pytest.fixture
def bimat_bg():
    players_actions = [[0, 1, 2], [0, 1]]
    utilities = [[[-3, -7, -10, -1, -5, -9], [-3, -7, -1, -5, -10, -9]],
                 [[-2, -6, -9, -1, -4, -8], [-2, -6, -1, -4, -9, -8]],
                 [[-2, -5, -8, -1, -3, -7], [-2, -5, -1, -3, -8, -7]],
                 [[-2, -4, -7, -1, -3, -6], [-2, -4, -1, -3, -7, -6]],
                 [[-2, -4, -6, -1, -3, -5], [-2, -4, -1, -3, -6, -5]],
                 [[-3, -7, -1, -5, -10, -9], [-3, -7, -10, -1, -5, -9]]]
    theta = [[0, 1], [0, 1, 2]]
    p = [2, 4, 4, 4, 2, 4]
    return BG(players_actions, utilities, theta, p)


@pytest.fixture
def sherif_bg1():
    players_actions = [[0, 1], [0, 1]]
    utilities = [[[-1, -1, -2, 0], [-3, -2, -1, 0]],
                 [[0, -1, -2, 1], [0, -2, 2, -1]]]
    theta = [[0], [0, 1]]
    p = [1, 2]
    return BG(players_actions, utilities, theta, p)


@pytest.fixture
def sherif_bg2():
    players_actions = [[0, 1], [0, 1]]
    utilities = [[[-1, -1, -2, 0], [-3, -2, -1, 0]],
                 [[0, -1, -2, 1], [0, -2, 2, -1]]]
    theta = [[0], [0, 1]]
    p = [2, 1]
    return BG(players_actions, utilities, theta, p)


@pytest.fixture
def sherif_bg3():
    players_actions = [[0, 1], [0, 1]]
    utilities = [[[-1, -1, -2, 0], [-3, -2, -1, 0]],
                 [[0, -1, -2, 1], [0, -2, 2, -1]]]
    theta = [[0], [0, 1]]
    p = [3, 1]
    return BG(players_actions, utilities, theta, p)


@pytest.fixture
def three_bg():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    theta = [[0, 1], [0, 1], [0, 1]]
    all_p = [1, 2, 1, 4, 2, 2, 2, 6]
    utilities = [
        [[87, 56, 33, 21, 88, 77, 79, 69], [39, 52, 4, 92, 1, 78, 60, 69],
         [2, 28, 92, 11, 16, 63, 21, 22]],
        [[97, 12, 13, 92, 38, 2, 91, 62], [32, 40, 10, 57, 19, 18, 19, 15],
         [35, 12, 0, 56, 93, 22, 52, 35]],
        [[67, 0, 13, 87, 83, 6, 1, 80], [27, 63, 31, 22, 18, 8, 46, 81],
         [88, 28, 35, 5, 52, 67, 21, 12]],
        [[76, 13, 70, 36, 8, 39, 22, 42], [43, 82, 81, 37, 70, 58, 28, 91],
         [13, 25, 6, 96, 31, 27, 5, 37]],
        [[42, 62, 83, 91, 62, 11, 19, 0], [33, 88, 78, 14, 90, 27, 40, 86],
         [29, 91, 63, 65, 78, 36, 3, 35]],
        [[78, 51, 25, 64, 84, 53, 19, 30], [94, 8, 47, 52, 17, 89, 21, 54],
         [39, 13, 7, 46, 4, 14, 46, 3]],
        [[21, 33, 41, 4, 40, 5, 47, 13], [72, 6, 92, 29, 73, 54, 22, 30],
         [23, 86, 14, 46, 99, 34, 62, 97]],
        [[69, 11, 25, 65, 82, 52, 68, 56], [33, 12, 39, 98, 41, 63, 99, 10],
         [18, 62, 99, 58, 62, 25, 55, 7]]]
    return BG(players_actions, utilities, theta, all_p)


# [Fraction(1, 20), Fraction(1, 10), Fraction(1, 20), Fraction(1, 5),
# Fraction(1, 10), Fraction(1, 10), Fraction(1, 10), Fraction(3, 10)]


def test_joint_actions1(bimat_bg):
    assert (bimat_bg.joint_actions == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.], [2., 0.], [2., 1.]])).all()


def test_joint_actions2(sherif_bg1):
    assert (sherif_bg1.joint_actions == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_actions3(three_bg):
    assert (three_bg.joint_actions == np.mat(
        [[0., 0., 0.], [0., 0., 1.], [0., 1., 0.], [0., 1., 1.], [1., 0., 0.],
         [1., 0., 1.], [1., 1., 0.],
         [1., 1., 1.]])).all()


def test_joint_type1(bimat_bg):
    assert (bimat_bg.joint_theta == np.mat(
        [[0., 0.], [0., 1.], [0., 2.], [1., 0.], [1., 1.], [1., 2.]])).all()


def test_joint_type2(sherif_bg1):
    assert (sherif_bg1.joint_theta == np.mat([[0., 0.], [0., 1.]])).all()


def test_joint_type3(three_bg):
    assert (three_bg.joint_theta == np.mat(
        [[0., 0., 0.], [0., 0., 1.], [0., 1., 0.], [0., 1., 1.], [1., 0., 0.],
         [1., 0., 1.], [1., 1., 0.],
         [1., 1., 1.]])).all()


def test_proba_norm1(bimat_bg):
    assert (sum(bimat_bg.p) == 1)


def test_proba_norm2(sherif_bg1):
    assert (sum(sherif_bg1.p) == 1)


def test_proba_norm3(three_bg):
    assert (sum(three_bg.p) == 1)


"""
generate_joint_matrix(into_mat)
        Generate a matrix to create all the possible combination
        of action/type possible
    generate_local_normalformgame(hypergraph_temp, index_hyper_edge)
        Generate a normal form game corresponding to a possible joint type/nfg
"""


def test_proba_type1(bimat_bg):
    assert bimat_bg.proba_type() == {0: Fraction(1, 10), 1: Fraction(2, 10),
                                     2: Fraction(2, 10), 3: Fraction(2, 10),
                                     4: Fraction(1, 10), 5: Fraction(2, 10)}


def test_proba_type2(sherif_bg1):
    assert sherif_bg1.proba_type() == {0: Fraction(1, 3), 1: Fraction(2, 3)}


def test_proba_type3(three_bg):
    assert three_bg.proba_type() == {0: Fraction(1, 20), 1: Fraction(2, 20),
                                     2: Fraction(1, 20), 3: Fraction(4, 20),
                                     4: Fraction(2, 20), 5: Fraction(2, 20),
                                     6: Fraction(2, 20), 7: Fraction(6, 20)}


def test_get_index_of_type1(bimat_bg):
    assert bimat_bg.get_index_of_type([0, 0]) == 0


def test_get_index_of_type2(bimat_bg):
    assert bimat_bg.get_index_of_type([0, 1]) == 1


def test_get_index_of_type3(bimat_bg):
    assert bimat_bg.get_index_of_type([0, 2]) == 2


def test_get_index_of_type4(bimat_bg):
    assert bimat_bg.get_index_of_type([1, 0]) == 3


def test_get_index_of_type5(bimat_bg):
    assert bimat_bg.get_index_of_type([1, 1]) == 4


def test_get_index_of_type6(bimat_bg):
    assert bimat_bg.get_index_of_type([1, 2]) == 5


def test_get_index_of_type7(sherif_bg1):
    assert sherif_bg1.get_index_of_type([0, 0]) == 0


def test_get_index_of_type8(sherif_bg1):
    assert sherif_bg1.get_index_of_type([0, 1]) == 1


def test_get_index_of_type9(three_bg):
    assert three_bg.get_index_of_type([0, 0, 0]) == 0


def test_get_index_of_type10(three_bg):
    assert three_bg.get_index_of_type([0, 0, 1]) == 1


def test_get_index_of_type11(three_bg):
    assert three_bg.get_index_of_type([0, 1, 0]) == 2


def test_get_index_of_type12(three_bg):
    assert three_bg.get_index_of_type([0, 1, 1]) == 3


def test_get_index_of_type13(three_bg):
    assert three_bg.get_index_of_type([1, 0, 0]) == 4


def test_get_index_of_type14(three_bg):
    assert three_bg.get_index_of_type([1, 0, 1]) == 5


def test_get_index_of_type15(three_bg):
    assert three_bg.get_index_of_type([1, 1, 0]) == 6


def test_get_index_of_type16(three_bg):
    assert three_bg.get_index_of_type([1, 1, 1]) == 7


def test_conditional_probabilities1(bimat_bg):
    assert bimat_bg.conditional_probabilities(0, 0) == {0: Fraction(1, 5),
                                                        1: Fraction(2, 5),
                                                        2: Fraction(2, 5)}


def test_conditional_probabilities2(bimat_bg):
    assert bimat_bg.conditional_probabilities(0, 1) == {3: Fraction(2, 5),
                                                        4: Fraction(1, 5),
                                                        5: Fraction(2, 5)}


def test_conditional_probabilities3(bimat_bg):
    assert bimat_bg.conditional_probabilities(1, 0) == {0: Fraction(1, 3),
                                                        3: Fraction(2, 3)}


def test_conditional_probabilities4(bimat_bg):
    assert bimat_bg.conditional_probabilities(1, 1) == {1: Fraction(2, 3),
                                                        4: Fraction(1, 3)}


def test_conditional_probabilities5(bimat_bg):
    assert bimat_bg.conditional_probabilities(1, 2) == {2: Fraction(1, 2),
                                                        5: Fraction(1, 2)}


def test_conditional_probabilities6(sherif_bg1):
    assert sherif_bg1.conditional_probabilities(0, 0) == {0: Fraction(1, 3),
                                                          1: Fraction(2, 3)}


def test_conditional_probabilities7(sherif_bg1):
    assert sherif_bg1.conditional_probabilities(1, 0) == {0: Fraction(1, 1)}


def test_conditional_probabilities8(sherif_bg1):
    assert sherif_bg1.conditional_probabilities(1, 1) == {1: Fraction(3, 3)}


def test_conditional_probabilities9(sherif_bg2):
    assert sherif_bg2.conditional_probabilities(0, 0) == {1: Fraction(1, 3),
                                                          0: Fraction(2, 3)}


def test_conditional_probabilities10(three_bg):
    assert three_bg.conditional_probabilities(0, 0) == {0: Fraction(1, 8),
                                                        1: Fraction(1, 4),
                                                        2: Fraction(1, 8),
                                                        3: Fraction(1, 2)}


def test_conditional_probabilities11(three_bg):
    assert three_bg.conditional_probabilities(0, 1) == {4: Fraction(1, 6),
                                                        5: Fraction(1, 6),
                                                        6: Fraction(1, 6),
                                                        7: Fraction(1, 2)}


def test_conditional_probabilities12(three_bg):
    assert three_bg.conditional_probabilities(1, 0) == {0: Fraction(1, 7),
                                                        1: Fraction(2, 7),
                                                        4: Fraction(2, 7),
                                                        5: Fraction(2, 7)}


def test_conditional_probabilities13(three_bg):
    assert three_bg.conditional_probabilities(1, 1) == {2: Fraction(1, 13),
                                                        3: Fraction(4, 13),
                                                        6: Fraction(2, 13),
                                                        7: Fraction(6, 13)}


def test_conditional_probabilities14(three_bg):
    assert three_bg.conditional_probabilities(2, 0) == {0: Fraction(1, 6),
                                                        2: Fraction(1, 6),
                                                        4: Fraction(1, 3),
                                                        6: Fraction(1, 3)}


def test_conditional_probabilities15(three_bg):
    assert three_bg.conditional_probabilities(2, 1) == {1: Fraction(1, 7),
                                                        3: Fraction(2, 7),
                                                        5: Fraction(1, 7),
                                                        7: Fraction(3, 7)}


def test_dico_utilities1(bimat_bg):
    assert bimat_bg.dico_utilities() == {
        0: [[-3, -7, -10, -1, -5, -9], [-3, -7, -1, -5, -10, -9]],
        1: [[-2, -6, -9, -1, -4, -8], [-2, -6, -1, -4, -9, -8]],
        2: [[-2, -5, -8, -1, -3, -7], [-2, -5, -1, -3, -8, -7]],
        3: [[-2, -4, -7, -1, -3, -6], [-2, -4, -1, -3, -7, -6]],
        4: [[-2, -4, -6, -1, -3, -5], [-2, -4, -1, -3, -6, -5]],
        5: [[-3, -7, -1, -5, -10, -9], [-3, -7, -10, -1, -5, -9]]}


def test_dico_utilities2(sherif_bg1):
    assert sherif_bg1.dico_utilities() == {
        0: [[-1, -1, -2, 0], [-3, -2, -1, 0]],
        1: [[0, -1, -2, 1], [0, -2, 2, -1]]}


def test_dico_utilities3(three_bg):
    assert three_bg.dico_utilities() == {
        0: [[87, 56, 33, 21, 88, 77, 79, 69], [39, 52, 4, 92, 1, 78, 60, 69],
            [2, 28, 92, 11, 16, 63, 21, 22]],
        1: [[97, 12, 13, 92, 38, 2, 91, 62], [32, 40, 10, 57, 19, 18, 19, 15],
            [35, 12, 0, 56, 93, 22, 52, 35]],
        2: [[67, 0, 13, 87, 83, 6, 1, 80], [27, 63, 31, 22, 18, 8, 46, 81],
            [88, 28, 35, 5, 52, 67, 21, 12]],
        3: [[76, 13, 70, 36, 8, 39, 22, 42], [43, 82, 81, 37, 70, 58, 28, 91],
            [13, 25, 6, 96, 31, 27, 5, 37]],
        4: [[42, 62, 83, 91, 62, 11, 19, 0], [33, 88, 78, 14, 90, 27, 40, 86],
            [29, 91, 63, 65, 78, 36, 3, 35]],
        5: [[78, 51, 25, 64, 84, 53, 19, 30], [94, 8, 47, 52, 17, 89, 21, 54],
            [39, 13, 7, 46, 4, 14, 46, 3]],
        6: [[21, 33, 41, 4, 40, 5, 47, 13], [72, 6, 92, 29, 73, 54, 22, 30],
            [23, 86, 14, 46, 99, 34, 62, 97]],
        7: [[69, 11, 25, 65, 82, 52, 68, 56], [33, 12, 39, 98, 41, 63, 99, 10],
            [18, 62, 99, 58, 62, 25, 55, 7]]}


def test_expected_utilities1(bimat_bg):
    assert bimat_bg.expected_utilities(
        {(0, 0): [1, 0, 0], (0, 1): [1, 0, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (1, 2): [1, 0]}) == \
           {(0, 0): Fraction(-11, 5),
            (0, 1): Fraction(-12, 5),
            (1, 0): Fraction(-7, 3),
            (1, 1): Fraction(-2, 1),
            (1, 2): Fraction(-5, 2)}


def test_expected_utilities2(bimat_bg):
    assert bimat_bg.expected_utilities(
        {(0, 0): [1, 0, 0], (0, 1): [1, 0, 0], (1, 0): [0, 1], (1, 1): [0, 1],
         (1, 2): [0, 1]}) == \
           {(0, 0): Fraction(-29, 5),
            (0, 1): Fraction(-26, 5),
            (1, 0): Fraction(-5, 1),
            (1, 1): Fraction(-16, 3),
            (1, 2): Fraction(-6, 1)}


def test_expected_utilities3(sherif_bg1):
    assert sherif_bg1.expected_utilities(
        {(0, 0): [1, 0], (1, 0): [1, 0], (1, 1): [0, 1]}) == {
               (0, 0): Fraction(-1, 1), (1, 0): Fraction(-3, 1),
               (1, 1): Fraction(-2, 1)}


def test_expected_utilities4(sherif_bg1):
    assert sherif_bg1.expected_utilities(
        {(0, 0): [0, 1], (1, 0): [0, 1], (1, 1): [1, 0]}) == {
               (0, 0): Fraction(-4, 3), (1, 0): Fraction(0, 1),
               (1, 1): Fraction(2, 1)}


def test_expected_utilities5(three_bg):
    assert three_bg.expected_utilities(
        {(0, 0): [1, 0], (0, 1): [1, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (2, 0): [1, 0], (2, 1): [1, 0]}) == {(0, 0): Fraction(163, 2),
                                              (0, 1): Fraction(58, 1),
                                              (1, 0): Fraction(51, 1),
                                              (1, 1): Fraction(541, 13),
                                              (2, 0): Fraction(97, 3),
                                              (2, 1): Fraction(22, 1)
                                              }


"""
expected_utilities(bayes_mixed_joint_strat)
    Compute and return the expected utility of each player/type
    given an mixed bayesian strategy
is_equilibrium(bayes_mixed_joint_strat,precision)
    Given a bayesiant mixed strategy check if it correspond to
    a bayesian nash equilibrium
convert_to_HGG()
    Create and return the hypergraphical or polymatricial game
    equivalent to the bayesian game

"""


def test_is_equilibrium1(bimat_bg):
    assert bimat_bg.is_equilibrium(
        {(0, 0): [1, 0, 0], (0, 1): [1, 0, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (1, 2): [1, 0]}, 0.0001)


def test_is_equilibrium2(bimat_bg):
    assert not bimat_bg.is_equilibrium(
        {(0, 0): [1, 0, 0], (0, 1): [1, 0, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (1, 2): [0, 1]}, 0.0001)


def test_is_equilibrium3(bimat_bg):
    assert not bimat_bg.is_equilibrium(
        {(0, 0): [0, 1, 0], (0, 1): [1, 0, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (1, 2): [1, 0]}, 0.0001)


def test_is_equilibrium4(bimat_bg):
    assert not bimat_bg.is_equilibrium(
        {(0, 0): [1, 0, 0], (0, 1): [1, 0, 0], (1, 0): [0, 1], (1, 1): [0, 1],
         (1, 2): [0, 1]}, 0.0001)


def test_is_equilibrium5(sherif_bg1):
    assert sherif_bg1.is_equilibrium(
        {(0, 0): [1, 0], (1, 0): [0, 1], (1, 1): [1, 0]}, 0.0001)


def test_is_equilibrium6(sherif_bg1):
    assert not sherif_bg1.is_equilibrium(
        {(0, 0): [0, 1], (1, 0): [0, 1], (1, 1): [1, 0]}, 0.0001)


def test_is_equilibrium7(sherif_bg2):
    assert sherif_bg2.is_equilibrium(
        {(0, 0): [Fraction(1, 2), Fraction(1, 2)], (1, 0): [0, 1],
         (1, 1): [1, 0]}, 0.0001)


def test_is_equilibrium8(sherif_bg2):
    assert sherif_bg2.is_equilibrium(
        {(0, 0): [Fraction(1, 3), Fraction(2, 3)], (1, 0): [0, 1],
         (1, 1): [1, 0]}, 0.0001)


def test_is_equilibrium9(sherif_bg2):
    assert sherif_bg2.is_equilibrium(
        {(0, 0): [0, 1], (1, 0): [0, 1], (1, 1): [1, 0]}, 0.0001)


def test_is_equilibrium10(sherif_bg3):
    assert sherif_bg3.is_equilibrium(
        {(0, 0): [0, 1], (1, 0): [0, 1], (1, 1): [1, 0]}, 0.0001)


def test_is_equilibrium11(sherif_bg3):
    assert not sherif_bg3.is_equilibrium(
        {(0, 0): [1, 0], (1, 0): [0, 1], (1, 1): [1, 0]}, 0.0001)


def test_read_GameFile1():
    read_bg = BG.read_GameFile("filestest/internet.bg")
    assert read_bg.players_actions == [[0, 1], [0, 1]]
    assert read_bg.theta == [[0, 1], [0, 1]]
    assert read_bg.p == [Fraction(4, 10), Fraction(1, 10), Fraction(1, 10),
                         Fraction(4, 10)]
    assert read_bg.utilities == [[[3, 0, 0, 2], [3, 0, 0, 2]],
                                 [[1, 0, 0, 2], [3, 0, 0, 2]],
                                 [[3, 0, 0, 2], [1, 0, 0, 2]],
                                 [[1, 0, 0, 2], [1, 0, 0, 2]]]


def test_read_GameFile2():
    read_bg = BG.read_GameFile("filestest/test.bg")
    assert read_bg.players_actions == [[0, 1], [0, 1], [0, 1]]
    assert read_bg.theta == [[0, 1], [0, 1], [0, 1]]
    assert read_bg.p == [Fraction(1, 15), Fraction(2, 15), Fraction(1, 30),
                         Fraction(1, 6), Fraction(1, 15), Fraction(1, 5),
                         Fraction(1, 10), Fraction(7, 30)]
    assert read_bg.utilities == [
        [[-3, -10, -1, 4, -7, -9, -5, 5], [-3, -10, -1, 4, -7, -9, -5, 5],
         [-3, -5, -10, 8, -7, -9, -1, 5]],
        [[-2, -9, -1, 5, -6, -8, -4, 5], [-2, -9, -1, 5, -6, -8, -4, 5],
         [-2, -4, -9, 2, -6, -8, -1, 5]],
        [[-2, -8, -1, 8, -5, -7, -4, 4], [-2, -8, -1, 8, -5, -7, -4, 5],
         [-2, -3, -8, 5, -5, -7, -1, 4]],
        [[-2, -7, -1, 7, -4, -6, -4, 1], [-2, -7, -1, 8, -4, -6, -4, 2],
         [-2, -3, -7, 5, -4, -6, -1, 5]],
        [[-3, -10, -1, 4, -7, -9, -5, 5], [-3, -10, -1, 4, -7, -9, -5, 5],
         [-3, -5, -10, 8, -7, -9, -1, 5]],
        [[-2, -9, -1, 5, -6, -8, -4, 5], [-2, -9, -1, 5, -6, -8, -4, 5],
         [-2, -4, -9, 2, -6, -8, -1, 5]],
        [[-2, -8, -1, 8, -5, -7, -4, 4], [-2, -8, -1, 8, -5, -7, -4, 5],
         [-2, -3, -8, 5, -5, -7, -1, 4]],
        [[-2, -7, -1, 7, -4, -6, -4, 1], [-2, -7, -1, 8, -4, -6, -4, 2],
         [-2, -3, -7, 5, -4, -6, -1, 5]]]


def test_write_GameFile1(bimat_bg):
    bimat_bg.write_GameFile("filestest/bimat_bg.bg")
    read_bg = BG.read_GameFile("filestest/bimat_bg.bg")
    assert read_bg.players_actions == bimat_bg.players_actions
    assert read_bg.theta == bimat_bg.theta
    assert read_bg.p == bimat_bg.p
    assert read_bg.utilities == bimat_bg.utilities


def test_write_GameFile2(sherif_bg1):
    sherif_bg1.write_GameFile("filestest/sherif_bg1.bg")
    read_bg = BG.read_GameFile("filestest/sherif_bg1.bg")
    assert read_bg.players_actions == sherif_bg1.players_actions
    assert read_bg.theta == sherif_bg1.theta
    assert read_bg.p == sherif_bg1.p
    assert read_bg.utilities == sherif_bg1.utilities


def test_write_GameFile3(sherif_bg2):
    sherif_bg2.write_GameFile("filestest/sherif_bg2.bg")
    read_bg = BG.read_GameFile("filestest/sherif_bg2.bg")
    assert read_bg.players_actions == sherif_bg2.players_actions
    assert read_bg.theta == sherif_bg2.theta
    assert read_bg.p == sherif_bg2.p
    assert read_bg.utilities == sherif_bg2.utilities


def test_write_GameFile4(sherif_bg3):
    sherif_bg3.write_GameFile("filestest/sherif_bg3.bg")
    read_bg = BG.read_GameFile("filestest/sherif_bg3.bg")
    assert read_bg.players_actions == sherif_bg3.players_actions
    assert read_bg.theta == sherif_bg3.theta
    assert read_bg.p == sherif_bg3.p
    assert read_bg.utilities == sherif_bg3.utilities


def test_write_GameFile5(three_bg):
    three_bg.write_GameFile("filestest/three_bg.bg")
    read_bg = BG.read_GameFile("filestest/three_bg.bg")
    assert read_bg.players_actions == three_bg.players_actions
    assert read_bg.theta == three_bg.theta
    assert read_bg.p == three_bg.p
    assert read_bg.utilities == three_bg.utilities
