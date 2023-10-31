"""
Implementation of Iterated Removal of Dominated Alternatives.

Modules' methods
----------------

- ``subutilities_player(hgg, player, action, subgame)``:
    Computes local utilities of 'player' playing 'action' in 'subgame'.

- ``local_difference(hgg, player, action1, action2, subgame)``:
    Computes the local difference table of 'action1' and 'action2' of
    'player' in 'subgame'.

- ``nondominated(hgg, player, action1, action2)``:
    Determines whether action1 of player is nondominated by action2 in hgg.

- ``find_dominated_alternatives(hgg)``:
    Returns the first dominated alternative in hgg if there is one.

- ``eliminate_alternative(hgg, j, aj)``:
    Removes alternative aj from player j in game hgg.
    Actually generates a new game...

- ``irda(hgg)``:
    Performs iterated removal of dominated alternatives for hgg.

Detailed description of methods
-------------------------------

"""
from sage.all import MixedIntegerLinearProgram, QQ, QQbar  # noqa
from gtnash.game.hypergraphicalgame import HGG
import numpy as np
# from copy import *
from copy import deepcopy


def subutilities_player(hgg, player, action, subgame):
    """
    Computes local utilities of 'player' playing 'action' in 'subgame'.

    :param HGG hgg: Input hypergraphical game.
    :param int player: Player index in hgg.
    :param int action1: Action  index of player.
    :param int subgame: Index of subgame in hgg.

    :returns: Array of utilities obtained by 'player' playing 'action' \
in 'subgame'.
    :rtype: List of lists.

    """
    player_in_subgame = hgg.hypergraph[subgame].index(player)
    utility_of_player_in_subgame = hgg.utilities[subgame][player_in_subgame]
    return [utility_of_player_in_subgame[i] for i in
            hgg.local_normalformgames[subgame].row_where_p_is_i(
                player_in_subgame, action)]


def local_difference(hgg, player, action1, action2, subgame):
    """
    Computes the local difference of utility tables between 'action1' and \
'action2' of 'player' in 'subgame'.

    :param HGG hgg: Input hypergraphical game.
    :param int player: Player index in hgg.
    :param int action1: Action 1 index of player.
    :param int action2: Action 2 index of player.
    :param int subgame: Index of subgame in hgg.

    :returns: Array of local differences in utility obtained by 'player' in \
'subgame', when player's action is either 'action1' or 'action2'.
    :rtype: Numpy array.

    """
    return np.array(
        subutilities_player(hgg, player, action1, subgame)) - np.array(
        subutilities_player(hgg, player, action2, subgame))


############################################################################
# Functions to compute a BILP to determine whether a strategy is dominated.
############################################################################

def nondominated(hgg, player, action1, action2):
    """
    Determines whether action1 of player is nondominated by action2 in hgg.

    :param HGG hgg: Input hypergraphical game.
    :param int player: Player index in hgg.
    :param int action1: Action 1 index of player.
    :param int action2: Action 2 index of player.

    :returns: ``True`` if action1 is nondominated by action2, ``False`` else.
    :rtype: bool.

    """

    hypergraph = hgg.hypergraph

    # Definition of the bilp and variables.
    bilp = MixedIntegerLinearProgram(maximization=True, solver="GLPK")  # noqa
    b = bilp.new_variable(binary=True)

    # First set of constraints:
    for e in range(len(hypergraph)):
        subgame = hypergraph[e]
        if player in subgame:
            a_e_i = hgg.joint_action_except_i(player)[e]
            # print(a_e_i)
            number_of_k = np.size(a_e_i, 0)  # Number of rows in a_e_i
            bilp.add_constraint(
                bilp.sum(b[player, e, k] for k in range(number_of_k)) == 1)

    # Second set of constraints:
    for e1 in range(len(hypergraph)):
        for e2 in range(len(hypergraph)):
            if e1 != e2:
                subgame1 = hypergraph[e1]
                subgame2 = hypergraph[e2]
                inter = [p for p in subgame1 if p in subgame2 if p != player]
                a_e1_i = hgg.joint_action_except_i(player)[e1]
                a_e2_i = hgg.joint_action_except_i(player)[e2]
                for k1 in range(np.size(a_e1_i, 0)):
                    for k2 in range(np.size(a_e2_i, 0)):
                        add_c = False
                        for p in inter:
                            s1 = [n for n in subgame1 if (n != player)]
                            s2 = [n for n in subgame2 if (n != player)]
                            j1 = s1.index(p)
                            j2 = s2.index(p)
                            if a_e1_i[k1, j1] != a_e2_i[k2, j2]:
                                add_c = True
                                break
                        if add_c:
                            bilp.add_constraint(
                                b[player, e1, k1] + b[player, e2, k2] <= 1)

    # Linear utility function:
    temp_list = []
    ld = {}
    for e in range(len(hypergraph)):
        if player in hypergraph[e]:
            ld[e] = local_difference(hgg, player, action1, action2, e)
            for k in range(len(ld[e])):
                temp_list.append((e, k))

    bilp.set_objective(sum(b[player, e, k] * QQ(ld[e][k])
                       for e, k in temp_list))
    # bilp.show()
    # print("Solution value: ",bilp.solve())
    return bilp.solve() >= 0


