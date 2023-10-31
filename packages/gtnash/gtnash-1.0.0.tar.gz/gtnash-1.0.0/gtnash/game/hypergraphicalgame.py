
from gtnash.game.abstractgame import AbstractGame
from gtnash.game.normalformgame import NFG
from itertools import combinations
from fractions import Fraction
import numpy as np
import math
import re
import shlex
from copy import deepcopy
import itertools


class HGG(AbstractGame):
    """Hypergraphical game class, attributes and methods.

    :param list of lists players_actions: Actions of every players of
        input game
    :param list of lists of lists utilities: Utilities of every players of
        input game. *utilities[g][n][a]* is the local utility of
        player *n* in local game *g* if the local joint action's index is *a*.
    :param list of lists hypergraph: List of sublist containing all the
        players' indices of all local games. *hypergraph[g]* is the list of
        players' indices involved in local game *g*.
    :param list index_to_player: Players' numbering.

    """

    def __init__(self, players_actions, utilities, hypergraph,
                 index_to_player={}):
        """Hypergraphical game constructor.
        """
        self.n_players = len(players_actions)
        self.players_actions = players_actions
        self.hypergraph = hypergraph
        self.utilities = utilities
        self.local_normalformgames = []
        for index_hyper_edge, hyper_edge in enumerate(hypergraph):
            self.local_normalformgames.append(
                self.generate_local_normalformgame(index_hyper_edge))
        if not index_to_player:
            self.index_to_player = {i: i for i in range(self.n_players)}
        else:
            self.index_to_player = index_to_player

    @classmethod
    def random(cls, nplayers, nactions, size_edges, nminedges, utilmax):
        """Random hypergraphical game generator.

        :param int nplayers: Number of players of the hypergraphical game.
        :param int nactions: Number of actions (identical for every players).
        :param int size_edges: Number of players per local game (identical
            for every local games).
        :param int nminedges: Minimum number of local games (hyperedges).
        :param int utilmax: Maximal utility (utilities are
            between 0 and utilmax).

        :returns: Hypergraphical game.
        :rtype: HGG.
        """
        players_actions = [list(range(nactions)) for n in range(nplayers)]
        all_poss_edges = list(map(list, combinations(range(nplayers),
                                                     size_edges)))
        hypergraph = []
        np.random.shuffle(all_poss_edges)
        players_left = set(range(nplayers))
        while len(players_left) > 0 or len(hypergraph) < nminedges:
            e = all_poss_edges.pop()
            hypergraph.append(list(e))
            players_left = players_left.difference(set(e))
        utilities = []
        for e in hypergraph:
            local_utility = []
            for n in e:
                local_utility.append(list(np.random.randint(0, utilmax,
                                                            nactions**len(e))))
            utilities.append(local_utility)
        shifted_utilities = deepcopy(utilities)
        for g in range(len(utilities)):
            for n in range(len(utilities[g])):
                for a in range(len(utilities[g][n])):
                    shifted_utilities[g][n][a] -= utilmax
        return HGG(players_actions, shifted_utilities, hypergraph)

    @classmethod
    def random_hyperconnect(cls, n_players, n_actions,
                            size_edges, connect, u_max):
        players_actions = [list(range(n_actions)) for n in range(n_players)]
        nb_edge = int(connect *
                      (math.factorial(n_players) /
                       (math.factorial(size_edges) *
                        math.factorial(n_players - size_edges))))
        all_poss_edges = list(map(list, combinations(range(n_players),
                                                     size_edges)))
        hypergraph = []
        np.random.shuffle(all_poss_edges)
        all_players = range(n_players)
        players_left = set(all_players)
        while players_left or len(hypergraph) < nb_edge:
            e = all_poss_edges.pop()
            hypergraph += [e]
            players_left = set(all_players).difference(
                set().union(*hypergraph))
            if len(hypergraph) == nb_edge and players_left:
                np.random.shuffle(hypergraph)
                e_remove = hypergraph.pop()
                all_poss_edges.insert(-1, e_remove)
                np.random.shuffle(all_poss_edges)
        utilities = [[list(np.random.randint(0, u_max, n_actions**len(e)))
                      for n in e]for e in hypergraph]
        return HGG(players_actions, utilities, hypergraph)

    def generate_local_normalformgame(self, index_hyper_edge):
        """Generates a local normal form game associated to the input
        hyperedge index.

        :param int index_hyper_edge: the index of the hyperedge in
            the hypergraph list.

        :returns: Normal-form game *normal_forme_game*.
        :rtype: NFG.
        """
        players_action_involved = [self.players_actions[
            self.hypergraph[index_hyper_edge][x]]
            for x in range(len(self.hypergraph[
                index_hyper_edge]))]
        normal_form_game = NFG(players_action_involved,
                               self.utilities[index_hyper_edge])
        return normal_form_game

    def joint_action_except_i(self, player_ind):
        """Generates all the possible joint pure strategies excluding
        player *player_ind*'s action.

        :param int player_ind: Index of the player whose action is excluded.

        :returns: A matrix which rows are all the pure joint strategies
            excluding player *player_ind*'s action.
        :rtype: np.matrix.
        """
        list_joint_action_except_i = []
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            if player_ind in hyper_edge:
                i = 0
                while player_ind != hyper_edge[i]:
                    i = i + 1
                player_ind_joint = i
                list_joint_action_except_i.append(
                    self.local_normalformgames[index_hyper_edge]
                        .joint_action_except_i(player_ind_joint))
            else:
                list_joint_action_except_i.append([])
        return list_joint_action_except_i

    def expected_utilities(self, mixed_joint_strat):
        """Returns the expected utilities of *mixed_joint_strategy* for all
        players.

        :param dict mixed_joint_strat: *mixed_joint_strategy[play]* is
            the mixed strategy of player *play* (a list).

        :returns: List of the expected utilities to players
            of *mixed_joint_strategy*.
        :rtype: list of floats.
        """
        somme_expected_util = [0 for i in range(self.n_players)]
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            mixed_joint_strat_involved = {i: mixed_joint_strat[n]
                                          for i, n in enumerate(hyper_edge)}
            local_normalgame = self.local_normalformgames[index_hyper_edge]
            expected_util_local = \
                local_normalgame.expected_utilities(mixed_joint_strat_involved)
            compteur = 0
            expected_util = [0 for i in range(self.n_players)]
            for play in range(self.n_players):
                if play in hyper_edge:
                    expected_util[play] = expected_util_local[compteur]
                    compteur = compteur + 1
            somme_expected_util = \
                [exputil + expected_util[n]
                 for n, exputil in enumerate(somme_expected_util)]
        return somme_expected_util

    def expected_utilities_of_n(self, n, mixed_joint_strat):
        """Returns the expected utilities of *mixed_joint_strategy* for the
        player *n*.

        :param int n: Index of the player whose utility is computed
        :param dict mixed_joint_strat: *mixed_joint_strategy[play]* is
            the mixed strategy of player *play* (a list).

        :returns: Value of the expected utility of the player n
        :rtype: float.
        """
        somme_expected_util = 0
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            mixed_joint_strat_involved = {i: mixed_joint_strat[n]
                                          for i, n in enumerate(hyper_edge)}
            local_normalgame = self.local_normalformgames[index_hyper_edge]
            # expected_util_local = \
            # local_normalgame.expected_utilities(mixed_joint_strat_involved)
            if n in hyper_edge:
                n_loc = hyper_edge.index(n)
                exp_util = local_normalgame.expected_utilities_of_n(
                    n_loc, mixed_joint_strat_involved)
            else:
                exp_util = 0
            # compteur = 0
            # exp_util = 0
            # for play in range(self.n_players):
            #     if play in hyper_edge:
            #         if n == play:
            #             exp_util = expected_util_local[compteur]
            #         compteur = compteur + 1
            somme_expected_util += exp_util
        return somme_expected_util

    def util_of_joint_action(self, n, jact):
        """ Return the utility of the player n for a given joint action

        :param int n: Index of the player whose utility is computed
        :param list jact: List of the actions played

        :return: Value of the utility of n
        :rtype: int.
        """
        somme_util = 0
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            local_normalgame = self.local_normalformgames[index_hyper_edge]
            if n in hyper_edge:
                n_in_local = hyper_edge.index(n)
                sub_jact = [jact[ne] for ne in hyper_edge]
                somme_util += local_normalgame.util_of_joint_action(
                    n_in_local, sub_jact)
        return somme_util

    def is_equilibrium(self, mixed_joint_strategy, gap=0.0001):
        """Checks whether *mixed_joint_strategy* is a Nash equilibrium.

        :param dict mixed_joint_strategy: *mixed_joint_strategy[play]* is
            the mixed strategy of player *play* (a list).
        :param float gap: maximum deviation to equilibrium allowed.

        :returns: *True* if *mixed_joint_strategy* is a mixed Nash
            equilibrium and *False* if not.
        :rtype: boolean.
        """
        expected_util_of_mixed_joint_strategy =\
            self.expected_utilities(mixed_joint_strategy)
        for play in range(self.n_players):
            for ai in range(len(self.players_actions[play])):
                other_strategy = mixed_joint_strategy.copy()
                other_strategy[play] = np.zeros(len(
                    mixed_joint_strategy[play]))
                other_strategy[play][ai] = 1
                expected_util_of_other = self.expected_utilities_of_n(
                    play, other_strategy)
                if not (expected_util_of_other <=
                        expected_util_of_mixed_joint_strategy[play] + gap):
                    return False
        return True

    def is_pure_equilibrium(self, pure_joint_strategy, gap=0.0001):
        """Checks whether *pure_joint_strategy* is a Pure Nash equilibrium.

        :param list pure_joint_strategy: List of the actions played by each
            player.
        :param float gap: maximum deviation to equilibrium allowed.

        :return: False if the joint strategy is not an equilibrium,
            True otherwise.
        :rtype: boolean.
        """
        tmp_nfg = NFG(self.players_actions, [])
        for n in range(self.n_players):
            alt_jact = tmp_nfg.all_response_of_player(n, pure_joint_strategy)
            currentutil = self.util_of_joint_action(n, pure_joint_strategy)
            for tmp_jact in alt_jact.tolist():
                if not (self.util_of_joint_action(n, tmp_jact) <=
                        currentutil + gap):
                    return False
        return True

    def get_all_PNE(self):
        """Returns every existing pure Nash equilibrium.
        Returns the empty dictionary if the game admits no pure Nash
        equilibrium

        :returns: The list of encountered Nash equilibria (if any),
            represented as dictionaries.
        :rtype: list of dict.
        """
        all_pne = []
        all_pure_strat = list(itertools.product(*self.players_actions))
        for pure_strat in all_pure_strat:
            tmp_dic_strat = {i: [1 if self.players_actions[i][s_i] == s else 0
                                 for s_i in
                                 range(len(self.players_actions[i]))]
                             for i, s in enumerate(pure_strat)}
            if self.is_pure_equilibrium(list(pure_strat)):
                all_pne += [tmp_dic_strat]
        return all_pne

    def pne_exist(self):
        """Checks whether the hypergraphical game has a pure Nash equilibrium.

        :returns: ``True`` if the hypergraphical game has a pure Nash
            equilibrium and ``False``, otherwise.
        :rtype: bool.
        """
        all_pure_strat = list(itertools.product(*self.players_actions))
        for pure_strat in all_pure_strat:
            if self.is_pure_equilibrium(list(pure_strat)):
                return True
        return False

    def first_pne(self):
        """Returns the first encountered pure Nash equilibrium.
        Returns the empty dictionary if the game admits no pure Nash
        equilibrium.

        :returns: The first encountered Nash equilibrium (if any),
            represented as a dictionary.
        :rtype: dict.
        """
        all_pure_strat = list(itertools.product(*self.players_actions))
        for pure_strat in all_pure_strat:
            tmp_dic_strat = {
                i: [1 if self.players_actions[i][s_i] == s else 0
                    for s_i in range(len(self.players_actions[i]))] for
                i, s in enumerate(pure_strat)}
            if self.is_pure_equilibrium(list(pure_strat)):
                return tmp_dic_strat
        return {}

    def util_of_player(self, player):
        """Computes the utilities of the input *player* in every games it
        participates in.

        :param int player: The index of a player of the hypergraphical game.

        :returns: A dictionary, *util*, associating the list of utilities of
            player *player* to the indices of the local
            games, *player* participates in.
        :rtype: dict.
        """
        util = {}
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            if player in hyper_edge:
                i = 0
                while player != hyper_edge[i]:
                    i = i + 1
                player_ind_joint = i
                util[index_hyper_edge] =\
                    self.local_normalformgames[
                        index_hyper_edge].utilities[player_ind_joint]
        return util

    def build_subgame(self, partial_mixed_strategy):
        """Builds a subgame of a hypergraphical game by fixing the mixed
        strategies of some arbitrary players.

        :param dict partial_mixed_strategy: *partial_mixed_strategy[n]* is
            a probability distribution over actions of player n (a list).

        :returns: Hypergraphical subgame *hgg_out*.
        :rtype: HGG.
        """
        players_actions = deepcopy(self.players_actions)
        for n in partial_mixed_strategy.keys():
            players_actions[n] = [-1]
        hypergraph = deepcopy(self.hypergraph)
        utilities = deepcopy(self.utilities)
        for e in range(len(hypergraph)):
            set_s = set(hypergraph[e]) & set(partial_mixed_strategy.keys())
            if set_s:
                localgame = self.local_normalformgames[e]
                local_partial_mixed_strategy = {}
                for s in set_s:
                    t = self.index_of_player_in_local(s)[e]
                    local_partial_mixed_strategy[t] = partial_mixed_strategy[s]
                localsubgame = localgame.build_subgame(
                    local_partial_mixed_strategy)
                utilities[e] = localsubgame.utilities
            else:
                utilities[e] = self.utilities[e]
        hgg_out = HGG(players_actions, utilities, hypergraph)
        return hgg_out

    def simplify_subgame(self):
        """Simplifies a hypergraphical game obtained using
        method *build_subgame*.
        The sub-hypergraphical game is cleaned-up, by removing the players
        which strategies are fixed.

        :returns: Hypergraphical game *hgg_simple*, where players with
            empty action set (represented by list [-1]) have been removed.
        :rtype: HGG.
        """
        players_actions = deepcopy(self.players_actions)
        utilities = deepcopy(self.utilities)
        hypergraph = deepcopy(self.hypergraph)
        for n in reversed(range(len(self.players_actions))):
            if self.players_actions[n][0] == -1:
                del players_actions[n]
                for e in reversed(range(len(hypergraph))):
                    if n in hypergraph[e]:
                        index_n_e = hypergraph[e].index(n)
                        del utilities[e][index_n_e]
                        del hypergraph[e][index_n_e]
        for e in reversed(range(len(hypergraph))):
            if not hypergraph[e]:
                del utilities[e]
                del hypergraph[e]
        hgg_simple = HGG(players_actions, utilities, hypergraph)
        return hgg_simple

    def get_subgame_fixed_strat(self, played_strat):
        """
        Computes the hypergraphical game resulting from a given hypergraphical
        game, when only subsets of the initial allowed actions
        are allowed for every players.

        :param dict played_strat: A dictionary associating a list of allowed
            actions (1 if allowed, 0 else) to every player.

        :returns: Reduced hypergraphical game.
        :rtype: HGG.
        """
        new_player_actions = [[n_act_a
                               for n_act_i, n_act_a in enumerate(n_act)
                               if played_strat[n][n_act_i] == 1]
                              for n, n_act in enumerate(self.players_actions)]
        new_util = []
        for i_e, e in enumerate(self.hypergraph):
            local_played_strat = {n_loc: played_strat[n]
                                  for n_loc, n in enumerate(e)}
            local_nfg = self.local_normalformgames[i_e].\
                get_subgame_fixed_strat(local_played_strat)
            new_util += [local_nfg.utilities]
        return HGG(new_player_actions, new_util, self.hypergraph)

    def local_game_of_player_n(self, player_ind):
        """Returns the list of local games,
         player *player_ind* participates in.

        :param int player_ind: Index of the player.

        :returns: Indices of the subgames player *player_ind* participates in.
        :rtype: list.
        """
        local_g_ind = []
        for i, hyper in enumerate(self.hypergraph):
            if player_ind in hyper:
                local_g_ind += [i]
        return local_g_ind

    def get_max_value_of_player_n(self, player_ind):
        """
        Computes the highest utility of a given player of the
        hypergraphical game.

        :param int player_ind: The index of the player

        :returns: The maximum utility of the player.
        :rtype: int.
        """
        # list_e=self.local_game_of_player_n(player_ind)
        e_to_index = self.index_of_player_in_local(player_ind)
        max_value = -math.inf
        for e_i in e_to_index.keys():
            tmp_max = max(self.utilities[e_i][e_to_index[e_i]])
            if max_value < tmp_max:
                max_value = tmp_max
        return max_value

    def index_of_player_in_local(self, player_ind):
        """
        Returns the indices of the player *player_ind* in the local games
        he participates in.

        :param int player_ind: Global index of the player in the
            hypergraphical game.

        :returns dict index_game_to_local_index_player: A dictionary
            associating the local index of player *player_ind* to
            every indices of local games the player participates in.
        :rtype: dict.
        """
        local_ind = self.local_game_of_player_n(player_ind)
        index_game_to_local_index_player = {}
        for ind in local_ind:
            index_game_to_local_index_player[ind] = \
                self.hypergraph[ind].index(player_ind)
        return index_game_to_local_index_player

    def get_subgame_level(self, proba):
        """
        Returns a hypergraphical subgame without the last player,
        fixing its mixed strategy

        :param dict proba: The mixed strategy of the "last" player.

        :returns: Resulting hypergraphical game without the "last" player.
        :rtype: HGG.
        """
        local_ind = self.local_game_of_player_n(self.n_players - 1)
        new_sub_hyper = []
        new_sub_util = []
        for i, subli in enumerate(self.hypergraph):
            if i in local_ind:
                local_prob = [proba[sub_player_ind]
                              for sub_player_ind in self.hypergraph[i]]
                local_game = self.local_normalformgames[i]
                new_g = local_game.get_subgame_level(local_prob)
                new_sub_util += [new_g.utilities]
                new_sub_hyper += [[p for p in subli if p !=
                                   self.n_players - 1]]
            else:
                new_sub_util += [self.utilities[i]]
                new_sub_hyper += [subli]
        return HGG(self.players_actions[:-1], new_sub_util, new_sub_hyper)

    def get_subgame_without_n(self, proba, player_ind):
        """
        Returns a hypergraphical subgame without the player which index is
        given as input, fixing its mixed strategy

        :param dict proba: The mixed strategy of the "removed" player.
        :param int player_ind: The index of the "removed" player.

        :returns: Resulting hypergraphical game without the "removed" player.
        :rtype: HGG.
        """
        local_ind = self.local_game_of_player_n(player_ind)
        ind_in_local = self.index_of_player_in_local(player_ind)
        old_playerindex_to_new = {}
        new_index_to_player_id = {}
        new_sub_hyper = []
        new_sub_util = []
        for p in range(self.n_players):
            if p > player_ind:
                old_playerindex_to_new[p] = p - 1
                new_index_to_player_id[p - 1] = p
            elif p != player_ind:
                old_playerindex_to_new[p] = p
                new_index_to_player_id[p] = p
        for i, subli in enumerate(self.hypergraph):
            if i in local_ind:
                local_prob = [proba[sub_player_ind]
                              for sub_player_ind in self.hypergraph[i]]
                local_game = self.local_normalformgames[i]
                new_g = local_game.get_subgame_without_n(local_prob,
                                                         ind_in_local[i])
                new_sub_util += [new_g.utilities]
                new_sub_hyper += [[old_playerindex_to_new[p]
                                   for p in subli if p != player_ind]]
            else:
                new_sub_util += [self.utilities[i]]
                new_sub_hyper += [[old_playerindex_to_new[p] for p in subli]]
        return HGG([p_act
                    for i, p_act in enumerate(self.players_actions)
                    if i != player_ind],
                   new_sub_util, new_sub_hyper, new_index_to_player_id)

    def get_player_interact(self, player_index):
        """
        Computes the list of all players in the game interacting with a given
        player.

        :param int player_index: Index of the player of interest.

        :returns: List of the players interacting with the player of
            interest (present in a common hyperedge).
        :rtype: list.
        """
        set_interact = set()
        for e in self.hypergraph:
            if player_index in e:
                tmp_e = set(e)
                tmp_e.discard(player_index)
                set_interact = set_interact.union(tmp_e)
        return list(set_interact)

    def get_player_interact_except_e(self, player_index, hyper_e):
        """
        Computes the list of all players in the game interacting with a given
        player in all hyperedges except the one given in parameter.

        :param int player_index: Index of the player of interest.
        :param int hyper_e: Index of the excluded hyperedge.

        :returns: List of the players interacting with the player of
            interest (present in a common hyperedge,
            apart from hyperedge of index *hyper_e*).
        :rtype: list.
        """
        set_interact = set()
        for e in self.hypergraph:
            if player_index in e and e != hyper_e:
                tmp_e = set(e)
                tmp_e.discard(player_index)
                set_interact = set_interact.union(tmp_e)
        return list(set_interact)

    def get_player_except_e(self, hyper_e):
        """
        Computes the list of all the players of the hypergraphical game,
        except those in the local hyperedge given as input.

        :param list hyper_e: List of players in the input hyperedge.

        :returns: List of the players not belonging to the hyperedge.
        :rtype: list.
        """
        set_interact = set([i for i in range(self.n_players)])
        set_interact = set_interact.difference(set(hyper_e))
        return list(set_interact)

    def is_GG(self):
        """Checks whether the hypergraphical game is a graphical game.

        :returns: ``True`` if the hypergraphical game is a graphical game
            and ``False``, otherwise.
        :rtype: bool.
        """
        if len(self.hypergraph) != self.n_players:
            return False
        else:
            for index_hyper_edge in range(len(self.hypergraph)):
                for index_play in range(self.local_normalformgames
                                        [index_hyper_edge].n_players):
                    if self.hypergraph[index_hyper_edge][index_play] ==\
                            index_hyper_edge:
                        if (self.local_normalformgames[index_hyper_edge].
                                utilities[index_play]).any() == 0:
                            return False
                    else:
                        if (self.local_normalformgames[index_hyper_edge].
                                utilities[index_play]).all() != 0:
                            return False
            return True

    def is_PMG(self):
        """Checks whether the hypergraphical game is a polymatrix game.

        :returns: ``True`` if the hypergraphical game is a polymatrix game
            and ``False``, otherwise.
        :rtype: bool.
        """
        for index_hyper_edge in range(len(self.hypergraph)):
            if len(self.hypergraph[index_hyper_edge]) != 2:
                return False
        return True

    def convert_to_NFG(self):
        """
        Converts the hypergraphical game to a normal form game.

        :returns: Normal form subgame.
        :rtype: NFG.
        """
        nb_actglob = 1
        tmp_util = []
        for n in range(self.n_players):
            nb_actglob *= len(self.players_actions[n])
            tmp_util += [[]]
        tmp_nfg = NFG(self.players_actions, [[0 for j in range(nb_actglob)]
                                             for n in range(self.n_players)])
        for i in range(nb_actglob):
            jact_i = list(np.array(tmp_nfg.joint_actions[i])[0])
            prob_jact_i = {}
            for n, act_n in enumerate(jact_i):
                p_n_prob = []
                for j in range(len(self.players_actions[n])):
                    if j == act_n:
                        p_n_prob += [1]
                    else:
                        p_n_prob += [0]
                prob_jact_i[n] = p_n_prob
            expc_util_i = self.expected_utilities(prob_jact_i)
            for n, val_util in enumerate(expc_util_i):
                tmp_util[n] += [int(val_util)]
                # Int a supprimer
        return NFG(self.players_actions, tmp_util)

    # should be classmethod
    @staticmethod
    def convert_to_HGG(nfgame):
        """
        Converts a normal form game to an hypergraphical game.

        :param NFG nfgame: A normal-form game.

        :returns: Hypergraphical game *hypergraphical_game*.
        :rtype: HGG.
        """
        if isinstance(nfgame, NFG):
            hypergraph = [[play for play in range(nfgame.n_players)]]
            hypergraphical_game = HGG(nfgame.players_actions,
                                      [nfgame.utilities], hypergraph)
        else:
            hypergraphical_game, index_to_old_player = nfgame.convert_to_HGG()

        return hypergraphical_game

    def game_as_int(self):
        """
        Transforms an hypergraphical game with fractional utilities
        into one where all the utilities are integer.

        :returns: Hypergraphical game with integer utilities.
        :rtype: HGG.

        .. WARNING::

            Not sure that it works when utilities are of type *float*.
            Maybe use Python's *fractions class* to convert floats into
            fractions?

        """
        util_int = []
        player_to_list_denom = {n: set() for n in range(self.n_players)}
        for e_i, e in enumerate(self.hypergraph):
            local_util = self.utilities[e_i]
            for n_i, n in enumerate(e):
                u_p = local_util[n_i]
                player_to_list_denom[n].update(
                    [f_val.denominator if isinstance(f_val, Fraction) else 1
                     for f_val in u_p])
        player_to_lcm = {n: np.lcm.reduce(list(player_to_list_denom[n]))
                         for n in range(self.n_players)}
        for e_i, e in enumerate(self.hypergraph):
            local_util = self.utilities[e_i]
            empty_local = []
            for n_i, n in enumerate(e):
                util_e_ni = np.array(local_util[n_i])
                u_p0 = (util_e_ni * player_to_lcm[n]).astype('int')
                empty_local += [list(u_p0)]
            util_int += [empty_local]
        return HGG(self.players_actions, util_int, self.hypergraph)

    @classmethod
    def read_GameFile(cls, file_path):
        """Using a .hgg game file, creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of that in
            the utilities table (Player 1 in the .nfg file is the "last" player
            in the utilites table).

        :param string file_path: Path of the .nfg file to read.
        :returns: Hypergraphical game.
        :rtype: HGG.
        """
        # Read file
        file_read = open(file_path, 'r')
        content = file_read.read()
        # List of content (3 String: NFG, string and rest)
        content_list = content.split('"', 2)
        game_info = content_list[2]
        game_info_bis = game_info.split(game_info.split('\n{')[0])[1]
        file_read.close()
        iterTest = re.finditer('{(.*?)}', game_info)
        p_actions = []
        # Get the name and actions of the players
        for i, s in enumerate(iterTest):
            if i == 1:
                p_actions = [int(str_int)
                             for str_int in shlex.split(s.group(1))]
        iterTest = re.finditer('\n{1,}{(.*?)}',
                               (game_info.split("\n{1,}")[0]).replace(',', ''))
        hypergraph = []
        for i, s in enumerate(iterTest):
            sublist_hypergraph = [int(sub_int)
                                  for sub_int in
                                  s.group(1).strip('\n').split(" ") if sub_int]
            hypergraph.append(sublist_hypergraph)
        utilities = []
        iterTest = re.finditer('}\n(.*?)\n', game_info_bis)
        # Get the string of payoff, an iterator is used
        # but there is only 1 element to iterate on
        for i, s in enumerate(iterTest):
            sublist_utilites = [int(sub_int)
                                for sub_int in
                                s.group(1).strip('\n').split(" ")
                                if sub_int]
            n_players = len(hypergraph[i])
            # Initialize the list of utility
            subsublist_utilities = [[] for i in range(n_players)]
            # According to the way the utility are written in
            # the nfg file get for each player their utility
            for j, pay in enumerate(sublist_utilites):
                subsublist_utilities[j % n_players] += [pay]
            utilities.append(subsublist_utilities)
        # Reverse the order of the players of each utility
        # and the order of the players action so that they
        # correspond to the order used in utilitiesTabl
        for index_hyper_edge in range(len(hypergraph)):
            utilities[index_hyper_edge].reverse()
        p_actions.reverse()
        # Generate list of actions like [[0,1,2][0,1][0,1,2,4]]
        # (for 3 player where one they have 3,2 and 4 actions)
        players_actions = [[j for j in range(p_actions[i])]
                           for i in range(len(p_actions))]
        old_player_to_old = {i: list(reversed(range(len(p_actions))))[i]
                             for i in range(len(p_actions))}
        new_hypergraph = [sorted([old_player_to_old[e_n] for e_n in e])
                          for e in hypergraph]
        return HGG(players_actions, utilities, new_hypergraph)

    def write_GameFile(self, file_path):
        """Using a utilities table, writes the corresponding .hgg game file.

        .. WARNING::

            Note that currently the order of players is the reverse of that in
            the utilities table (Player 1 in the .nfg file is the "last" player
            in the utilites table).

        :param string file_path: Path where the .hgg file should be written.

        """
        # Get the number of players and their number of actions
        n_players = len(self.players_actions)
        p_actions = [len(subl) for subl in self.players_actions]
        # Get all the joint actions
        jact = [self.local_normalformgames[i].joint_actions
                for i in range(len(self.hypergraph))]
        # Get hypergraph
        hyperg = self.hypergraph
        # Get the utilities as a list
        util_list = []
        payoffwrite = []
        for k in range(len(hyperg)):
            util_list.append(self.utilities[k])
            n_players_involved = len(hyperg[k])
            payoffwrite.append([util_list[k][n][i] for i in range(len(jact[k]))
                                for n in reversed(range(n_players_involved))])
        # Reverse the order of the actions
        p_actions.reverse()
        old_player_to_old = {i: list(reversed(range(n_players)))[i]
                             for i in range(n_players)}
        new_hypergraph = [sorted([old_player_to_old[e_n] for e_n in e])
                          for e in hyperg]
        # Create a string that correspond to the utility
        # of the player to write in the hgg file
        gamedescript = "nothing"
        playernames = "{"
        nb_actions = "{"
        for n_p, n_act in enumerate(p_actions):
            playernames += f' "Player {n_p}"'
            nb_actions += f" {n_act}"
            if n_p == len(p_actions) - 1:
                playernames += " }"
                nb_actions += " }"
        # Create the prolog of the file
        writeligne = f'HGG 0 R "{gamedescript}" {playernames} {nb_actions}'
        if not file_path[-4:] == ".hgg":
            file_path += ".hgg"
        # fileTestwrite = open(file_path + '.hgg',"w+")
        fileTestwrite = open(file_path, "w+")
        fileTestwrite.write(writeligne + "\n")
        # Create the rest
        for index_hyper_edge, hyper_edge in enumerate(new_hypergraph):
            str_hyper_edge = "{"
            for play in hyper_edge:
                str_hyper_edge += f' {play}'
            str_hyper_edge += ' }\n'
            fileTestwrite.write(str_hyper_edge)
            str_utilities = ""
            for uti in (payoffwrite[index_hyper_edge]):
                str_utilities += f'{int(uti)} '
            fileTestwrite.write(str_utilities + "\n")
        fileTestwrite.close()

    def __str__(self):
        """
        Given the utilities table and the hypergraph of the hypergaphical game
        """
        for j in range(len(self.hypergraph)):
            label = []
            players_id = self.hypergraph[j]
            for i in range(len(players_id)):
                label.append('Ax'.replace("x", str(players_id[i])))
            for i in range(len(players_id), 2 * (len(players_id))):
                label.append('Ux'.replace(
                    "x", str(players_id[i - len(players_id)])))
            mat_utilities = \
                np.transpose(self.local_normalformgames[j].utilities)
            mat_utilities = mat_utilities.astype(str)
            joint_actions = \
                np.copy(self.local_normalformgames[j].joint_actions)
            joint_actions = \
                self.local_normalformgames[j].joint_actions.astype(str)
            tableau_final = \
                np.concatenate(
                    (np.mat(label),
                     np.concatenate((joint_actions, mat_utilities), axis=1)),
                    axis=0)
            print('Local game ', j, ': \n', tableau_final)
        return '\n Hypergraph: \n' + str(self.hypergraph)

    def normalize_utilities(self):
        new_util = []
        player_to_list_denom = {n: set() for n in range(self.n_players)}
        for i_e, e in enumerate(self.hypergraph):
            util_e = self.utilities[i_e]
            for e_n, util_e_n in enumerate(util_e):
                player_to_list_denom[e[e_n]].update([
                    f_val.denominator if isinstance(f_val, Fraction)
                    else 1 for f_val in util_e_n])
        player_to_lcm = {n: np.lcm.reduce(list(player_to_list_denom[n]))
                         for n
                         in range(self.n_players)}
        for i_e, e in enumerate(self.hypergraph):
            util_e = np.array(deepcopy(self.utilities[i_e]))
            tmp_new_e = []
            for n_i, n in enumerate(e):
                tmp_new_e_n = list(
                    (util_e[n_i] * player_to_lcm[n]).astype('int'))
                player_to_list_denom[n].update(
                    [f_val.denominator for f_val in tmp_new_e_n if
                     isinstance(f_val, Fraction)])
                tmp_new_e += [tmp_new_e_n]
            new_util += [tmp_new_e]
        return HGG(self.players_actions, new_util, self.hypergraph)
        # u_p0 = (util_e[0] * player_to_lcm[e[0]]).astype('int')
        # self.maxu_of_p[e[0]] = max(self.maxu_of_p[e[0]], max(u_p0))
        # player_to_list_denom[e[0]].update(
        #     [f_val.denominator for f_val in u_p0 if
        #      isinstance(f_val, Fraction)])

        # u_p1 = (util_e[1] * player_to_lcm[e[1]]).astype('int')
        # self.maxu_of_p[e[1]] = max(self.maxu_of_p[e[1]], max(u_p1))
        # player_to_list_denom[e[1]].update(
        #     [f_val.denominator if isinstance(f_val, Fraction)
        #      else 1 for f_val in u_p1])
        # # nb_p0 = len(game.players_actions[e[0]])

        # nb_p1 = len(game.players_actions[e[1]])
        # new_util_p0 = []
        # new_util_p1 = [[] for i in range(nb_p1)]
        # tmp_u = []
        # for u_p_index, u_p_val in enumerate(u_p0):
        #     tmp_u += [u_p_val]
        #     if len(tmp_u) == nb_p1:
        #         new_util_p0 += [tmp_u]
        #         tmp_u = []
        # for u_p_index, u_p_val in enumerate(u_p1):
        #     new_util_p1[u_p_index % nb_p1] += [u_p_val]
        # self.all_utilities[e[0]][e[1]] = new_util_p0
        # self.all_utilities[e[1]][e[0]] = new_util_p1
