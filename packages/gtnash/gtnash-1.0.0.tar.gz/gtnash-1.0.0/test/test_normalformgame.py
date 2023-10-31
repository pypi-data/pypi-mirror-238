import numpy as np
import pytest

from gtnash.game.normalformgame import NFG
from fractions import Fraction

"""
Separate  assert in multiple fucntion
"""


@pytest.fixture
def first_nfg():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[-3, -7, -7, -10, -1, -5, -5, -9],
                 [-3, -7, -1, -5, -7, -10, -5, -9],
                 [-3, -1, -7, -5, -7, -5, -10, -9]]
    return NFG(players_actions, utilities)


@pytest.fixture
def second_nfg():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [51, 29, 47, 43, 75, 61, 42, 19, 28, 39, 40, 21, 60, 60, 67, 44],
        [58, 72, 31, 41, 37, 5, 37, 41, 53, 68, 38, 30, 58, 72, 75, 0],
        [29, 73, 42, 13, 34, 31, 54, 25, 47, 29, 19, 46, 85, 79, 65, 24],
        [1, 17, 49, 9, 51, 25, 21, 49, 28, 77, 41, 69, 13, 100, 49, 27]]
    return NFG(players_actions, utilities)


@pytest.fixture
def third_nfg():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    # # util=[[79, 50, 98, 11, 17, 95, 46, 0],
    # [6, 5, 43, 38, 39, 65, 51, 19], [92, 86, 63, 100, 29, 48, 53, 68]]
    util = [[86, 100, 87, 90, 1, 5, 0, 94], [16, 71, 4, 3, 4, 59, 66, 86],
            [92, 0, 14, 65, 96, 45, 2, 51]]
    return NFG(players_actions, util)


@pytest.fixture
def bimat_nfg():
    players_actions = [[0, 1, 2], [0, 1]]
    util = [[3, 3, 2, 5, 0, 6], [3, 2, 2, 6, 3, 1]]
    return NFG(players_actions, util)


# joint_actions
def test_joint_actions1(first_nfg):
    assert (first_nfg.joint_actions == np.mat(
        [[0., 0., 0.], [0., 0., 1.], [0., 1., 0.], [0., 1., 1.], [1., 0., 0.],
         [1., 0., 1.], [1., 1., 0.], [1., 1., 1.]])).all()


def test_joint_actions2(second_nfg):
    assert (second_nfg.joint_actions == np.mat(
        [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0],
         [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1],
         [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0],
         [1, 1, 1, 1]])).all()


def test_joint_actions3(bimat_nfg):
    assert (bimat_nfg.joint_actions == np.mat(
        [[0., 0.], [0., 1.], [1., 0.], [1., 1.], [2., 0.], [2., 1.]])).all()


# all_response_of_player
def test_all_response_of_player1(first_nfg):
    assert (first_nfg.all_response_of_player(0, [0, 0, 0]) == np.mat(
        [[0., 0., 0.], [1., 0., 0.]])).all()


def test_all_response_of_player2(first_nfg):
    assert (first_nfg.all_response_of_player(1, [0, 0, 0]) == np.mat(
        [[0., 0., 0.], [0., 1., 0.]])).all()


def test_all_response_of_player3(first_nfg):
    assert (first_nfg.all_response_of_player(2, [0, 0, 0]) == np.mat(
        [[0., 0., 0.], [0., 0., 1.]])).all()


def test_all_response_of_player4(first_nfg):
    assert (first_nfg.all_response_of_player(0, [1, 1, 1]) == np.mat(
        [[0., 1., 1.], [1., 1., 1.]])).all()


def test_all_response_of_player5(first_nfg):
    assert (first_nfg.all_response_of_player(1, [1, 1, 1]) == np.mat(
        [[1., 0., 1.], [1., 1., 1.]])).all()


def test_all_response_of_player6(first_nfg):
    assert (first_nfg.all_response_of_player(2, [1, 1, 1]) == np.mat(
        [[1., 1., 0.], [1., 1., 1.]])).all()


