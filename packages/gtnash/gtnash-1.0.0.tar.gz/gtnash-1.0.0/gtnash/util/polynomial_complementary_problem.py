"""
Polynomial complementarity problems definition and solution.

Classes:
--------

- Class ``PolynomialComplementaryProblem``:
    An instance of the class provides a polynomial complementarity problem \
definition from a (hypergraphical) game as well as methods for solving it.

- Class ``Subsystem``:
    An instance of the class is a system of equations/inequations constructed \
from a PCP and a choice of subsets of equations given as input.


Detailed description of the classes
-----------------------------------

"""
import numpy as np
from sage.all import QQ, QQbar, PolynomialRing, ideal, prod
from gtnash.game.hypergraphicalgame import HGG
from copy import deepcopy


class PolynomialComplementaryProblem:
    """
    Class creating and solving polynomial complementarity problems from a game

    :param HGG game: Input game.
    :param list omega0: arbitrary fixed joint strategy.
    :param boolean fact_y: True if variable Y are to be used to \
    in the polynomials, False otherwise

    Attributes
    ----------
    :param ``HGG`` game: The game from which the PCP is constructed.
    :param list set_x: List of string of the variables x used in the PCP.
    :param list set_y: List of strings of the variables y^n_g used in \
subsystems in the cas of hypergraphical games.
    :param list set_poly: List of the polyomials of the PCP.
    :param dict couple_to_x: Associates string variables xnj to couples (n,j).
    :param dict couple_to_y: Associatea string variables yng to couples (n,g).
    :param dict couple_to_poly: Associates polynomials Anj to couples (n,j).
    :param dict couple_to_poly_y: Associates poly yn_g - yn'_g.sum(xn_i) \
to couples (n,g) where n' is the index of P - Pg just before n.
    :param dict id_to_act: Associates allowed actions to players' id.
    :param dict id_to_nb_act: Associates number of allowed actions to players.
    :param ``PolynomialRing`` ring: Polynomial ring used in the PCP.
    :param dict omega0: omega0[n] is the non-dominated alternative \
of player n of lowest index
    :param dict x_omega0: x_omega0[(n,omega0[n])] = 1 and \
x_omega0[(n,i)]=0 if i!=omega0[n], for all players n.
    :param list z0: List of dominated alternatives (n,i) obtained after irda.

    """

    def __init__(self, game, omega0=[], fact_y=True):
        self.game_tmp = game
        self.game = self.transform_game_to_hgg()
        self.id_to_act = self.generate_id_to_act()
        self.id_to_nb_act = self.generate_id_to_nb_act()
        self.set_x = []
        self.couple_to_x = {}
        self.set_y = []
        self.couple_to_y = {}
        self.gen_var_x()
        if fact_y:
            self.gen_var_y()
        # Ring:
        var_xy = self.set_x + self.set_y
        self.ring = PolynomialRing(QQbar, var_xy, order='lex')
        self.couple_to_poly = {}
        self.generate_poly(fact_y)
        self.couple_to_poly_y = {}
        if fact_y:
            self.generate_poly_y()
        if not omega0:
            # self.gen_omega0()
            self.omega0 = {}
            for n in range(self.game.n_players - 1, -1,
                           -1):  # players in reverse order
                self.omega0[n] = min([i for i in self.game.players_actions[n]])
        else:
            self.omega0 = omega0

    def __str__(self):
        result = "Variables:\n"
        for var in self.set_x:
            result += var
            result += "' "
        for var in self.set_y:
            result += var
            result += "' "
        result += "\nPolynomials Ani(x):\n"
        for pol in self.couple_to_poly.keys():
            result += f"{pol}: {self.couple_to_poly[pol]}\n"
        result += "\nPolynomials yng(x):\n"
        for pol in self.couple_to_poly_y.keys():
            result += f"{pol}: {self.couple_to_poly_y[pol]}\n"
        return result

    def transform_game_to_hgg(self):
        """
        Transform the input game of the PCP into an hypergraphical game.

        :param PolynomialComplementaryProblem self: The PCP object \
with game attribute.

        :returns: A hypergraphical game.
        :rtype: ``HGG``.

        """
        # If it's a HGG#TO CHANGE BHGG ALSO HAS A hypergraph ATTRIBUTE
        # hasattr(self.game_tmp, 'hypergraph'):
        if isinstance(self.game_tmp, HGG):
            return self.game_tmp
        # If it's a NFG
        else:
            return HGG.convert_to_HGG(self.game_tmp)

    def generate_id_to_act(self):
        """
        Generates a dictionnary {index of player:list of her actions).

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: id_to_act: player-to-action dictionary.
        :rtype: dict.

        """
        id_to_act = {}
        for i in range(self.game.n_players):
            id_to_act[i] = self.game.players_actions[i]
        return id_to_act

    def generate_id_to_nb_act(self):
        """
        Generates a dictionary {index of player:number of her actions).

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: id_to_nb_act: player-to-number of actions dictionary.
        :rtype: dict.

        """
        id_to_nb_act = {}
        for n in range(self.game.n_players):
            id_to_nb_act[n] = len(self.game.players_actions[n])
        return id_to_nb_act

    def gen_var_x(self):
        """
        Generates dictionary {variable xni:string 'xn_i'} for the variables \
and updates ``self`` attribute ``couple_to_x``.

        :param PolynomialComplementaryProblem self: A PCP object.

        """
        # Generate all the variable x used in the pcp
        for n in range(self.game.n_players):
            for j in self.game.players_actions[n]:
                var_x = f'x{n}_{j}'
                self.set_x += [var_x]
                self.couple_to_x[(n, j)] = var_x

    def gen_var_y(self):
        """
        Generates dictionary {variable ynj:string 'yn_j'} for the variables y \
and updates ``self`` attribute ``couple_to_y``.

        :param PolynomialComplementaryProblem self: A PCP object.

       """
        hypergraph = self.game.hypergraph
        for n in range(self.game.n_players):
            for g in range(len(hypergraph)):
                # if n not in hypergraph[g]:
                var_y = f'y{n}_{g}'
                self.set_y += [var_y]
                self.couple_to_y[(n, g)] = var_y

    def substitute(self, x_values, level):
        """
        Substitutes some variables of the PCP with prescribed values.

        :param PolynomialComplementaryProblem self: A PCP object.
        :param dict x_values: Associates value to some variable xn_i.
        :param int level: Only substitutes for variables xn_i with n<level.

        :returns: subpcp: Polynomial complementarity subproblem.
        :rtype: ``PolynomialComplementaryProblem``.

        """
        # To improve, by using a reduced_dico n<level
        # an poly.subs(reduced_dico)
        sub_pcp = deepcopy(self)
        for (n, i) in self.couple_to_poly.keys():
            poly = self.couple_to_poly[(n, i)]
            for variab, valu in x_values.items():
                poly = eval('poly.subs(' + str(variab) + '=valu)')
            if n <= level:
                sub_pcp.couple_to_poly[(n, i)] = poly
            else:
                sub_pcp.couple_to_poly.pop((n, i))
        return sub_pcp

    def get_negative_utilities(self):
        """
        Returns the utilities of an equivalent game with negative utilities.

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: copy_util: Negative utilities of an equivalent game.
        :rtype: List of Numpy arrays.

        """
        # copy_util=np.array(self.game.utilities)
        copy_util = [np.array(e_u) for e_u in self.game.utilities]
        for n in range(self.game.n_players):
            max_of_n = self.game.get_max_value_of_player_n(n)
            if max_of_n >= 0:
                e_to_index = self.game.index_of_player_in_local(n)
                for e_i in e_to_index.keys():
                    copy_util[e_i][e_to_index[e_i]] = [val - (max_of_n + 1) for
                                                       val in copy_util[e_i][
                                                           e_to_index[e_i]]]
                    # copy_util[e_i, e_to_index[e_i]]=[val -(max_of_n+1)
                    # for val in copy_util[e_i,e_to_index[e_i]]]
                    # copy_util[e_i,e_to_index[e_i]]-=(max_of_n+1)
        return copy_util

    def generate_Q(self):
        """
        For each local game (only 1 if NFG) creates the variables y^N_g \
and creates Q[g] = y^N_g. Old version (incorrect). To suppress?

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: poly_Q: List of Sagemath variables.
        :rtype: Sagemath variables.

        """
        poly_Q = {}
        nlocgames = len(self.game.hypergraph)
        nplayers = len(self.game.players_actions)
        for g in range(nlocgames):
            poly_Q[g] = self.ring(self.couple_to_y[(nplayers - 1, g)])
        return poly_Q

    def generate_Q_alt(self):
        """
        For each local game (only 1 if NFG) creates the variables y^N_g \
and creates Q[g] = y^N_g. New version (correct).

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: poly_Q: List of Sagemath polynomials.
        :rtype: Sagemath polynomials.
        """
        poly_Q = {}
        nlocgames = len(self.game.hypergraph)
        nplayers = len(self.game.players_actions)
        for g in range(nlocgames):
            sys_S = []
            for n in range(nplayers):
                if n not in self.game.hypergraph[g]:
                    sys_S.append(sum(
                        self.ring(self.couple_to_x[(n, i)]) for i in
                        self.game.players_actions[n]))
            poly_Q[g] = prod(sys_S)
        return poly_Q

    def generate_R(self):
        """
        Generates a dictionary R, where R[(n,i,g)] = R_{n,i,g} for \
any local game g involving player n and action i of n (see documentation).

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: poly_r: List of Sagemath polynomials.
        :rtype: Sagemath polynomials.

        """
        poly_r = {}
        hypergraph = self.game.hypergraph
        nlocgames = len(self.game.hypergraph)
        nplayers = len(self.game.players_actions)
        negative_util = self.get_negative_utilities()
        for n in range(nplayers):
            for i in self.game.players_actions[n]:
                for g in range(nlocgames):
                    if n in hypergraph[g]:
                        index_n = hypergraph[g].index(n)
                        locgame_players_actions = \
                            self.game.local_normalformgames[g].joint_actions
                        locgame_utilities = negative_util[g]
                        sys_s = []
                        for index_w in range(locgame_players_actions.shape[0]):
                            w = [locgame_players_actions[index_w, k] for k in
                                 range(locgame_players_actions.shape[1])]
                            if w[index_n] == i:
                                pw = QQ(locgame_utilities[index_n][index_w])
                                for index_nu in range(len(hypergraph[g])):
                                    if index_nu != index_n:
                                        nu = hypergraph[g][index_nu]
                                        pw *= \
                                            self.ring(
                                                self.couple_to_x[(
                                                    nu,
                                                    locgame_players_actions[
                                                        index_w, index_nu])])
                                sys_s.append(pw)
                        poly_r[(n, i, g)] = sum(sys_s)
        return poly_r

    def generate_poly(self, fact_y):
        """
        Generates the polynomials of the PCP.

        :param PolynomialComplementaryProblem self: A PCP object.
        :param boolean fact_y: True if variable Y are to be used

        :returns: couple_to_poly: List of Sagemath polynomials.
        :rtype: Sagemath polynomials.

        """
        couple_to_poly = {}
        hypergraph = self.game.hypergraph
        nlocgames = len(self.game.hypergraph)
        nplayers = len(self.game.players_actions)
        poly_r = self.generate_R()
        if fact_y:
            poly_q = self.generate_Q()
            for n in range(nplayers):
                for i in self.game.players_actions[n]:
                    couple_to_poly[(n, i)] = 0
                    for g in range(nlocgames):
                        if n in hypergraph[g]:
                            couple_to_poly[(n, i)] -=\
                                poly_q[g] * poly_r[(n, i, g)]
                    couple_to_poly[(n, i)] -= 1
        else:
            poly_q = self.generate_poly_fact()
            for n in range(nplayers):
                for i in self.game.players_actions[n]:
                    couple_to_poly[(n, i)] = 0
                    for g in range(nlocgames):
                        if n in hypergraph[g]:
                            couple_to_poly[(n, i)] -=\
                                (poly_q[g]) * poly_r[(n, i, g)]
                    couple_to_poly[(n, i)] -= 1
        self.couple_to_poly = couple_to_poly

    def generate_poly_y(self):
        """
        Generates the additional polynomials defining the yng. \
Useful only for hypergraphical games.

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: couple_to_poly_y: List of Sagemath polynomials.
        :rtype: Sagemath polynomials.

        """
        couple_to_poly_y = {}
        hypergraph = self.game.hypergraph
        nplayers = self.game.n_players
        for g in range(len(hypergraph)):
            for n in range(nplayers):
                polyloc = self.ring(self.couple_to_y[(n, g)])
                if n == 0:
                    if n in hypergraph[g]:
                        couple_to_poly_y[(n, g)] = polyloc - 1
                    else:
                        couple_to_poly_y[(n, g)] = polyloc - sum(
                            self.ring(self.couple_to_x[(n, i)])
                            for i in self.game.players_actions[n])
                else:
                    if n in hypergraph[g]:
                        couple_to_poly_y[(n, g)] = polyloc - self.ring(
                            self.couple_to_y[(n - 1, g)])
                    else:
                        couple_to_poly_y[(n, g)] = polyloc - self.ring(
                            self.couple_to_y[(n - 1, g)]) * sum(
                            self.ring(self.couple_to_x[(n, i)]) for i in
                            self.game.players_actions[n])
        self.couple_to_poly_y = couple_to_poly_y

    def generate_poly_fact(self):
        """
        Generates the additional monomials of the player not playing
        in each local game. \
        Useful only for hypergraphical games.

        :param PolynomialComplementaryProblem self: A PCP object.

        :returns: couple_to_poly_fact: List of Sagemath polynomials.
        :rtype: Sagemath polynomials.

        """
        couple_to_poly_fact = {}
        hypergraph = self.game.hypergraph
        nplayers = self.game.n_players
        for g in range(len(hypergraph)):
            couple_to_poly_fact[g] = 1
            for n in range(nplayers):
                # polyloc = 1
                # polyloc = self.ring(self.couple_to_y[(n, g)])
                # if n == 0:
                #     if n in hypergraph[g]:
                #         couple_to_poly_fact[(n, g)] = polyloc - 1
                #     else:
                #         couple_to_poly_fact[(n, g)] = polyloc - sum(
                #             self.ring(self.couple_to_x[(n, i)])
                #             for i in self.game.players_actions[n])
                if n in hypergraph[g]:
                    couple_to_poly_fact[g] = couple_to_poly_fact[g] * 1
                else:
                    couple_to_poly_fact[g] = couple_to_poly_fact[g] * sum(
                        self.ring(self.couple_to_x[(n, i)])
                        for i in self.game.players_actions[n])
        return couple_to_poly_fact


