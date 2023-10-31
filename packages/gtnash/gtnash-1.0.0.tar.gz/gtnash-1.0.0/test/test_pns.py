# import numpy as np
import pytest
from gtnash.game.normalformgame import NFG
from gtnash.game.hypergraphicalgame import HGG
from fractions import Fraction
from gtnash.util.irda import irda
from gtnash.solver.pns import PNS_solver,\
    unbalance_partitions, allbalancedsupports

"""
PNS_solver
    launch_pns()
    normalized_strategy(solution_dic)
    create_W_from_support_strat(support_strat)
    create_Wb_from_support_strat(support_strat)
    support_to_strategy(support)


balancedpartitions
unbalance_partitions
allbalancedpartitions
supports
allbalancedsupports
"""


def test_unbalance_partitions1():
    # total= nb total action
    # n= nb players
    # m nb of played actions
    assert unbalance_partitions(3, 3, 0) == [[1, 1, 1]]


def test_unbalance_partitions2():
    assert unbalance_partitions(3, 4, 0) == []


def test_unbalance_partitions3():
    assert unbalance_partitions(3, 4, 1) == [[2, 1, 1], [1, 2, 1], [1, 1, 2]]


def test_unbalance_partitions4():
    assert unbalance_partitions(3, 5, 0) == []


def test_unbalance_partitions5():
    assert unbalance_partitions(3, 5, 1) == [[2, 2, 1], [2, 1, 2], [1, 2, 2]]


def test_unbalance_partitions6():
    assert unbalance_partitions(3, 5, 2) == [[3, 1, 1], [1, 3, 1], [1, 1, 3]]


# Optimization: add list action per players to skip
# redundant/impossible unbalance_partitions
# def test_allbalancedpartitions1():
#     assert allbalancedpartitions(3,6) ==
#     [[1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2],
#                                          [2, 2, 1], [2, 1, 2], [1, 2, 2],
#                                          [3, 1, 1], [1, 3, 1], [1, 1, 3],
#                                          [2, 2, 2], [3, 2, 1], [3, 1, 2],
#                                          [2, 3, 1], [2, 1, 3], [1, 3, 2],
#                                          [1, 2, 3], [4, 1, 1], [1, 4, 1],
#                                          [1, 1, 4]]


# def test_allbalancedsupports():
#     for i in allbalancedsupports([[0, 1, 2], [0, 1], [0, 1, 2]]):
#         print(i)

def test_allbalancedsupports1():
    all_support = [({0}, {0}, {0}), ({0}, {0}, {1}), ({0}, {1}, {0}),
                   ({0}, {1}, {1}), ({1}, {0}, {0}), ({1}, {0}, {1}),
                   ({1}, {1}, {0}), ({1}, {1}, {1}), ({0, 1}, {0}, {0}),
                   ({0, 1}, {0}, {1}), ({0, 1}, {1}, {0}), ({0, 1}, {1}, {1}),
                   ({0}, {0, 1}, {0}), ({0}, {0, 1}, {1}), ({1}, {0, 1}, {0}),
                   ({1}, {0, 1}, {1}), ({0}, {0}, {0, 1}), ({0}, {1}, {0, 1}),
                   ({1}, {0}, {0, 1}), ({1}, {1}, {0, 1}),
                   ({0, 1}, {0, 1}, {0}),
                   ({0, 1}, {0, 1}, {1}), ({0, 1}, {0}, {0, 1}),
                   ({0, 1}, {1}, {0, 1}),
                   ({0}, {0, 1}, {0, 1}), ({1}, {0, 1}, {0, 1}),
                   ({0, 1}, {0, 1}, {0, 1})]
    for s_i, s in enumerate(allbalancedsupports([[0, 1], [0, 1], [0, 1]])):
        assert s == all_support[s_i]