def test_all_response_of_player7(first_nfg):
    assert (first_nfg.all_response_of_player(0, [1, 1, 1]) ==
            first_nfg.all_response_of_player(0, [0, 1, 1])).all()


def test_all_response_of_player8(first_nfg):
    assert (first_nfg.all_response_of_player(1, [1, 0, 0]) ==
            first_nfg.all_response_of_player(1, [1, 1, 0])).all()


def test_all_response_of_player9(first_nfg):
    assert (first_nfg.all_response_of_player(2, [0, 1, 1]) ==
            first_nfg.all_response_of_player(2, [0, 1, 0])).all()


def test_all_response_of_player10(second_nfg):
    assert (second_nfg.all_response_of_player(0, [0, 0, 0, 0]) == np.mat(
        [[0., 0., 0., 0.], [1., 0., 0., 0.]])).all()


def test_all_response_of_player11(second_nfg):
    assert (second_nfg.all_response_of_player(1, [1, 0, 0, 1]) == np.mat(
        [[1., 0., 0., 1.], [1., 1., 0., 1.]])).all()


def test_all_response_of_player12(second_nfg):
    assert (second_nfg.all_response_of_player(2, [1, 1, 1, 1]) == np.mat(
        [[1., 1., 0., 1.], [1., 1., 1., 1.]])).all()


def test_all_response_of_player13(bimat_nfg):
    assert (bimat_nfg.all_response_of_player(0, [0, 0]) == np.mat(
        [[0., 0.], [1., 0.], [2., 0.]])).all()


def test_all_response_of_player14(bimat_nfg):
    assert (bimat_nfg.all_response_of_player(1, [0, 1]) == np.mat(
        [[0., 0.], [0., 1.]])).all()


def test_all_response_of_player15(bimat_nfg):
    assert (bimat_nfg.all_response_of_player(1, [2, 0]) == np.mat(
        [[2., 0.], [2., 1.]])).all()


def test_all_response_of_player16(bimat_nfg):
    assert (bimat_nfg.all_response_of_player(0, [0, 0]) ==
            bimat_nfg.all_response_of_player(0, [2, 0])).all()


def test_all_response_of_player17(bimat_nfg):
    assert (bimat_nfg.all_response_of_player(0, [1, 0]) ==
            bimat_nfg.all_response_of_player(0, [2, 0])).all()


# joint_action_except_i

def test_joint_action_except_i1(first_nfg, second_nfg, bimat_nfg):
    for n in range(first_nfg.n_players):
        assert (first_nfg.joint_action_except_i(n) == np.mat(
            [[0., 0.], [0., 1.], [1., 0.], [1., 1.]])).all()


def test_joint_action_except_i2(second_nfg):
    for n in range(second_nfg.n_players):
        assert (second_nfg.joint_action_except_i(n) == np.mat(
            [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1],
             [1, 1, 0], [1, 1, 1]])).all()


def test_joint_action_except_i3(bimat_nfg):
    assert (bimat_nfg.joint_action_except_i(0) == np.mat([[0], [1]])).all()


def test_joint_action_except_i4(bimat_nfg):
    assert (bimat_nfg.joint_action_except_i(1) == np.mat(
        [[0], [1], [2]])).all()


# get_sub_jointact_of_n
# No second_nfg


def test_get_sub_jointact_of_n1(first_nfg):
    assert (first_nfg.get_sub_jointact_of_n(0) == [[0, 4], [1, 5], [2, 6],
                                                   [3, 7]])


def test_get_sub_jointact_of_n2(first_nfg):
    assert (first_nfg.get_sub_jointact_of_n(1) == [[0, 2], [1, 3], [4, 6],
                                                   [5, 7]])


def test_get_sub_jointact_of_n3(first_nfg):
    assert (first_nfg.get_sub_jointact_of_n(2) == [[0, 1], [2, 3], [4, 5],
                                                   [6, 7]])


def test_get_sub_jointact_of_n4(bimat_nfg):
    assert (bimat_nfg.get_sub_jointact_of_n(0) == [[0, 2, 4], [1, 3, 5]])


