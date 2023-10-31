import numpy as np
import pytest
from sage.all import ideal

from gtnash.util.polynomial_complementary_problem import \
    PolynomialComplementaryProblem, Subsystem
from gtnash.game.normalformgame import NFG
from gtnash.game.hypergraphicalgame import HGG
# from gtnash.util.irda import irda
#
# from fractions import Fraction


# A LOT OF THING TO BE REDONE IN PolynomialComplementaryProblem
# SOME METHOD A REDONDANT
# SOME SHOULD RETURN OBJECT AN NOT MODIFY SELF
# ALL ATTRIBUTE SHOULD BE DECLARED IN THE __INIT__ AND NOT
# MODIFIED THROUGHT SECONDARY METHOD CALLED IN THE INIT
# HAVING AN EMPTY PCP SHOULD MAKE TEST EASIER
# REMOVE IRDA from PCP, should be done before not during creation of pcp

# ADD TEST FOR GAMES WHERE IRDA IS APPLIED (STUFF ABOUT INDEXES)


# getnegativeutilities: DEPRECATED WARNING THAT DO NOT STOP
# EXECUTION BUT VCREATE A WARNING/ERROR FOR TEST


def gen_random_nfg(players_actions):
    util = []
    nbjoint_act = np.prod([len(p_a) for p_a in players_actions])
    for n in range(len(players_actions)):
        util += [list(np.random.randint(0, 10, nbjoint_act))]
    rand_nfg = NFG(players_actions, util)
    return rand_nfg


@pytest.fixture
def pcp_4player_nfg():
    utilities = [
        [50, 59, 27, 4, 72, 69, 18, 35, 6, 89, 78, 19, 36, 76, 64, 20],
        [97, 5, 90, 60, 6, 13, 56, 82, 89, 79, 52, 34, 35, 100, 60, 34],
        [15, 30, 53, 12, 79, 77, 15, 38, 100, 82, 35, 10, 24, 0, 29, 27],
        [28, 66, 83, 1, 54, 89, 71, 35, 46, 62, 96, 26, 20, 58, 16, 81]]

    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    tmp_nfg = NFG(players_actions, utilities)
    return PolynomialComplementaryProblem(tmp_nfg, fact_y=False)
    # return PolynomialComplementaryProblem(NFG([],[]))


@pytest.fixture
def empty_pcp():
    return PolynomialComplementaryProblem(HGG([], [], []), {0: 0})


@pytest.fixture
def pcp_3player_nfg():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[6, 7, 0, 5, 1, 4, 2, 3], [0, 3, 7, 4, 6, 5, 1, 2],
                 [4, 7, 4, 0, 3, 2, 6, 1]]
    current_nfg = NFG(players_actions, utilities)
    return PolynomialComplementaryProblem(current_nfg)


@pytest.fixture
def pcp_3player_nfg_no_y():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[6, 7, 0, 5, 1, 4, 2, 3], [0, 3, 7, 4, 6, 5, 1, 2],
                 [4, 7, 4, 0, 3, 2, 6, 1]]
    current_nfg = NFG(players_actions, utilities)
    return PolynomialComplementaryProblem(current_nfg, fact_y=False)


@pytest.fixture
def pcp_4p_nfg_degen():
    utilities = [
        [50, 59, 27, 4, 72, 69, 18, 35, 6, 89, 78, 19, 36, 76, 64, 20],
        [97, 5, 90, 60, 6, 13, 56, 82, 89, 79, 52, 34, 35, 100, 60, 34],
        [15, 30, 53, 12, 79, 77, 15, 38, 100, 82, 35, 10, 24, 0, 29, 27],
        [28, 66, 83, 1, 54, 89, 71, 35, 46, 62, 96, 26, 20, 58, 16, 81]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    current_nfg = NFG(players_actions, utilities)
    return PolynomialComplementaryProblem(current_nfg)


@pytest.fixture
def pcp_hgg1():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
         [-3, -1, -7, -5, -7, -5, -10, -9]],
        [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3], [-1, 0, -5, -3]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PolynomialComplementaryProblem(hgg)