def test_allbalancedsupports2():
    all_support = [({0}, {0}, {0}), ({0}, {0}, {1}), ({0}, {0}, {2}),
                   ({0}, {1}, {0}),
                   ({0}, {1}, {1}), ({0}, {1}, {2}), ({1}, {0}, {0}),
                   ({1}, {0}, {1}),
                   ({1}, {0}, {2}), ({1}, {1}, {0}), ({1}, {1}, {1}),
                   ({1}, {1}, {2}),
                   ({2}, {0}, {0}), ({2}, {0}, {1}), ({2}, {0}, {2}),
                   ({2}, {1}, {0}),
                   ({2}, {1}, {1}), ({2}, {1}, {2}), ({0, 1}, {0}, {0}),
                   ({0, 1}, {0}, {1}),
                   ({0, 1}, {0}, {2}), ({0, 1}, {1}, {0}), ({0, 1}, {1}, {1}),
                   ({0, 1}, {1}, {2}),
                   ({0, 2}, {0}, {0}), ({0, 2}, {0}, {1}), ({0, 2}, {0}, {2}),
                   ({0, 2}, {1}, {0}),
                   ({0, 2}, {1}, {1}), ({0, 2}, {1}, {2}), ({1, 2}, {0}, {0}),
                   ({1, 2}, {0}, {1}),
                   ({1, 2}, {0}, {2}), ({1, 2}, {1}, {0}), ({1, 2}, {1}, {1}),
                   ({1, 2}, {1}, {2}),
                   ({0}, {0, 1}, {0}), ({0}, {0, 1}, {1}), ({0}, {0, 1}, {2}),
                   ({1}, {0, 1}, {0}),
                   ({1}, {0, 1}, {1}), ({1}, {0, 1}, {2}), ({2}, {0, 1}, {0}),
                   ({2}, {0, 1}, {1}),
                   ({2}, {0, 1}, {2}), ({0}, {0}, {0, 1}), ({0}, {0}, {0, 2}),
                   ({0}, {0}, {1, 2}),
                   ({0}, {1}, {0, 1}), ({0}, {1}, {0, 2}), ({0}, {1}, {1, 2}),
                   ({1}, {0}, {0, 1}),
                   ({1}, {0}, {0, 2}), ({1}, {0}, {1, 2}), ({1}, {1}, {0, 1}),
                   ({1}, {1}, {0, 2}),
                   ({1}, {1}, {1, 2}), ({2}, {0}, {0, 1}), ({2}, {0}, {0, 2}),
                   ({2}, {0}, {1, 2}),
                   ({2}, {1}, {0, 1}), ({2}, {1}, {0, 2}), ({2}, {1}, {1, 2}),
                   ({0, 1}, {0, 1}, {0}),
                   ({0, 1}, {0, 1}, {1}), ({0, 1}, {0, 1}, {2}),
                   ({0, 2}, {0, 1}, {0}), ({0, 2}, {0, 1}, {1}),
                   ({0, 2}, {0, 1}, {2}), ({1, 2}, {0, 1}, {0}),
                   ({1, 2}, {0, 1}, {1}), ({1, 2}, {0, 1}, {2}),
                   ({0, 1}, {0}, {0, 1}), ({0, 1}, {0}, {0, 2}),
                   ({0, 1}, {0}, {1, 2}), ({0, 1}, {1}, {0, 1}),
                   ({0, 1}, {1}, {0, 2}), ({0, 1}, {1}, {1, 2}),
                   ({0, 2}, {0}, {0, 1}), ({0, 2}, {0}, {0, 2}),
                   ({0, 2}, {0}, {1, 2}), ({0, 2}, {1}, {0, 1}),
                   ({0, 2}, {1}, {0, 2}), ({0, 2}, {1}, {1, 2}),
                   ({1, 2}, {0}, {0, 1}), ({1, 2}, {0}, {0, 2}),
                   ({1, 2}, {0}, {1, 2}), ({1, 2}, {1}, {0, 1}),
                   ({1, 2}, {1}, {0, 2}), ({1, 2}, {1}, {1, 2}),
                   ({0}, {0, 1}, {0, 1}), ({0}, {0, 1}, {0, 2}),
                   ({0}, {0, 1}, {1, 2}), ({1}, {0, 1}, {0, 1}),
                   ({1}, {0, 1}, {0, 2}), ({1}, {0, 1}, {1, 2}),
                   ({2}, {0, 1}, {0, 1}), ({2}, {0, 1}, {0, 2}),
                   ({2}, {0, 1}, {1, 2}), ({0, 1, 2}, {0}, {0}),
                   ({0, 1, 2}, {0}, {1}), ({0, 1, 2}, {0}, {2}),
                   ({0, 1, 2}, {1}, {0}), ({0, 1, 2}, {1}, {1}),
                   ({0, 1, 2}, {1}, {2}), ({0}, {0}, {0, 1, 2}),
                   ({0}, {1}, {0, 1, 2}), ({1}, {0}, {0, 1, 2}),
                   ({1}, {1}, {0, 1, 2}), ({2}, {0}, {0, 1, 2}),
                   ({2}, {1}, {0, 1, 2}), ({0, 1}, {0, 1}, {0, 1}),
                   ({0, 1}, {0, 1}, {0, 2}), ({0, 1}, {0, 1}, {1, 2}),
                   ({0, 2}, {0, 1}, {0, 1}),
                   ({0, 2}, {0, 1}, {0, 2}),
                   ({0, 2}, {0, 1}, {1, 2}), ({1, 2}, {0, 1}, {0, 1}),
                   ({1, 2}, {0, 1}, {0, 2}),
                   ({1, 2}, {0, 1}, {1, 2}),
                   ({0, 1, 2}, {0, 1}, {0}), ({0, 1, 2}, {0, 1}, {1}),
                   ({0, 1, 2}, {0, 1}, {2}),
                   ({0, 1, 2}, {0}, {0, 1}),
                   ({0, 1, 2}, {0}, {0, 2}), ({0, 1, 2}, {0}, {1, 2}),
                   ({0, 1, 2}, {1}, {0, 1}),
                   ({0, 1, 2}, {1}, {0, 2}),
                   ({0, 1, 2}, {1}, {1, 2}), ({0, 1}, {0}, {0, 1, 2}),
                   ({0, 1}, {1}, {0, 1, 2}),
                   ({0, 2}, {0}, {0, 1, 2}),
                   ({0, 2}, {1}, {0, 1, 2}), ({1, 2}, {0}, {0, 1, 2}),
                   ({1, 2}, {1}, {0, 1, 2}),
                   ({0}, {0, 1}, {0, 1, 2}),
                   ({1}, {0, 1}, {0, 1, 2}), ({2}, {0, 1}, {0, 1, 2}),
                   ({0, 1, 2}, {0, 1}, {0, 1}),
                   ({0, 1, 2}, {0, 1}, {0, 2}),
                   ({0, 1, 2}, {0, 1}, {1, 2}), ({0, 1}, {0, 1}, {0, 1, 2}),
                   ({0, 2}, {0, 1}, {0, 1, 2}),
                   ({1, 2}, {0, 1}, {0, 1, 2}),
                   ({0, 1, 2}, {0}, {0, 1, 2}), ({0, 1, 2}, {1}, {0, 1, 2}),
                   ({0, 1, 2}, {0, 1}, {0, 1, 2})]
    for s_i, s in enumerate(
            allbalancedsupports([[0, 1, 2], [0, 1], [0, 1, 2]])):
        assert s == all_support[s_i]


