import numpy as np
import pytest

from gtnash.game.hypergraphicalgame import HGG
from gtnash.game.normalformgame import NFG
from fractions import Fraction

"""
Separate  assert in multiple fucntion
"""


@pytest.fixture
def first_hgg():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
         [-3, -1, -7, -5, -7, -5, -10, -9]],
        [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3], [-1, 0, -5, -3]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]

    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def second_hgg():
    utilities = [
        [[-3, -1, -3, -2, -2, -3, -2, -1], [-1, -3, -5, -1, -1, -6, -3, -4],
         [-2, -3, -6, -4, -3, -1, -3, -4]],
        [[-1, -3, -2, -2], [-1, -2, -2, -1]],
        [[-3, -1, -4, -5], [-1, -3, -1, -5]]]
    # Error up level impossible, 2->3, [[0,1],[0,1],[0,1],[0,1]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def third_hgg():
    utilities = [
        [[74, 6, 9, 60, 77, 30, 47, 0], [51, 97, 98, 83, 90, 1, 2, 47],
         [18, 16, 29, 86, 100, 96, 93, 64]],
        [[84, 48, 27, 5, 100, 62, 16, 62], [10, 88, 72, 47, 13, 24, 42, 72],
         [1, 36, 68, 0, 53, 5, 61, 97]]]
    hypergraph = [[0, 1, 3], [0, 2, 3]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def degen_hgg():
    players_actions = [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]]
    hypergraph = [[1, 2, 3], [0, 1, 3], [0, 1, 2]]
    utilities = [[[-6, -3, -3, -1, -4, -10, -7, -5, -5, -10, -2, -1, -1, -3,
                   -7, -6, -1, -2, -6, -3, -3, -4, -8, -3, -7, -8, -8],
                  [-9, -1, -8, -2, -7, -6, -7, -6, -9, -2, -4, -2, -5, -2, -3,
                   -7, -3, -7, -7, -5, -3, -5, -10, -5, -8, -9, -9],
                  [-3, -1, -2, -4, -1, -4, -8, -7, -3, -6, -9, -1, -1, -3, -7,
                   -3, -7, -2, -1, -4, -10, -4, -9, -4, -3, -6, -3]],
                 [[-7, -3, -5, -9, -9, -5, -6, -5, -2, -8, -7, -10, -2, -10,
                   -6, -10, -5, -8, -6, -1, -7, -6, -3, -5, -3, -6, -6],
                  [-3, -6, -3, -2, -9, -3, -1, -3, -6, -10, -5, -4, -9, -2,
                   -10, -7, -10, -10, -6, -8, -6, -4, -4, -1, -3, -5, -8],
                  [-9, -9, -5, -9, -6, -3, -6, -2, -7, -2, -5, -10, -3, -5, -3,
                   -4, -9, -8, -3, -1, -6, -2, -2, -7, -10, -10, -3]],
                 [[-1, -8, -5, -4, -2, -5, -1, -10, -5, -2, -1, -3, -7, -3, -5,
                   -1, -7, -9, -9, -4, -5, -5, -10, -3, -6, -2, -6],
                  [-5, -7, -1, -9, -3, -7, -6, -10, -8, -9, -4, -1, -8, -5, -1,
                   -10, -6, -4, -4, -7, -6, -10, -5, -8, -7, -3, -2],
                  [-6, -8, -6, -3, -1, -6, -7, -2, -9, -7, -9, -10, -4, -3, -6,
                   -5, -5, -10, -4, -4, -5, -4, -10, -3, -4, -5, -3]]]
    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def first_hgg_fraction():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [[[Fraction(-3, 2), Fraction(-7, 2), Fraction(-7, 2),
                   Fraction(-10, 2), Fraction(-1, 2), Fraction(-5, 2),
                   Fraction(-5, 2), Fraction(-9, 2)],
                  [Fraction(-3, 4), Fraction(-7, 4), Fraction(-1, 4),
                   Fraction(-5, 4), Fraction(-7, 4), Fraction(-10, 4),
                   Fraction(-5, 4), Fraction(-9, 4)],
                  [-3, -1, -7, -5, -7, -5, -10, -9]],
                 [[Fraction(-1, 4), Fraction(-5, 4), 0, Fraction(-3, 4)],
                  [Fraction(-1, 3), 0, Fraction(-5, 3), Fraction(-3, 3)]],
                 [[-1, -5, 0, -3],
                  [Fraction(-1, 3), 0, Fraction(-5, 3), Fraction(-3, 3)]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]

    return HGG(players_actions, utilities, hypergraph)


# joint_actions

def test_joint_actions1(first_hgg):
    assert (first_hgg.local_normalformgames[0].joint_actions == np.mat(
        [[0., 0., 0.], [0., 0., 1.], [0., 1., 0.], [0., 1., 1.], [1., 0., 0.],
         [1., 0., 1.], [1., 1., 0.], [1., 1., 1.]])).all()


def test_joint_actions2(first_hgg):
    assert (first_hgg.local_normalformgames[1].joint_actions == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_actions3(first_hgg):
    assert (first_hgg.local_normalformgames[2].joint_actions == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_actions4(degen_hgg):
    assert (degen_hgg.local_normalformgames[0].joint_actions == np.mat(
        [[0., 0., 0.], [0., 0., 1.], [0., 0., 2.], [0., 1., 0.], [0., 1., 1.],
         [0., 1., 2.],
         [0., 2., 0.], [0., 2., 1.], [0., 2., 2.], [1., 0., 0.], [1., 0., 1.],
         [1., 0., 2.],
         [1., 1., 0.], [1., 1., 1.], [1., 1., 2.], [1., 2., 0.], [1., 2., 1.],
         [1., 2., 2.],
         [2., 0., 0.], [2., 0., 1.], [2., 0., 2.], [2., 1., 0.], [2., 1., 1.],
         [2., 1., 2.],
         [2., 2., 0.], [2., 2., 1.], [2., 2., 2.]])).all()


def test_joint_actions5(degen_hgg):
    assert (degen_hgg.local_normalformgames[0].joint_actions ==
            degen_hgg.local_normalformgames[1].joint_actions).all()


def test_joint_actions6(degen_hgg):
    assert (degen_hgg.local_normalformgames[0].joint_actions ==
            degen_hgg.local_normalformgames[2].joint_actions).all()


# Add test on creation of local games?


# Modification of  generate local normal form, remove the np.array()
# from method, useless?, confusing and redondant
def test_utilities1(first_hgg):
    assert first_hgg.local_normalformgames[0].utilities == [
        [-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
        [-3, -1, -7, -5, -7, -5, -10, -9]]
    # assert first_hgg.local_normalformgames[0].utilities.all() ==
    # np.array([[-3, -7, -7, -10, -1, -5, -5, -9],
    # [-3, -7, -1, -5, -7, -10, -5, -9],
    # [-3, -1, -7, -5, -7, -5, -10, -9]]).all()


def test_utilities2(first_hgg):
    assert first_hgg.local_normalformgames[1].utilities == [[-1, -5, 0, -3],
                                                            [-1, 0, -5, -3]]


def test_utilities3(first_hgg):
    assert first_hgg.local_normalformgames[2].utilities == [[-1, -5, 0, -3],
                                                            [-1, 0, -5, -3]]


def test_utilities4(degen_hgg):
    assert degen_hgg.local_normalformgames[0].utilities == \
           [[-6, -3, -3, -1, -4, -10, -7, -5, -5, -10, -2, -1, -1, -3, -7, -6,
             -1, -2, -6, -3, -3, -4, -8, -3, -7, -8, -8],
            [-9, -1, -8, -2, -7, -6, -7, -6, -9, -2, -4, -2, -5, -2, -3, -7,
             -3, -7, -7, -5, -3, -5, -10, -5, -8, -9, -9],
            [-3, -1, -2, -4, -1, -4, -8, -7, -3, -6, -9, -1, -1, -3, -7, -3,
             -7, -2, -1, -4, -10, -4, -9, -4, -3, -6, -3]]


def test_utilities5(degen_hgg):
    assert degen_hgg.local_normalformgames[1].utilities == \
           [[-7, -3, -5, -9, -9, -5, -6, -5, -2, -8, -7, -10, -2, -10, -6, -10,
             -5, -8, -6, -1, -7, -6, -3, -5, -3, -6, -6],
            [-3, -6, -3, -2, -9, -3, -1, -3, -6, -10, -5, -4, -9, -2, -10, -7,
             -10, -10, -6, -8, -6, -4, -4, -1, -3, -5, -8],
            [-9, -9, -5, -9, -6, -3, -6, -2, -7, -2, -5, -10, -3, -5, -3, -4,
             -9, -8, -3, -1, -6, -2, -2, -7, -10, -10, -3]]


def test_utilities6(degen_hgg):
    assert degen_hgg.local_normalformgames[2].utilities == \
           [[-1, -8, -5, -4, -2, -5, -1, -10, -5, -2, -1, -3, -7, -3, -5, -1,
             -7, -9, -9, -4, -5, -5, -10, -3, -6, -2, -6],
            [-5, -7, -1, -9, -3, -7, -6, -10, -8, -9, -4, -1, -8, -5, -1, -10,
             -6, -4, -4, -7, -6, -10, -5, -8, -7, -3, -2],
            [-6, -8, -6, -3, -1, -6, -7, -2, -9, -7, -9, -10, -4, -3, -6, -5,
             -5, -10, -4, -4, -5, -4, -10, -3, -4, -5, -3]]


# joint_action_except_i
# no degen hgg

def test_joint_action_except_i1(first_hgg):
    assert (first_hgg.joint_action_except_i(0)[0] == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_action_except_i2(first_hgg):
    assert (first_hgg.joint_action_except_i(1)[0] == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_action_except_i3(first_hgg):
    assert (first_hgg.joint_action_except_i(2)[0] == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_action_except_i4(first_hgg):
    assert (first_hgg.joint_action_except_i(0)[1] == [])


def test_joint_action_except_i5(first_hgg):
    assert (first_hgg.joint_action_except_i(0)[2] == [])


def test_joint_action_except_i6(first_hgg):
    assert (first_hgg.joint_action_except_i(1)[1] == np.mat(
        [[0.], [1.]])).all()


def test_joint_action_except_i7(first_hgg):
    assert (first_hgg.joint_action_except_i(1)[2] == [])


def test_joint_action_except_i8(first_hgg):
    assert (first_hgg.joint_action_except_i(2)[1] == [])


def test_joint_action_except_i9(first_hgg):
    assert (first_hgg.joint_action_except_i(1)[2] == np.mat(
        [[0.], [1.]])).all()


def test_joint_action_except_i10(first_hgg):
    assert (first_hgg.joint_action_except_i(3)[0] == [])


def test_joint_action_except_i11(first_hgg):
    assert (first_hgg.joint_action_except_i(3)[1] == np.mat(
        [[0.], [1.]])).all()


def test_joint_action_except_i12(first_hgg):
    assert (first_hgg.joint_action_except_i(3)[2] == np.mat(
        [[0.], [1.]])).all()


# expected_utilities
# no degen hff

def test_expected_utilities1(first_hgg):
    assert (first_hgg.expected_utilities(
        {0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [1, 0]}) == np.mat(
        [-3., -4., -4., -2.])).all()


def test_expected_utilities2(first_hgg):
    assert (first_hgg.expected_utilities(
        {0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1]}) == np.mat(
        [-9., -12., -12., -6.])).all()


def test_expected_utilities3(first_hgg):
    assert (first_hgg.expected_utilities(
        {0: [1, 0], 1: [1, 0], 2: [0, 1], 3: [0, 1]}) == np.mat(
        [-7., -12., -4., -3.])).all()


def test_expected_utilities4(first_hgg):
    assert (first_hgg.expected_utilities(
        {0: [1 / 2, 1 / 2], 1: [1 / 2, 1 / 2], 2: [1 / 2, 1 / 2],
         3: [1 / 2, 1 / 2]}) == np.mat([-5.875, -8.125, -8.125, -4.5])).all()


# is_equilibrium
# no degen

def test_is_equilibrium1(first_hgg):
    assert not (
        first_hgg.is_equilibrium({0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [1, 0]}))


def test_is_equilibrium2(first_hgg):
    assert (
        first_hgg.is_equilibrium({0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1]}))


def test_is_equilibrium3(first_hgg):
    assert not (
        first_hgg.is_equilibrium({0: [1, 0], 1: [1, 0], 2: [0, 1], 3: [0, 1]}))


def test_is_equilibrium4(first_hgg):
    assert not (first_hgg.is_equilibrium(
        {0: [1 / 2, 1 / 2], 1: [1 / 2, 1 / 2], 2: [1 / 2, 1 / 2],
         3: [1 / 2, 1 / 2]}))


# util_of_player
# no degen

def test_util_of_player1(first_hgg):
    assert (first_hgg.util_of_player(0).keys() == {0} and
            (first_hgg.util_of_player(0)[0] == [-3, -7, -7, -10, -1, -5, -5,
                                                -9]))


def test_util_of_player2(first_hgg):
    assert (first_hgg.util_of_player(1).keys() == {0, 1} and
            (first_hgg.util_of_player(1)[0] == [-3, -7, -1, -5, -7, -10, -5,
                                                -9]) and
            (first_hgg.util_of_player(1)[1] == [-1, -5, 0, -3]))


def test_util_of_player3(first_hgg):
    assert (first_hgg.util_of_player(2).keys() == {0, 2} and
            (first_hgg.util_of_player(2)[0] == [-3, -1, -7, -5, -7, -5, -10,
                                                -9]) and
            (first_hgg.util_of_player(2)[2] == [-1, -5, 0, -3]))


def test_util_of_player4(first_hgg):
    assert (first_hgg.util_of_player(3).keys() == {1, 2} and
            (first_hgg.util_of_player(3)[1] == [-1, 0, -5, -3]) and
            (first_hgg.util_of_player(3)[2] == [-1, 0, -5, -3]))


# PNE METHOD MISSING

# first_hgg
# second_hgg
# third_hgg
# degen_hgg
# first_hgg_fraction


def test_get_all_PNE1(first_hgg):
    assert first_hgg.get_all_PNE() == [
        {0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1]}
    ]


def test_get_all_PNE2(second_hgg):
    assert second_hgg.get_all_PNE() == []


def test_get_all_PNE3(third_hgg):
    assert third_hgg.get_all_PNE() == []


def test_get_all_PNE4(degen_hgg):
    assert degen_hgg.get_all_PNE() == [
        {0: [1, 0, 0], 1: [1, 0, 0], 2: [1, 0, 0], 3: [0, 0, 1]},
        {0: [1, 0, 0], 1: [0, 1, 0], 2: [0, 1, 0], 3: [0, 1, 0]},
        {0: [1, 0, 0], 1: [0, 0, 1], 2: [1, 0, 0], 3: [0, 1, 0]},
        {0: [0, 1, 0], 1: [1, 0, 0], 2: [0, 1, 0], 3: [1, 0, 0]}
    ]


def test_get_all_PNE5(first_hgg_fraction):
    tmp_hgg = first_hgg_fraction.game_as_int()
    assert tmp_hgg.get_all_PNE() == [
        {0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1]}
    ]


def test_pne_exist1(first_hgg):
    assert first_hgg.pne_exist()


def test_pne_exist2(second_hgg):
    assert not second_hgg.pne_exist()


def test_pne_exist3(third_hgg):
    assert not third_hgg.pne_exist()


def test_pne_exist4(degen_hgg):
    assert degen_hgg.pne_exist()


def test_pne_exist5(first_hgg_fraction):
    tmp_hgg = first_hgg_fraction.game_as_int()
    assert tmp_hgg.pne_exist()
# build_subgame
# no degen


def test_build_subgame1(first_hgg):
    sub_first_hgg1 = first_hgg.build_subgame({3: [1, 0]})
    assert (sub_first_hgg1.players_actions == [[0, 1], [0, 1], [0, 1],
                                               [-1]] and
            sub_first_hgg1.utilities == [[[-3, -7, -7, -10, -1, -5, -5, -9],
                                          [-3, -7, -1, -5, -7, -10, -5, -9],
                                          [-3, -1, -7, -5, -7, -5, -10, -9]],
                                         [[-1, 0], [-1, -5]],
                                         [[-1, 0], [-1, -5]]])


def test_build_subgame2(first_hgg):
    sub_first_hgg2 = first_hgg.build_subgame({0: [1, 0]})
    assert (sub_first_hgg2.players_actions == [[-1], [0, 1], [0, 1],
                                               [0, 1]] and
            sub_first_hgg2.utilities == [
                [[-3, -7, -7, -10], [-3, -7, -1, -5], [-3, -1, -7, -5]],
                [[-1, -5, 0, -3], [-1, 0, -5, -3]],
                [[-1, -5, 0, -3], [-1, 0, -5, -3]]])


def test_build_subgame3(first_hgg):
    sub_first_hgg3 = first_hgg.build_subgame({1: [1, 0], 2: [0, 1]})
    assert (sub_first_hgg3.players_actions == [[0, 1], [-1], [-1], [0, 1]] and
            sub_first_hgg3.utilities == [[[-7, -5], [-7, -10], [-1, -5]],
                                         [[-1, -5], [-1, 0]],
                                         [[0, -3], [-5, -3]]])

    # [[[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
    # [-3, -1, -7, -5, -7, -5, -10, -9]],
    # [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3], [-1, 0, -5, -3]]]


# [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
# [-3, -1, -7, -5, -7, -5, -10, -9]],
#        [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3],
#        [-1, 0, -5, -3]]]


# simplify_subgame
# no degen

"""
MODIFICATION OF SIMPLIFY REQUIRED
"""


def test_simplify_subgame1(first_hgg):
    simplify_first_hgg1 = first_hgg.build_subgame(
        {3: [1, 0]}).simplify_subgame()
    assert (simplify_first_hgg1.players_actions == [[0, 1], [0, 1], [0, 1]] and
            simplify_first_hgg1.utilities == [
                [[-3, -7, -7, -10, -1, -5, -5, -9],
                 [-3, -7, -1, -5, -7, -10, -5, -9],
                 [-3, -1, -7, -5, -7, -5, -10, -9]],
                [[-1, 0]], [[-1, 0]]])

    # ISSUE WITH THE DURING THE SIMPLIFICATION


# def test_simplify_subgame2(first_hgg):
#     simplify_first_hgg2 = first_hgg.build_subgame
#       ({0: [1, 0]}).simplify_subgame()
#     assert (simplify_first_hgg2.players_actions ==
#     [[0, 1], [0, 1], [0, 1]] and
#             simplify_first_hgg2.utilities ==
#             [[[-3, -7, -1, -5], [-3, -1, -7, -5]],
#                                          [[-1, -5, 0, -3], [-1, 0, -5, -3]],
#                                          [[-1, -5, 0, -3], [-1, 0, -5, -3]]])


# get_subgame_fixed_strat
# no degen

def test_get_subgame_fixed_strat1(first_hgg):
    sub_first_hgg1 = first_hgg.get_subgame_fixed_strat(
        {0: [1, 1], 1: [1, 1], 2: [1, 1], 3: [1, 0]})
    assert (sub_first_hgg1.players_actions == [[0, 1], [0, 1], [0, 1], [0]] and
            sub_first_hgg1.utilities == [[[-3, -7, -7, -10, -1, -5, -5, -9],
                                          [-3, -7, -1, -5, -7, -10, -5, -9],
                                          [-3, -1, -7, -5, -7, -5, -10, -9]],
                                         [[-1, 0], [-1, -5]],
                                         [[-1, 0], [-1, -5]]])


def test_get_subgame_fixed_strat2(first_hgg):
    sub_first_hgg2 = first_hgg.get_subgame_fixed_strat(
        {0: [1, 0], 1: [1, 1], 2: [1, 1], 3: [1, 1]})
    assert (sub_first_hgg2.players_actions == [[0], [0, 1], [0, 1], [0, 1]] and
            sub_first_hgg2.utilities == [
                [[-3, -7, -7, -10], [-3, -7, -1, -5], [-3, -1, -7, -5]],
                [[-1, -5, 0, -3], [-1, 0, -5, -3]],
                [[-1, -5, 0, -3], [-1, 0, -5, -3]]])


def test_get_subgame_fixed_strat3(first_hgg):
    sub_first_hgg3 = first_hgg.get_subgame_fixed_strat(
        {0: [1, 1], 1: [1, 0], 2: [0, 1], 3: [1, 1]})
    assert (sub_first_hgg3.players_actions == [[0, 1], [0], [1], [0, 1]] and
            sub_first_hgg3.utilities == [[[-7, -5], [-7, -10], [-1, -5]],
                                         [[-1, -5], [-1, 0]],
                                         [[0, -3], [-5, -3]]])


def test_local_game_of_player_n1(first_hgg, degen_hgg):
    assert (first_hgg.local_game_of_player_n(0) == [0])


def test_local_game_of_player_n2(first_hgg):
    assert (first_hgg.local_game_of_player_n(1) == [0, 1])


def test_local_game_of_player_n3(first_hgg):
    assert (first_hgg.local_game_of_player_n(2) == [0, 2])


def test_local_game_of_player_n4(first_hgg):
    assert (first_hgg.local_game_of_player_n(3) == [1, 2])


def test_local_game_of_player_n5(degen_hgg):
    assert (degen_hgg.local_game_of_player_n(0) == [1, 2])


def test_local_game_of_player_n6(degen_hgg):
    assert (degen_hgg.local_game_of_player_n(1) == [0, 1, 2])


def test_local_game_of_player_n7(degen_hgg):
    assert (degen_hgg.local_game_of_player_n(2) == [0, 2])


def test_local_game_of_player_n8(degen_hgg):
    assert (degen_hgg.local_game_of_player_n(3) == [0, 1])


"""
Add another hypergraphical game
"""


# get_max_value_of_player_n
def test_get_max_value_of_player_n1(first_hgg):
    assert (first_hgg.get_max_value_of_player_n(0) == -1)


def test_get_max_value_of_player_n2(first_hgg):
    assert (first_hgg.get_max_value_of_player_n(1) == 0)


def test_get_max_value_of_player_n3(first_hgg):
    assert (first_hgg.get_max_value_of_player_n(2) == 0)


def test_get_max_value_of_player_n4(first_hgg):
    assert (first_hgg.get_max_value_of_player_n(3) == 0)


def test_get_max_value_of_player_n5(degen_hgg):
    assert (degen_hgg.get_max_value_of_player_n(0) == -1)


def test_get_max_value_of_player_n6(degen_hgg):
    assert (degen_hgg.get_max_value_of_player_n(1) == -1)


def test_get_max_value_of_player_n7(degen_hgg):
    assert (degen_hgg.get_max_value_of_player_n(2) == -1)


def test_get_max_value_of_player_n8(degen_hgg):
    assert (degen_hgg.get_max_value_of_player_n(3) == -1)


# index_of_player_in_local
def test_index_of_player_in_local1(first_hgg, degen_hgg):
    assert (first_hgg.index_of_player_in_local(0) == {0: 0})


def test_index_of_player_in_local2(first_hgg):
    assert (first_hgg.index_of_player_in_local(1) == {0: 1, 1: 0})


def test_index_of_player_in_local3(first_hgg):
    assert (first_hgg.index_of_player_in_local(2) == {0: 2, 2: 0})


def test_index_of_player_in_local4(first_hgg):
    assert (first_hgg.index_of_player_in_local(3) == {1: 1, 2: 1})


def test_index_of_player_in_local5(degen_hgg):
    assert (degen_hgg.index_of_player_in_local(0) == {1: 0, 2: 0})


def test_index_of_player_in_local6(degen_hgg):
    assert (degen_hgg.index_of_player_in_local(1) == {0: 0, 1: 1, 2: 1})


def test_index_of_player_in_local7(degen_hgg):
    assert (degen_hgg.index_of_player_in_local(2) == {0: 1, 2: 2})


def test_index_of_player_in_local8(degen_hgg):
    assert (degen_hgg.index_of_player_in_local(3) == {0: 2, 1: 2})


# get_subgame_level

def test_get_subgame_level1(first_hgg):
    sub_level_first_hgg1 = first_hgg.get_subgame_level(
        {0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [1, 0]})
    assert (sub_level_first_hgg1.players_actions == [[0, 1], [0, 1],
                                                     [0, 1]] and
            sub_level_first_hgg1.utilities == [
                [[-3, -7, -7, -10, -1, -5, -5, -9],
                 [-3, -7, -1, -5, -7, -10, -5, -9],
                 [-3, -1, -7, -5, -7, -5, -10, -9]],
                [[-1, 0]], [[-1, 0]]])


def test_get_subgame_level2(first_hgg):
    sub_level_first_hgg2 = first_hgg.get_subgame_level(
        {0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [0, 1]})
    assert (sub_level_first_hgg2.players_actions == [[0, 1], [0, 1],
                                                     [0, 1]] and
            sub_level_first_hgg2.utilities == [
                [[-3, -7, -7, -10, -1, -5, -5, -9],
                 [-3, -7, -1, -5, -7, -10, -5, -9],
                 [-3, -1, -7, -5, -7, -5, -10, -9]],
                [[-5, -3]], [[-5, -3]]])


def test_get_subgame_level3(degen_hgg):
    sub_level_degen_hgg1 = degen_hgg.get_subgame_level(
        {0: [1, 0, 0], 1: [1, 0, 0], 2: [1, 0, 0], 3: [1, 0, 0]})
    assert (sub_level_degen_hgg1.players_actions == [[0, 1, 2], [0, 1, 2],
                                                     [0, 1, 2]] and
            sub_level_degen_hgg1.utilities == [
                [[-6, -1, -7, -10, -1, -6, -6, -4, -7],
                 [-9, -2, -7, -2, -5, -7, -7, -5, -8]],
                [[-7, -9, -6, -8, -2, -10, -6, -6, -3],
                 [-3, -2, -1, -10, -9, -7, -6, -4, -3]],
                [[-1, -8, -5, -4, -2, -5, -1, -10, -5, -2, -1, -3, -7, -3, -5,
                  -1, -7, -9, -9, -4, -5, -5, -10, -3, -6, -2, -6],
                 [-5, -7, -1, -9, -3, -7, -6, -10, -8, -9, -4, -1, -8, -5, -1,
                  -10, -6, -4, -4, -7, -6, -10, -5, -8, -7, -3, -2],
                 [-6, -8, -6, -3, -1, -6, -7, -2, -9, -7, -9, -10, -4, -3, -6,
                  -5, -5, -10, -4, -4, -5, -4, -10, -3, -4, -5, -3]]])


def test_get_subgame_level4(degen_hgg):
    sub_level_degen_hgg1 = degen_hgg.get_subgame_level(
        {0: [1, 0, 0], 1: [1, 0, 0], 2: [1, 0, 0], 3: [1, 0, 0]})
    sub_level_degen_hgg1bis = sub_level_degen_hgg1.get_subgame_level(
        {0: [1, 0, 0], 1: [1, 0, 0], 2: [1, 0, 0]})
    assert (sub_level_degen_hgg1bis.players_actions == [[0, 1, 2],
                                                        [0, 1, 2]] and
            sub_level_degen_hgg1bis.utilities == [
                [[-6, -10, -6, ]],
                [[-7, -9, -6, -8, -2, -10, -6, -6, -3],
                 [-3, -2, -1, -10, -9, -7, -6, -4, -3]],
                [[-1, -4, -1, -2, -7, -1, -9, -5, -6],
                 [-5, -9, -6, -9, -8, -10, -4, -10, -7]]])


def test_get_subgame_without_n1(first_hgg):
    sub_n_first_hgg = first_hgg.get_subgame_without_n(
        {0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [1, 0]}, 0)
    assert (sub_n_first_hgg.players_actions == [[0, 1], [0, 1], [0, 1]] and
            sub_n_first_hgg.utilities == [[[-3, -7, -1, -5], [-3, -1, -7, -5]],
                                          [[-1, -5, 0, -3], [-1, 0, -5, -3]],
                                          [[-1, -5, 0, -3], [-1, 0, -5, -3]]])


def test_get_subgame_without_n2(first_hgg):
    sub_n_first_hgg = first_hgg.get_subgame_without_n(
        {0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [1, 0]}, 2)
    assert (sub_n_first_hgg.players_actions == [[0, 1], [0, 1], [0, 1]] and
            sub_n_first_hgg.utilities == [[[-3, -7, -1, -5], [-3, -1, -7, -5]],
                                          [[-1, -5, 0, -3], [-1, 0, -5, -3]],
                                          [[-1, 0]]])


def test_get_subgame_without_n3(degen_hgg):
    sub_n_degen_hgg1 = degen_hgg.get_subgame_without_n(
        {0: [1, 0, 0], 1: [1, 0, 0], 2: [1, 0, 0], 3: [1, 0, 0]}, 0)
    assert (sub_n_degen_hgg1.players_actions == [[0, 1, 2], [0, 1, 2],
                                                 [0, 1, 2]] and
            sub_n_degen_hgg1.utilities == [[[-6, -3, -3, -1, -4, -10, -7, -5,
                                             -5, -10, -2, -1, -1, -3, -7, -6,
                                             -1, -2, -6, -3, -3, -4, -8, -3,
                                             -7, -8, -8],
                                            [-9, -1, -8, -2, -7, -6, -7, -6,
                                             -9, -2, -4, -2, -5, -2, -3, -7,
                                             -3, -7, -7, -5, -3, -5, -10, -5,
                                             -8, -9, -9],
                                            [-3, -1, -2, -4, -1, -4, -8, -7,
                                             -3, -6, -9, -1, -1, -3, -7, -3,
                                             -7, -2, -1, -4, -10, -4, -9, -4,
                                             -3, -6, -3]],
                                           [[-3, -6, -3, -2, -9, -3, -1, -3,
                                             -6],
                                            [-9, -9, -5, -9, -6, -3, -6, -2,
                                             -7]],
                                           [[-5, -7, -1, -9, -3, -7, -6, -10,
                                             -8],
                                            [-6, -8, -6, -3, -1, -6, -7, -2,
                                             -9]]])


# get_player_interact

def test_get_player_interact1(first_hgg):
    assert (first_hgg.get_player_interact(0) == [1, 2])


def test_get_player_interact2(first_hgg):
    assert (first_hgg.get_player_interact(1) == [0, 2, 3])


def test_get_player_interact3(first_hgg):
    assert (first_hgg.get_player_interact(2) == [0, 1, 3])


def test_get_player_interact4(first_hgg):
    assert (first_hgg.get_player_interact(3) == [1, 2])


def test_get_player_interact5(degen_hgg):
    assert (degen_hgg.get_player_interact(0) == [1, 2, 3])


def test_get_player_interact6(degen_hgg):
    assert (degen_hgg.get_player_interact(1) == [0, 2, 3])


def test_get_player_interact7(degen_hgg):
    assert (degen_hgg.get_player_interact(2) == [0, 1, 3])


def test_get_player_interact8(degen_hgg):
    assert (degen_hgg.get_player_interact(3) == [0, 1, 2])


def test_get_player_interact_except_e1(first_hgg, degen_hgg):
    assert (first_hgg.get_player_interact_except_e(0, [0, 1, 2]) == [])


def test_get_player_interact_except_e2(first_hgg):
    assert (first_hgg.get_player_interact_except_e(1, [0, 1, 2]) == [3])


def test_get_player_interact_except_e3(first_hgg):
    assert (first_hgg.get_player_interact_except_e(1, [1, 3]) == [0, 2])


def test_get_player_interact_except_e4(first_hgg):
    assert (first_hgg.get_player_interact_except_e(2, [0, 1, 2]) == [3])


def test_get_player_interact_except_e5(first_hgg):
    assert (first_hgg.get_player_interact_except_e(2, [2, 3]) == [0, 1])


def test_get_player_interact_except_e6(first_hgg):
    assert (first_hgg.get_player_interact_except_e(3, [1, 3]) == [2])


def test_get_player_interact_except_e7(first_hgg):
    assert (first_hgg.get_player_interact_except_e(3, [2, 3]) == [1])


# Depend on meaning of returned value of get_player_interact_except_e
# assert (degen_hgg.get_player_interact_except_e(0, [0, 1, 3]) == [2])
# or [1, 2]
# assert (degen_hgg.get_player_interact_except_e(0, [0, 1, 2]) == [3])
# or [1, 3]
# assert (degen_hgg.get_player_interact_except_e(1, [0, 1, 2]) == [3])
# or [2, 3]
# assert (degen_hgg.get_player_interact_except_e(1, [1, 2, 3]) == [0])
# or [0, 2]
# assert (degen_hgg.get_player_interact_except_e(2, [1, 2, 3]) == [0])
# or [0, 1]
# assert (degen_hgg.get_player_interact_except_e(2, [0, 1, 2]) == [3])
# or [1, 3]
# assert (degen_hgg.get_player_interact_except_e(3, [1, 2, 3]) == [0])
# or [0, 1]
# assert (degen_hgg.get_player_interact_except_e(3, [0, 1, 3]) == [2])
# or [0, 2]


def test_get_player_except_e1(first_hgg, degen_hgg):
    assert (first_hgg.get_player_except_e([0, 1, 2]) == [3])


def test_get_player_except_e2(first_hgg):
    assert (first_hgg.get_player_except_e([1, 3]) == [0, 2])


def test_get_player_except_e3(first_hgg):
    assert (first_hgg.get_player_except_e([2, 3]) == [0, 1])


def test_get_player_except_e4(degen_hgg):
    assert (degen_hgg.get_player_except_e([1, 2, 3]) == [0])


def test_get_player_except_e5(degen_hgg):
    assert (degen_hgg.get_player_except_e([0, 1, 3]) == [2])


def test_get_player_except_e6(degen_hgg):
    assert (degen_hgg.get_player_except_e([0, 1, 2]) == [3])


"""
    get_player_except_e(hyper_e)
    is_GG():
    is_PMG():
    convert_to_NFG()
    convert_to_HGG()

"""


def test_convert_to_NFG1(first_hgg):
    new_nfg = first_hgg.convert_to_NFG()
    assert new_nfg.players_actions == first_hgg.players_actions
    assert new_nfg.utilities == [
        [-3, -3, -7, -7, -7, -7, -10, -10, -1, -1, -5, -5, -5, -5, -9, -9],
        [-4, -8, -8, -12, -1, -4, -5, -8, -8, -12, -11, -15, -5, -8, -9, -12],
        [-4, -8, -1, -4, -8, -12, -5, -8, -8, -12, -5, -8, -11, -15, -9, -12],
        [-2, 0, -6, -3, -6, -3, -10, -6, -2, 0, -6, -3, -6, -3, -10, -6]]


def test_convert_to_NFG2(second_hgg):
    new_nfg = second_hgg.convert_to_NFG()
    assert new_nfg.players_actions == second_hgg.players_actions
    assert new_nfg.utilities == [
        [-3, -3, -1, -1, -3, -3, -2, -2, -2, -2, -3, -3, -2, -2, -1, -1],
        [-2, -4, -4, -6, -7, -7, -3, -3, -2, -4, -7, -9, -5, -5, -6, -6],
        [-5, -3, -7, -8, -9, -7, -8, -9, -6, -4, -5, -6, -6, -4, -8, -9],
        [-2, -5, -2, -7, -3, -4, -3, -6, -2, -5, -2, -7, -3, -4, -3, -6]]


def test_convert_to_NFG3(third_hgg):
    new_nfg = third_hgg.convert_to_NFG()
    assert new_nfg.players_actions == third_hgg.players_actions
    assert new_nfg.utilities == [
        [158, 54, 101, 11, 93, 108, 36, 65, 177, 92, 93, 92, 147, 62, 63, 62],
        [51, 97, 51, 97, 98, 83, 98, 83, 90, 1, 90, 1, 2, 47, 2, 47],
        [10, 88, 72, 47, 10, 88, 72, 47, 13, 24, 42, 72, 13, 24, 42, 72],
        [19, 52, 86, 16, 30, 122, 97, 86, 153, 101, 161, 193, 146, 69, 154,
         161]]


def test_convert_to_NFG4(degen_hgg):
    new_nfg = degen_hgg.convert_to_NFG()
    assert new_nfg.players_actions == degen_hgg.players_actions
    assert new_nfg.utilities == [
        [-8, -4, -6, -15, -11, -13, -12, -8, -10, -13, -13, -9, -11, -11, -7,
         -14, -14, -10, -7, -6, -3, -16, -15, -12, -11, -10, -7, -10, -9, -12,
         -9, -8, -11, -11, -10, -13, -9, -17, -13, -5, -13, -9, -7, -15, -11,
         -11, -6, -9, -17, -12, -15, -19, -14, -17, -15, -10, -16, -10, -5,
         -11, -11, -6, -12, -11, -8, -10, -16, -13, -15, -9, -6, -8, -9, -12,
         -12, -5, -8, -8, -9, -12, -12],
        [-14, -14, -11, -11, -17, -20, -11, -12, -9, -21, -20, -13, -6, -15,
         -13, -15, -17, -12, -13, -12, -15, -15, -21, -19, -16, -19, -22, -25,
         -17, -16, -15, -13, -18, -18, -11, -10, -27, -12, -19, -15, -10, -22,
         -16, -4, -13, -23, -23, -23, -17, -24, -19, -18, -22, -22, -16, -15,
         -13, -14, -19, -23, -19, -19, -17, -24, -16, -12, -10, -12, -13, -18,
         -13, -11, -16, -15, -18, -10, -16, -14, -12, -15, -18],
        [-15, -7, -14, -10, -15, -14, -13, -12, -15, -5, -7, -5, -6, -3, -4,
         -13, -9, -13, -14, -12, -10, -7, -12, -7, -17, -18, -18, -16, -8, -15,
         -11, -16, -15, -17, -16, -19, -6, -8, -6, -8, -5, -6, -13, -9, -13,
         -12, -10, -8, -10, -15, -10, -18, -19, -19, -13, -5, -12, -6, -11,
         -10, -12, -11, -14, -6, -8, -6, -15, -12, -13, -10, -6, -10, -11, -9,
         -7, -10, -15, -10, -11, -12, -12],
        [-12, -10, -7, -13, -10, -9, -17, -16, -8, -15, -15, -4, -10, -9, -10,
         -12, -13, -5, -7, -6, -17, -10, -11, -11, -9, -8, -10, -5, -6, -12,
         -6, -6, -14, -10, -12, -13, -9, -14, -4, -4, -8, -10, -6, -12, -5, -5,
         -13, -18, -8, -18, -12, -7, -15, -11, -6, -2, -8, -7, -2, -10, -11,
         -8, -9, -8, -11, -8, -3, -5, -14, -5, -9, -9, -11, -14, -13, -14, -19,
         -7, -13, -16, -6]]


def test_convert_to_HGG1():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[-3, -7, -7, -10, -1, -5, -5, -9],
                 [-3, -7, -1, -5, -7, -10, -5, -9],
                 [-3, -1, -7, -5, -7, -5, -10, -9]]
    nfg = NFG(players_actions, utilities)
    new_hgg = HGG.convert_to_HGG(nfg)
    assert new_hgg.players_actions == nfg.players_actions
    assert new_hgg.hypergraph == [[0, 1, 2]]
    assert new_hgg.utilities == [
        [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
         [-3, -1, -7, -5, -7, -5, -10, -9]]]


def test_convert_to_HGG2():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [51, 29, 47, 43, 75, 61, 42, 19, 28, 39, 40, 21, 60, 60, 67, 44],
        [58, 72, 31, 41, 37, 5, 37, 41, 53, 68, 38, 30, 58, 72, 75, 0],
        [29, 73, 42, 13, 34, 31, 54, 25, 47, 29, 19, 46, 85, 79, 65, 24],
        [1, 17, 49, 9, 51, 25, 21, 49, 28, 77, 41, 69, 13, 100, 49, 27]]
    nfg = NFG(players_actions, utilities)
    new_hgg = HGG.convert_to_HGG(nfg)
    assert new_hgg.players_actions == nfg.players_actions
    assert new_hgg.hypergraph == [[0, 1, 2, 3]]
    assert new_hgg.utilities == [
        [[51, 29, 47, 43, 75, 61, 42, 19, 28, 39, 40, 21, 60, 60, 67, 44],
         [58, 72, 31, 41, 37, 5, 37, 41, 53, 68, 38, 30, 58, 72, 75, 0],
         [29, 73, 42, 13, 34, 31, 54, 25, 47, 29, 19, 46, 85, 79, 65, 24],
         [1, 17, 49, 9, 51, 25, 21, 49, 28, 77, 41, 69, 13, 100, 49, 27]]]


def test_game_as_int(first_hgg_fraction, first_hgg):
    new_hgg = first_hgg_fraction.game_as_int()
    assert new_hgg.utilities == first_hgg.utilities


def test_read_GameFile1():
    read_hgg = HGG.read_GameFile("filestest/CovG_0.hgg")
    assert read_hgg.players_actions == [[0, 1], [0, 1], [0, 1], [0, 1]]
    assert read_hgg.hypergraph == [[0, 1, 3], [1, 2, 3]]
    assert read_hgg.utilities == [[[100, 33, 31, 40, 35, 52, 40, 30],
                                   [25, 34, 18, 47, 54, 30, 52, 44],
                                   [67, 34, 17, 0, 66, 37, 46, 33]],
                                  [[31, 70, 11, 59, 70, 78, 66, 52],
                                   [6, 87, 58, 42, 68, 92, 52, 51],
                                   [71, 65, 6, 74, 95, 59, 100, 0]]]


def test_read_GameFile2():
    read_hgg = HGG.read_GameFile("filestest/pileface.hgg")
    assert read_hgg.players_actions == [[0, 1], [0, 1], [0, 1], [0, 1]]
    assert read_hgg.hypergraph == [[1, 2, 3], [0, 2], [0, 1]]
    assert read_hgg.utilities == [[[0, -1, -1, -2, 2, 1, 1, 0],
                                   [0, -1, 2, 1, -1, -2, 1, 0],
                                   [0, 2, -1, 1, -1, 1, -2, 0]],
                                  [[0, -1, 1, 0], [0, 1, -1, 0]],
                                  [[0, -1, 1, 0], [0, 1, -1, 0]]]


def test_read_GameFile3():
    read_hgg = HGG.read_GameFile("filestest/DDP_poly.hgg")
    assert read_hgg.players_actions == [[0, 1], [0, 1], [0, 1]]
    assert read_hgg.hypergraph == [[1, 2], [0, 1]]
    assert read_hgg.utilities == [[[-1, -5, 0, -3], [-1, 0, -5, -3]],
                                  [[-1, -4, 0, -3], [-1, 0, -4, -3]]]


def test_write_GameFile1(first_hgg):
    first_hgg.write_GameFile("filestest/first_hgg.hgg")
    read_game = HGG.read_GameFile("filestest/first_hgg.hgg")
    assert read_game.players_actions == first_hgg.players_actions
    assert read_game.hypergraph == first_hgg.hypergraph
    assert read_game.utilities == first_hgg.utilities


def test_write_GameFile2(second_hgg):
    second_hgg.write_GameFile("filestest/second_hgg.hgg")
    read_game = HGG.read_GameFile("filestest/second_hgg.hgg")
    assert read_game.players_actions == second_hgg.players_actions
    assert read_game.hypergraph == second_hgg.hypergraph
    assert read_game.utilities == second_hgg.utilities


def test_write_GameFile3(third_hgg):
    third_hgg.write_GameFile("filestest/third_hgg.hgg")
    read_game = HGG.read_GameFile("filestest/third_hgg.hgg")
    assert read_game.players_actions == third_hgg.players_actions
    assert read_game.hypergraph == third_hgg.hypergraph
    assert read_game.utilities == third_hgg.utilities


def test_write_GameFile4(degen_hgg):
    degen_hgg.write_GameFile("filestest/degen_hgg.hgg")
    read_game = HGG.read_GameFile("filestest/degen_hgg.hgg")
    assert read_game.players_actions == degen_hgg.players_actions
    assert read_game.hypergraph == degen_hgg.hypergraph
    assert read_game.utilities == degen_hgg.utilities