def pcp_hgg1_no_y():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[-3, -7, -7, -10, -1, -5, -5, -9], [-3, -7, -1, -5, -7, -10, -5, -9],
         [-3, -1, -7, -5, -7, -5, -10, -9]],
        [[-1, -5, 0, -3], [-1, 0, -5, -3]], [[-1, -5, 0, -3], [-1, 0, -5, -3]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PolynomialComplementaryProblem(hgg, fact_y=False)


@pytest.fixture
def pcp_hgg2():
    utilities = [
        [[-3, -1, -3, -2, -2, -3, -2, -1], [-1, -3, -5, -1, -1, -6, -3, -4],
         [-2, -3, -6, -4, -3, -1, -3, -4]],
        [[-1, -3, -2, -2], [-1, -2, -2, -1]],
        [[-3, -1, -4, -5], [-1, -3, -1, -5]]]
    # Error up level impossible, 2->3, [[0,1],[0,1],[0,1],[0,1]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PolynomialComplementaryProblem(hgg)


@pytest.fixture
def pcp_hgg3():
    utilities = [
        [[74, 6, 9, 60, 77, 30, 47, 0], [51, 97, 98, 83, 90, 1, 2, 47],
         [18, 16, 29, 86, 100, 96, 93, 64]],
        [[84, 48, 27, 5, 100, 62, 16, 62], [10, 88, 72, 47, 13, 24, 42, 72],
         [1, 36, 68, 0, 53, 5, 61, 97]]]
    hypergraph = [[0, 1, 3], [0, 2, 3]]
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    hgg = HGG(players_actions, utilities, hypergraph)
    return PolynomialComplementaryProblem(hgg)


def test_generate_id_to_act1(empty_pcp):
    assert empty_pcp.generate_id_to_act() == {}


def test_generate_id_to_act2(pcp_4player_nfg):
    assert pcp_4player_nfg.generate_id_to_act() == {0: [0, 1], 1: [0, 1],
                                                    2: [0, 1], 3: [0, 1]}


def test_generate_id_to_act3(pcp_3player_nfg):
    assert pcp_3player_nfg.generate_id_to_act() == {0: [0, 1], 1: [0, 1],
                                                    2: [0, 1]}


def test_generate_id_to_act4(pcp_4p_nfg_degen):
    assert pcp_4p_nfg_degen.generate_id_to_act() == {0: [0, 1], 1: [0, 1],
                                                     2: [0, 1], 3: [0, 1]}


def test_generate_id_to_act5(pcp_hgg1):
    assert pcp_hgg1.generate_id_to_act() == {0: [0, 1], 1: [0, 1], 2: [0, 1],
                                             3: [0, 1]}


def test_generate_id_to_act6(pcp_hgg2):
    assert pcp_hgg2.generate_id_to_act() == {0: [0, 1], 1: [0, 1], 2: [0, 1],
                                             3: [0, 1]}


def test_generate_id_to_act7(pcp_hgg3):
    assert pcp_hgg3.generate_id_to_act() == {0: [0, 1], 1: [0, 1], 2: [0, 1],
                                             3: [0, 1]}


def test_generate_id_to_act8(empty_pcp):
    players_actions = [[0, 1, 2], [0, 1, 2], [0, 1, 2, 3], [0, 1]]
    empty_pcp.game = gen_random_nfg(players_actions)
    assert empty_pcp.generate_id_to_act() == {0: [0, 1, 2], 1: [0, 1, 2],
                                              2: [0, 1, 2, 3], 3: [0, 1]}


def test_generate_id_to_nb_act1(empty_pcp):
    assert empty_pcp.generate_id_to_nb_act() == {}


def test_generate_id_to_nb_act2(pcp_4player_nfg):
    assert pcp_4player_nfg.generate_id_to_nb_act() == {0: 2, 1: 2, 2: 2, 3: 2}


def test_generate_id_to_nb_act3(pcp_3player_nfg):
    assert pcp_3player_nfg.generate_id_to_nb_act() == {0: 2, 1: 2, 2: 2}


def test_generate_id_to_nb_act4(pcp_4p_nfg_degen):
    assert pcp_4p_nfg_degen.generate_id_to_nb_act() == {0: 2, 1: 2, 2: 2, 3: 2}


def test_generate_id_to_nb_act5(pcp_hgg1):
    assert pcp_hgg1.generate_id_to_nb_act() == {0: 2, 1: 2, 2: 2, 3: 2}


def test_generate_id_to_nb_act6(pcp_hgg2):
    assert pcp_hgg2.generate_id_to_nb_act() == {0: 2, 1: 2, 2: 2, 3: 2}


def test_generate_id_to_nb_act7(pcp_hgg3):
    assert pcp_hgg3.generate_id_to_nb_act() == {0: 2, 1: 2, 2: 2, 3: 2}


def test_generate_id_to_nb_act8(empty_pcp):
    players_actions = [[0, 1, 2], [0, 1, 2], [0, 1, 2, 3], [0, 1]]
    empty_pcp.game = gen_random_nfg(players_actions)
    assert empty_pcp.generate_id_to_nb_act() == {0: 3, 1: 3, 2: 4, 3: 2}


def test_gen_var_x0(empty_pcp):
    players_actions = [[0, 1, 2], [0, 1, 2], [0, 1, 2, 3], [0, 1]]
    empty_pcp.game = gen_random_nfg(players_actions)
    empty_pcp.gen_var_x()
    assert empty_pcp.set_x == ['x0_0', 'x0_1', 'x0_2', 'x1_0', 'x1_1', 'x1_2',
                               'x2_0', 'x2_1', 'x2_2', 'x2_3', 'x3_0',
                               'x3_1', ]
    assert empty_pcp.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                     (0, 2): 'x0_2', (1, 0): 'x1_0',
                                     (1, 1): 'x1_1', (1, 2): 'x1_2',
                                     (2, 0): 'x2_0', (2, 1): 'x2_1',
                                     (2, 2): 'x2_2', (2, 3): 'x2_3',
                                     (3, 0): 'x3_0', (3, 1): 'x3_1'}