def test_allbalancedsupports3():
    all_support = [({1}, {0}, {0}), ({1}, {0}, {1}), ({1}, {0}, {2}),
                   ({1}, {0}, {0, 1}), ({1}, {0}, {0, 2}), ({1}, {0}, {1, 2}),
                   ({1}, {0}, {0, 1, 2})]
    for s_i, s in enumerate(allbalancedsupports([[1], [0], [0, 1, 2]])):
        assert s == all_support[s_i]


# @pytest.fixture
# def nfg1():
#     return 0


@pytest.fixture
def pns_4player_nfg():
    utilities = [
        [50, 59, 27, 4, 72, 69, 18, 35, 6, 89, 78, 19, 36, 76, 64, 20],
        [97, 5, 90, 60, 6, 13, 56, 82, 89, 79, 52, 34, 35, 100, 60, 34],
        [15, 30, 53, 12, 79, 77, 15, 38, 100, 82, 35, 10, 24, 0, 29, 27],
        [28, 66, 83, 1, 54, 89, 71, 35, 46, 62, 96, 26, 20, 58, 16, 81]]

    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    tmp_nfg = NFG(players_actions, utilities)
    return PNS_solver(tmp_nfg)


@pytest.fixture
def empty_pns():
    return PNS_solver(HGG([], [], []), {0: 0})


