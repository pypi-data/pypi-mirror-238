"""Implementation of Porter, Nudelman and Shoam's algorithm.

Class
-----

- Class ``LHpolymatrix``:
    An instance is a representation as a polymatrix game,
    as well as a representation as a Tucker scheme.
    It includes several methods, including the solver.

Detailed description of the class:
----------------------------------

"""

from fractions import Fraction

import numpy as np
import math



class LHpolymatrix:
    """
    Polymatrix game solver using Howson algorithm

    :param PMG game: Polymatrix game used in the solver

    Attributes
    ----------
    n_players : int
        Number of players in the polymatrix game
    players_actions : list
        List of actions of each player
    m_action: int
        Total number of action
    all_utilities: dictionary
        List of local utilities of each player
    maxu_of_p : dictionary
        Maximum utility of a player
    inverse_utilities: dictionary
        Disutilities of the players
    col_var : dictionary
        Associate to each variable a column index
    row_var : dictionary
        Associate to each variable a row index
    var_of_p : dictionary
        Associate to each player all of his variable,might be useless
    col_var_by_index : dictionary
        Associate to each column index a variable
    row_var_by_index : dictionary
        Associate to each row index a variable
    tucker : np.matrix
        Tucker scheme of the current game.

    """
    def __init__(self, game):
        self.n_players = game.n_players
        self.players_actions = game.players_actions
        self.m_action = sum([len(acts) for acts in game.players_actions])
        self.all_utilities = {n: {} for n in range(self.n_players)}
        self.maxu_of_p = {n: -math.inf for n in range(self.n_players)}
        self.currentgame = game
        player_to_list_denom = {n: set() for n in range(self.n_players)}
        for i_e, e in enumerate(game.hypergraph):
            util_e = game.utilities[i_e]
            # if np.array(game.utilities[i_e]).dtype==float:
            #     util_e=[[Fraction(e).limit_denominator() for e in li] for li in util_e]
            u_p0 = util_e[0]
            # player_to_list_denom[e[0]].update([f_val.denominator
            # for f_val in u_p0 if type(f_val) == Fraction])
            player_to_list_denom[e[0]].update(
                [f_val.denominator if isinstance(f_val, Fraction)
                 else 1 for f_val in u_p0])
            u_p1 = util_e[1]
            # player_to_list_denom[e[1]].update([f_val.denominator
            # for f_val in u_p1 if type(f_val) == Fraction])
            player_to_list_denom[e[1]].update(
                [f_val.denominator if isinstance(f_val, Fraction)
                 else 1 for f_val in u_p1])
        player_to_lcm = {n: np.lcm.reduce(list(player_to_list_denom[n])) for n
                         in range(self.n_players)}
        # player_to_lcm = {n: np.lcm.reduce(np.array(list(player_to_list_denom[n]), dtype=np.int64)) for n
        #                  in range(self.n_players)}
        for i_e, e in enumerate(game.hypergraph):
            util_e = np.array(game.utilities[i_e])
            # if util_e.dtype==float:
            #     util_e=np.array([[Fraction(e).limit_denominator() for e in li] for li in util_e])
            u_p0 = (util_e[0] * player_to_lcm[e[0]]).astype(np.int64)
            self.maxu_of_p[e[0]] = max(self.maxu_of_p[e[0]], max(u_p0))
            player_to_list_denom[e[0]].update(
                [f_val.denominator for f_val in u_p0 if
                 isinstance(f_val, Fraction)])
            u_p1 = (util_e[1] * player_to_lcm[e[1]]).astype(np.int64)
            self.maxu_of_p[e[1]] = max(self.maxu_of_p[e[1]], max(u_p1))
            player_to_list_denom[e[1]].update(
                [f_val.denominator if isinstance(f_val, Fraction)
                 else 1 for f_val in u_p1])
            # nb_p0 = len(game.players_actions[e[0]])
            nb_p1 = len(game.players_actions[e[1]])
            new_util_p0 = []
            new_util_p1 = [[] for i in range(nb_p1)]
            tmp_u = []
            for u_p_index, u_p_val in enumerate(u_p0):
                tmp_u += [u_p_val]
                if len(tmp_u) == nb_p1:
                    new_util_p0 += [tmp_u]
                    tmp_u = []
            for u_p_index, u_p_val in enumerate(u_p1):
                new_util_p1[u_p_index % nb_p1] += [u_p_val]
            self.all_utilities[e[0]][e[1]] = new_util_p0
            self.all_utilities[e[1]][e[0]] = new_util_p1
        self.inverse_utilities = self.inverse_utilities()
        self.col_var = {}
        self.row_var = {}
        # self.var_of_p = {}
        self.col_var_by_index = {}
        self.row_var_by_index = {}
        self.tucker = np.zeros((self.m_action + self.n_players,
                                1 + self.m_action + self.n_players))

    def inverse_utilities(self):
        """
        Computes the disutilities of the current polymatrix game.

        :param ``LHpolymatrix`` self: The polymatrix game solver instance.
        :returns: inverse_utilities: Inverses the utilities of  every players \
in every local games.
        :rtype: dict.

        """
        inverse_utilities = {}
        for n in range(self.n_players):
            util_of_n = self.all_utilities[n]
            inv_util_of_n = {}
            for k in util_of_n.keys():
                inv_util_of_n[k] = self.inv_util(n, util_of_n[k])
            inverse_utilities[n] = inv_util_of_n
        return inverse_utilities

    def inv_util(self, current_n, util_of_n_e):
        """
        Computes the disutility of a player in a local game.

        :param int current_n: Index of the current player.
        :param list util_of_n_e: Utilities of current player in local games\
it is involved in.
        :returns: newMatrix: A matrix of disutilities.
        :rtype: Numpy array.

        """
        mj = len(util_of_n_e[0])
        matrixE = np.ones((len(util_of_n_e), mj)).astype(np.int64).astype(object)
        newMatrix = util_of_n_e - (
            (self.maxu_of_p[current_n] + Fraction(1, 1)) * matrixE)
        newMatrix = -newMatrix
        return newMatrix

    def tucker_schema(self):
        """
        Creates the tucker scheme associated to the current game.

        :param ``LHpolymatrix`` self: The polymatrix game solver instance.

        """
        schema = np.zeros((self.m_action, self.m_action))
        matrixv = np.zeros((self.m_action, self.n_players))
        matrixu = np.zeros((self.n_players, self.m_action))
        matrix0 = np.zeros((self.n_players, self.n_players))
        self.col_var["1"] = 0
        current_i = 0
        for n in range(self.n_players):
            basic_str = "y" + str(n) + "_"
            nonbasic_str = "x" + str(n) + "_"
            # self.var_of_p[n]=[]
            current_j = 0  # current column
            # Inverse the utilities matrix
            util_of_n = self.inverse_utilities[n]
            actions_n = len(self.players_actions[n])
            for nbis in range(self.n_players):
                actions_nbis = len(self.players_actions[nbis])
                if n == nbis:
                    schema[
                        current_i:current_i + actions_n,
                        current_j:current_j + actions_n] =\
                        np.zeros((actions_n, actions_n))
                    for k in range(current_j, current_j + actions_n):
                        # self.var_of_p[n] +=
                        # [nonbasic_str + str(k - current_j)]
                        self.col_var[nonbasic_str + str(k - current_j)] = k + 1
                    matrixu[n, current_j:current_j + actions_n] = np.ones(
                        actions_n)
                    self.col_var["v" + str(n)] = self.m_action + n + 1
                    # self.var_of_p[n] += ["v" + str(n)]
                    current_j = current_j + actions_n
                else:
                    if nbis in list(util_of_n.keys()):
                        schema[
                            current_i:current_i + actions_n,
                            current_j:current_j + actions_nbis] =\
                            util_of_n[nbis]
                    current_j = current_j + actions_nbis
            for r in range(current_i, current_i + actions_n):
                self.row_var[basic_str + str(r - current_i)] = r
                # self.var_of_p[n] += [basic_str + str(r - current_i)]
            matrixv[current_i:current_i + actions_n, n] = -np.ones(actions_n)
            self.row_var["u" + str(n)] = self.m_action + n
            # self.var_of_p[n] += ["u" + str(n)]
            current_i = current_i + actions_n
        schema = np.hstack((np.zeros((self.m_action, 1)), schema))
        matrixu = np.hstack((-np.ones((self.n_players, 1)), matrixu))
        self.tucker = np.block([[schema, matrixv], [matrixu, matrix0]])
        # Associate index with variable
        for k in self.col_var.keys():
            self.col_var_by_index[self.col_var[k]] = k
        for k in self.row_var.keys():
            self.row_var_by_index[self.row_var[k]] = k

    def lemke(self, list_action):
        """
        Executes the Lemke-Howson algorithm, initialized by *list_action* \
on a polymatrix game

        :param ``LHpolymatrix`` self: The polymatrix game solver instance.
        :param list list_action: Joint strategy used to initialize \
Lemke-Howson's algorithm.
        :returns: A Nash equilibrium.
        :rtype: list.

        """
        self.block_pivot(list_action)
        # Need to adjust value according to variable number
        epsilon = Fraction(1, 1000)
        column_epsilon = (np.ones((self.m_action + self.n_players, 1)).astype(
            np.int64).astype(object)) * epsilon
        for i in range(self.m_action + self.n_players):
            column_epsilon[i] = column_epsilon[i] ** (i + 1)
        self.tucker = np.block([self.tucker, column_epsilon])
        p = 0
        while True:  # Until a solution is returned
            index_col_v = self.col_var[
                "v" + str(p)]  # Step 2: Get the current v^p
            outbase = self.enter_in_base(index_col_v)
            # Step3: Pivot until
            while not self.complementary_of_p(p, list_action[p]):
                outvar_str = outbase[1:]
                next_var_in = [s for s in list(self.col_var.keys()) if
                               s[1:] == outvar_str and s != outbase]
                outbase = self.enter_in_base(self.col_var[next_var_in[0]],p)
                while outbase[0] == "v":  # Step 5: Decrement p and
                    p = p - 1
                    var_of_p = [s for s in list(self.col_var.keys()) if
                                s[1:] == str(p) + "_" + str(list_action[p])][0]
                    outbase = self.enter_in_base(self.col_var[var_of_p])
            # Step 4: If p== number of players then the solution is
            # found otherwise increment p and go back to step 2
            if p == self.n_players - 1:
                return self.nash_equi()
            p = p + 1

    def nash_equi(self):
        """
        Extracts a Nash equilibrium from the final Tucker's scheme of the game.

        :param ``LHpolymatrix`` self: The polymatrix game solver instance.
        :returns: nash_equilibrium: A Nash equilibrium
        :rtype: list.

        """
        nash_equilibrium = {}
        col_q = self.tucker[:, self.col_var["1"]]
        for i in range(self.n_players):
            x_of_i = "x" + str(i)
            var_base = list(self.row_var.keys())
            strat_used = [s for s in var_base if s[:1 + len(str(i))] == x_of_i]
            strat_i = []
            for j in range(len(self.players_actions[i])):
                xij = x_of_i + "_" + str(j)
                if xij in strat_used:
                    strat_i += [col_q[self.row_var[xij]]]
                else:
                    strat_i += [0]
            nash_equilibrium[i] = strat_i
        return nash_equilibrium

    def complementary_of_p(self, n, action_i):
        """
        Complementarity check within Lemke-Howson's algorithm.

        :param int n: Index of the current player.
        :param int action_i: index of player i's strategy.
        :returns: ``True`` if the player's variables in the Tucker scheme are \
complementary.
        :rtype: bool.

        """
        var_base = list(self.row_var.keys())
        var_of_n = []
        for s in var_base:
            s_size = len(s)
            n_size = len(str(n))
            tmp_split = s[1:].split('_')
            # if s_size == 2+n_size+act_size and
            # int(s[1:s_size - act_size-1]) == n:
            if np.int64(tmp_split[0]) == n and s_size > (1 + n_size):
                var_of_n += [s[1:]]
            # if len(s)==3+len(str(n)) and int(s[1:len(s)-2])==n:
            #     var_of_n+=[s[1:]]
        if var_of_n.count(str(n) + "_" + str(action_i)) > 1:
            return False
        return True

    def block_pivot(self, col):
        """
        Given a column variable, updates the tucker scheme by pivoting \
this variable with the correct row.

        :param string col: Variable corresponding to the pivoting column.

        """
        new_col_var_by_index = {}
        new_row_var_by_index = {}
        index_piv_row = []
        for i in range(self.n_players):
            index_piv_row += [self.m_action + i]
        index_piv_col = []
        for i in range(self.n_players):
            varx = "x" + str(i) + "_" + str(col[i])
            index_piv_col += [self.col_var[varx]]
        index_nopiv_col = [x for x in self.col_var_by_index.keys() if
                           x not in index_piv_col]
        index_nopiv_row = [x for x in self.row_var_by_index.keys() if
                           x not in index_piv_row]
        # Init position of the var before the pivot
        allcol = index_piv_col + index_nopiv_col
        allrow = index_piv_row + index_nopiv_row
        for i in range(len(allcol)):
            new_col_var_by_index[i] = self.col_var_by_index[allcol[i]]
        for i in range(len(allrow)):
            new_row_var_by_index[i] = self.row_var_by_index[allrow[i]]
        # Submatrix
        m11 = self.tucker[np.ix_(index_piv_row, index_piv_col)]
        m12 = self.tucker[np.ix_(index_piv_row, index_nopiv_col)]
        m21 = self.tucker[np.ix_(index_nopiv_row, index_piv_col)]
        m22 = self.tucker[np.ix_(index_nopiv_row, index_nopiv_col)]
        # Block Pivot
        invm11 = np.linalg.inv(m11)
        blockPiv = np.block([[invm11, -invm11.dot(m12)], [m21.dot(invm11),
                                                          m22 - (m21.dot(
                                                              invm11.dot(
                                                                  m12)))]])
        # Updating the variable position to keep track of the index
        self.update_var_position(new_col_var_by_index, new_row_var_by_index)
        self.tucker = blockPiv
        self.tucker = self.tucker.astype(
            np.int64)  # mauvaise valeur lorsque float/fraction
        self.tucker = self.tucker.astype(object)

    def update_var_position(self, new_col_var_by_index, new_row_var_by_index):
        """
        Method used in ``block_pivot``.

        """
        for i in range(self.n_players):
            var_col_i = new_col_var_by_index[i]
            var_row_i = new_row_var_by_index[i]
            new_col_var_by_index[i] = var_row_i
            new_row_var_by_index[i] = var_col_i
        new_col_var = {}
        new_row_var = {}
        for k in new_col_var_by_index.keys():
            new_col_var[new_col_var_by_index[k]] = k
        for k in new_row_var_by_index.keys():
            new_row_var[new_row_var_by_index[k]] = k
        self.col_var_by_index = new_col_var_by_index
        self.row_var_by_index = new_row_var_by_index
        self.col_var = new_col_var
        self.row_var = new_row_var

    def enter_in_base(self, index_col,p=math.inf):
        """
        Given a column index, returns the variable corresponding to the \
row that allows to pivot while respecting the positivity constraint \
and does this operation.

        """
        # Get column 1/Q
        index_q = self.col_var["1"]
        col_q = self.tucker[:, index_q]
        # Get column of entering variable
        col_enter = self.tucker[:, index_col]
        # Get all possible pivot S={j,a_j<0}
        index_value_col = []
        for j in range(len(col_enter)):
            if col_enter[j] != 0 : # and int(self.row_var_by_index[j][1])<=p : can pivot for variable above current level Do more test for validation
                index_value_col += [j]
        # Get max ratio (q+epsilon)/a_j
        max_row_index = self.max_coefEpsilon(col_q, col_enter, index_value_col)
        # Make pivot of row and column and the other row update
        self.pivot_row_col(max_row_index, index_col, index_value_col)
        return self.switch_var_base(max_row_index, index_col)

    def max_coefEpsilon(self, col_q, col_enter, index_value_col):
        """
        Given a column to pivot, return the row with the \
maximum value when pivoted.

        """
        max_value = -math.inf
        col_epsi = self.tucker[:, -1]
        for j in index_value_col:
            if col_enter[j] < 0:
                tmpMax = ((col_q[j]) + col_epsi[j]) / (col_enter[j])
                if max_value < tmpMax:
                    max_value = tmpMax
                    max_row_index = j
        return max_row_index

    def pivot_row_col(self, index_row, index_col, index_value_col):
        """
        Given a row and column to pivot, compute the updated Tucker scheme.

        """
        # Get row of pivot
        new_rowj = self.tucker[index_row]
        coef_of_enter = new_rowj[index_col]
        # Switch the column and row variable
        for k in range(len(new_rowj)):
            if k == index_col:
                new_rowj[index_col] = Fraction(1, coef_of_enter)
            else:
                new_rowj[k] = Fraction(new_rowj[k], -coef_of_enter)
        # Update the row of the variables concerned by the pivot
        for j in index_value_col:
            if j != index_row:
                coef_in_j = self.tucker[j, index_col]
                subrow = new_rowj.copy()
                for k in range(len(subrow)):
                    subrow[k] = (subrow[k]) * coef_in_j
                self.tucker[j] = self.tucker[j] + subrow
                self.tucker[j, index_col] = subrow[index_col]

    def switch_var_base(self, index_row, index_col):
        """
        Given variable index of the row and column to switch, \
update the basis accordingly.

        """
        outbase = self.row_var_by_index[index_row]
        inbase = self.col_var_by_index[index_col]
        self.row_var_by_index[index_row] = inbase
        self.col_var_by_index[index_col] = outbase
        self.col_var.pop(inbase)
        self.row_var.pop(outbase)
        self.col_var[outbase] = index_col
        self.row_var[inbase] = index_row
        return outbase

    def launch_solver(self, list_action):
        """
        Launches Lemke Howson algorithm on the current polymatrix game, using \
input joint strategy.

        :param ``LHpolymatrix`` self: The polymatrix game solver instance.
        :param list list_action: Joint strategy used to initialize \
Lemke-Howson's algorithm.
        :returns: A mixed Nash equilibrium.
        :rtype: list.

        """
        self.tucker_schema()
        return self.lemke(list_action)