# {(0,0):'x0_0','x0_1','x0_2',
# 'x1_0','x1_1','x1_2',
# 'x2_0','x2_1','x2_2','x2_3',
# 'x3_0','x3_1',}


def test_gen_var_x1(pcp_3player_nfg):
    assert pcp_3player_nfg.set_x == ['x0_0', 'x0_1', 'x1_0', 'x1_1', 'x2_0',
                                     'x2_1']
    assert pcp_3player_nfg.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                           (1, 0): 'x1_0', (1, 1): 'x1_1',
                                           (2, 0): 'x2_0', (2, 1): 'x2_1'}


def test_gen_var_x2(pcp_4player_nfg):
    assert pcp_4player_nfg.set_x == ['x0_0', 'x0_1', 'x1_0', 'x1_1', 'x2_0',
                                     'x2_1', 'x3_0', 'x3_1']
    assert pcp_4player_nfg.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                           (1, 0): 'x1_0', (1, 1): 'x1_1',
                                           (2, 0): 'x2_0', (2, 1): 'x2_1',
                                           (3, 0): 'x3_0', (3, 1): 'x3_1'}


def test_gen_var_x3(pcp_4p_nfg_degen):
    assert pcp_4p_nfg_degen.set_x == ['x0_0', 'x0_1', 'x1_0', 'x1_1', 'x2_0',
                                      'x2_1', 'x3_0', 'x3_1']
    assert pcp_4p_nfg_degen.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                            (1, 0): 'x1_0', (1, 1): 'x1_1',
                                            (2, 0): 'x2_0', (2, 1): 'x2_1',
                                            (3, 0): 'x3_0', (3, 1): 'x3_1'}


def test_gen_var_x4(pcp_hgg1):
    assert pcp_hgg1.set_x == ['x0_0', 'x0_1', 'x1_0', 'x1_1', 'x2_0', 'x2_1',
                              'x3_0', 'x3_1']
    assert pcp_hgg1.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                    (1, 0): 'x1_0', (1, 1): 'x1_1',
                                    (2, 0): 'x2_0', (2, 1): 'x2_1',
                                    (3, 0): 'x3_0', (3, 1): 'x3_1'}


