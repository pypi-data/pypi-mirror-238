from gtnash.game.abstractgame import AbstractGame
from gtnash.game.normalformgame import NFG
from gtnash.game.hypergraphicalgame import HGG
from gtnash.game.polymatrixgame import PMG
from fractions import Fraction
from copy import deepcopy
import numpy as np
import re
import shlex
import itertools


class BG(AbstractGame):
    """Bayesian games class, attributes and methods.

    :param list of lists players_actions: Actions of every players.
    :param list of lists utilities: \
    List of utilities of each player for every possible joint types.
    :param list of list theta: *theta[n]* is the list of types of player *n*.
    :param list p_unorm: List of *unnormalized* probabilities \
    (integers, for example) of joint types.

    """

    def __init__(self, players_actions, utilities, theta, p_unorm):
        # super().__init__(players_actions, utilities, theta, p)
        self.n_players = len(players_actions)
        self.players_actions = players_actions
        self.utilities = utilities
        self.theta = theta
        self.p_unormalized = p_unorm
        p_unorm_sum = sum(p_unorm)
        self.p = [Fraction(p_t, p_unorm_sum) for p_t in p_unorm]
        if theta == []:
            self.n_theta = 0
        else:
            self.n_theta = 1  # len(theta[0])*len(theta[1])
            for i in range(self.n_players):
                self.n_theta = self.n_theta * len(theta[i])
        hypergraph_temp = [[j for j in range(self.n_players)]
                           for i in range(self.n_theta)]
        self.joint_theta = self.generate_joint_matrix(theta)
        self.local_normalformgames = []
        for index_hyper_edge in range(self.n_theta):
            self.local_normalformgames.append(
                self.generate_local_normalformgame(
                    hypergraph_temp,
                    index_hyper_edge))
        self.joint_actions = self.generate_joint_matrix(players_actions)

    def generate_joint_matrix(self, into_mat):
        """Returns a matrix which rows are \
        all the possible (types,strategies) combinations of every players.

        :param list of lists into_mat: \
        each sublist is either the set of types or \
        the set of strategies of a player.

        :returns: Matrix of joint (types/strategies).
        :rtype: mat.
        """
        matA = np.mat([])
        for p_a in reversed(into_mat):
            p_i = np.mat(p_a)
            p_i = p_i.transpose()
            if matA.size == 0:
                matA = p_i
            else:
                one_vec = np.ones((matA.shape[0], 1))
                mat = np.concatenate((int(p_i[0]) * one_vec, matA), axis=1)
                for action_i in p_i[1:]:
                    mati = np.concatenate((int(action_i) * one_vec, matA),
                                          axis=1)
                    mat = np.concatenate((mat, mati), axis=0)
                matA = mat
        return matA.astype(int)

    def generate_local_normalformgame(self, hypergraph_temp, index_hyper_edge):
        """Returns a normal form game corresponding to a joint type/nfg.

        .. WARNING::

            Is this function used? \
            Is it the correct class? \
            If so, variables names are obscure (hypergraphical??).

        """
        if len(self.players_actions) == 0:
            return NFG([], [])
        else:
            players_action_involved = \
                [self.players_actions[hypergraph_temp[index_hyper_edge][x]]
                 for x in range(len(hypergraph_temp[index_hyper_edge]))]
            normal_forme_game = \
                NFG(players_action_involved,
                    np.array(self.utilities[index_hyper_edge]))
            return normal_forme_game

    def proba_type(self):
        """Returns the probabilities of all joint types

        :returns: The dictionary *dico*
            of probabilities of every joint types of a bayesian game. \
            *dico[i]* is the probability of the joint type indexed by *i*.
        :rtype: dict.
        """
        dico = {}
        for i, t_e in enumerate(self.joint_theta):
            # for n,t_e_n in enumerate(t_e):
            dico[i] = self.p[i]
        return dico

    def get_index_of_type(self, type_theta):
        """Returns the index of a given joint type in a bayesian game.

        :param np.array joint type: An arbitrary joint type.

        :returns: The index of the joint type.
        :rtype: int.
        """
        return np.where(np.all(type_theta
                               == np.array(self.joint_theta), axis=1))[0][0]
        # return np.where(np.array(type_theta)==np.array(self.joint_theta))

    # np.where(action_value ==
    #           np.array(self.joint_actions[:, player_id]).flatten())[0]

    def conditional_probabilities(self, known_player, type_known_player):
        """Returns the conditionnal probabilities of other players' types, \
        given that player *known_player* is of type *type_known_player*.

        :param int known_player: Index of the player.
        :param int type_known_player: Type index of the player.

        :returns: *prob_cond*, the conditional probabilities \
        of every joint types (given that \
        *type[known_player]=type_known_player*).
        :rtype: dict.
        """
        dico_p = self.proba_type()
        prob_cond = {}
        prob_type = 0
        # tmp_theta=[t_e for n,t_e in enumerate(self.theta)
        # if n!=known_player ]
        tmp_theta_alt = [t_e for t_e in np.array(self.joint_theta)
                         if t_e[known_player] == type_known_player]
        for t_e in tmp_theta_alt:
            prob_type += dico_p[self.get_index_of_type(t_e)]
        for t_e in tmp_theta_alt:
            tmp_index = self.get_index_of_type(t_e)
            prob_cond[tmp_index] = dico_p[tmp_index] / prob_type
        return prob_cond

    def dico_utilities(self):
        """Returns the dictionary that associate to each joint type index, \
        the appropriate utilities

        :returns: *dico*, \
        a dictionary representing the utilities tables \
        associated to every joint types indices.
        :rtype: dict.
        """
        dico = {}
        for t_e in np.array(self.joint_theta):
            tmp_ind = self.get_index_of_type(t_e)
            dico[tmp_ind] = self.utilities[tmp_ind]
        return dico

    def expected_utilities(self, bayes_mixed_joint_strat):
        """Computes the expected utilities of every pair (player,type), \
        for a given joint mixed bayesian strategy.

        :param dict bayes_mixed_joint_strat: \
        *bayes_mixed_joint_strat[(n, t_n)]* \
        is a probability distribution (list) over player *n*'s startegies.

        :returns: *expected_util*, where *expected_util[(n,t_n)]* \
        is the utility for player *n* of type *t_n* of \
        the bayesian joint mixed strategy *bayes_mixed_joint_strat*.
        :rtype: dict.
        """
        expected_util = {}
        dico_of_games = self.dico_utilities()
        for n in range(self.n_players):
            for t_n in self.theta[n]:
                dico_cond = self.conditional_probabilities(n, t_n)
                # t_n_mixed = bayes_mixed_joint_strat[(n, t_n)]
                somme_util_type_n = 0
                for tmp_type in [t_e for t_e in np.array(self.joint_theta)
                                 if t_e[n] == t_n]:
                    somme_util_type_joint = 0
                    proba_cond_type = \
                        dico_cond[self.get_index_of_type(tmp_type)]
                    current_game = \
                        dico_of_games[self.get_index_of_type(tmp_type)]
                    current_strat = \
                        [bayes_mixed_joint_strat[(n_p, tmp_type[n_p])]
                         for n_p in range(self.n_players)]
                    for i_ja, ja in enumerate(np.array(self.joint_actions)):
                        current_proba = 1
                        for n_a, ja_a in enumerate(list(ja)):
                            current_proba *= current_strat[n_a][ja_a]
                        somme_util_type_joint += \
                            current_game[n][i_ja] * current_proba
                    somme_util_type_joint *= proba_cond_type
                    somme_util_type_n += somme_util_type_joint
                expected_util[(n, t_n)] = somme_util_type_n
        return expected_util

    def expected_utilities_of_n_t(self, n, t_n, bayes_mixed_joint_strat):
        dico_of_games = self.dico_utilities()
        dico_cond = self.conditional_probabilities(n, t_n)
        # t_n_mixed = bayes_mixed_joint_strat[(n, t_n)]
        somme_util_type_n = 0
        for tmp_type in [t_e for t_e in np.array(self.joint_theta)
                         if t_e[n] == t_n]:
            somme_util_type_joint = 0
            proba_cond_type = \
                dico_cond[self.get_index_of_type(tmp_type)]
            current_game = \
                dico_of_games[self.get_index_of_type(tmp_type)]
            current_strat = \
                [bayes_mixed_joint_strat[(n_p, tmp_type[n_p])]
                 for n_p in range(self.n_players)]
            for i_ja, ja in enumerate(np.array(self.joint_actions)):
                current_proba = 1
                for n_a, ja_a in enumerate(list(ja)):
                    current_proba *= current_strat[n_a][ja_a]
                somme_util_type_joint += \
                    current_game[n][i_ja] * current_proba
            somme_util_type_joint *= proba_cond_type
            somme_util_type_n += somme_util_type_joint
        return somme_util_type_n

    def is_equilibrium(self, bayes_mixed_joint_strat, gap=0.0001):
        """Checks whether *bayes_mixed_joint_strategy* \
        is a Nash equilibrium of the bayesian game.

        :param dict bayes_mixed_joint_strategy: \
        *bayes_mixed_joint_strategy[(n,t_n)]* \
        is the mixed strategy of player *n* of type *t_n* (a list).
        :param float gap: maximum deviation to equilibrium allowed.

        :returns: ``True`` if *bayes_mixed_joint_strategy* \
        is a bayesian mixed Nash equilibrium and ``False`` if not.
        :rtype: boolean.
        """
        current_exp_util = self.expected_utilities(bayes_mixed_joint_strat)
        for n in range(self.n_players):
            for type_n in range(len(self.theta[n])):
                for a_i in range(len(self.players_actions[n])):
                    other_strategy = bayes_mixed_joint_strat.copy()
                    other_strategy[(n, type_n)] = \
                        np.zeros(len(self.players_actions[n]))
                    other_strategy[(n, type_n)][a_i] = 1
                    expected_util_of_other = \
                        self.expected_utilities_of_n_t(n, type_n,
                                                       other_strategy)
                    if expected_util_of_other \
                            > current_exp_util[(n, type_n)] + gap:
                        return False
        return True

    def convert_to_HGG(self):
        """Converts a bayesian game to an hypergraphical game.

        :param BG self: A bayesian game.

        :returns: Hypergraphical game or polymatrix game.
        :rtype: HGG or PMG.
        """
        index_to_old_player = {}
        player_to_new_index = {}
        new_players_actions = []
        cond_proba = []
        for n, n_act in enumerate(self.players_actions):
            for n_type in range(len(self.theta[n])):
                index_to_old_player[len(new_players_actions)] = (n, n_type)
                player_to_new_index[(n, n_type)] = len(new_players_actions)
                cond_proba += [self.conditional_probabilities(n, n_type)]
                new_players_actions += [deepcopy(n_act)]
        # new_players_actions=[n_act for n,n_act in
        # enumerate(self.players_actions)
        # for p_type in range(len(self.theta[n])) ]
        dico_util = self.dico_utilities()
        hypergraph = []
        util = []
        for t_joint in np.array(self.joint_theta):
            tmp_current_util = dico_util[self.get_index_of_type(list(t_joint))]
            local_player = []
            local_game = []
            for n, n_type in enumerate(t_joint):
                local_player += [player_to_new_index[(n, n_type)]]
                current_prob = cond_proba[player_to_new_index[(n, n_type)]][
                    self.get_index_of_type(list(t_joint))]
                local_game += [[current_prob * u for u in tmp_current_util[n]]]
            hypergraph += [local_player]
            util += [local_game]
        if self.n_players == 2:
            return PMG(new_players_actions, util, hypergraph), \
                index_to_old_player
        return HGG(new_players_actions, util, hypergraph), index_to_old_player

    @classmethod
    def random_game(cls, n_players, n_actions, n_type, u_max):
        """ Random bayesian game generation.

        .. WARNING::

            There are two bayesian games generator. Which is correct?

        """
        players_actions = [list(range(n_actions)) for n in range(n_players)]
        players_theta = [list(range(n_type)) for n in range(n_players)]
        util = []
        prob_p = []
        n_type_joint = len([i for i in itertools.product(*players_theta)])
        for t_e in range(n_type_joint):
            tmp_t_e1 = []
            for n in range(n_players):
                tmp_t_e1 += [list(np.random.randint(0, u_max, n_actions ** 2))]
            util += [tmp_t_e1]
            prob_p += [Fraction(1, n_type_joint)]

        return BG(players_actions, util, players_theta, prob_p)

    @classmethod
    def random_bayesian(cls, n_player, n_action, n_type, u_max):
        """ Random bayesian game generation.

        .. WARNING::

            There are two bayesian games generator. Which is correct?

        """
        player_actions = []
        player_thetas = []
        nb_theta = n_type ** n_player
        nb_actions = n_action ** n_player
        theta_p = np.random.dirichlet([1 for i in range(nb_theta)])
        util = [[list(np.random.randint(0, u_max, nb_actions))
                 for n in range(n_player)] for j_type in range(nb_theta)]
        for n in range(n_player):
            player_actions += [[n_a for n_a in range(n_action)]]
            player_thetas += [[n_t for n_t in range(n_type)]]
        return BG(player_actions, util, player_thetas, theta_p)

    @classmethod
    def read_GameFile(cls, file_path):
        """Using a .bg game file, creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of
            that in the utilities table (Player 1 in the .bg file
            is the "last" player in the utilites table).

        :param string file_path: Path of the .bg file to read.

        :returns: utilities table.
        :rtype: list of lists of lists of integers.
        """

        file_read = open(file_path, 'r')
        content = file_read.read()
        content_list = content.split('"', 2)
        if content_list[0] != 'BG 0 R ':
            print('Ce fichier n est pas reconnu')
            util_table = None
        else:
            game_info = content_list[2]
            game_info_bis = game_info.split(game_info.split('}\n')[1])[1]
            file_read.close()
            iterTest = re.finditer('{(.*?)}', game_info)
            p_actions = []
            p_theta = []
            p_unorm = []
            for i, s in enumerate(iterTest):
                if i == 1:
                    p_actions = [int(str_int)
                                 for str_int in shlex.split(s.group(1))]
                if i == 2:
                    p_theta = [int(str_int)
                               for str_int in shlex.split(s.group(1))]
                if i == 3:
                    p_unorm = [int(str_int)
                               for str_int in shlex.split(s.group(1))]
            utilities = []
            # payoff_value = []
            # iterTest = re.finditer('\d(.*?)\n', game_info_bis)
            payoff_str = game_info_bis.split("\n")[1:-1]
            for s in payoff_str:
                payoff_value = [int(sub_int) for sub_int in s.split(" ")
                                if sub_int]
                n_players = len(p_actions)
                # Initialize the list of utility
                sublist_utilites = [[] for i in range(n_players)]
                # According to the way the utility are written
                # in the nfg file get for each player their utility
                for i, pay in enumerate(payoff_value):
                    sublist_utilites[i % n_players] += [pay]
                utilities.append(sublist_utilites)
            # Reverse the order of the players of each utility
            # and the order of the players action so that they
            # correspond to the order used in utilitiesTabl
            n_theta = 1  # len(theta[0])*len(theta[1])
            for i in range(n_players):
                n_theta = n_theta * p_theta[i]
            for i in range(n_theta):
                utilities[i].reverse()
            p_actions.reverse()
            p_theta.reverse()
            # Reverse proba
            dico_p = {}
            theta = [[j for j in range(p_theta[i])]
                     for i in range(len(p_theta))]
            tmp_bg = BG([], [], [], [])
            joint_theta_mat = tmp_bg.generate_joint_matrix(theta)
            joint_theta = []
            for i in range(n_players):
                sub_joint_theta = [joint_theta_mat[j, i]
                                   for j in range(joint_theta_mat.shape[0])]
                joint_theta.append(sub_joint_theta)
            for i in range(n_theta):
                dico_p[tuple(joint_theta[j][i]
                             for j in range(n_players))] = p_unorm[i]
            joint_theta.reverse()
            tmp_p = [dico_p[tuple(reversed(np.array(joint_theta)[:, i]))]
                     for i in range(n_theta)]
            players_actions = [[j for j in range(p_actions[i])]
                               for i in range(len(p_actions))]
            util_table = BG(players_actions, utilities, theta, tmp_p)
            return util_table

    def write_GameFile(self, file_path):
        """Using a utilities table, writes the corresponding .bg game file.

        .. WARNING::

            Note that currently the order of players is the reverse \
            of that in the utilities table \
            (Player 1 in the .bg file is the "last" player in the \
            utilites table).

        :param string file_path: Path where the .bg file should be written.

        """

        # Get the number of players and their number of actions
        # n_players = len(self.players_actions)
        p_actions = [len(subl) for subl in self.players_actions]
        # t_type = [len(subl) for subl in self.theta]
        # Get all the joint actions
        jact = [self.local_normalformgames[i].joint_actions
                for i in range(self.n_theta)]
        # Get theta
        theta = [len(subl) for subl in self.theta]
        # Get p
        current_p = self.p_unormalized
        # Get the utilities as a list
        util_list = []
        payoffwrite = []
        for k in range(len(self.utilities)):
            util_list.append(self.utilities[k])
            payoffwrite.append(
                [util_list[k][n][i]
                 for i in range(len(jact[k]))
                 for n in reversed(range(self.n_players))])
        # Reverse the order of the actions
        p_actions.reverse()
        theta.reverse()
        # Create a string that correspond to
        # the utility of the player to write in the bg file
        gamedescript = "nothing"
        playernames = "{"
        nb_actions = "{"
        typ = "{"
        for n_p, n_act in enumerate(p_actions):
            playernames += f' "Player {n_p}"'
            nb_actions += f" {n_act}"
            typ += f" {theta[n_p]}"
            if (n_p == len(p_actions) - 1):
                playernames += " }"
                nb_actions += " }"
                typ += " }"

        dico_p = {}
        joint_theta = []
        for i in range(self.n_players):
            sub_joint_theta = [self.joint_theta[j, i]
                               for j in range(self.n_theta)]
            joint_theta.append(sub_joint_theta)
        for i in range(self.n_theta):
            dico_p[tuple(joint_theta[j][i]
                         for j in range(self.n_players))] = current_p[i]
        joint_theta.reverse()
        tmp_p = [dico_p[tuple(reversed(np.array(joint_theta)[:, i]))]
                 for i in range(self.n_theta)]
        proba = "{"
        for i in range(len(tmp_p)):
            proba += f" {tmp_p[i]}"
        proba += " }"
        # Create the prolog of the file
        writeligne = \
            f'BG 0 R "{gamedescript}" {playernames} {nb_actions} {typ}'
        if not file_path[-3:] == '.bg':
            file_path += '.bg'
        fileTestwrite = open(file_path, "w+")
        fileTestwrite.write(writeligne + "\n\n")
        fileTestwrite.write(proba + "\n")
        # Create the rest
        for i in range(len(payoffwrite)):
            str_utilities = ""
            for uti in (payoffwrite[i]):
                str_utilities += f'{int(uti)} '
            fileTestwrite.write(str_utilities + "\n")
        fileTestwrite.close()

    def __str__(self):
        """
        Given the utilities table and the type : theta of the bayesian game
        """
        for j in range(self.n_theta):
            label = []
            players_id = [i for i in range(self.n_players)]
            for i in range(len(players_id)):
                label.append('Ax'.replace("x", str(players_id[i])))  # 'A _i'
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
            tableau_final = np.concatenate((np.mat(label),
                                            np.concatenate((joint_actions,
                                                            mat_utilities),
                                                           axis=1)),
                                           axis=0)
            print('Theta', j, '=', self.joint_theta[j],
                  'and P(Theta', j, ') =',
                  self.p[j], '\n', tableau_final, '\n')
        return '\n Type: \n' + str(self.theta)