#################################################################
# Iterated removal of dominated alternatives
#################################################################


def find_dominated_alternatives(hgg):
    """
    Returns the first dominated alternative in hgg if there is one.

    :param HGG hgg: Input hypergraphical game.

    :returns: (j,aj), where aj is a dominated strategy for player j.
    :rtype: tuple.

    """
    i = 0
    players_actions = deepcopy(hgg.players_actions)
    n = len(players_actions)
    finished = False
    while not finished:
        if len(players_actions[i]) > 1:
            for ai in players_actions[i]:
                for aibis in players_actions[i]:
                    if aibis != ai:
                        if nondominated(hgg, i, ai, aibis):
                            pass
                        else:
                            finished = True
                            j, aj = i, ai
                            break
                if finished:
                    break
        if finished:
            return j, aj
        else:
            if i == n - 1:
                return None
            else:
                i += 1


def eliminate_alternative(hgg, j, aj):
    """
    Removes alternative aj from player j in game hgg and returns a new game....

    :param HGG hgg: Input hypergraphical game.
    :param int j: Player's index.
    :param int aj: Action's index

    :returns: hgg_out: a game obtained from hgg, where aternative aj \
of player j has been removed.
    :rtype: ``HGG``.

    """
    players_actions = deepcopy(hgg.players_actions)
    hypergraph = deepcopy(hgg.hypergraph)
    utilities = deepcopy(hgg.utilities)
    # For all subgames e where j plays, remove utility
    # element corresponding to j playing aj
    for e in range(len(hypergraph)):
        if j in hypergraph[e]:
            subgame = hgg.local_normalformgames[e]
            # Joint actions of the players in subgame e
            joint_acts = subgame.joint_actions
            # Index of player j in subgame e
            idx = hypergraph[e].index(j)
            to_remove = [il for il in range(joint_acts.shape[0]) if
                         joint_acts[il, idx] == aj]
            for r in sorted(to_remove, reverse=True):
                for i in range(len(hypergraph[e])):
                    del utilities[e][i][r]
    players_actions[j].remove(aj)
    return HGG(players_actions, utilities, hypergraph)


def irda(hgg):
    """
    Performs iterated removal of dominated alternatives for hgg.

    :param HGG hgg: Input hypergraphical game.

    :returns: hgg_out: Game obtained after iterated removal \
of dominated alternatives.
    :returns: z_out: The list of dominated alternatives.
    :rtype: ``HGG``, list.

    """
    hgg_out = deepcopy(hgg)
    z_out = []
    result = find_dominated_alternatives(hgg_out)
    if result is not None:
        z_out.append(result)
    while result is not None:
        hgg_out = eliminate_alternative(hgg_out, result[0], result[1])
        result = find_dominated_alternatives(hgg_out)
        if result is not None:
            z_out.append(result)
    return hgg_out, z_out