def test_gen_var_x5(pcp_hgg2):
    assert pcp_hgg2.set_x == ['x0_0', 'x0_1', 'x1_0', 'x1_1', 'x2_0', 'x2_1',
                              'x3_0', 'x3_1']
    assert pcp_hgg2.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                    (1, 0): 'x1_0', (1, 1): 'x1_1',
                                    (2, 0): 'x2_0', (2, 1): 'x2_1',
                                    (3, 0): 'x3_0', (3, 1): 'x3_1'}


def test_gen_var_x6(pcp_hgg3):
    assert pcp_hgg3.set_x == ['x0_0', 'x0_1', 'x1_0', 'x1_1', 'x2_0', 'x2_1',
                              'x3_0', 'x3_1']
    assert pcp_hgg3.couple_to_x == {(0, 0): 'x0_0', (0, 1): 'x0_1',
                                    (1, 0): 'x1_0', (1, 1): 'x1_1',
                                    (2, 0): 'x2_0', (2, 1): 'x2_1',
                                    (3, 0): 'x3_0', (3, 1): 'x3_1'}


# GEN OMEGA0 was modified to avoid using IRDA which was "useless"
# as we are supposed to use it before creating the pcp

def test_omega0_1(pcp_3player_nfg):
    assert pcp_3player_nfg.omega0 == {0: 0, 1: 0, 2: 0}


def test_omega0_2(pcp_4player_nfg):
    assert pcp_4player_nfg.omega0 == {0: 0, 1: 0, 2: 0, 3: 0}


def test_omega0_3(pcp_hgg1):
    # print(irda(pcp_hgg1.game)[0])
    assert pcp_hgg1.omega0 == {0: 0, 1: 0, 2: 0, 3: 0}


def test_omega0_4(pcp_hgg2):
    print(pcp_hgg2)
    assert pcp_hgg2.omega0 == {0: 0, 1: 0, 2: 0, 3: 0}


# def test_generate_Q0(empty_pcp):

def test_generate_R1(pcp_3player_nfg):
    ring = pcp_3player_nfg.ring
    assert pcp_3player_nfg.generate_R() == {
        (0, 0, 0): (-2) * ring('x1_0') * ring('x2_0') - ring('x1_0') * ring(
            'x2_1') + (-8) * ring('x1_1') * ring('x2_0') + (-3) * ring(
            'x1_1') * ring('x2_1'),
        (0, 1, 0): (-7) * ring('x1_0') * ring('x2_0') + (-4) * ring(
            'x1_0') * ring('x2_1') + (-6) * ring('x1_1') * ring('x2_0') + (
                       -5) * ring('x1_1') * ring('x2_1'),
        (1, 0, 0): (-8) * ring('x0_0') * ring('x2_0') + (-5) * ring(
            'x0_0') * ring('x2_1') + (-2) * ring('x0_1') * ring('x2_0') + (
                       -3) * ring('x0_1') * ring('x2_1'),
        (1, 1, 0): -ring('x0_0') * ring('x2_0') + (-4) * ring('x0_0') * ring(
            'x2_1') + (-7) * ring('x0_1') * ring('x2_0') + (-6) * ring(
            'x0_1') * ring('x2_1'),
        (2, 0, 0): (-4) * ring('x0_0') * ring('x1_0') + (-4) * ring(
            'x0_0') * ring('x1_1') + (-5) * ring('x0_1') * ring('x1_0') + (
                       -2) * ring('x0_1') * ring('x1_1'),
        (2, 1, 0): -ring('x0_0') * ring('x1_0') + (-8) * ring('x0_0') * ring(
            'x1_1') + (-6) * ring('x0_1') * ring('x1_0') + (-7) * ring(
            'x0_1') * ring('x1_1')}