def test_get_sub_jointact_of_n5(bimat_nfg):
    assert (bimat_nfg.get_sub_jointact_of_n(1) == [[0, 1], [2, 3], [4, 5]])


# disutilities

def test_disutilities1(first_nfg):
    assert (first_nfg.disutilities == np.mat(
        [[3, 3, 3], [7, 7, 1], [7, 1, 7], [10, 5, 5], [1, 7, 7], [5, 10, 5],
         [5, 5, 10], [9, 9, 9]])).all()


def test_disutilities2(second_nfg):
    assert (second_nfg.disutilities == np.mat(
        [[25, 18, 57, 100], [47, 4, 13, 84], [29, 45, 44, 52],
         [33, 35, 73, 92], [1, 39, 52, 50], [15, 71, 55, 76], [34, 39, 32, 80],
         [57, 35, 61, 52], [48, 23, 39, 73], [37, 8, 57, 24], [36, 38, 67, 60],
         [55, 46, 40, 32], [16, 18, 1, 88], [16, 4, 7, 1], [9, 1, 21, 52],
         [32, 76, 62, 74]])).all()


def test_disutilities3(bimat_nfg):
    assert (bimat_nfg.disutilities == np.mat(
        [[4, 4], [4, 5], [5, 5], [2, 1], [7, 4], [1, 6]])).all()


# row_where_p_is_i
# No second_nfg

def test_row_where_p_is_i1(first_nfg, second_nfg, bimat_nfg):
    assert (first_nfg.row_where_p_is_i(0, 0) == np.mat([0, 1, 2, 3])).all()


def test_row_where_p_is_i2(first_nfg):
    assert (first_nfg.row_where_p_is_i(0, 1) == np.mat([4, 5, 6, 7])).all()


def test_row_where_p_is_i3(first_nfg):
    assert (first_nfg.row_where_p_is_i(1, 0) == np.mat([0, 1, 4, 5])).all()


def test_row_where_p_is_i4(first_nfg):
    assert (first_nfg.row_where_p_is_i(1, 1) == np.mat([2, 3, 6, 7])).all()


def test_row_where_p_is_i5(first_nfg):
    assert (first_nfg.row_where_p_is_i(2, 0) == np.mat([0, 2, 4, 6])).all()


def test_row_where_p_is_i6(first_nfg):
    assert (first_nfg.row_where_p_is_i(2, 1) == np.mat([1, 3, 5, 7])).all()


def test_row_where_p_is_i7(bimat_nfg):
    assert (bimat_nfg.row_where_p_is_i(0, 0) == np.mat([0, 1])).all()


def test_row_where_p_is_i8(bimat_nfg):
    assert (bimat_nfg.row_where_p_is_i(0, 1) == np.mat([2, 3])).all()


def test_row_where_p_is_i9(bimat_nfg):
    assert (bimat_nfg.row_where_p_is_i(0, 2) == np.mat([4, 5])).all()


def test_row_where_p_is_i10(bimat_nfg):
    assert (bimat_nfg.row_where_p_is_i(1, 0) == np.mat([0, 2, 4])).all()


def test_row_where_p_is_i11(bimat_nfg):
    assert (bimat_nfg.row_where_p_is_i(1, 1) == np.mat([1, 3, 5])).all()


# util_of_row
# no second_nfg
def test_util_of_row1(first_nfg):
    for n in range(first_nfg.n_players):
        assert (first_nfg.util_of_row(n, 0) == np.mat([-3, -7, -7, -10])).all()
        assert (first_nfg.util_of_row(n, 1) == np.mat([-1, -5, -5, -9])).all()


def test_util_of_row2(bimat_nfg):
    assert (bimat_nfg.util_of_row(0, 0) == np.mat([3, 3])).all()


def test_util_of_row3(bimat_nfg):
    assert (bimat_nfg.util_of_row(0, 1) == np.mat([2, 5])).all()


def test_util_of_row4(bimat_nfg):
    assert (bimat_nfg.util_of_row(0, 2) == np.mat([0, 6])).all()


def test_util_of_row5(bimat_nfg):
    assert (bimat_nfg.util_of_row(1, 0) == np.mat([3, 2, 3])).all()


