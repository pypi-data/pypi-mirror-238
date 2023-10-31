# import numpy as np
import pytest
# from fractions import Fraction
from sage.all import QQ

from gtnash.solver.wilsonalgorithm import Node, irda_on_game, first_node
from gtnash.util.polynomial_complementary_problem import \
    PolynomialComplementaryProblem, Subsystem
from gtnash.game.normalformgame import NFG
from gtnash.game.hypergraphicalgame import HGG


@pytest.fixture
def nfg_3player():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[6, 7, 0, 5, 1, 4, 2, 3], [0, 3, 7, 4, 6, 5, 1, 2],
                 [4, 7, 4, 0, 3, 2, 6, 1]]
    return NFG(players_actions, utilities)
    # return PolynomialComplementaryProblem(current_nfg)


@pytest.fixture
def nfg_4degen():
    utilities = [
        [50, 59, 27, 4, 72, 69, 18, 35, 6, 89, 78, 19, 36, 76, 64, 20],
        [97, 5, 90, 60, 6, 13, 56, 82, 89, 79, 52, 34, 35, 100, 60, 34],
        [15, 30, 53, 12, 79, 77, 15, 38, 100, 82, 35, 10, 24, 0, 29, 27],
        [28, 66, 83, 1, 54, 89, 71, 35, 46, 62, 96, 26, 20, 58, 16, 81]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    return NFG(players_actions, utilities)


@pytest.fixture
def nfg_3descent():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[19, 58, 64, 66, 87, 52, 59, 79],
                 [73, 23, 80, 0, 100, 89, 43, 69],
                 [77, 60, 29, 35, 52, 98, 19, 70]]
    return NFG(players_actions, utilities)


@pytest.fixture
def hgg1():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
         [-3, -1, -7, -5, -7, -5, -10, -9]],
        [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3], [-1, 0, -5, -3]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    return HGG(players_actions, utilities, hypergraph)


def pcp_of_game(game):
    return PolynomialComplementaryProblem(game)


def x_pairval_of_pcp(pcp):
    xpairs_val = {}
    for (n, i) in pcp.couple_to_x.keys():
        if pcp.omega0[n] == i:
            xpairs_val[(n, i)] = 1
        else:
            xpairs_val[(n, i)] = 0
    return xpairs_val


# Faire un test_irda.py a part pour plus de test la dessus

def test_irda_on_game1(nfg_3player):
    red_game, red_var = irda_on_game(nfg_3player)
    assert (red_game.utilities, red_var) == ([nfg_3player.utilities], [])


def test_irda_on_game2(hgg1):
    red_game, red_var = irda_on_game(hgg1)
    assert not (red_game.utilities, red_var) == (hgg1.utilities, [])


def test_irda_on_game3(hgg1):
    red_game, red_var = irda_on_game(hgg1)
    assert red_game.players_actions == [[1], [1], [1], [1]]


def test_node_complementary1(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(2, 1)],
                        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2, x_pairval)
    assert Node(pcp, [(2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2,
                x_pairval, sub_sys, sub_sys.solutions[0]).is_complementary


def test_node_complementary2(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(2, 1)],
                        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], 2, x_pairval)
    assert not Node(pcp, [(2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], 2,
                    x_pairval, sub_sys, {}).is_complementary


def test_node_complementary3(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1, x_pairval)
    assert not Node(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1, x_pairval,
                    sub_sys, sub_sys.solutions[0]).is_complementary


def test_node_complementary4(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)], 1,
                        x_pairval)
    assert Node(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)], 1, x_pairval,
                sub_sys, sub_sys.solutions[0]).is_complementary


def test_node_initial1(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(2, 1)],
                        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2, x_pairval)
    assert Node(pcp, [(2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2,
                x_pairval, sub_sys, sub_sys.solutions[0]).is_initial


def test_node_initial2(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)], 1,
                        x_pairval)
    assert not Node(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)], 1, x_pairval,
                    sub_sys, sub_sys.solutions[0]).is_initial


def test_node_initial3(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1, x_pairval)
    assert not Node(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1, x_pairval,
                    sub_sys, sub_sys.solutions[0]).is_initial


def test_node_initial4(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(0, 1), (1, 1)], [(0, 0), (1, 1)], 1, x_pairval)
    assert Node(pcp, [(0, 1), (1, 1)], [(0, 0), (1, 1)], 1, x_pairval, sub_sys,
                sub_sys.solutions[0]).is_initial


# def test_node_degen1(nfg_3player):
#     pcp=pcp_of_game(nfg_3player)
#     x_pairval=x_pairval_of_pcp(pcp)
#     sub_sys=Subsystem(pcp, [(2, 1)], [(0, 0), (0, 1),
#     (1, 0), (1, 1), (2, 0)], 2, x_pairval)
#     assert not Node(pcp,[(2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
#     2,x_pairval,sub_sys,sub_sys.solutions[0]).is_degenerate
#
# def test_node_degen2(nfg_3player):
#     pcp = pcp_of_game(nfg_3player)
#     x_pairval = x_pairval_of_pcp(pcp)
#     sub_sys = Subsystem(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1,
#     x_pairval)
#     assert not Node(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1,
#     x_pairval, sub_sys,sub_sys.solutions[0] ).is_degenerate
#
# def test_node_degen3(nfg_3player):
#     pcp = pcp_of_game(nfg_3player)
#     x_pairval = x_pairval_of_pcp(pcp)
#     sub_sys = Subsystem(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)],
#     1, x_pairval)
#     assert not Node(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)],
#     1, x_pairval, sub_sys,sub_sys.solutions[0]).is_degenerate
#
# def test_node_degen4(nfg_4degen):
#     pcp = pcp_of_game(nfg_4degen)
#     pcp.omega0 = {0: 0, 1: 0, 2: 1, 3: 1}
#     x_pairval = x_pairval_of_pcp(pcp)
#     sub_sys = Subsystem(pcp, [(0, 0), (1, 1)], [(0, 1), (1, 0)],
#     1, x_pairval)
#     node=Node(pcp, [(0, 0), (1, 1)], [(0, 1), (1, 0)], 1,
#     x_pairval, sub_sys,sub_sys.solutions[0])
#     node.check_degeneracy()
#     assert Node(pcp, [(0, 0), (1, 1)], [(0, 1), (1, 0)], 1,
#     x_pairval, sub_sys,sub_sys.solutions[0]).is_degenerate