def test_generate_R2(pcp_hgg1):
    ring = pcp_hgg1.ring
    assert pcp_hgg1.generate_R() == {
        (0, 0, 0): (-3) * ring('x1_0') * ring('x2_0') + (-7) * ring(
            'x1_0') * ring('x2_1') + (-7) * ring('x1_1') * ring('x2_0') + (
                       -10) * ring('x1_1') * ring('x2_1'),
        (0, 1, 0): -ring('x1_0') * ring('x2_0') + (-5) * ring('x1_0') * ring(
            'x2_1') + (-5) * ring('x1_1') * ring('x2_0') + (-9) * ring(
            'x1_1') * ring('x2_1'),
        (1, 0, 0): (-4) * ring('x0_0') * ring('x2_0') + (-8) * ring(
            'x0_0') * ring('x2_1') + (-8) * ring('x0_1') * ring('x2_0') + (
                       -11) * ring('x0_1') * ring('x2_1'),
        (1, 0, 1): (-2) * ring('x3_0') + (-6) * ring('x3_1'),
        (1, 1, 0): (-2) * ring('x0_0') * ring('x2_0') + (-6) * ring(
            'x0_0') * ring('x2_1') + (-6) * ring('x0_1') * ring('x2_0') + (
                       -10) * ring('x0_1') * ring('x2_1'),
        (1, 1, 1): -ring('x3_0') + (-4) * ring('x3_1'),
        (2, 0, 0): (-4) * ring('x0_0') * ring('x1_0') + (-8) * ring(
            'x0_0') * ring('x1_1') + (-8) * ring('x0_1') * ring('x1_0') + (
                       -11) * ring('x0_1') * ring('x1_1'),
        (2, 0, 2): (-2) * ring('x3_0') + (-6) * ring('x3_1'),
        (2, 1, 0): (-2) * ring('x0_0') * ring('x1_0') + (-6) * ring(
            'x0_0') * ring('x1_1') + (-6) * ring('x0_1') * ring('x1_0') + (
                       -10) * ring('x0_1') * ring('x1_1'),
        (2, 1, 2): -ring('x3_0') + (-4) * ring('x3_1'),
        (3, 0, 1): (-2) * ring('x1_0') + (-6) * ring('x1_1'),
        (3, 0, 2): (-2) * ring('x2_0') + (-6) * ring('x2_1'),
        (3, 1, 1): -ring('x1_0') + (-4) * ring('x1_1'),
        (3, 1, 2): -ring('x2_0') + (-4) * ring('x2_1')
    }


# def test_gen_poly

def test_generate_poly1(pcp_3player_nfg):
    ring = pcp_3player_nfg.ring
    y_value = {ring('y2_0'): 1}
    tmp_couple_poly = {
        (n, i): pcp_3player_nfg.couple_to_poly[(n, i)].subs(y_value) for (n, i)
        in pcp_3player_nfg.couple_to_poly.keys()}
    assert tmp_couple_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') + ring('x1_0') * ring(
            'x2_1') + 8 * ring('x1_1') * ring('x2_0') + 3 * ring(
            'x1_1') * ring('x2_1') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') + 4 * ring('x1_0') * ring(
            'x2_1') + 6 * ring('x1_1') * ring('x2_0') + 5 * ring(
            'x1_1') * ring('x2_1') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') + 5 * ring('x0_0') * ring(
            'x2_1') + 2 * ring('x0_1') * ring('x2_0') + 3 * ring(
            'x0_1') * ring('x2_1') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') + 4 * ring('x0_0') * ring(
            'x2_1') + 7 * ring('x0_1') * ring('x2_0') + 6 * ring(
            'x0_1') * ring('x2_1') - 1,
        (2, 0): 4 * ring('x0_0') * ring('x1_0') + 4 * ring('x0_0') * ring(
            'x1_1') + 5 * ring('x0_1') * ring('x1_0') + 2 * ring(
            'x0_1') * ring('x1_1') - 1,
        (2, 1): ring('x0_0') * ring('x1_0') + 8 * ring('x0_0') * ring(
            'x1_1') + 6 * ring('x0_1') * ring('x1_0') + 7 * ring(
            'x0_1') * ring('x1_1') - 1}


def test_substitute1(pcp_3player_nfg):
    ring = pcp_3player_nfg.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0, ring('x2_1'): 0}
    assert pcp_3player_nfg.substitute(x_dico, 2).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') * ring('y2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') * ring('y2_0') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') * ring('y2_0') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') * ring('y2_0') - 1,
        (2, 0): 4 * ring('x0_0') * ring('x1_0') * ring('y2_0') - 1,
        (2, 1): ring('x0_0') * ring('x1_0') * ring('y2_0') - 1}