@pytest.fixture
def pns_3player_nfg():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[6, 7, 0, 5, 1, 4, 2, 3], [0, 3, 7, 4, 6, 5, 1, 2],
                 [4, 7, 4, 0, 3, 2, 6, 1]]
    current_nfg = NFG(players_actions, utilities)
    return PNS_solver(current_nfg)


@pytest.fixture
def pns_4p_nfg_degen():
    utilities = [
        [50, 59, 27, 4, 72, 69, 18, 35, 6, 89, 78, 19, 36, 76, 64, 20],
        [97, 5, 90, 60, 6, 13, 56, 82, 89, 79, 52, 34, 35, 100, 60, 34],
        [15, 30, 53, 12, 79, 77, 15, 38, 100, 82, 35, 10, 24, 0, 29, 27],
        [28, 66, 83, 1, 54, 89, 71, 35, 46, 62, 96, 26, 20, 58, 16, 81]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    current_nfg = NFG(players_actions, utilities)
    return PNS_solver(current_nfg)


@pytest.fixture
def pns_hgg1():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
         [-3, -1, -7, -5, -7, -5, -10, -9]],
        [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3], [-1, 0, -5, -3]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PNS_solver(hgg)


@pytest.fixture
def pns_hgg2():
    utilities = [
        [[-3, -1, -3, -2, -2, -3, -2, -1], [-1, -3, -5, -1, -1, -6, -3, -4],
         [-2, -3, -6, -4, -3, -1, -3, -4]],
        [[-1, -3, -2, -2], [-1, -2, -2, -1]],
        [[-3, -1, -4, -5], [-1, -3, -1, -5]]]
    # Error up level impossible, 2->3, [[0,1],[0,1],[0,1],[0,1]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PNS_solver(hgg)


@pytest.fixture
def pns_hgg3():
    utilities = [
        [[74, 6, 9, 60, 77, 30, 47, 0], [51, 97, 98, 83, 90, 1, 2, 47],
         [18, 16, 29, 86, 100, 96, 93, 64]],
        [[84, 48, 27, 5, 100, 62, 16, 62], [10, 88, 72, 47, 13, 24, 42, 72],
         [1, 36, 68, 0, 53, 5, 61, 97]]]
    hypergraph = [[0, 1, 3], [0, 2, 3]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PNS_solver(hgg)


@pytest.fixture
def pns_hgg_irda1():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[87, 77, 0, 49, 63, 99, 98, 25], [76, 100, 10, 43, 73, 65, 8, 56],
         [8, 36, 3, 100, 24, 3, 64, 28]],
        [[67, 38, 60, 64, 55, 100, 16, 13], [23, 59, 0, 9, 1, 8, 47, 33],
         [9, 7, 100, 39, 16, 18, 16, 62]]]
    hypergraph = [[0, 1, 2], [1, 2, 3]]
    hgg = HGG(players_actions, utilities, hypergraph)
    red_hgg, z_excluded = irda(hgg)
    return PNS_solver(red_hgg)


