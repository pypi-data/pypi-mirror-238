from gtnash.game.abstractgame import AbstractGame
from gtnash.game.bayesiangame import BG
from gtnash.game.hypergraphicalgame import HGG
from gtnash.game.polymatrixgame import PMG
from fractions import Fraction
from copy import deepcopy
import numpy as np
import math
import re
import shlex
from itertools import combinations


class BHGG(AbstractGame):
    """Bayesian hypergraphical games class, attributes and methods.

    :param list of sublists players_actions:  \
    List of sublists containing all the strategies of every players.
    :param list of sublists utilities: \
    List of sublists containing the utilities of players.
    :param list hypergraph: \
    List of sublists containing all the players' indices of every local games.
    :param list of sublists theta: \
    List of sublists containing the set of types of every players.
    :param list of sublists p: List (for every local games) of sublists of \
    probabilities of joint types of the local games. \
    The probabilities may be unnormalized (integers), \
    in which case they will be normalized as fractions at instanciation.
    :param dict index_to_player: A dictionary of identifiers of players.

    """

    def __init__(self, players_actions, utilities, hypergraph,
                 theta, p, index_to_player={}):
        """Hypergraphical bayesian game constructor"""
        self.n_players = len(players_actions)
        self.players_actions = players_actions
        self.hypergraph = hypergraph
        self.utilities = utilities
        self.theta = theta
        self.p_unorm = p
        self.p = [[Fraction(p_t, sum(sub_p_unorm))
                   for p_t in sub_p_unorm]for sub_p_unorm in p]
        self.local_bayesiangames = []
        for i_e, e in enumerate(hypergraph):
            self.local_bayesiangames += [self.generate_local_bayesiangame(i_e)]
        if not index_to_player:
            self.index_to_player = {i: i for i in range(self.n_players)}
        else:
            self.index_to_player = index_to_player

    def generate_local_bayesiangame(self, index_game):
        """Returns the local bayesian game which index is *index_game*.

        :param int index_game: Index of the local bayesian game.

        :returns: *bayesian_local_game*, the corresponding bayesian local game.
        :rtype: BG
        """
        player_action_local = [self.players_actions[
            self.hypergraph[index_game][n]]
            for n in
            range(len(self.hypergraph[index_game]))]
        player_theta_local = [self.theta[self.hypergraph[index_game][n]]
                              for n in range(len(self.hypergraph[index_game]))]
        player_p_local = self.p[index_game]
        bayesian_local_game = BG(
            player_action_local,
            self.utilities[index_game],
            player_theta_local,
            player_p_local)
        return bayesian_local_game

    def expected_utilities(self, bayes_mixed_joint_strat):
        """Computes the expected utilities of every pair (player,type), \
        for a given joint mixed bayesian strategy.

        :param dict bayes_mixed_joint_strat: \
        *bayes_mixed_joint_strat[(n, t_n)]* \
        is a probability distribution (list) over player *n*'s strategies.

        :returns: *expected_util*, where *expected_util[(n,t_n)]* \
        is the utility for player *n* of type *t_n* \
        of the bayesian joint mixed strategy *bayes_mixed_joint_strat*.
        :rtype: dict.
        """
        expect_util = {}
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            local_bayesiangame = self.local_bayesiangames[index_hyper_edge]
            local_mixed_strat = {}
            local_couple_to_global = {}
            for n_local, n in enumerate(hyper_edge):
                for t_n in local_bayesiangame.theta[n_local]:
                    local_couple_to_global[(n_local, t_n)] = (n, t_n)
                    local_mixed_strat[(n_local, t_n)
                                      ] = bayes_mixed_joint_strat[(n, t_n)]
            expected_util_local = local_bayesiangame.expected_utilities(
                local_mixed_strat)
            for (n_local, t_n) in local_couple_to_global.keys():
                (n_global, t_n) = local_couple_to_global[(n_local, t_n)]
                if (n_global, t_n) in expect_util:
                    expect_util[(n_global, t_n)
                                ] += expected_util_local[(n_local, t_n)]
                else:
                    expect_util[(n_global, t_n)
                                ] = expected_util_local[(n_local, t_n)]
        return expect_util

    def expected_utilities_of_n_t(self, current_n, current_t,
                                  bayes_mixed_joint_strat):
        expect_util = 0
        for index_hyper_edge, hyper_edge in enumerate(self.hypergraph):
            local_mixed_strat = {}
            local_couple_to_global = {}
            if np in hyper_edge:
                loc_bg = self.local_bayesiangames[index_hyper_edge]
                local_mixed_strat = {}
                for n_local, n in enumerate(hyper_edge):
                    for t_n in loc_bg.theta[n_local]:
                        if n == current_n and t_n == current_t:
                            (curr_n_loc, curr_t_loc) = (n, t_n)
                        local_couple_to_global[(n_local, t_n)] = (n, t_n)
                        local_mixed_strat[(n_local, t_n)] = \
                            bayes_mixed_joint_strat[(n, t_n)]
                expected_util_local_of_n_t = \
                    loc_bg.expected_utilities_of_n_t(curr_n_loc, curr_t_loc,
                                                     local_mixed_strat)
                expect_util += expected_util_local_of_n_t
        return expect_util

    def __str__(self):
        for j in range(len(self.hypergraph)):
            print(f"Local Game {j}: {self.hypergraph[j]}")
            for t in range(len(self.utilities[j])):
                label = []
                players_id = self.hypergraph[j]
                for i in range(len(players_id)):
                    label.append(
                        'Ax'.replace(
                            "x", str(
                                players_id[i])))  # 'A _i'
                for i in range(len(players_id), 2 * (len(players_id))):
                    label.append('Ux'.replace(
                        "x", str(players_id[i - len(players_id)])))
                mat_utilities = np.transpose(
                    self.local_bayesiangames[j].utilities[t])
                mat_utilities = mat_utilities.astype(str)
                joint_actions = np.copy(
                    self.local_bayesiangames[j].joint_actions)
                joint_actions = \
                    self.local_bayesiangames[j].joint_actions.astype(str)
                tableau_final = np.concatenate(
                    (np.mat(label), np.concatenate(
                        (joint_actions, mat_utilities), axis=1)), axis=0)
                print('Theta', t, '=',
                      self.local_bayesiangames[j].joint_theta[t],
                      'and P(Theta', j, ') =', self.p[j][t], '\n',
                      tableau_final, '\n')
        return '\n Hypergraph: \n' + \
            str(self.hypergraph) + '\n Type: \n' + str(self.theta)

    def is_equilibrium(self, bayes_mixed_join_strat, gap=0.0001):
        """Checks whether *bayes_mixed_join_strat* \
        is a Nash equilibrium of the bayesian game.

        :param dict bayes_mixed_join_strat: *bayes_mixed_join_strat[(n,t_n)]* \
        is the mixed strategy of player *n* of type *t_n* (a list).
        :param float gap: maximum deviation to equilibrium allowed.

        :returns: ``True`` if *bayes_mixed_joint_strategy* is a \
        bayesian mixed Nash equilibrium and ``False`` if not.
        :rtype: boolean.
        """
        expected_util_of_bayes_joint_strategy = self.expected_utilities(
            bayes_mixed_join_strat)
        for n in range(self.n_players):
            for t_n in range(len(self.theta[n])):
                for a_n in range(len(self.players_actions[n])):
                    other_strategy = bayes_mixed_join_strat.copy()
                    other_strategy[(n, t_n)] = np.zeros(
                        len(self.players_actions[n]))
                    other_strategy[(n, t_n)][a_n] = 1
                    expected_util_of_other = \
                        self.expected_utilities_of_n_t(n, t_n, other_strategy)
                    if expected_util_of_other \
                            > expected_util_of_bayes_joint_strategy[(n, t_n)] \
                            + gap:
                        return False
        return True

    def local_game_of_player_n(self, player_ind):
        """Returns the list of local games player *player_ind* participates in.

        :param int player_ind: Index of the player.

        :returns: Indices of the subgames player *player_ind* participates in.
        :rtype: list.
        """

        local_g_ind = []
        for i, hyper in enumerate(self.hypergraph):
            if player_ind in hyper:
                local_g_ind += [i]
        return local_g_ind

    def convert_to_HGG(self):
        """Converts a bayesian hypergraphical game to an hypergraphical game.

        :param BHGG self: A bayesian hypergraphical game.

        :returns: Hypergraphical game or polymatrix game.
        :rtype: HGG or PMG.
        """

        index_to_old_player = {}
        player_to_new_index = {}
        new_players_actions = []
        for n, n_act in enumerate(self.players_actions):
            for n_type in range(len(self.theta[n])):
                index_to_old_player[len(new_players_actions)] = (n, n_type)
                player_to_new_index[(n, n_type)] = len(new_players_actions)
                new_players_actions += [deepcopy(n_act)]
        util = []
        new_hypergraphe = []
        for index_bg, bg in enumerate(self.local_bayesiangames):
            bg_hyper = self.hypergraph[index_bg]
            tmp_hgg, local_index_to_player = bg.convert_to_HGG()
            local_hyper = []
            for index_e, e in enumerate(tmp_hgg.hypergraph):
                new_e = []
                new_util = tmp_hgg.local_normalformgames[index_e].utilities
                for e_n in e:
                    (n_local, t_local) = local_index_to_player[e_n]
                    new_n_index = player_to_new_index[(
                        bg_hyper[n_local], t_local)]
                    new_e += [new_n_index]
                local_hyper += [new_e]
                util += [new_util]
            new_hypergraphe += local_hyper
        if max([len(e) for e in self.hypergraph]) == 2:
            return PMG(new_players_actions, util,
                       new_hypergraphe), index_to_old_player
        return HGG(new_players_actions, util,
                   new_hypergraphe), index_to_old_player

    def convert_to_NFG(self):
        """
        Converts the bayesian hypergraphical game to a normal form game.

        :returns: Normal form subgame.
        :rtype: NFG.
        """
        hgg, index_old = self.convert_to_HGG()
        return hgg.convert_to_NFG()

    @classmethod
    def random_bayesian_hyper(cls, n_players, n_actions, n_type,
                              size_edges, connect, u_max):
        """ Random bayesian hypergraphical game generation.

        :param int n_players: Number of players of the BHGG.
        :param int n_actions: Number of actions (identical for every players).
        :param int n_type: Number of types (identical for every players).
        :param int size_edges: Number of players per local game \
        (identical for every local games).
        :param float connect: hypergraph connectivity.
        :param int u_max: Maximal utility (utilities
            are between 0 and utilmax).

        :returns: Hypergraphical game.
        :rtype: BHGG.
        """
        # players_actions = [list(range(n_actions)) for n in range(n_players)]
        # players_theta = [list(range(n_type)) for n in range(n_players)]
        nb_edge = int(connect *
                      (math.factorial(n_players) /
                       (math.factorial(size_edges) *
                        math.factorial(n_players -
                                       size_edges))))
        all_poss_edges = list(
            map(list, combinations(range(n_players), size_edges)))
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
        # Create joint proba on joint type
        # Compute local joint probabilities

    @classmethod
    def read_GameFile(cls, file_path):
        """Using a .bhgg game file, creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of that \
            in the utilities table (Player 1 in the .bhgg file is \
            the "last" player in the utilites table).

        :param string file_path: Path of the .bhgg file to read.

        :returns: A bayesian hypergraphical game.
        :rtype: BHGG.
        """

        file_read = open(file_path, 'r')
        content = file_read.read()
        content_list = content.split('"', 2)
        if content_list[0] != 'BHGG 0 R ':
            print('Ce fichier n est pas reconnu')
        else:
            game_info = content_list[2]
            game_info_bis = (
                game_info.split(
                    game_info.split('\n{')[0])[1]).split('\n\n')
            list_util_e = [txt_e_util.split('}\n')[-1]
                           for txt_e_util in game_info_bis]
            file_read.close()
            iterTest = re.finditer('{(.*?)}', game_info)
            p_actions = []
            p_theta = []
            e_hyper = []
            p_unorm = []
            for i, s in enumerate(iterTest):
                if i == 1:
                    p_actions = [int(str_int)
                                 for str_int in shlex.split(s.group(1))]
                elif i == 2:
                    p_theta = [int(str_int)
                               for str_int in shlex.split(s.group(1))]
                elif (i >= 3 and not i % 2 == 0):
                    e_hyper += [[int(str_int)
                                 for str_int in shlex.split(s.group(1))]]
                elif i >= 3:
                    p_unorm += [[int(str_int)
                                 for str_int in shlex.split(s.group(1))]]
            util_glob = []
            p_unorm_glob = []
            for e_i, e in enumerate(e_hyper):
                n_player_loc = len(e)
                # p_actions_loc = [p_a for p_ai,
                #                  p_a in enumerate(p_actions) if p_ai in e]
                # n_actions_loc = np.prod(p_actions_loc)
                p_theta_loc = [p_t for p_ti,
                               p_t in enumerate(p_theta) if p_ti in e]
                n_theta_loc = np.prod(p_theta_loc)
                util_local = [
                    [[] for nt_np in range(n_player_loc)]
                    for nt in range(n_theta_loc)]
                tmpg_game_info = list_util_e[e_i].split('\n')
                payoff_value = [[int(v_u) for v_u in st_util.split(
                    " ")[:-1] if v_u] for st_util in tmpg_game_info]
                for tu_i, tu in enumerate(payoff_value):
                    for i, pay in enumerate(tu):
                        util_local[tu_i][i % n_player_loc] += [pay]
                for i in range(n_theta_loc):
                    util_local[i].reverse()
                dico_p = {}
                theta_loc = [[j for j in range(p_theta_loc[i])]
                             for i in range(len(p_theta_loc))]
                tmp_bg = BG([], [], [], [])
                joint_theta_mat = tmp_bg.generate_joint_matrix(theta_loc)
                joint_theta = []
                for i in range(n_player_loc):
                    sub_joint_theta = [joint_theta_mat[j, i]
                                       for j in
                                       range(joint_theta_mat.shape[0])]
                    joint_theta.append(sub_joint_theta)
                for i in range(n_theta_loc):
                    dico_p[tuple(joint_theta[j][i]
                                 for j in range(n_player_loc))] \
                        = p_unorm[e_i][i]
                joint_theta.reverse()
                tmp_p = [dico_p[tuple(reversed(np.array(joint_theta)[:, i]))]
                         for i in range(n_theta_loc)]
                p_unorm_glob += [tmp_p]
                util_glob += [util_local]
        p_actions.reverse()
        p_theta.reverse()
        players_actions = [
            [j for j in range(p_actions[i])] for i in range(len(p_actions))]
        players_theta = [[j for j in range(p_theta[i])]
                         for i in range(len(p_theta))]
        old_player_to_old = {i: list(reversed(range(len(p_actions))))[i]
                             for i in range(len(p_actions))}
        new_hypergraph = [sorted([old_player_to_old[e_n]
                                 for e_n in e]) for e in e_hyper]
        test_bhgg = BHGG(players_actions, util_glob, new_hypergraph,
                         players_theta, p_unorm_glob)
        return test_bhgg

    def write_GameFile(self, file_path):
        """Writes .bhgg game file corresponding to a bayesian hypergrap. game.

        .. WARNING::

            Note that currently the order of players is the reverse of
            that in the utilities table (Player 1 in the .nfg file is
            the "last" player in the utilites table).

        :param string file_path: Path where the .bhgg file should be written.

        """
        p_actions = [len(subl) for subl in self.players_actions]
        jact = [self.local_bayesiangames[i].joint_actions for i in range(
            len(self.hypergraph))]
        theta = [len(subl) for subl in self.theta]
        current_p = self.p_unorm
        # Get hypergraph
        hyperg = self.hypergraph
        # Get the utilities as a list
        util_list = []
        payoffwrite = []
        for k in range(len(hyperg)):
            util_list.append(self.utilities[k])
            util_list_k = []
            n_players_involved = len(hyperg[k])
            for k_t in range(len(self.utilities[k])):
                util_list_k.append(self.utilities[k][k_t])
            payoffwrite.append([[util_list[k][k_t][n][i]
                                 for i in range(len(jact[k]))
                                 for n in reversed(range(n_players_involved))]
                                for k_t in range(len(self.utilities[k]))])
        p_actions.reverse()
        theta.reverse()
        old_player_to_old = {
            i: list(
                reversed(
                    range(
                        self.n_players)))[i] for i in range(
                self.n_players)}
        new_hypergraph = [sorted([old_player_to_old[e_n]
                                 for e_n in e]) for e in hyperg]
        gamedescript = "nothing"
        playernames = "{"
        nb_actions = "{"
        typ = "{"
        for n_p, n_act in enumerate(p_actions):
            playernames += f' "Player {n_p}"'
            nb_actions += f" {n_act}"
            typ += f" {theta[n_p]}"
            if n_p == len(p_actions) - 1:
                playernames += " }"
                nb_actions += " }"
                typ += " }"
        all_local_p = []
        for e_i, e in enumerate(self.local_bayesiangames):
            dico_p = {}
            joint_theta = []
            for i in range(e.n_players):
                sub_joint_theta = [e.joint_theta[j, i]
                                   for j in range(e.n_theta)]
                joint_theta.append(sub_joint_theta)
            for i in range(e.n_theta):
                dico_p[tuple(joint_theta[j][i]
                             for j in range(e.n_players))] = current_p[e_i][i]
            joint_theta.reverse()
            tmp_p = [dico_p[tuple(reversed(np.array(joint_theta)[:, i]))]
                     for i in range(e.n_theta)]
            proba = "{"
            for i in range(len(tmp_p)):
                proba += f" {tmp_p[i]}"
            proba += " }"
            all_local_p += [proba]
        writeligne = \
            f'BHGG 0 R "{gamedescript}" {playernames} {nb_actions} {typ}'
        if not file_path[-5:] == ".bhgg":
            file_path += ".bhgg"
        fileTestwrite = open(file_path, "w+")
        fileTestwrite.write(writeligne + "\n")
        for index_hyper_edge, hyper_edge in enumerate(new_hypergraph):
            str_hyper_edge = "{"
            for play in hyper_edge:
                str_hyper_edge += f' {play}'
            str_hyper_edge += ' }\n'
            fileTestwrite.write(str_hyper_edge)
            fileTestwrite.write(all_local_p[index_hyper_edge] + "\n")
            str_utilities = ""
            for uti in (payoffwrite[index_hyper_edge]):
                for uti_t in uti:
                    str_utilities += f'{int(uti_t)} '
                str_utilities += "\n"
            fileTestwrite.write(str_utilities + "\n")
        fileTestwrite.close()
