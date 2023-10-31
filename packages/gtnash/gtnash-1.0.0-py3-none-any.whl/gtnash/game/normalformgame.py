import numpy as np
import re
import shlex
from copy import deepcopy
import itertools
from gtnash.game.abstractgame import AbstractGame


class NFG(AbstractGame):
    """Normal-form game class, attributes and methods.

    :param list of lists players_actions: Actions of
        every players of input game.
    :param list of lists utilities: Utilities of every players of input game.
    :param list index_to_player: Players' numbering.

    """

    def __init__(self, players_actions, utilities, index_to_player={}):
        """Normal-form game constructor."""
        self.n_players = len(players_actions)
        self.players_actions = players_actions
        self.joint_actions = []
        self.joint_actions = self.generate_joint_actions(players_actions)
        self.utilities = utilities
        self.disutilities = np.mat(np.zeros(self.joint_actions.shape))
        for i, i_utilities in enumerate(utilities):
            u_tmp = np.mat(i_utilities)
            u_tmp = u_tmp.transpose()
            self.disutilities[:, i] = u_tmp
        self.transform_utilities()
        if not index_to_player:
            self.index_to_player = {i: i for i in range(self.n_players)}
        else:
            self.index_to_player = index_to_player

    def generate_joint_actions(self, players_actions):
        """Generates all the possible joint strategies.

        :param list of lists players_actions: The list of all
            lists of actions available to every players.

        :returns: A matrix which rows are the joint strategies.
        :rtype: np.matrix of int.
        """
        matA = np.mat([])
        for p_a in reversed(players_actions):
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

    def all_response_of_player(self, player_ind, action):
        """Generates all the possible joint strategies obtained by
        fixing joint strategy *action* and varying only the
        strategies of player *player_ind*.

        :param int player_ind: Index of the player whose action is not fixed.
        :param list action: Arbitrary joint strategy of players.

        :returns: A matrix which rows are the obtained joint strategies.
        :rtype: np.matrix.
        """
        action_in_use = []
        for i in range(self.n_players):
            action_i = [action[i]]
            if i == player_ind:
                action_i = self.players_actions[i]
            action_in_use += [action_i]
        return self.generate_joint_actions(action_in_use)

    def joint_action_except_i(self, player_ind):
        """Generates all the possible joint pure strategies excluding
        player *player_ind*'s action.

        :param int player_ind: Index of the player whose action is excluded.

        :returns: A matrix which rows are all the pure joint strategies
            excluding player *player_ind*'s action.
        :rtype: np.matrix.
        """
        action_in_use = [act for i, act in enumerate(self.players_actions)
                         if (i != player_ind)]
        return self.generate_joint_actions(action_in_use)

    def get_sub_jointact_of_n(self, player_ind):
        """For player *player_ind*, get the indices of every joint actions
         of the other player, for every strategies of *player_ind*.

        :param int player_ind: The player of interest.
        :return: A list of lists of joint actions, ordered by actions
            of player *player_ind*.
        :rtype: list of lists of integers.
        """
        jactions = self.joint_action_except_i(player_ind)
        tmp_index_of_all = []
        for jact in jactions:
            tmp_jact = list(np.array(jact).flatten())
            tmp_index_of_alt = []
            for i in range(len(self.players_actions[player_ind])):
                tmp_act = list(tmp_jact)
                tmp_act.insert(player_ind, i)
                tmp_index_of_alt += [
                    np.where(
                        (self.joint_actions == np.array(tmp_act)
                         ).all(1))[0][0]]
            tmp_index_of_all += [tmp_index_of_alt]
        return tmp_index_of_all

    def transform_utilities(self):
        """Computes the disutility matrix of the utility
         matrix of the considered game.

        """
        for i in range(self.n_players):
            max_i = np.max(self.disutilities[:, i])
            if max_i >= 0:
                self.disutilities[:, i] -= max_i + 1
            self.disutilities[:, i] = abs(self.disutilities[:, i])

    def row_where_p_is_i(self, player_id, action_value):
        """Get all the rows' indices in the list of joint strategies
         where player *player_id* plays strategy *action_value*.

        :param int player_id: Index of the player whose utilities are computed.
        :param int action_value: Arbitrary strategy of player *player_id*.

        :returns: rows' indices of the joint strategies list.
        :rtype: list of integers.
        """
        return np.where(action_value == np.array(
            self.joint_actions[:, player_id]).flatten())[0]

    def disutil_of_row(self, player_id, action_value):
        """Returns the disutility of joint strategies where the
         strategy is *action_value* for player *player_id*.

        :param int player_id: Index of the player whose
            disutilities are computed.
        :param int action_value: Arbitrary strategy of player *player_id*.

        :returns: list of integers .
        :rtype: list.
        """
        ind_row = self.row_where_p_is_i(player_id, action_value)
        return np.array(self.disutilities[ind_row, player_id]
                        ).flatten().astype(int)

    def util_of_row(self, player_id, action_value):
        """Returns the utility of joint strategies where the
        strategy is *action_value* for player *player_id*.

        :param int player_id: Index of the player whose utilities are computed.
        :param int action_value: Arbitrary strategy of player *player_id*.

        :returns: list of integers .
        :rtype: list.
        """
        ind_row = self.row_where_p_is_i(player_id, action_value)
        return np.array([self.utilities[player_id][tmp_ind]
                         for tmp_ind in ind_row]).flatten().astype(object)

    def util_of_joint_action(self, player_id, jact):
        """Returns the utility of joint action *jact* for
         player *player_id*.

        :param int player_id: Index of the player whose utility is computed.
        :param list jact: Arbitrary joint strategy of players.

        :returns: Utility.
        :rtype: int.
        """
        ind_row = np.where((self.joint_actions == np.array(jact)).all(1))[0][0]
        return self.utilities[player_id][ind_row]

    def disutil_of_joint_action(self, player_id, jact):
        """Returns the disutility of joint action *jact* for
         player *player_id*.

        :param int player_id: Index of the player whose disutility is computed.
        :param list jact: Arbitrary joint strategy of players.

        :returns: Disutility.
        :rtype: int.
        """
        ind_row = np.where((self.joint_actions == np.array(jact)).all(1))[0][0]
        return self.disutilities[ind_row, player_id]

    def expected_utilities(self, mixed_joint_strat):
        """Returns the expected utilities of *mixed_joint_strategy*
        for all players.

        :param dict mixed_joint_strat: *mixed_joint_strategy[play]* is
            the mixed strategy of player *play* (a list).

        :returns: List of the expected utilities to players
            of *mixed_joint_strategy*.
        :rtype: list of floats.
        """

        expected_util = []
        for n in mixed_joint_strat.keys():
            prob_n = mixed_joint_strat[n]
            util_of_n = np.copy(self.utilities[n][:]).tolist()
            # Use the strategy of the other player to get the
            # possible expected utility of every joint action
            for nbis in mixed_joint_strat.keys():
                prob_nbis = mixed_joint_strat[nbis]
                if not (nbis == n):
                    for j, prob_nbis_j in enumerate(prob_nbis):
                        index_nbis_j = \
                            self.row_where_p_is_i(
                                nbis,
                                self.players_actions[nbis][j])
                        for ind_nbis in index_nbis_j:
                            util_of_n[ind_nbis] = \
                                util_of_n[ind_nbis] * prob_nbis_j
            # Get the expected utility of each action
            value_all_i = []
            for i in range(len(prob_n)):
                value_i = 0
                index_n_i = self.row_where_p_is_i(n,
                                                  self.players_actions[n][i])
                for ind_n in index_n_i:
                    value_i += util_of_n[ind_n]
                value_all_i += [value_i]
            # The expected utility of the strategy
            max_proba = np.array(value_all_i).dot(prob_n)
            expected_util.append(max_proba)
        return expected_util

    def expected_utilities_of_n(self, n, mixed_joint_strat):
        """Returns the expected utilities of *mixed_joint_strategy*
        for player n.

        :param int n: Index of a player
        :param dict mixed_joint_strat: *mixed_joint_strategy[play]* is
            the mixed strategy of player *play* (a list).

        :returns: List of the expected utilities to players
            of *mixed_joint_strategy*.
        :rtype: list of floats.
        """
        prob_n = mixed_joint_strat[n]
        util_of_n = np.copy(self.utilities[n][:]).tolist()
        # Use the strategy of the other player to get the
        # possible expected utility of every joint action
        for nbis in mixed_joint_strat.keys():
            prob_nbis = mixed_joint_strat[nbis]
            if not (nbis == n):
                for j, prob_nbis_j in enumerate(prob_nbis):
                    index_nbis_j = \
                        self.row_where_p_is_i(
                            nbis,
                            self.players_actions[nbis][j])
                    for ind_nbis in index_nbis_j:
                        util_of_n[ind_nbis] = \
                            util_of_n[ind_nbis] * prob_nbis_j
        # Get the expected utility of each action
        value_all_i = []
        for i in range(len(prob_n)):
            value_i = 0
            index_n_i = self.row_where_p_is_i(n,
                                              self.players_actions[n][i])
            for ind_n in index_n_i:
                value_i += util_of_n[ind_n]
            value_all_i += [value_i]
        # The expected utility of the strategy
        max_proba = np.array(value_all_i).dot(prob_n)
        return max_proba

    # def is_equilibrium(self, mixed_joint_strategy, gap=0.0001):
    #     """Checks whether *mixed_joint_strategy* is a Nash equilibrium.
    #
    #     :param dict mixed_joint_strategy: *mixed_joint_strategy[play]* is
    #         the mixed strategy of player *play* (a list).
    #     :param float gap: maximum deviation to equilibrium allowed.
    #
    #     :returns: *True* if *mixed_joint_strategy* is a mixed
    #         Nash equilibrium and *False* if not.
    #     :rtype: boolean.
    #     """
    #     expected_util_of_mixed_joint_strategy = \
    #         self.expected_utilities(mixed_joint_strategy)
    #     for play in range(self.n_players):
    #         for ai in range(len(self.players_actions[play])):
    #             other_strategy = mixed_joint_strategy.copy()
    #             other_strategy[play] = \
    #                 np.zeros(len(mixed_joint_strategy[play]))
    #             other_strategy[play][ai] = 1
    #             expected_util_of_other = \
    #                 self.expected_utilities(other_strategy)
    #             if not(expected_util_of_other[play] <=
    #                    expected_util_of_mixed_joint_strategy[play] + gap):
    #                 return False
    #     return True

    def is_equilibrium(self, mixed_joint_strategy, gap=0.0001):
        """Checks whether *mixed_joint_strategy* is a Nash equilibrium.

        :param dict mixed_joint_strategy: *mixed_joint_strategy[play]* is
            the mixed strategy of player *play* (a list).
        :param float gap: maximum deviation to equilibrium allowed.

        :returns: *True* if *mixed_joint_strategy* is a mixed
            Nash equilibrium and *False* if not.
        :rtype: boolean.
        """
        expected_util_of_mixed_joint_strategy = \
            self.expected_utilities(mixed_joint_strategy)
        for play in range(self.n_players):
            for ai in range(len(self.players_actions[play])):
                other_strategy = mixed_joint_strategy.copy()
                other_strategy[play] = \
                    np.zeros(len(mixed_joint_strategy[play]))
                other_strategy[play][ai] = 1
                expected_util_of_other = \
                    self.expected_utilities_of_n(play, other_strategy)
                if not (expected_util_of_other <=
                        expected_util_of_mixed_joint_strategy[play] + gap):
                    return False
        return True

    def is_pure_equilibrium(self, pure_joint_strategy, gap=0.0001):
        for n in range(self.n_players):
            alt_jact = self.all_response_of_player(n, pure_joint_strategy)
            currentutil = self.util_of_joint_action(n, pure_joint_strategy)
            for tmp_jact in alt_jact:
                if not (self.util_of_joint_action(n, tmp_jact) <=
                        currentutil+gap):
                    return False
        return True

    def error_equilibrium(self, mixed_joint_strategy):
        """Returns the maximum utility gaps to any player
        of *mixed_joint_strategy*.
        This measures how far *mixed_joint_strategy* is from
        being an equilibrium.

        :param dict mixed_joint_strategy: *mixed_joint_strategy[play]*
            is the mixed strategy of player *play* (a list).

        :returns: the maximal gaps of the expected utilities to players
            of any deviation from *mixed_joint_strategy*.
        :rtype: list of float.
        """
        all_valuediff = []
        for play in range(self.n_players):
            expected_util_of_mixed_joint_strategy = \
                self.expected_utilities(mixed_joint_strategy)
            for ai in range(len(self.players_actions[play])):
                other_strategy = mixed_joint_strategy.copy()
                other_strategy[play] = np.zeros(
                    len(mixed_joint_strategy[play]))
                other_strategy[play][ai] = 1
                expected_util_of_other =\
                    self.expected_utilities(other_strategy)
                all_valuediff += \
                    [expected_util_of_other[play] -
                     expected_util_of_mixed_joint_strategy[play]]
        return max(all_valuediff)

    def get_all_PNE(self):
        """Returns every existing pure Nash equilibrium.
        Returns the empty dictionary if the game admits
        no pure Nash equilibrium.

        :returns: The list of encountered Nash equilibria (if any),
            represented as dictionaries.
        :rtype: list of dict.
        """
        all_pne = []
        all_pure_strat = list(itertools.product(*self.players_actions))
        for pure_strat in all_pure_strat:
            tmp_dic_strat = {i: [1 if self.players_actions[i][s_i] == s else 0
                                 for s_i in range(len(self.players_actions[i]))
                                 ] for i, s in enumerate(pure_strat)}
            pure_stratbis = list(pure_strat)
            if self.is_pure_equilibrium(pure_stratbis):
                all_pne += [tmp_dic_strat]
        return all_pne

    def pne_exist(self):
        """Checks whether there is a PNE in the game

        :returns: *True* if there exists a pure Nash equilibrium
            and *False* if not.
        :rtype: boolean.
        """
        all_pure_strat = list(itertools.product(*self.players_actions))
        for pure_strat in all_pure_strat:
            pure_stratbis = list(pure_strat)
            if self.is_pure_equilibrium(pure_stratbis):
                return True
        return False

    def first_pne(self):
        """Returns the first encountered pure Nash equilibrium.
        Returns the empty dictionary if the game admits no
        pure Nash equilibrium.

        :returns: The first encountered Nash equilibrium (if any),
            represented as a dictionary.
        :rtype: dict.
        """
        all_pure_strat = list(itertools.product(*self.players_actions))
        for pure_strat in all_pure_strat:
            tmp_dic_strat = {
                i: [1 if self.players_actions[i][s_i] == s else 0
                    for s_i in range(len(self.players_actions[i]))]
                for i, s in enumerate(pure_strat)}
            pure_stratbis = list(pure_strat)
            if self.is_pure_equilibrium(pure_stratbis):
                return tmp_dic_strat
        return {}

    def build_subgame(self, partial_mixed_strategy):
        """Builds a subgame of a normal form game by fixing the mixed
            strategies of some arbitrary players.

        :param dict partial_mixed_strategy: *partial_mixed_strategy[n]* is
            a probability distribution over actions of player n (a list).

        :returns: Normal form subgame *nfg_out*.
        :rtype: NFG.
        """
        n_players = self.n_players
        players_actions = deepcopy(self.players_actions)
        joint_actions_before = self.generate_joint_actions(
            self.players_actions)
        for n in partial_mixed_strategy.keys():
            players_actions[n] = [-1]
        joint_actions_after = self.generate_joint_actions(players_actions)
        utilities = [[0 for a in range(len(joint_actions_after))]
                     for n in range(n_players)]
        for aa in range(len(joint_actions_after)):
            for ab in range(len(joint_actions_before)):
                are_equal = True
                for n in range(n_players):
                    if n not in partial_mixed_strategy.keys():
                        if joint_actions_after[aa, n] !=\
                                joint_actions_before[ab, n]:
                            are_equal = False
                            break
                if are_equal:
                    for n in range(n_players):
                        local_proba = 1
                        for m in partial_mixed_strategy.keys():
                            local_proba *= partial_mixed_strategy[m][
                                joint_actions_before[ab, m]]
                        utilities[n][aa] += local_proba * self.utilities[n][ab]
        nfg_out = NFG(players_actions, utilities)
        return nfg_out

    def get_subgame_level(self, proba):
        """Given a joint mixed strategy, returns the subgame with the
        last player's mixed strategy fixed.

        :param dict proba: Joint mixed strategy represented as a dictionary.
            *proba[n]* is the mixed strategy played by player n.

        :returns: Normal form subgame with one player less.
        :rtype: NFG.
        """

        # Get mixed strategy of the last player
        proba_k = proba[self.n_players - 1]
        # for each action of the last players give the index of
        # the joint action where it is used
        dict_actions_index = {}
        # For each actions gives its probability
        dict_actions_proba = {}
        for j, proba_k_j in enumerate(proba_k):
            dict_actions_index[j] = self.row_where_p_is_i(
                self.n_players - 1, j)
            dict_actions_proba[j] = proba_k_j
        new_util = []
        new_players_action = []
        # Compute the nex utility for each player
        for n in range(self.n_players - 1):
            util_of_n = self.utilities[n]
            new_util_of_n = []
            new_players_action_of_n = [na for na in range(len(proba[n]))]
            # For every possible joint action of the active players
            for i in range(len(util_of_n) // len(dict_actions_proba)):
                new_util_i = 0
                # Compute the new utility given the probability
                for j in range(len(proba_k)):
                    new_util_i += util_of_n[
                        dict_actions_index[j][i]
                    ] * dict_actions_proba[j]
                new_util_of_n += [new_util_i]
            new_players_action += [new_players_action_of_n]
            new_util += [new_util_of_n]
        return NFG(new_players_action, new_util)

    def get_subgame_without_n(self, proba, player_ind):
        """Given a joint mixed strategy and a player's index,
         returns the subgame with the indexed player's mixed strategy fixed.

        :param dict proba: Joint mixed strategy represented as a dictionary.
            *proba[n]* is the mixed strategy played by player n.
        :param int player_ind: Player which strategy is fixed.

        :returns: Normal form subgame with player *player_ind* removed.
        :rtype: NFG.
        """
        # Distribution probability of the player n
        proba_n = proba[player_ind]
        # For each action of the removed player associate
        # the indexes at which it is found
        dict_actions_index = {}
        # For each action of the removed player associate its probability
        dict_actions_proba = {}
        old_playerindex_to_new = {}
        new_index_to_player_id = {}
        for p in range(self.n_players):
            if p > player_ind:
                old_playerindex_to_new[p] = p - 1
                new_index_to_player_id[p - 1] = self.index_to_player[p]
            elif p != player_ind:
                old_playerindex_to_new[p] = p
                new_index_to_player_id[p] = self.index_to_player[p]
                # new_index_to_player_id[p]=p
        for j, proba_k_j in enumerate(proba_n):
            dict_actions_index[j] = self.row_where_p_is_i(player_ind, j)
            dict_actions_proba[j] = proba_k_j
        list_of_index = self.get_sub_jointact_of_n(player_ind)
        new_util = []
        new_players_action = []
        for m in range(self.n_players):
            if m != player_ind:
                new_index_to_player_id[len(new_util)] = m
                util_of_m = self.utilities[m]
                new_util_of_m = []
                new_players_action_of_m = [na for na in range(len(proba[m]))]
                for li_index in list_of_index:
                    new_util_i = 0
                    for j, ind in enumerate(li_index):
                        new_util_i += util_of_m[ind] * proba_n[j]
                    new_util_of_m += [new_util_i]
                new_util += [new_util_of_m]
                new_players_action += [new_players_action_of_m]
        # Keep Track of players indexes
        return NFG(new_players_action, new_util, new_index_to_player_id)

    def get_subgame_fixed_strat(self, played_strat):
        """For a given partial pure strategy, returns the subgame
        where this is played.

        :param dict played_strat: Partial strategy represented as a
            dictionary (integer values). *played_strat[n]* is
            the pure strategy played by player n.

        :returns: Normal form subgame.
        :rtype: NFG.
        """
        new_player_actions = []
        valid_row = set(range(len(self.utilities[0])))
        for n, act_n in enumerate(self.players_actions):
            tmp_n_set = set()
            tmp_n_act = []
            for a_i, a in enumerate(act_n):
                if played_strat[n][a_i] == 1:
                    tmp_n_set = tmp_n_set.union(
                        list(self.row_where_p_is_i(n, a))
                    )
                    tmp_n_act += [a]
            valid_row = valid_row.intersection(tmp_n_set)
            new_player_actions += [tmp_n_act]
        list_row = sorted(valid_row)
        new_util = [[self.utilities[n][i] for i in list_row]
                    for n in range(len(new_player_actions))]
        return NFG(new_player_actions, new_util)

    @classmethod
    def readNFGpayoff(cls, file_path):
        """Using a .nfg game file (payoff version),
         creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of that
            in the utilities table (Player 1 in the .nfg file is the
            "last" player in the utilites table).

        :param string file_path: Path of the .nfg file to read.

        :returns: utilities table.
        :rtype: list of lists of integers.
        """

        # Read file
        file_read = open(file_path, 'r')
        content = file_read.read()
        # List of content (3 String: NFG, string and rest)
        content_list = content.split('"', 2)
        game_info = content_list[2]
        file_read.close()
        iterTest = re.finditer('{(.*?)}', game_info)
        p_actions = []
        # Get the name and actions of the players
        for i, s in enumerate(iterTest):
            if i > 0:
                p_actions = [int(str_int)
                             for str_int in shlex.split(s.group(1))]
        payoff_value = []
        iterTest = re.finditer('\n{1,}(.*?)\n', game_info)
        # Get the string of payoff, an iterator is use
        # but there is only 1 element to iterate on
        for s in iterTest:
            payoff_value = [int(sub_int)
                            for sub_int in s.group(0).strip('\n').split(" ")
                            if sub_int]
        n_players = len(p_actions)
        # Initialize the list of utility
        u = [[] for i in range(n_players)]
        # According to the way the utility are written in the nfg file
        # get for each player their utility
        for i, pay in enumerate(payoff_value):
            u[i % n_players] += [pay]
        # Reverse the order of the players of each utility and
        # the order of the players action so that
        # they correspond to the order used in utilitiesTabl
        u.reverse()
        p_actions.reverse()
        # Generate list of actions like [[0,1,2][0,1][0,1,2,4]]
        # (for 3 player where one they have 3,2 and 4 actions)
        players_actions = [[j for j in range(p_actions[i])]
                           for i in range(len(p_actions))]
        return NFG(players_actions, u)

    def writeNFGpayoff(self, file_path):
        """Using a utilities table, creates the
         corresponding .nfg game file (payoff version).

        .. WARNING::

            Note that currently the order of players is the reverse of that
            in the utilities table (Player 1 in the .nfg file is the "last"
            player in the utilites table).

        :param string file_path: Path where the .nfg file should be written.

        """

        # Get the number of players and their number of actions
        n_players = len(self.players_actions)
        p_actions = [len(subl) for subl in self.players_actions]
        # Get all the joint actions
        jact = self.joint_actions
        # Get the utilities as a list
        util_list = self.utilities
        payoffwrite = [util_list[n][i] for i in range(len(jact))
                       for n in reversed(range(n_players))]
        # Reverse the order of the actions
        p_actions.reverse()
        # Create a string that correspond to the
        # utility of the player to write in the nfg file
        str_payoff = "".join(f"{p} " for p in payoffwrite)
        gamedescript = "nothing"
        playernames = "{"
        nb_actions = "{"
        for n_p, n_act in enumerate(p_actions):
            playernames += f' "Player {n_p+1}"'
            nb_actions += f" {n_act}"
            if n_p == len(p_actions) - 1:
                playernames += " }"
                nb_actions += " }"
        # Create the prolog of the file
        writeligne = f'NFG 1 R "{gamedescript}" {playernames} {nb_actions}'
        fileTestwrite = open(file_path, "w+")
        fileTestwrite.write(writeligne + "\n\n")
        fileTestwrite.write(str_payoff + "\n")
        fileTestwrite.close()

    def readNFGoutcome(self, file_path):
        """Using a .nfg game file (outcome version),
        creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of
            that in the utilities table (Player 1 in the .nfg file is
            the "last" player in the utilites table).

        :param string file_path: Path of the .nfg file to read.

        :returns: utilities table.
        :rtype: list of lists of integers.
        """
        # Read file
        my_file = open(file_path, 'r')
        content = my_file.read()
        # List of content (3 String: NFG, string and rest)
        content_list = content.split('"', 2)
        my_file.close()
        game_info = content_list[2]
        p_actions = []
        iterTest = re.finditer('"(?:[^"]")+', game_info.split("\n\n")[1])
        # Get actions of the players
        for i, s in enumerate(iterTest):
            p_actions += [len(shlex.split(s.group(0)))]
        iterTest = re.finditer('{(.*?)}',
                               (game_info.split("\n\n")[2]).replace(',', ''))
        payoff_value = []
        # Get Payoff, write it in a list as if it were written
        # like in the nfg payoff version
        for i, s in enumerate(iterTest):
            payoff_value += [int(sub_int)
                             for sub_ind, sub_int in
                             enumerate(shlex.split(s.group(1)))
                             if sub_ind != 0]
        # payoff_value=[int(sub_int) for sub_ind,sub_int in
        # enumerate(shlex.split(s.group(1))) if sub_ind!=0 for i,s
        # in enumerate(iterTest)]
        n_players = len(p_actions)
        u = [[] for i in range(n_players)]
        # According to the way the utility are written in the nfg
        # file get for each player their utility
        for i, pay in enumerate(payoff_value):
            u[i % n_players] += [pay]
        u.reverse()
        p_actions.reverse()
        players_actions = [[j for j in range(p_actions[i])]
                           for i in range(len(p_actions))]
        self.players_actions = players_actions
        self.utilities = u
        util_table = NFG(self.players_actions, self.utilities)
        return util_table

    def writeNFGoutcome(self, file_path):
        """Using a utilities table, creates the corresponding .nfg game
        file (payoff version).

        .. WARNING::

            Note that currently the order of players is the reverse of
            that in the utilities table (Player 1 in the .nfg file is
            the "last" player in the utilites table).

        :param string file_path: Path where the .nfg file should be written.

        """
        # Get the number of players and their number of actions
        n_players = len(self.players_actions)
        p_actions = [len(subl) for subl in self.players_actions]
        # Get the joint actions and utility
        jact = self.joint_actions
        util_list = self.utilities
        payoffwrite = []
        tmp_act_ut = []
        # Get the utility in a list ordered like required
        # for the outcome version of a nfg file
        # (reversing the order of players)
        for i in range(len(jact)):
            for n in reversed(range(n_players)):
                if n == 0:
                    tmp_act_ut += [util_list[n][i]]
                    payoffwrite += [tmp_act_ut]
                    tmp_act_ut = []
                else:
                    tmp_act_ut += [util_list[n][i]]
        # reverse the players actions order
        p_actions.reverse()
        # Create the string of the actions of the player to write into the file
        str_actions = "{ "
        for act in self.players_actions:
            str_act_p = "{"
            for a in act:
                str_act_p += f' "{a+1}"'
            str_act_p += " }\n"
            str_actions += str_act_p
        str_actions += '}\n""\n'
        str_payoff = "{\n"
        # Create the string og the utility of the outcomes
        # to write into to file
        for a, p in enumerate(payoffwrite):
            str_payoff += '{ ""'
            for n, p_n in enumerate(p):
                if n < len(p_actions) - 1:
                    str_payoff += f' {p_n},'
                else:
                    str_payoff += f' {p_n}'
            str_payoff += ' }\n'
        str_payoff += '}\n'
        str_jact = [str(i + 1) for i in range(len(jact))]
        str_payoff += " ".join(str_jact) + "\n"
        gamedescript = "nothing"
        playernames = "{"
        # nb_actions = "{"
        for n_p, n_act in enumerate(p_actions):
            playernames += f' "Player {n_p+1}"'
            if n_p == len(p_actions) - 1:
                playernames += " }"
        # Create prolog line
        writeligne = f'NFG 1 R "{gamedescript}" {playernames}'

        fileTestwrite = open(file_path, "w+")
        fileTestwrite.write(writeligne + "\n\n")
        fileTestwrite.write(str_actions + "\n")
        fileTestwrite.write(str_payoff)
        fileTestwrite.close()

    def read_GameFile(self, file_path):
        """Using a .nfg game file (whichever version),
        creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of that in
            the utilities table (Player 1 in the .nfg file is the "last"
            player in the utilites table).

        :param string file_path: Path of the .nfg file to read.

        :returns: utilities table.
        :rtype: list of lists of integers.
        """
        file_read = open(file_path, 'r')
        text = file_read.readlines()
        number_of_line = len(text)
        if number_of_line == 3:
            print('Payoff nfg file.')
            util_table = NFG.readNFGpayoff(self, file_path)
        else:
            print('Outcome nfg file.')
            util_table = NFG.readNFGoutcome(self, file_path)
        return util_table

    def write_GameFile(self, file_path):
        """Using a utilities table, writes the corresponding .nfg
        game file (payoff version).

        .. WARNING::

            Note that currently the order of players is the reverse of that
            in the utilities table (Player 1 in the .nfg file is the "last"
            player in the utilites table).

        :param string file_path: Path where the .nfg file should be written.

        """
        if isinstance(self, NFG):
            file_path = file_path + '.nfg'
            NFG.writeNFGpayoff(self, file_path)
        else:
            print('Unrecognized')

    def __str__(self):
        """
        Given the utilities table of the normal form game
        """
        label = []
        for i in range(len(self.players_actions)):
            label.append('Ax'.replace("x", str(i)))
        for i in range(len(self.players_actions),
                       2 * (len(self.players_actions))):
            label.append('Ux'.replace("x", str(i - len(self.players_actions))))
        mat_utilities = np.transpose(self.utilities)
        mat_utilities = mat_utilities.astype(str)
        tableau_final = np.concatenate(
            (np.mat(label),
             np.concatenate((self.joint_actions, mat_utilities), axis=1)),
            axis=0)
        return str(tableau_final)