@pytest.fixture
def pns_hgg_irda2():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[29, 39, 100, 46, 40, 18, 97, 37], [23, 81, 64, 62, 90, 73, 76, 53],
         [26, 36, 51, 5, 14, 99, 0, 54]],
        [[12, 37, 7, 7, 41, 59, 27, 86], [65, 100, 100, 49, 97, 31, 68, 58],
         [29, 70, 44, 61, 0, 53, 92, 74]]]
    hypergraph = [[0, 2, 3], [1, 2, 3]]
    hgg = HGG(players_actions, utilities, hypergraph)
    red_hgg, z_excluded = irda(hgg)
    return PNS_solver(red_hgg)


def test_final_support_size1(pns_4player_nfg):
    assert pns_4player_nfg.final_support_size == 8


def test_final_support_size2(pns_3player_nfg):
    assert pns_3player_nfg.final_support_size == 6


def test_final_support_size3(pns_4p_nfg_degen):
    assert pns_4p_nfg_degen.final_support_size == 8


def test_final_support_size4(pns_hgg1):
    assert pns_hgg1.final_support_size == 8


def test_final_support_size5(pns_hgg2):
    assert pns_hgg2.final_support_size == 8


def test_final_support_size6(pns_hgg3):
    assert pns_hgg3.final_support_size == 8


def test_final_support_size7(pns_hgg_irda1):
    assert pns_hgg_irda1.final_support_size == 6


def test_final_support_size8(pns_hgg_irda2):
    assert pns_hgg_irda2.final_support_size == 7


def test_support_to_strategy1(pns_4player_nfg):
    assert pns_4player_nfg.support_to_strategy(({0}, {0}, {0}, {0})) == {
        0: [1, 0], 1: [1, 0], 2: [1, 0], 3: [1, 0]}


def test_support_to_strategy2(pns_4player_nfg):
    assert pns_4player_nfg.support_to_strategy(
        ({0, 1}, {0, 1}, {0, 1}, {0, 1})) == {0: [1, 1], 1: [1, 1], 2: [1, 1],
                                              3: [1, 1]}


def test_support_to_strategy3(pns_4player_nfg):
    assert pns_4player_nfg.support_to_strategy(({0, 1}, {1}, {0}, {1})) == {
        0: [1, 1], 1: [0, 1], 2: [1, 0], 3: [0, 1]}


def test_support_to_strategy4(pns_hgg_irda1):
    assert pns_hgg_irda1.support_to_strategy(({0, 1}, {0}, {1}, {0})) == {
        0: [1, 1], 1: [1], 2: [0, 1], 3: [1]}


def test_support_to_strategy5(pns_hgg_irda2):
    assert pns_hgg_irda2.support_to_strategy(({0, 1}, {1}, {0}, {1})) == {
        0: [1, 1], 1: [1], 2: [1, 0], 3: [0, 1]}


def test_create_W_from_support_strat1(pns_4player_nfg):
    stratsupport = pns_4player_nfg.support_to_strategy(({0}, {0}, {0}, {0}))
    assert set(
        pns_4player_nfg.create_W_from_support_strat(stratsupport)) == set(
        [(0, 0), (1, 0), (2, 0), (3, 0)])


def test_create_W_from_support_strat2(pns_4player_nfg):
    stratsupport = pns_4player_nfg.support_to_strategy(
        ({0, 1}, {0, 1}, {0, 1}, {0, 1}))
    assert set(
        pns_4player_nfg.create_W_from_support_strat(stratsupport)) == {(0, 0),
                                                                       (1, 0),
                                                                       (2, 0),
                                                                       (3, 0),
                                                                       (0, 1),
                                                                       (1, 1),
                                                                       (2, 1),
                                                                       (3, 1)}