def test_util_of_row6(bimat_nfg):
    assert (bimat_nfg.util_of_row(1, 1) == np.mat([2, 6, 1])).all()


# disutil_of_row
# no second_nfg

def test_disutil_of_row1(first_nfg):
    for n in range(first_nfg.n_players):
        assert (first_nfg.disutil_of_row(n, 0) == np.mat([3, 7, 7, 10])).all()
        assert (first_nfg.disutil_of_row(n, 1) == np.mat([1, 5, 5, 9])).all()


def test_disutil_of_row2(bimat_nfg):
    assert (bimat_nfg.disutil_of_row(0, 0) == np.mat([4, 4])).all()


def test_disutil_of_row3(bimat_nfg):
    assert (bimat_nfg.disutil_of_row(0, 1) == np.mat([5, 2])).all()


def test_disutil_of_row4(bimat_nfg):
    assert (bimat_nfg.disutil_of_row(0, 2) == np.mat([7, 1])).all()


def test_disutil_of_row5(bimat_nfg):
    assert (bimat_nfg.disutil_of_row(1, 0) == np.mat([4, 5, 4])).all()


def test_disutil_of_row6(bimat_nfg):
    assert (bimat_nfg.disutil_of_row(1, 1) == np.mat([5, 1, 6])).all()


# def test_disutil_of_joint_action(first_nfg,bimat_nfg)


# expected_utilities
# no second_nfg
def test_expected_utilities1(first_nfg):
    assert (first_nfg.expected_utilities(
        {0: [1, 0], 1: [1, 0], 2: [1, 0]}) == np.mat([-3, -3, -3])).all()


def test_expected_utilities2(first_nfg):
    assert (first_nfg.expected_utilities(
        {0: [1, 0], 1: [0, 1], 2: [1, 0]}) == np.mat([-7, -1, -7])).all()


def test_expected_utilities3(first_nfg):
    assert (first_nfg.expected_utilities(
        {0: [0, 1], 1: [0, 1], 2: [0, 1]}) == np.mat([-9, -9, -9])).all()


def test_expected_utilities4(first_nfg):
    assert (first_nfg.expected_utilities(
        {0: [1 / 2, 1 / 2], 1: [1 / 2, 1 / 2], 2: [1 / 2, 1 / 2]}) == np.mat(
        [-5.875, -5.875, -5.875])).all()


def test_expected_utilities5(bimat_nfg):
    assert (bimat_nfg.expected_utilities({0: [1, 0, 0], 1: [1, 0]}) == np.mat(
        [3, 3])).all()


def test_expected_utilities6(bimat_nfg):
    assert (bimat_nfg.expected_utilities({0: [0, 0, 1], 1: [0, 1]}) == np.mat(
        [6, 1])).all()


def test_expected_utilities7(bimat_nfg):
    assert (bimat_nfg.expected_utilities({0: [0, 1, 0], 1: [1, 0]}) == np.mat(
        [2, 2])).all()


def test_expected_utilities8(bimat_nfg):
    assert (bimat_nfg.expected_utilities(
        {0: [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)],
         1: [Fraction(1, 2), Fraction(1, 2)]}) == np.mat(
        [Fraction(19, 6), Fraction(17, 6)])).all()


# is_equilibrium
# No second/bimat
def test_is_equilibrium1(first_nfg):
    assert not (first_nfg.is_equilibrium(
        {0: [1 / 2, 1 / 2], 1: [1 / 2, 1 / 2], 2: [1 / 2, 1 / 2]}))


# def test_error_equilibrium1(first_nfg):
#     assert first_nfg.error_equilibrium({0:
#     [1/2, 1/2], 1: [1/2, 1/2], 2: [1/2, 1/2]})==0
#
# def test_error_equilibrium2(first_nfg):
#     assert first_nfg.error_equilibrium({0: [0, 1], 1: [0, 1], 2: [0, 1]})==0

def test_is_equilibrium2(first_nfg):
    assert (first_nfg.is_equilibrium({0: [0, 1], 1: [0, 1], 2: [0, 1]}))


