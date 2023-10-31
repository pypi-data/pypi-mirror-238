from gtnash.game.hypergraphicalgame import HGG
from gtnash.util.irda import find_dominated_alternatives, irda
from gtnash.game.normalformgame import NFG
from gtnash.game.bayesiangame import BG
from gtnash.game.bayesian_hypergraphicalgame import BHGG

import pytest


@pytest.fixture
def hgg1():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [[[-3, -1, -3, -2, -2, -3, -2, -1],
                  [-2, -4, -6, -2, -2, -7, -4, -5],
                  [-2, -3, -6, -4, -3, -1, -3, -4]],
                 [[-1, -3, -2, -2], [-2, -3, -3, -2]],
                 [[-3, -1, -4, -5], [-1, -3, -1, -5]]]
    hypergraph = [[0, 1, 2], [1, 3], [2, 3]]
    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def hgg2():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[87, 77, 0, 49, 63, 99, 98, 25], [76, 100, 10, 43, 73, 65, 8, 56],
         [8, 36, 3, 100, 24, 3, 64, 28]],
        [[67, 38, 60, 64, 55, 100, 16, 13], [23, 59, 0, 9, 1, 8, 47, 33],
         [9, 7, 100, 39, 16, 18, 16, 62]]]
    hypergraph = [[0, 1, 2], [1, 2, 3]]
    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def hgg3():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [
        [[29, 39, 100, 46, 40, 18, 97, 37], [23, 81, 64, 62, 90, 73, 76, 53],
         [26, 36, 51, 5, 14, 99, 0, 54]],
        [[12, 37, 7, 7, 41, 59, 27, 86], [65, 100, 100, 49, 97, 31, 68, 58],
         [29, 70, 44, 61, 0, 53, 92, 74]]]
    hypergraph = [[0, 2, 3], [1, 2, 3]]
    return HGG(players_actions, utilities, hypergraph)


@pytest.fixture
def nfg1():
    players_actions = [[0, 1], [0, 1], [0, 1]]
    utilities = [[37, 63, 100, 69, 46, 60, 47, 41],
                 [24, 14, 79, 75, 100, 70, 34, 0],
                 [90, 34, 25, 25, 33, 68, 70, 3]]
    return NFG(players_actions, utilities)


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


@pytest.fixture
def bayesian_hgg1():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    theta = [[0, 1], [0, 1], [0, 1], [0, 1]]
    utilities = [[[[39, 19, 95, 0, 32, 97, 65, 69],
                   [22, 40, 67, 14, 100, 60, 5, 34],
                   [46, 27, 72, 45, 18, 84, 100, 33]],
                  [[61, 96, 22, 34, 34, 35, 39, 54],
                   [39, 42, 77, 76, 27, 45, 56, 0],
                   [21, 94, 80, 74, 100, 20, 55, 65]],
                  [[34, 47, 56, 73, 55, 59, 31, 17],
                   [57, 43, 0, 23, 41, 100, 73, 86],
                   [24, 53, 95, 45, 38, 17, 28, 76]],
                  [[47, 37, 100, 6, 20, 16, 17, 59],
                   [40, 44, 64, 13, 0, 73, 76, 71],
                   [23, 52, 19, 70, 41, 43, 30, 28]],
                  [[53, 38, 44, 33, 9, 71, 31, 82],
                   [62, 100, 70, 65, 74, 22, 47, 59],
                   [66, 82, 20, 0, 15, 3, 57, 60]],
                  [[46, 33, 0, 31, 50, 50, 35, 50],
                   [26, 77, 56, 47, 37, 51, 56, 57],
                   [28, 27, 100, 21, 29, 26, 83, 25]],
                  [[70, 88, 0, 15, 7, 34, 100, 58],
                   [53, 68, 17, 17, 16, 26, 84, 61],
                   [63, 80, 10, 15, 11, 43, 84, 50]],
                  [[91, 49, 99, 85, 62, 38, 21, 87],
                   [18, 36, 74, 84, 40, 45, 39, 88],
                   [63, 54, 57, 100, 45, 20, 0, 76]]],
                 [[[72, 67, 47, 94, 73, 92, 80, 81],
                   [55, 66, 45, 62, 78, 91, 55, 53],
                   [54, 75, 47, 42, 0, 52, 47, 100]],
                  [[64, 79, 39, 7, 43, 22, 68, 26],
                   [48, 67, 62, 5, 74, 82, 77, 65],
                   [40, 65, 38, 0, 59, 69, 100, 86]],
                  [[44, 53, 46, 82, 44, 89, 69, 97],
                   [61, 96, 88, 93, 70, 20, 100, 46],
                   [31, 89, 0, 61, 48, 77, 84, 46]],
                  [[59, 74, 63, 100, 34, 31, 38, 45],
                   [55, 52, 83, 74, 10, 65, 5, 50],
                   [74, 64, 65, 96, 19, 70, 0, 38]],
                  [[32, 100, 0, 54, 5, 37, 45, 66],
                   [2, 23, 49, 3, 62, 21, 23, 44],
                   [11, 54, 67, 8, 37, 69, 83, 27]],
                  [[41, 67, 72, 12, 65, 74, 65, 53],
                   [68, 68, 57, 49, 0, 91, 80, 61],
                   [97, 78, 86, 100, 34, 62, 57, 87]],
                  [[52, 54, 63, 18, 37, 67, 75, 73],
                   [47, 65, 93, 91, 59, 60, 0, 43],
                   [82, 76, 49, 91, 100, 82, 95, 50]],
                  [[39, 19, 95, 0, 32, 97, 65, 69],
                   [22, 40, 67, 14, 100, 60, 5, 34],
                   [46, 27, 72, 45, 18, 84, 100, 33]]]]
    p = [[6, 9, 8, 6, 6, 4, 3, 3], [1, 7, 9, 1, 7, 3, 6, 9]]
    hypergraph = [[0, 1, 2], [0, 2, 3]]
    return BHGG(players_actions, utilities, hypergraph, theta, p)