def test_create_W_from_support_strat3(pns_hgg_irda1):
    stratsupport = pns_hgg_irda1.support_to_strategy(({0}, {0}, {0}, {0}))
    assert set(pns_hgg_irda1.create_W_from_support_strat(stratsupport)) == {
        (0, 0), (1, 0), (2, 0), (3, 0)}


def test_create_Wb_from_support_strat1(pns_4player_nfg):
    stratsupport = pns_4player_nfg.support_to_strategy(({0}, {0}, {0}, {0}))
    assert set(
        pns_4player_nfg.create_Wb_from_support_strat(stratsupport)) == {(0, 1),
                                                                        (1, 1),
                                                                        (2, 1),
                                                                        (3, 1)}


def test_create_Wb_from_support_strat2(pns_4player_nfg):
    stratsupport = pns_4player_nfg.support_to_strategy(
        ({0, 1}, {0, 1}, {0, 1}, {0, 1}))
    assert set(
        pns_4player_nfg.create_Wb_from_support_strat(stratsupport)) == set([])


def test_create_Wb_from_support_strat3(pns_hgg_irda1):
    stratsupport = pns_hgg_irda1.support_to_strategy(({0}, {0}, {0}, {0}))
    assert set(
        pns_hgg_irda1.create_Wb_from_support_strat(stratsupport)) == {(0, 1),
                                                                      (2, 1)}


def test_launch_pns1(pns_4player_nfg):
    sol = pns_4player_nfg.launch_pns()
    # for x in sol.keys():
    #     for v_i, v in enumerate(sol[x]):
    #         print(v.radical_expression())
    check_sol = {0: [Fraction(65, 103), Fraction(38, 103)], 1: [1, 0],
                 2: [Fraction(51, 95), Fraction(44, 95)], 3: [1, 0]}
    for p in sol.keys():
        for v_i, v in enumerate(sol[p]):
            assert float(v) - check_sol[p][v_i] < 0.00001 and float(v) - \
                   check_sol[p][v_i] > -0.000001


def test_launch_pns2(pns_hgg1):
    assert pns_hgg1.launch_pns() == {0: [0, 1], 1: [0, 1], 2: [0, 1],
                                     3: [0, 1]}


def test_launch_pns3(pns_hgg2):
    sol = pns_hgg2.launch_pns()
    check_sol = {0: [Fraction(1, 3), Fraction(2, 3)], 1: [1, 0],
                 2: [Fraction(2, 3), Fraction(1, 3)], 3: [1, 0]}
    for p in sol.keys():
        for v_i, v in enumerate(sol[p]):
            assert float(v) - check_sol[p][v_i] < 0.00001 and float(v) - \
                   check_sol[p][v_i] > -0.000001


def test_launch_pns4(pns_hgg3):
    sol = pns_hgg3.launch_pns()
    check_sol = {0: [Fraction(23, 30), Fraction(7, 30)],
                 1: [Fraction(23, 42), Fraction(19, 42)], 2: [1, 0],
                 3: [0, 1]}
    for p in sol.keys():
        for v_i, v in enumerate(sol[p]):
            assert float(v) - check_sol[p][v_i] < 0.00001 and float(v) - \
                   check_sol[p][v_i] > -0.000001


def test_launch_pns5(pns_hgg_irda1):
    sol = pns_hgg_irda1.launch_pns()
    check_sol = {0: [Fraction(44, 49), Fraction(5, 49)], 1: [1],
                 2: [Fraction(11, 23), Fraction(12, 23)], 3: [1]}
    for p in sol.keys():
        for v_i, v in enumerate(sol[p]):
            assert float(v) - check_sol[p][v_i] < 0.00001 and float(v) - \
                   check_sol[p][v_i] > -0.000001


def test_launch_pns6(pns_hgg_irda2):
    assert pns_hgg_irda2.launch_pns() == {0: [1, 0], 1: [1], 2: [0, 1],
                                          3: [1, 0]}