def test_substitute1b(pcp_3player_nfg_no_y):
    ring = pcp_3player_nfg_no_y.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0, ring('x2_1'): 0}
    assert pcp_3player_nfg_no_y.substitute(x_dico, 2).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') - 1,
        (2, 0): 4 * ring('x0_0') * ring('x1_0') - 1,
        (2, 1): ring('x0_0') * ring('x1_0') - 1}


def test_substitute2(pcp_3player_nfg):
    ring = pcp_3player_nfg.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0, ring('x2_1'): 0}
    assert pcp_3player_nfg.substitute(x_dico, 1).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') * ring('y2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') * ring('y2_0') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') * ring('y2_0') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') * ring('y2_0') - 1}


def test_substitute2b(pcp_3player_nfg_no_y):
    ring = pcp_3player_nfg_no_y.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0, ring('x2_1'): 0}
    assert pcp_3player_nfg_no_y.substitute(x_dico, 1).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') - 1}


def test_substitute3(pcp_3player_nfg):
    ring = pcp_3player_nfg.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0, ring('x2_1'): 0}
    assert pcp_3player_nfg.substitute(x_dico, 0).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') * ring('y2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') * ring('y2_0') - 1
        }


def test_substitute3b(pcp_3player_nfg_no_y):
    ring = pcp_3player_nfg_no_y.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0, ring('x2_1'): 0}
    assert pcp_3player_nfg_no_y.substitute(x_dico, 0).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') - 1
        }


def test_substitute4(pcp_3player_nfg):
    ring = pcp_3player_nfg.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0}
    assert pcp_3player_nfg.substitute(x_dico, 2).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') * ring('y2_0') + ring(
            'x1_0') * ring('x2_1') * ring('y2_0') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') * ring('y2_0') + 4 * ring(
            'x1_0') * ring('x2_1') * ring('y2_0') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') * ring('y2_0') + 5 * ring(
            'x0_0') * ring('x2_1') * ring('y2_0') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') * ring('y2_0') + 4 * ring(
            'x0_0') * ring('x2_1') * ring('y2_0') - 1,
        (2, 0): 4 * ring('x0_0') * ring('x1_0') * ring('y2_0') - 1,
        (2, 1): ring('x0_0') * ring('x1_0') * ring('y2_0') - 1}


def test_substitute4b(pcp_3player_nfg_no_y):
    ring = pcp_3player_nfg_no_y.ring
    x_dico = {ring('x0_1'): 0, ring('x1_1'): 0}
    assert pcp_3player_nfg_no_y.substitute(x_dico, 2).couple_to_poly == {
        (0, 0): 2 * ring('x1_0') * ring('x2_0') + ring(
            'x1_0') * ring('x2_1') - 1,
        (0, 1): 7 * ring('x1_0') * ring('x2_0') + 4 * ring(
            'x1_0') * ring('x2_1') - 1,
        (1, 0): 8 * ring('x0_0') * ring('x2_0') + 5 * ring(
            'x0_0') * ring('x2_1') - 1,
        (1, 1): ring('x0_0') * ring('x2_0') + 4 * ring(
            'x0_0') * ring('x2_1') - 1,
        (2, 0): 4 * ring('x0_0') * ring('x1_0') - 1,
        (2, 1): ring('x0_0') * ring('x1_0') - 1}

# Substitue for Hgg?


@pytest.fixture
def subsys_empty(pcp_3player_nfg):
    return Subsystem(pcp_3player_nfg, [], [], 2, {})


@pytest.fixture
def subsys_empty_no_y(pcp_3player_nfg_no_y):
    return Subsystem(pcp_3player_nfg_no_y, [], [], 2, {})