def test_find_dominated_alternatives1(hgg1):
    assert find_dominated_alternatives(hgg1) == (3, 1)


def test_find_dominated_alternatives2(hgg2):
    assert find_dominated_alternatives(hgg2) == (1, 1)


def test_find_dominated_alternatives3(hgg3):
    assert find_dominated_alternatives(hgg3) == (1, 0)


# eliminate_alternative
# nondominated
# local_difference
# subutilities_player


def test_irda1(hgg1):
    red_hgg, z_excluded = irda(hgg1)
    assert z_excluded == [(3, 1)]
    assert red_hgg.players_actions == [[0, 1], [0, 1], [0, 1], [0]]
    assert red_hgg.utilities == [[[-3, -1, -3, -2, -2, -3, -2, -1],
                                  [-2, -4, -6, -2, -2, -7, -4, -5],
                                  [-2, -3, -6, -4, -3, -1, -3, -4]],
                                 [[-1, -2], [-2, -3]],
                                 [[-3, -4], [-1, -1]]]


def test_irda2(hgg2):
    red_hgg, z_excluded = irda(hgg2)
    assert set(z_excluded) == {(1, 1), (3, 1)}
    assert red_hgg.players_actions == [[0, 1], [0], [0, 1], [0]]
    assert red_hgg.utilities == [
        [[87, 77, 63, 99], [76, 100, 73, 65], [8, 36, 24, 3]],
        [[67, 60], [23, 0], [9, 100]]]


def test_irda3(hgg3):
    red_hgg, z_excluded = irda(hgg3)
    assert set(z_excluded) == {(1, 0)}
    assert red_hgg.players_actions == [[0, 1], [1], [0, 1], [0, 1]]
    assert red_hgg.utilities == [
        [[29, 39, 100, 46, 40, 18, 97, 37], [23, 81, 64, 62, 90, 73, 76, 53],
         [26, 36, 51, 5, 14, 99, 0, 54]],
        [[41, 59, 27, 86], [97, 31, 68, 58], [0, 53, 92, 74]]]


def test_irda4(nfg1):
    red_hgg, z_excluded = irda(HGG.convert_to_HGG(nfg1))
    assert set(z_excluded) == set([])
    assert red_hgg.players_actions == [[0, 1], [0, 1], [0, 1]]
    assert red_hgg.utilities == [nfg1.utilities]


def test_irda5(three_bg):
    tmp_hgg = three_bg.convert_to_HGG()[0]
    red_hgg, z_excluded = irda(tmp_hgg)
    assert set(z_excluded) == set([])
    assert red_hgg.players_actions == \
        [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
    assert red_hgg.utilities == tmp_hgg.utilities


def test_irda6(bayesian_hgg1):
    tmp_hgg = bayesian_hgg1.convert_to_HGG()[0]
    red_hgg, z_excluded = irda(tmp_hgg)
    assert set(z_excluded) == set([])
    assert red_hgg.players_actions == [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1],
                                       [0, 1], [0, 1], [0, 1], ]
    assert red_hgg.utilities == tmp_hgg.utilities