class Subsystem:
    """
    Construction and solution of systems of polynomial equations.

    :param list equations: List of polynomials.
    :param list inequations: List of polynomials.
    :param ring: Ring (Sagemath object) in which solutions are looked for.
    :param ideal: Ideal of the set of equations (Sagemath object).
    :param int idealdimension: Dimension of the ideal of the set of equations.
    :param variety: Variety of the ideal (sgaemath object), \
if of dimension 0. Else, empty.
    :param int nbsols: Number of solutions of the system (can be 0 or +infty).
    :param dict solution: Coordinates of a solution of the system, when unique.

    """

    def __init__(self, pcp, z, w, level, xpairs_val):
        """
        Constructs a subsystem of a PCP.
        """
        # Level:
        self.level = level
        # Keep track of z and w:
        self.set_z = z
        self.set_w = w
        # Ring:
        self.ring = pcp.ring
        # Equations:
        self.equations = self.generate_equations(pcp, z, w, level, xpairs_val)
        # Inequations:
        self.inequations = self.generate_inequations(pcp, z, w, level,
                                                     xpairs_val)
        # Ideal of the equations
        self.ideal = self.compute_ideal()
        self.idealdimension = self.ideal.dimension()
        # Variety
        self.variety = self.compute_variety()
        self.solutions = self.compute_solutions()
        if self.idealdimension == 0:
            self.nbsols = len(self.solutions)
            if self.nbsols > 1:  # Should be impossible
                self.solutions = [self.solutions[0]]
                self.nbsols = 1
                # raise Error("Test")
        else:
            self.nbsols = np.inf

    def __str__(self):
        niceprint = "Ring: "
        niceprint += str(self.ring) + "\n"
        niceprint += "Level:" + str(self.level) + "\n"
        niceprint += "Equations:\n"
        for e in range(len(self.equations)):
            niceprint += str(self.equations[e]) + " = 0\n"
        niceprint += "Inequations:\n"
        for e in range(len(self.inequations)):
            niceprint += str(self.inequations[e]) + " >=0\n"
        niceprint += "Dimension of the ideal: " + str(
            self.idealdimension) + "\n"
        niceprint += "Variety: " + str(self.variety) + "\n"
        niceprint += "Number of solutions: " + str(self.nbsols) + "\n"
        niceprint += "Solutions: " + str(self.solutions) + "\n"
        return (niceprint)

    def generate_equations(self, pcp, z, w, level, xpairs_val):
        """
        Generates the set of equations of the subsystem of pcp, given z, w \
and level.

        :param ``PolynomialComplementaryProblem`` pcp: The input PCP.
        :param set z: Set of pairs (n,i) where xn_i = 0.
        :param set w: Set of pairs (n,i) where Pn_i(x) = 0.
        :param int level: Current level.
        :param dict xpairs_val: Values of svariable above the current level.

        :returns: equations: List of polynomial equations (including \
variables set to 0) that are in the subsystem.
        :rtype: list.

        """
        equations = [pcp.ring(pcp.couple_to_x[(n, i)]) for (n, i) in
                     z]  # was self.ring
        dico = {}
        for e in range(len(equations)):
            dico[equations[e]] = 0
        subpcp = pcp.substitute(dico, level)
        # Zero polynomials equation:
        equations += [subpcp.couple_to_poly[(n, i)] for (n, i) in w if
                      n <= level]
        # Add equations defining the y
        equations += [pcp.couple_to_poly_y[(n, g)] for (n, g) in
                      pcp.couple_to_poly_y.keys()]
        # Add fixed variables values for n>level
        equations += [pcp.ring(pcp.couple_to_x[(n, i)]) - xpairs_val[(n, i)]
                      for (n, i) in pcp.couple_to_x.keys() if n > level]
        # That's it for equations
        return equations

    def generate_inequations(self, pcp, z, w, level, xpairs_val):
        """
         Generates the set of inequations of the subsystem of pcp, given z, w \
and level.

        :param ``PolynomialComplementaryProblem`` pcp: The input PCP.
        :param set z: Set of pairs (n,i) where xn_i = 0.
        :param set w: Set of pairs (n,i) where Pn_i(x) = 0.
        :param int level: Current level.
        :param dict xpairs_val: Values of svariable above the current level.

        :returns: inequations: List of polynomial inequations (including \
variables >= 0) that are in the subsystem.
        :rtype: list.

        """
        x_values = {}
        for (n, i) in pcp.couple_to_x.keys():
            if (n, i) in z:
                x_values[
                    self.ring(pcp.couple_to_x[(n, i)])] = 0  # was pcp.ring
            # if n>level:
            #    x_values[pcp.ring(pcp.couple_to_x[(n,i)])] = xpairs_val[(n,i)]
        subpcp = pcp.substitute(x_values, level)
        inequations = [subpcp.couple_to_poly[(n, i)] for (n, i) in
                       set(pcp.couple_to_x.keys()).intersection(
                           set(subpcp.couple_to_poly.keys())) if
                       (n, i) not in w]
        return inequations

    def compute_ideal(self):
        """
        Returns the ideal of the set of equation of the input subsytem.

        :param Subsystem self: Input subsystem.

        :returns: Ideal of the set of equations (Sagemath object).

        """
        return ideal(self.equations)

    def compute_variety(self):
        """
        Returns the variety corresponding to the ideal of the set of \
equations of the input subsytem, if the latter is of dimension 0.

        :param Subsystem self: Input subsystem.

        :returns: Variety of the set of equations (Sagemath object).
        :rtype: list of dict.

        """
        if self.idealdimension != 0:
            return []
        else:
            return self.ideal.variety()

    def compute_solutions(self):
        """
        Returns the feasible solutions of the variety.

        :param Subsystem self: Input subsystem.

        :returns: Feasible solutions.
        :rtype: list of dict.

        """
        solutions = []
        for dict_sol in self.variety:
            if all([v.imag() == 0 for v in dict_sol.values()]):
                feasible, slacks = self.feasible_point(dict_sol)
                if feasible:
                    solutions += [dict_sol]
        return solutions

    def feasible_point(self, dict_point):
        """
        Checks whether a point is feasible.

        :param dict dict_point: Coordinates of a point.

        :returns: ``True`` if the point is feasible and ``False`` else.
        :returns: The list of "slacks" of the inequations.
        :rtype: bool and list.

        """
        slacks = [s for s in dict_point.values()]
        for ineq in self.inequations:
            slacks.append(ineq.subs(dict_point))
        if all(s >= 0 for s in slacks):
            feasible = True
        else:
            feasible = False
        return feasible, slacks