def test_is_equilibrium3(first_nfg):
    assert not (first_nfg.is_equilibrium({0: [1, 0], 1: [1, 0], 2: [1, 0]}))


# def test_error_equilibrium1(first_nfg):
#     assert first_nfg.error_equilibrium({0: [1, 0], 1: [0, 1], 2: [1,0]})==0


def test_is_equilibrium4(first_nfg):
    assert not (first_nfg.is_equilibrium({0: [1, 0], 1: [0, 1], 2: [1, 0]}))


def test_is_pure_equilibrium1(first_nfg):
    assert (first_nfg.is_pure_equilibrium([1, 1, 1]))


def test_is_pure_equilibrium2(first_nfg):
    assert not (first_nfg.is_pure_equilibrium([0, 0, 0]))


def test_is_pure_equilibrium3(first_nfg):
    assert not (first_nfg.is_pure_equilibrium([0, 1, 0]))


def test_get_all_PNE1(first_nfg):
    assert (first_nfg.get_all_PNE() == [{0: [0, 1], 1: [0, 1], 2: [0, 1]}])


def test_get_all_PNE2(second_nfg):
    assert (second_nfg.get_all_PNE() == [])


def test_get_all_PNE3(bimat_nfg):
    assert (bimat_nfg.get_all_PNE() == [{0: [1, 0, 0], 1: [1, 0]}])


def test_pne_exist1(first_nfg, second_nfg, bimat_nfg):
    assert (first_nfg.pne_exist())


def test_pne_exist2(second_nfg):
    assert not (second_nfg.pne_exist())


def test_pne_exist3(bimat_nfg):
    assert (bimat_nfg.pne_exist())


# get_all_PNE

def test_first_pne1(first_nfg, second_nfg, bimat_nfg):
    assert (first_nfg.first_pne() == {0: [0, 1], 1: [0, 1], 2: [0, 1]})


def test_first_pne2(second_nfg):
    assert (second_nfg.first_pne() == {})


def test_first_pne3(bimat_nfg):
    assert (bimat_nfg.first_pne() == {0: [1, 0, 0], 1: [1, 0]})


# def test_build_subgame(first_nfg,second_nfg,bimat_nfg):
#     tmp_firstnfg=NFG([[0,1],[0,1]],[[-3, -7, -1, -5], [-3, -1, -7, -5,]])
#     sub_first_nfg1=first_nfg.build_subgame({2:[1,0]})
#     assert(sub_first_nfg1.players_actions==tmp_firstnfg.players_actions)
#     assert (sub_first_nfg1.utilities == tmp_firstnfg.utilities)


# build_subgame
# no second_nfg

def test_build_subgame1(first_nfg, second_nfg, bimat_nfg):
    sub_first1 = first_nfg.build_subgame({2: [0, 1]})
    assert (sub_first1.players_actions == [[0, 1], [0, 1], [-1]] and
            sub_first1.utilities == [[-7, -10, -5, -9], [-7, -5, -10, -9],
                                     [-1, -5, -5, -9]])


def test_build_subgame2(first_nfg):
    sub_first2 = first_nfg.build_subgame({0: [1, 0], 1: [0, 1]})
    assert (sub_first2.players_actions == [[-1], [-1], [0, 1]] and
            sub_first2.utilities == [[-7, -10], [-1, -5], [-7, -5]])


def test_build_subgame3(first_nfg):
    sub_first_mixed = first_nfg.build_subgame({2: [1 / 2, 1 / 2]})
    assert (sub_first_mixed.players_actions == [[0, 1], [0, 1], [-1]] and
            sub_first_mixed.utilities == [[-5, -8.5, -3, -7],
                                          [-5, -3, -8.5, -7],
                                          [-2, -6, -6, -9.5]])


def test_build_subgame4(bimat_nfg):
    sub_bimat1 = bimat_nfg.build_subgame({1: [1, 0]})
    assert (sub_bimat1.players_actions == [[0, 1, 2], [-1]] and
            sub_bimat1.utilities == [[3, 2, 0], [3, 2, 3]])