def test_first_node0(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    first_n = first_node(pcp, x_pairval)[0]
    assert first_n.set_z == [(0, 1)]
    assert first_n.set_w == [(0, 0)]
    assert first_n.coordinates == {pcp.ring('x0_0'): 1, pcp.ring('x0_1'): 0}


def test_first_node1(nfg_4degen):
    pcp = pcp_of_game(nfg_4degen)
    pcp.omega0 = {0: 0, 1: 0, 2: 1, 3: 1}
    x_pairval = x_pairval_of_pcp(pcp)
    first_n = first_node(pcp, x_pairval)[0]
    assert first_n.set_z == [(0, 0)]
    assert first_n.set_w == [(0, 1)]
    assert first_n.coordinates == {pcp.ring('x0_0'): 0, pcp.ring('x0_1'): 1}


def test_first_node2(hgg1):
    pcp = pcp_of_game(hgg1)
    x_pairval = x_pairval_of_pcp(pcp)
    first_n = first_node(pcp, x_pairval)[0]
    assert first_n.set_z == [(0, 0)]
    assert first_n.set_w == [(0, 1)]
    assert first_n.coordinates == {pcp.ring('x0_0'): 0, pcp.ring('x0_1'): 1}


def test_lift0(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    first_n = first_node(pcp, x_pairval)[0]
    lift_node = first_n.lift(pcp, x_pairval)[0]
    sub_sys = Subsystem(pcp, [(0, 1), (1, 1)], [(0, 0), (1, 1)], 1, x_pairval)
    assert set(lift_node.set_z) == {(0, 1), (1, 1)}
    assert set(lift_node.set_w) == {(0, 0), (1, 1)}
    assert lift_node.coordinates == sub_sys.solutions[0]


def test_lift1(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)], 1,
                        x_pairval)
    lift_node = Node(pcp, [], [(0, 0), (1, 1), (0, 1), (1, 0)],
                     1, x_pairval, sub_sys,
                     sub_sys.solutions[0]).lift(pcp, x_pairval)[0]
    sub_sys_lift = Subsystem(pcp, [(2, 1)],
                             [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2,
                             x_pairval)
    assert set(lift_node.set_z) == {(2, 1)}
    assert set(lift_node.set_w) == {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)}
    assert lift_node.coordinates == sub_sys_lift.solutions[0]


def test_traverse0(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    # sub_sys = Subsystem(pcp, [ (0, 1),(1, 1)], [(0, 0), (1, 1)],
    # 1, x_pairval)
    # current_node=Node(pcp, [ (0, 1),(1, 1)], [(0, 0), (1, 1)],
    # 1, x_pairval, sub_sys, sub_sys.solutions[0])
    first_n = first_node(pcp, x_pairval)[0]
    lift_node = first_n.lift(pcp, x_pairval)[0]
    next_node = lift_node.traverse(first_n, x_pairval)[0]
    sub_sys_trav = Subsystem(pcp, [(0, 1)], [(0, 0), (1, 1), (0, 1)], 1,
                             x_pairval)
    assert set(next_node.set_z) == {(0, 1)}
    assert set(next_node.set_w) == {(0, 0), (1, 1), (0, 1)}
    assert next_node.coordinates == sub_sys_trav.solutions[0]


def test_descent0(nfg_3descent):
    pcp = pcp_of_game(nfg_3descent)
    pcp.omega0 = {0: 0, 1: 1, 2: 0}
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(2, 1)],
                        [(0, 0), (1, 1), (2, 1), (1, 0), (0, 1)], 2, x_pairval)
    current_node = Node(pcp, [(2, 1)],
                        [(0, 0), (1, 1), (2, 1), (1, 0), (0, 1)], 2, x_pairval,
                        sub_sys, sub_sys.solutions[0])
    descent_node = current_node.descend(pcp, x_pairval)[0]
    sub_sys_desc = Subsystem(pcp, [], [(0, 0), (1, 1), (1, 0), (0, 1)], 1,
                             x_pairval)
    assert set(descent_node.set_z) == set([])
    assert set(descent_node.set_w) == {(0, 0), (1, 1), (1, 0), (0, 1)}
    assert descent_node.coordinates == sub_sys_desc.solutions[0]


def test_compute_arc0(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    first_n = first_node(pcp, x_pairval)[0]
    lift_node = first_n.lift(pcp, x_pairval)[0]
    (set_z, set_w) = lift_node.compute_arc(first_n)
    assert set(set_z) == {(0, 1)} and set(set_w) == {(0, 0), (1, 1)}


def test_normalized_strategy0(nfg_3player):
    pcp = pcp_of_game(nfg_3player)
    x_pairval = x_pairval_of_pcp(pcp)
    sub_sys = Subsystem(pcp, [(2, 1)],
                        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2, x_pairval)
    node = Node(pcp, [(2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2,
                x_pairval, sub_sys, sub_sys.solutions[0])
    assert node.normalized_strategy() == {0: [QQ(5 / 12), QQ(7 / 12)],
                                          1: [QQ(2 / 7), QQ(5 / 7)], 2: [1, 0]}
