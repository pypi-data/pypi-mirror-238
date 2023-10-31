import numpy as np
import pytest

from gtnash.game.bayesian_hypergraphicalgame import BHGG
from fractions import Fraction


@pytest.fixture
def bayesian_polymatrix():
    players_actions = [[0, 1], [0, 1], [0, 1], [0, 1]]
    theta = [[0, 1], [0, 1], [0, 1], [0, 1]]
    same_game = [[[3, 0, 0, 2], [3, 0, 0, 2]], [[3, 0, 0, 2], [1, 0, 0, 2]],
                 [[1, 0, 0, 2], [3, 0, 0, 2]], [[1, 0, 0, 2], [1, 0, 0, 2]]]
    same_p = [4, 1, 1, 4]
    hypergr = [[0, 1], [1, 2], [2, 3], [0, 3]]
    return BHGG(players_actions, [same_game, same_game, same_game, same_game],
                hypergr, theta, [same_p, same_p, same_p, same_p])


# ADD a 4 player hypergraphe with edge size 3

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


def test_joint_actions1(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[0].joint_actions == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_actions2(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[1].joint_actions == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_actions3(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[2].joint_actions == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_actions4(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[3].joint_actions == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_actions5(bayesian_hgg1):
    assert (bayesian_hgg1.local_bayesiangames[0].joint_actions == np.mat(
        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
         [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])).all()


def test_joint_actions6(bayesian_hgg1):
    assert (bayesian_hgg1.local_bayesiangames[1].joint_actions == np.mat(
        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
         [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])).all()


def test_joint_type1(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[0].joint_theta == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_type2(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[1].joint_theta == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_type3(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[2].joint_theta == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_type4(bayesian_polymatrix):
    assert (bayesian_polymatrix.local_bayesiangames[3].joint_theta == np.mat(
        [[0, 0], [0, 1], [1, 0], [1, 1]])).all()


def test_joint_type5(bayesian_hgg1):
    assert (bayesian_hgg1.local_bayesiangames[0].joint_theta == np.mat(
        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
         [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])).all()


def test_joint_type6(bayesian_hgg1):
    assert (bayesian_hgg1.local_bayesiangames[1].joint_theta == np.mat(
        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
         [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])).all()


def test_local_utilities1(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[0].utilities == [
        [[3, 0, 0, 2], [3, 0, 0, 2]], [[3, 0, 0, 2], [1, 0, 0, 2]],
        [[1, 0, 0, 2], [3, 0, 0, 2]], [[1, 0, 0, 2], [1, 0, 0, 2]]]


def test_local_utilities2(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[1].utilities == [
        [[3, 0, 0, 2], [3, 0, 0, 2]], [[3, 0, 0, 2], [1, 0, 0, 2]],
        [[1, 0, 0, 2], [3, 0, 0, 2]], [[1, 0, 0, 2], [1, 0, 0, 2]]]


def test_local_utilities3(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[2].utilities == [
        [[3, 0, 0, 2], [3, 0, 0, 2]], [[3, 0, 0, 2], [1, 0, 0, 2]],
        [[1, 0, 0, 2], [3, 0, 0, 2]], [[1, 0, 0, 2], [1, 0, 0, 2]]]


def test_local_utilities4(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[3].utilities == [
        [[3, 0, 0, 2], [3, 0, 0, 2]], [[3, 0, 0, 2], [1, 0, 0, 2]],
        [[1, 0, 0, 2], [3, 0, 0, 2]], [[1, 0, 0, 2], [1, 0, 0, 2]]]


def test_local_utilities5(bayesian_hgg1):
    assert bayesian_hgg1.local_bayesiangames[0].utilities == [
        [[39, 19, 95, 0, 32, 97, 65, 69], [22, 40, 67, 14, 100, 60, 5, 34],
         [46, 27, 72, 45, 18, 84, 100, 33]],
        [[61, 96, 22, 34, 34, 35, 39, 54], [39, 42, 77, 76, 27, 45, 56, 0],
         [21, 94, 80, 74, 100, 20, 55, 65]],
        [[34, 47, 56, 73, 55, 59, 31, 17], [57, 43, 0, 23, 41, 100, 73, 86],
         [24, 53, 95, 45, 38, 17, 28, 76]],
        [[47, 37, 100, 6, 20, 16, 17, 59], [40, 44, 64, 13, 0, 73, 76, 71],
         [23, 52, 19, 70, 41, 43, 30, 28]],
        [[53, 38, 44, 33, 9, 71, 31, 82], [62, 100, 70, 65, 74, 22, 47, 59],
         [66, 82, 20, 0, 15, 3, 57, 60]],
        [[46, 33, 0, 31, 50, 50, 35, 50], [26, 77, 56, 47, 37, 51, 56, 57],
         [28, 27, 100, 21, 29, 26, 83, 25]],
        [[70, 88, 0, 15, 7, 34, 100, 58], [53, 68, 17, 17, 16, 26, 84, 61],
         [63, 80, 10, 15, 11, 43, 84, 50]],
        [[91, 49, 99, 85, 62, 38, 21, 87], [18, 36, 74, 84, 40, 45, 39, 88],
         [63, 54, 57, 100, 45, 20, 0, 76]]]


def test_local_utilities6(bayesian_hgg1):
    assert bayesian_hgg1.local_bayesiangames[1].utilities == [
        [[72, 67, 47, 94, 73, 92, 80, 81], [55, 66, 45, 62, 78, 91, 55, 53],
         [54, 75, 47, 42, 0, 52, 47, 100]],
        [[64, 79, 39, 7, 43, 22, 68, 26], [48, 67, 62, 5, 74, 82, 77, 65],
         [40, 65, 38, 0, 59, 69, 100, 86]],
        [[44, 53, 46, 82, 44, 89, 69, 97], [61, 96, 88, 93, 70, 20, 100, 46],
         [31, 89, 0, 61, 48, 77, 84, 46]],
        [[59, 74, 63, 100, 34, 31, 38, 45], [55, 52, 83, 74, 10, 65, 5, 50],
         [74, 64, 65, 96, 19, 70, 0, 38]],
        [[32, 100, 0, 54, 5, 37, 45, 66], [2, 23, 49, 3, 62, 21, 23, 44],
         [11, 54, 67, 8, 37, 69, 83, 27]],
        [[41, 67, 72, 12, 65, 74, 65, 53], [68, 68, 57, 49, 0, 91, 80, 61],
         [97, 78, 86, 100, 34, 62, 57, 87]],
        [[52, 54, 63, 18, 37, 67, 75, 73], [47, 65, 93, 91, 59, 60, 0, 43],
         [82, 76, 49, 91, 100, 82, 95, 50]],
        [[39, 19, 95, 0, 32, 97, 65, 69], [22, 40, 67, 14, 100, 60, 5, 34],
         [46, 27, 72, 45, 18, 84, 100, 33]]]


def test_local_proba1(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[0].p == [Fraction(4, 10),
                                                            Fraction(1, 10),
                                                            Fraction(1, 10),
                                                            Fraction(4, 10)]


def test_local_proba2(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[1].p == [Fraction(4, 10),
                                                            Fraction(1, 10),
                                                            Fraction(1, 10),
                                                            Fraction(4, 10)]


def test_local_proba3(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[2].p == [Fraction(4, 10),
                                                            Fraction(1, 10),
                                                            Fraction(1, 10),
                                                            Fraction(4, 10)]


def test_local_proba4(bayesian_polymatrix):
    assert bayesian_polymatrix.local_bayesiangames[3].p == [Fraction(4, 10),
                                                            Fraction(1, 10),
                                                            Fraction(1, 10),
                                                            Fraction(4, 10)]


def test_local_proba5(bayesian_hgg1):
    assert bayesian_hgg1.local_bayesiangames[0].p == [Fraction(6, 45),
                                                      Fraction(1, 5),
                                                      Fraction(8, 45),
                                                      Fraction(6, 45),
                                                      Fraction(6, 45),
                                                      Fraction(4, 45),
                                                      Fraction(1, 15),
                                                      Fraction(1, 15)]


def test_local_proba6(bayesian_hgg1):
    assert bayesian_hgg1.local_bayesiangames[1].p == [Fraction(1, 43),
                                                      Fraction(7, 43),
                                                      Fraction(9, 43),
                                                      Fraction(1, 43),
                                                      Fraction(7, 43),
                                                      Fraction(3, 43),
                                                      Fraction(6, 43),
                                                      Fraction(9, 43)]


def test_expected_utilities1(bayesian_polymatrix):
    assert bayesian_polymatrix.expected_utilities(
        {(0, 0): [1, 0], (0, 1): [1, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (2, 0): [1, 0], (2, 1): [1, 0], (3, 0): [1, 0], (3, 1): [1, 0]}) == {
               (0, 0): Fraction(6, 1), (0, 1): Fraction(2, 1),
               (1, 0): Fraction(6, 1), (1, 1): Fraction(2, 1),
               (2, 0): Fraction(6, 1), (2, 1): Fraction(2, 1),
               (3, 0): Fraction(6, 1), (3, 1): Fraction(2, 1)}


def test_expected_utilities2(bayesian_polymatrix):
    assert bayesian_polymatrix.expected_utilities(
        {(0, 0): [0, 1], (0, 1): [0, 1], (1, 0): [0, 1], (1, 1): [0, 1],
         (2, 0): [0, 1], (2, 1): [0, 1], (3, 0): [0, 1],
         (3, 1): [0, 1]}) == {(0, 0): Fraction(4, 1), (0, 1): Fraction(4, 1),
                              (1, 0): Fraction(4, 1), (1, 1): Fraction(4, 1),
                              (2, 0): Fraction(4, 1), (2, 1): Fraction(4, 1),
                              (3, 0): Fraction(4, 1),
                              (3, 1): Fraction(4, 1)}


def test_expected_utilities3(bayesian_hgg1):
    assert bayesian_hgg1.expected_utilities({(0, 0): [1, 0], (0, 1): [1, 0],
                                             (1, 0): [1, 0], (1, 1): [1, 0],
                                             (2, 0): [1, 0], (2, 1): [1, 0],
                                             (3, 0): [1, 0],
                                             (3, 1): [1, 0]}) == {
               (0, 0): Fraction(17447, 174), (0, 1): Fraction(8157, 80),
               (1, 0): Fraction(959, 25), (1, 1): Fraction(909, 20),
               (2, 0): Fraction(10987, 138), (2, 1): Fraction(19774, 275),
               (3, 0): Fraction(902, 23), (3, 1): Fraction(1059, 20)}


def test_is_equilibrium1(bayesian_polymatrix):
    assert bayesian_polymatrix.is_equilibrium(
        {(0, 0): [0, 1], (0, 1): [0, 1], (1, 0): [0, 1], (1, 1): [0, 1],
         (2, 0): [0, 1], (2, 1): [0, 1], (3, 0): [0, 1],
         (3, 1): [0, 1]})


def test_is_equilibrium2(bayesian_polymatrix):
    assert bayesian_polymatrix.is_equilibrium(
        {(0, 0): [1, 0], (0, 1): [1, 0], (1, 0): [1, 0], (1, 1): [1, 0],
         (2, 0): [1, 0], (2, 1): [1, 0], (3, 0): [1, 0], (3, 1): [1, 0]})


def test_is_equilibrium3(bayesian_polymatrix):
    assert bayesian_polymatrix.is_equilibrium(
        {(0, 0): [1, 0], (0, 1): [0, 1], (1, 0): [1, 0], (1, 1): [0, 1],
         (2, 0): [1, 0], (2, 1): [0, 1], (3, 0): [1, 0], (3, 1): [0, 1]})


def test_read_GameFile():
    read_bhgg = BHGG.read_GameFile("filestest/RandG_0.bhgg")
    assert read_bhgg.players_actions == [[0, 1], [0, 1], [0, 1]]
    assert read_bhgg.theta == [[0, 1], [0, 1], [0, 1]]
    assert read_bhgg.hypergraph == [[1, 2], [0, 1]]
    assert read_bhgg.p == [
        [Fraction(7, 19), Fraction(1, 19), Fraction(2, 19), Fraction(9, 19)],
        [Fraction(1, 17), Fraction(4, 17), Fraction(5, 17), Fraction(7, 17)]]
    assert read_bhgg.utilities == [[[[15, 41, 0, 7], [14, 23, 65, 100]],
                                    [[0, 41, 58, 92], [100, 51, 72, 93]],
                                    [[56, 38, 0, 14], [100, 95, 43, 0]],
                                    [[53, 69, 17, 15], [98, 12, 100, 0]]],
                                   [[[39, 12, 42, 50], [0, 78, 38, 100]],
                                    [[0, 7, 100, 58], [15, 10, 66, 78]],
                                    [[74, 100, 96, 76], [0, 29, 98, 35]],
                                    [[52, 21, 10, 100], [0, 43, 81, 56]]]]


def test_read_GameFile2(bayesian_hgg1):
    read_bhgg = BHGG.read_GameFile("filestest/CovG_0.bhgg")
    assert read_bhgg.players_actions == bayesian_hgg1.players_actions
    assert read_bhgg.theta == bayesian_hgg1.players_actions
    assert read_bhgg.hypergraph == bayesian_hgg1.hypergraph
    assert read_bhgg.p == bayesian_hgg1.p
    assert read_bhgg.utilities == bayesian_hgg1.utilities


"""
[[[[15, 41, 0, 7], [14, 23, 65, 100]],
[[[15, 41, 0, 7], [14, 23, 65, 100]]
  [[0, 41, 58, 92], [100, 51, 72, 93]],
  [[0, 41, 58, 92], [100, 51, 72, 93]]
  [[56, 38, 0, 14], [100, 95, 43, 0]],
  [[56, 38, 0, 14], [100, 95, 43, 0]]
  [[53, 69, 17, 15], [98, 12, 100, 0]]]
  [[53, 69, 17, 15], [98, 12, 100, 0]]],
 [[[39, 12, 42, 50], [0, 78, 38, 100]],
  [[0, 7, 100, 58], [15, 10, 66, 78]],
  [[74, 100, 96, 76], [0, 29, 98, 35]],
  [[52, 21, 10, 100], [0, 43, 81, 56]]]] != [,
  ,
  ,
  ,
 ,
   [[0, 7, 100, 58], [15, 10, 66, 78]],
   [[74, 100, 96, 76], [0, 29, 98, 35]],
   [[52, 21, 10, 100], [0, 43, 81, 56]]]]]


"""


def test_write_GameFile1(bayesian_polymatrix):
    bayesian_polymatrix.write_GameFile("filestest/bayesian_polymatrix.bhgg")
    read_bhgg = BHGG.read_GameFile("filestest/bayesian_polymatrix.bhgg")
    assert read_bhgg.players_actions == bayesian_polymatrix.players_actions
    assert read_bhgg.theta == bayesian_polymatrix.theta
    assert read_bhgg.p == bayesian_polymatrix.p
    assert read_bhgg.hypergraph == bayesian_polymatrix.hypergraph
    assert read_bhgg.utilities == bayesian_polymatrix.utilities


def test_write_GameFile2(bayesian_hgg1):
    bayesian_hgg1.write_GameFile("filestest/bayesian_hgg1.bhgg")
    read_bhgg = BHGG.read_GameFile("filestest/bayesian_hgg1.bhgg")
    assert read_bhgg.players_actions == bayesian_hgg1.players_actions
    assert read_bhgg.theta == bayesian_hgg1.theta
    assert read_bhgg.p == bayesian_hgg1.p
    assert read_bhgg.hypergraph == bayesian_hgg1.hypergraph
    assert read_bhgg.utilities == bayesian_hgg1.utilities


def test_convert_to_HGG(bayesian_polymatrix):
    pmg, index_old = bayesian_polymatrix.convert_to_HGG()
    assert pmg.players_actions == [[0, 1], [0, 1], [0, 1], [0, 1],
                                   [0, 1], [0, 1], [0, 1], [0, 1]]
    for couple in pmg.hypergraph:
        assert couple in [[0, 2], [0, 3], [1, 2], [1, 3], [2, 4], [2, 5],
                          [3, 4], [3, 5], [4, 6], [4, 7], [5, 6], [5, 7],
                          [0, 6], [0, 7], [1, 6], [1, 7]]
    # assert pmg.utilities ==[]
    assert pmg.utilities == [
        [[Fraction(12, 5), 0, 0, Fraction(8, 5)],
         [Fraction(12, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(3, 5), 0, 0, Fraction(2, 5)],
         [Fraction(1, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(1, 5), 0, 0, Fraction(2, 5)],
         [Fraction(3, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(4, 5), 0, 0, Fraction(8, 5)],
         [Fraction(4, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(12, 5), 0, 0, Fraction(8, 5)],
         [Fraction(12, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(3, 5), 0, 0, Fraction(2, 5)],
         [Fraction(1, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(1, 5), 0, 0, Fraction(2, 5)],
         [Fraction(3, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(4, 5), 0, 0, Fraction(8, 5)],
         [Fraction(4, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(12, 5), 0, 0, Fraction(8, 5)],
         [Fraction(12, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(3, 5), 0, 0, Fraction(2, 5)],
         [Fraction(1, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(1, 5), 0, 0, Fraction(2, 5)],
         [Fraction(3, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(4, 5), 0, 0, Fraction(8, 5)],
         [Fraction(4, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(12, 5), 0, 0, Fraction(8, 5)],
         [Fraction(12, 5), 0, 0, Fraction(8, 5)]],
        [[Fraction(3, 5), 0, 0, Fraction(2, 5)],
         [Fraction(1, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(1, 5), 0, 0, Fraction(2, 5)],
         [Fraction(3, 5), 0, 0, Fraction(2, 5)]],
        [[Fraction(4, 5), 0, 0, Fraction(8, 5)],
         [Fraction(4, 5), 0, 0, Fraction(8, 5)]]]