def test_build_subgame5(bimat_nfg):
    sub_bimat2 = bimat_nfg.build_subgame({0: [1, 0, 0]})
    assert (sub_bimat2.players_actions == [[-1], [0, 1]] and
            sub_bimat2.utilities == [[3, 3], [3, 2]])


# get_subgame_level
# no second_nfg


def test_get_subgame_level1(first_nfg):
    sub_level_first_nfg1 = first_nfg.get_subgame_level(
        {0: [0, 1], 1: [0, 1], 2: [0, 1]})
    assert (sub_level_first_nfg1.players_actions == [[0, 1], [0, 1]] and
            sub_level_first_nfg1.utilities == [[-7, -10, -5, -9],
                                               [-7, -5, -10, -9]])


def test_get_subgame_level2(first_nfg):
    sub_level_first_mixed = first_nfg.get_subgame_level(
        {0: [0, 1], 1: [1, 0], 2: [1 / 2, 1 / 2]})
    assert (sub_level_first_mixed.players_actions == [[0, 1], [0, 1]] and
            sub_level_first_mixed.utilities == [[-5, -8.5, -3, -7],
                                                [-5, -3, -8.5, -7]])


def test_get_subgame_level3(bimat_nfg):
    sub_level_bimat1 = bimat_nfg.get_subgame_level({0: [0, 1, 0], 1: [1, 0]})
    assert (sub_level_bimat1.players_actions == [[0, 1, 2]] and
            sub_level_bimat1.utilities == [[3, 2, 0]])


# get_subgame_without_n
# no second_nfg, bimat

def test_get_subgame_without_n1(first_nfg):
    sub_level_first_nfg1 = first_nfg.get_subgame_without_n(
        {0: [0, 1], 1: [0, 1], 2: [0, 1]}, 2)
    assert (sub_level_first_nfg1.players_actions == [[0, 1], [0, 1]] and
            sub_level_first_nfg1.utilities == [[-7, -10, -5, -9],
                                               [-7, -5, -10, -9]])


def test_get_subgame_without_n2(first_nfg):
    sub_level_first_nfg2 = first_nfg.get_subgame_without_n(
        {0: [1, 0], 1: [0, 1], 2: [0, 1]}, 0)
    assert (sub_level_first_nfg2.players_actions == [[0, 1], [0, 1]] and
            sub_level_first_nfg2.utilities == [[-3, -7, -1, -5],
                                               [-3, -1, -7, -5]])


"""
[[3,3,2,5,0,6],[3,2,2,6,3,1]]
utilities = [[-3, -7, -7, -10, -1, -5, -5, -9],
 [-3, -7, -1, -5, -7, -10, -5, -9],[-3, -1, -7, -5, -7, -5, -10, -9]]
    util=[[3,3,2,5,0,6],[3,2,2,6,3,1]]
build_subgame(self,partial_mixed_strategy):
    Builds a subgame of the NFG by fixing mixed strategies of some players.
get_subgame_level(proba)
    Given the current game and a probability distribution over the action,
     return the subgame without the last player
get_subgame_without_n(proba,player_ind)
    Given the current game and a probability distribution over the action,
     return the subgame without the last player
get_subgame_fixed_strat(played_strat)
    For a given strategy create the subgame where only the action with a
     positive value are played
readNFGpayoff
"""


# get_subgame_fixed_strat
# no second_nfg

def test_get_subgame_fixed_strat1(first_nfg):
    sub_first_nfg1 = first_nfg.get_subgame_fixed_strat(
        {0: [1, 1], 1: [1, 1], 2: [1, 0]})
    assert (sub_first_nfg1.players_actions == [[0, 1], [0, 1], [
        0]] and sub_first_nfg1.utilities == [[-3, -7, -1, -5],
                                             [-3, -1, -7, -5],
                                             [-3, -7, -7, -10]])