@pytest.fixture
def subsys_3p_2l_n1(pcp_3player_nfg):
    # return Subsystem(pcp_3player_nfg,[(0,1),(1,0),(2,0)]
    # ,[(1,1),(0,0),(2,0)],2,{})
    return Subsystem(pcp_3player_nfg, [(2, 1)],
                     [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2, {})


@pytest.fixture
def subsys_3p_2l_n1_no_y(pcp_3player_nfg_no_y):
    # return Subsystem(pcp_3player_nfg,[(0,1),(1,0),(2,0)]
    # ,[(1,1),(0,0),(2,0)],2,{})
    return Subsystem(pcp_3player_nfg_no_y, [(2, 1)],
                     [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2, {})


@pytest.fixture
def subsys_3p_2l_n2(pcp_3player_nfg):
    # return Subsystem(pcp_3player_nfg,[(0,1),(1,0),(2,0)],
    # [(1,1),(0,0),(2,1)],2,{})
    return Subsystem(pcp_3player_nfg, [(2, 1)],
                     [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], 2, {})


@pytest.fixture
def subsys_3p_2l_n2_no_y(pcp_3player_nfg_no_y):
    # return Subsystem(pcp_3player_nfg,[(0,1),(1,0),(2,0)],
    # [(1,1),(0,0),(2,1)],2,{})
    return Subsystem(pcp_3player_nfg_no_y, [(2, 1)],
                     [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], 2, {})


def test_equations1(subsys_empty):
    ring = subsys_empty.ring
    assert set(
        subsys_empty.equations
    ) == {ring('y0_0') - 1, ring('y1_0') -
          ring('y0_0'), ring('y2_0') -
          ring('y1_0')}

# def test_equations1b(subsys_empty_no_y):
#     # ring = subsys_empty_no_y.ring
#     assert Error
#     # print("Hello")
#     # print(subsys_empty_no_y.equations)
#     # assert set(
#     #     subsys_empty_no_y.equations
#     # ) == {}


def test_equations2(subsys_3p_2l_n1, pcp_3player_nfg):
    ring = subsys_3p_2l_n1.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(
        subsys_3p_2l_n1.equations
    ) == {ring('x2_1'), pcp_3player_nfg.couple_to_poly[(0, 0)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(0, 1)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(1, 0)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(1, 1)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(2, 0)].subs(dico_x0),
          ring('y0_0') - 1, ring('y1_0') - ring('y0_0'),
          ring('y2_0') - ring('y1_0')}


def test_equations2b(subsys_3p_2l_n1_no_y, pcp_3player_nfg_no_y):
    ring = subsys_3p_2l_n1_no_y.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(
        subsys_3p_2l_n1_no_y.equations
    ) == {ring('x2_1'),
          pcp_3player_nfg_no_y.couple_to_poly[(0, 0)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(0, 1)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(1, 0)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(1, 1)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(2, 0)].subs(dico_x0)}


def test_equations3(subsys_3p_2l_n2, pcp_3player_nfg):
    ring = subsys_3p_2l_n2.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(
        subsys_3p_2l_n2.equations
    ) == {ring('x2_1'),
          pcp_3player_nfg.couple_to_poly[(0, 0)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(0, 1)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(1, 0)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(1, 1)].subs(dico_x0),
          pcp_3player_nfg.couple_to_poly[(2, 1)].subs(dico_x0),
          ring('y0_0') - 1,
          ring('y1_0') - ring('y0_0'),
          ring('y2_0') - ring('y1_0')}


def test_equations3b(subsys_3p_2l_n2_no_y, pcp_3player_nfg_no_y):
    ring = subsys_3p_2l_n2_no_y.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(
        subsys_3p_2l_n2_no_y.equations
    ) == {ring('x2_1'),
          pcp_3player_nfg_no_y.couple_to_poly[(0, 0)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(0, 1)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(1, 0)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(1, 1)].subs(dico_x0),
          pcp_3player_nfg_no_y.couple_to_poly[(2, 1)].subs(dico_x0)
          }


def test_inequations1(subsys_empty, pcp_3player_nfg):
    assert set(subsys_empty.inequations) == set(
        pcp_3player_nfg.couple_to_poly.values())


def test_inequations2(subsys_3p_2l_n1, pcp_3player_nfg):
    ring = subsys_3p_2l_n1.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(subsys_3p_2l_n1.inequations) == {
        pcp_3player_nfg.couple_to_poly[(2, 1)].subs(dico_x0)}


def test_inequations2b(subsys_3p_2l_n1_no_y, pcp_3player_nfg_no_y):
    ring = subsys_3p_2l_n1_no_y.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(subsys_3p_2l_n1_no_y.inequations) == {
        pcp_3player_nfg_no_y.couple_to_poly[(2, 1)].subs(dico_x0)}


def test_inequations3(subsys_3p_2l_n2, pcp_3player_nfg):
    ring = subsys_3p_2l_n2.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(subsys_3p_2l_n2.inequations) == {
        pcp_3player_nfg.couple_to_poly[(2, 0)].subs(dico_x0)}


def test_inequations3b(subsys_3p_2l_n2_no_y, pcp_3player_nfg_no_y):
    ring = subsys_3p_2l_n2_no_y.ring
    dico_x0 = {ring('x2_1'): 0}
    assert set(subsys_3p_2l_n2_no_y.inequations) == {
        pcp_3player_nfg_no_y.couple_to_poly[(2, 0)].subs(dico_x0)}


def test_ideal1(subsys_3p_2l_n1, pcp_3player_nfg):
    ring = subsys_3p_2l_n1.ring
    dico_x0 = {ring('x2_1'): 0}
    assert subsys_3p_2l_n1.ideal ==\
        ideal([ring('x2_1'),
               pcp_3player_nfg.couple_to_poly[(0, 0)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(0, 1)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(1, 0)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(1, 1)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(2, 0)].subs(dico_x0),
               ring('y0_0') - 1,
               ring('y1_0') - ring('y0_0'),
               ring('y2_0') - ring('y1_0')])


def test_ideal1b(subsys_3p_2l_n1_no_y, pcp_3player_nfg_no_y):
    ring = subsys_3p_2l_n1_no_y.ring
    dico_x0 = {ring('x2_1'): 0}
    assert subsys_3p_2l_n1_no_y.ideal ==\
        ideal([ring('x2_1'),
               pcp_3player_nfg_no_y.couple_to_poly[(0, 0)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(0, 1)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(1, 0)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(1, 1)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(2, 0)].subs(dico_x0)])


def test_ideal2(subsys_3p_2l_n2, pcp_3player_nfg):
    ring = subsys_3p_2l_n2.ring
    dico_x0 = {ring('x2_1'): 0}
    assert subsys_3p_2l_n2.ideal == \
        ideal([ring('x2_1'),
               pcp_3player_nfg.couple_to_poly[(0, 0)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(0, 1)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(1, 0)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(1, 1)].subs(dico_x0),
               pcp_3player_nfg.couple_to_poly[(2, 1)].subs(dico_x0),
               ring('y0_0') - 1,
               ring('y1_0') - ring('y0_0'),
               ring('y2_0') - ring('y1_0')])


def test_ideal2b(subsys_3p_2l_n2_no_y, pcp_3player_nfg_no_y):
    ring = subsys_3p_2l_n2_no_y.ring
    dico_x0 = {ring('x2_1'): 0}
    assert subsys_3p_2l_n2_no_y.ideal == \
        ideal([ring('x2_1'),
               pcp_3player_nfg_no_y.couple_to_poly[(0, 0)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(0, 1)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(1, 0)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(1, 1)].subs(dico_x0),
               pcp_3player_nfg_no_y.couple_to_poly[(2, 1)].subs(dico_x0)])


def test_compute_variety1(subsys_3p_2l_n1):
    assert len(subsys_3p_2l_n1.variety) == 2


def test_compute_variety2(subsys_3p_2l_n2):
    assert len(subsys_3p_2l_n2.variety) == 2


def test_feasible_point1(subsys_3p_2l_n1):
    assert not subsys_3p_2l_n1.feasible_point(subsys_3p_2l_n1.variety[0])[0]


def test_feasible_point2(subsys_3p_2l_n2):
    assert not subsys_3p_2l_n2.feasible_point(subsys_3p_2l_n2.variety[0])[0]


def test_feasible_point3(subsys_3p_2l_n1):
    assert subsys_3p_2l_n1.feasible_point(subsys_3p_2l_n1.variety[1])[0]


def test_feasible_point4(subsys_3p_2l_n2):
    assert not subsys_3p_2l_n2.feasible_point(subsys_3p_2l_n2.variety[1])[0]


def test_compute_solutions1(subsys_3p_2l_n1):
    assert subsys_3p_2l_n1.solutions == [subsys_3p_2l_n1.variety[1]]


def test_compute_solutions2(subsys_3p_2l_n2):
    assert subsys_3p_2l_n2.solutions == []