def test_get_subgame_fixed_strat2(first_nfg):
    sub_first_nfg2 = first_nfg.get_subgame_fixed_strat(
        {0: [0, 1], 1: [0, 1], 2: [0, 1]})
    assert (sub_first_nfg2.players_actions == [[1], [1], [
        1]] and sub_first_nfg2.utilities == [[-9], [-9], [-9]])


def test_get_subgame_fixed_strat3(bimat_nfg):
    sub_bimat_nfg1 = bimat_nfg.get_subgame_fixed_strat(
        {0: [1, 1, 0], 1: [1, 1]})
    assert (
            sub_bimat_nfg1.players_actions ==
            [[0, 1], [0, 1]] and sub_bimat_nfg1.utilities ==
            [[3, 3, 2, 5], [3, 2, 2, 6]])


def test_get_subgame_fixed_strat4(bimat_nfg):
    sub_bimat_nfg2 = bimat_nfg.get_subgame_fixed_strat(
        {0: [0, 1, 1], 1: [1, 0]})
    assert (sub_bimat_nfg2.players_actions == [[1, 2], [
        0]] and sub_bimat_nfg2.utilities == [[2, 0], [2, 3]])


def test_readNFGpayoff1():
    read_game = NFG.readNFGpayoff("filestest/e02.nfg")
    assert read_game.players_actions == [[0, 1], [0, 1, 2]]
    assert read_game.utilities == [[1, 2, 2, 1, 3, 0], [1, 0, 0, 1, 0, 2]]


def test_readNFGpayoff2():
    read_game = NFG.readNFGpayoff("filestest/RandG_0.nfg")
    assert read_game.players_actions == [[0, 1], [0, 1], [0, 1]]
    assert read_game.utilities == [[43, 38, 1, 63, 61, 21, 12, 46],
                                   [89, 35, 0, 88, 87, 68, 24, 22],
                                   [72, 92, 61, 71, 95, 2, 4, 100]]


def test_readNFGpayoff3():
    read_game = NFG.readNFGpayoff("filestest/custom_game1.nfg")
    assert read_game.players_actions == [[0, 1, 2], [0, 1, 2], [0, 1]]
    assert read_game.utilities == [
        [91, 49, 69, 98, 95, 15, 70, 59, 68, 52, 45, 22, 14, 37, 54, 58, 41,
         92],
        [71, 89, 23, 47, 26, 17, 94, 99, 49, 55, 22, 72, 70, 85, 85, 82, 38,
         62],
        [54, 39, 53, 50, 66, 55, 8, 59, 49, 40, 67, 19, 7, 39, 14, 62, 80, 76]]


def test_readNFGpayoff4():
    read_game = NFG.readNFGpayoff("filestest/custom_game2.nfg")
    assert read_game.players_actions == [[0, 1], [0, 1]]
    assert read_game.utilities == [[-69, -67, -100, -14], [-64, -86, -65, -75]]


def test_writeNFGpayoff1(first_nfg):
    first_nfg.writeNFGpayoff("filestest/first_nfg.nfg")
    read_game = NFG.readNFGpayoff("filestest/first_nfg.nfg")
    assert read_game.players_actions == first_nfg.players_actions
    assert read_game.utilities == first_nfg.utilities


def test_writeNFGpayoff2(second_nfg):
    second_nfg.writeNFGpayoff("filestest/second_nfg.nfg")
    read_game = NFG.readNFGpayoff("filestest/second_nfg.nfg")
    assert read_game.players_actions == second_nfg.players_actions
    assert read_game.utilities == second_nfg.utilities


def test_writeNFGpayoff3(third_nfg):
    third_nfg.writeNFGpayoff("filestest/third_nfg.nfg")
    read_game = NFG.readNFGpayoff("filestest/third_nfg.nfg")
    assert read_game.players_actions == third_nfg.players_actions
    assert read_game.utilities == third_nfg.utilities


def test_writeNFGpayoff4(bimat_nfg):
    bimat_nfg.writeNFGpayoff("filestest/bimat_nfg.nfg")
    read_game = NFG.readNFGpayoff("filestest/bimat_nfg.nfg")
    assert read_game.players_actions == bimat_nfg.players_actions
    assert read_game.utilities == bimat_nfg.utilities
