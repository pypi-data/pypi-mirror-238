"""Implementation of Wilson's algorithm, the combinatorial way.

Classes
-------

- Class ``Node``:
    An instance of the class includes the (algebraic and combinatorial)
    representations of a node in Wilson's algorithm, as well as methods used in
    the algorithm.

- Class ``NodePathData``:
    An instance of the class stores the full path to a node, as followed by
    Wilson's algorithm.

- Class ``WilsonError``:
    This error is raised when Wilson's algorithm fails, for whichever reason.

Module's methods
----------------

- ``wilson(game)``:
    Takes a game as input and returns acomplementary node at level N,
    including the equilibrium coordinates.
    It applies IRDA, then build an PCP representation of the game (using an
    external module) and then applies Wilson's algorithm to the PCP.

- ``irda_on_game(game)``:
    Transforms a game into a HGG if it is not yet and applies IRDA.

- ``first_node(pcp)``:
    Takes a pcp as input and returns a complementary node at level 0.

- ``wilson_loop(pcp)``:
    Applies Wilson's algorithm to the polynomial complementarity problem *pcp*.

Detailed description of classes and methods
-------------------------------------------

"""

from gtnash.game.hypergraphicalgame import HGG
from gtnash.game.normalformgame import NFG
from gtnash.game.bayesiangame import BG
from gtnash.util.polynomial_complementary_problem import \
    PolynomialComplementaryProblem, Subsystem
from gtnash.util.irda import irda
from sage.all import QQbar
from copy import deepcopy
import itertools


class WilsonError(Exception):
    """
    Error ``WilsonError`` is returned when the program fails for an unknown \
reason.
    """
    pass


def first_node(pcp, xpairs_val):
    """
    Takes a pcp as input and returns its complementary node at level 0.

    :param ``PolynomialComplementaryProblem`` pcp: \
A Polynomial Complementarity problem.
    :param dictionary xpairs_val: xpairs_val[(n,i)] is the initial value \
of xni.

    :returns: nextnodeslist, a list of potnential initial complementary nodes \
    ( a single one if the game is non-dgenerate).
    :rtype: list of ``Node``.

    """
    x_values_level_0 = {pcp.couple_to_x[(n, i)]: xpairs_val[(n, i)] for (n, i)
                        in pcp.couple_to_x.keys() if n > 0}
    subpcp = pcp.substitute(x_values_level_0, 0)
    minval = min(
        [sum(v.coefficients()) for v in subpcp.couple_to_poly.values()])
    set_w = [(n, i) for (n, i) in subpcp.couple_to_poly.keys() if
             sum(subpcp.couple_to_poly[(n, i)].coefficients()) == minval]
    level = 0
    sys_s = []
    nextnodeslist = []
    if len(set_w) > 1:
        print("First node is degenerate.")
        print("Several pairs can be added to W: ", set_w)
    if len(set_w) == 0:
        raise WilsonError(
            "Ouch! No almost complementary point at level 0, that's strange!")
    for (m, j) in set_w:
        # if (len(set_w)==1):
        set_z = [(n, i) for (n, i) in subpcp.couple_to_poly.keys() if
                 (n, i) != (m, j)]  # not in set_w]
        sols = {}
        sols[pcp.ring(pcp.couple_to_x[(m, j)])] = 1
        for (n, i) in set_z:
            sols[pcp.ring(pcp.couple_to_x[(n, i)])] = 0
        node0 = Node(subpcp, set_z, [(m, j)], level, xpairs_val, sys_s, sols)
        node0.check_complementarity()
        nextnodeslist.append(node0)
    return nextnodeslist


def wilson(game):
    """
    Takes a game as output and returns a Nash equilibrium.

    :param ``AbstractGame`` game: A game of any class.
    :returns: A  Nash equilibrium.
    :rtype: dict.

    """
    reduced_hgg, z0 = irda_on_game(game)
    pcpglobal = PolynomialComplementaryProblem(reduced_hgg)
    node = wilson_loop(pcpglobal)
    proba = node.normalized_strategy()
    return proba_from_reduced_to_normal(proba, z0)


def irda_on_game(game):
    """
    Transforms a game into a HGG and applies IRDA.

    :param ``AbstractGame`` game: A game of any class.
    :returns: reduced_hgg: a reduced hypergraphical game.
    :returns: z0: a list of dominated alternatives.
    :rtype: ``HGG`` and list.

    """
    if isinstance(game, NFG):
        # hgg = HGG([[0]], [[[0]]], [[0]])
        # hgg = hgg.convert_to_HGG(game)
        hgg = HGG.convert_to_HGG(game)
    elif isinstance(game, BG):
        hgg = BG.convert_to_HGG()
    else:
        hgg = game
    reduced_hgg, z0 = irda(hgg)
    return reduced_hgg, z0


def proba_from_reduced_to_normal(proba, z_excluded):
    """
    Converts a mixed strategy of a reduced game to one of the initial game.

    :param dict proba: Joint mixed strategy assigning a list of probabilities \
to each player.
    :param list z_excluded: List of pairs (player,action) of dominated \
strategies.
    :returns: new_prob: A joint strategy of the initial game.
    :rtype: dict.

    """
    new_prob = {}
    for n in proba.keys():
        n_act = proba[n]
        z_excluded_of_n = [coup for coup in z_excluded if coup[0] == n]
        proba_of_n = []
        index_old_prob = 0
        for n_i in range(len(n_act) + len(z_excluded_of_n)):
            if (n, n_i) in z_excluded_of_n:
                proba_of_n += [0]
            else:
                proba_of_n += [n_act[index_old_prob]]
                index_old_prob += 1
        new_prob[n] = proba_of_n
    return new_prob


def gen_all_omega0(game):
    """
    Generates all the possible pure joint strategies of an input game.

    :param ``Abstractgame`` game: Input game.
    :returns: all_joint_actions: The list of all joint actions.
    :rtype: list.

    """
    all_joint_actions = list(itertools.product(*game.players_actions))
    all_dict_joint_actions = []
    for ja in all_joint_actions:
        joint_act_dic = {}
        for n in range(len(ja)):
            joint_act_dic[n] = ja[n]
        all_dict_joint_actions += [joint_act_dic]
    return all_joint_actions


def gen_only_omega_to_used(game):
    """
    Generates all the possible pure joint strategies of an input game.

    :param ``Abstractgame`` game: Input game.
    :returns: all_joint_actions: The list of all joint actions.
    :rtype: list.

    """
    print(game.players_actions)
    all_joint_actions = list(itertools.product(
        *[[game.players_actions[0][0]]] + [pact for n, pact in
                                           enumerate(game.players_actions) if
                                           not n == 0]))
    all_dict_joint_actions = []
    for ja in all_joint_actions:
        joint_act_dic = {}
        for n in range(len(ja)):
            joint_act_dic[n] = ja[n]
        all_dict_joint_actions += [joint_act_dic]
    return all_joint_actions


def wilson_loop(pcpglobal):
    """
    Applies Wilson' algorithm to find a solution of an input PCP.

    :param ``PolynomialComplementaryProblem`` pcpglobal: The input PCP.
    :returns: currentnode: A solution of the PCP.
    :rtype: ``Node``.

    """
    xpairs_val = {}
    for (n, i) in pcpglobal.couple_to_x.keys():
        if pcpglobal.omega0[n] == i:
            xpairs_val[(n, i)] = 1
        else:
            xpairs_val[(n, i)] = 0
    # Maintain a list of visited nodes, in order to account for degeneracy.
    visitednodes = []
    opennodes = []
    # Now, we start path following.
    nextnodeslist = first_node(pcpglobal, xpairs_val)
    if len(nextnodeslist) == 0:
        raise WilsonError("Normally we always have at least one first node!")
    elif len(nextnodeslist) > 1:
        print("Node 0 is degenerate.")
    opennodes += nextnodeslist
    currentnode = None
    # Main loop
    while len(opennodes) > 0:
        last_var = -1
        nextnode = opennodes.pop(last_var)
        while len(opennodes) > 0 and nextnode.already_visited(visitednodes):
            nextnode = opennodes.pop(last_var)
        currentnode = nextnode
        visitednodes.append(currentnode)
        if currentnode.is_complementary and \
                currentnode.level == pcpglobal.game.n_players - 1:
            break  # we are done
        if currentnode.is_complementary and (
                currentnode.level == 0 or
                currentnode.level >= currentnode.prev_node.level):
            nextnodeslist = currentnode.lift(pcpglobal, xpairs_val)
        elif currentnode.is_initial and \
                currentnode.level <= currentnode.prev_node.level:
            nextnodeslist = currentnode.descend(currentnode.pcp, xpairs_val)
            # Update xpairs_val
            level = currentnode.level
            xpairs_val[
                (level, pcpglobal.omega0[level])] = currentnode.coordinates[
                pcpglobal.couple_to_x[(level, pcpglobal.omega0[level])]]
        else:
            nextnodeslist = currentnode.traverse(currentnode.prev_node,
                                                 xpairs_val)
            # Deal with degeneracy, cycles or impossible pivots.
        if len(nextnodeslist) == 0:
            print(
                "Current path in Wilson's algorithm leads nowhere."
                " We have to backtrack.")
        else:
            if len(nextnodeslist) > 1:
                print("Current node is degenerate.")
        opennodes += nextnodeslist
    if currentnode.level < pcpglobal.game.n_players - 1:
        raise WilsonError("Cannot continue")
    return currentnode


class NodePathData:
    """
    Provides a set of methods to compute the path followed by Wilson's \
algorithm, as well as some statistics about this path.

    Attributes
    ----------
    listZW: list
        list of the pairs (Z,W) of the nodes encountered along the path.
    level_to_number_of_node: dict
        Number of nodes encountered at each level.
    level_to_number_of_comp: dictionary
        Number of complementary nodes encountered at each level.
    level_to_number_of_init: dictionary
        Number of initial nodes encountered at each level
    degen_encount: boolean
        True if a degenerate node has been encountered.
    max_size_W: int
        Size of the largest set W encountered (largest system of equations).

    """

    def __init__(self, n_player):
        """Node path data constructor.
        """
        self.listZW = []
        self.level_to_number_of_node = {n: 0 for n in range(n_player)}
        self.level_to_number_of_comp = {n: 0 for n in range(n_player)}
        self.level_to_number_of_init = {n: 0 for n in range(n_player)}
        self.degen_encount = False
        self.max_size_W = 0

    def get_data_node_path(self, tmp_node):
        """
        Appends tmp_node to the path.

        :param ``Node`` tmp_node: Current Node.

        """
        current_node = tmp_node
        while current_node is not None:
            level_k = current_node.level
            self.listZW.insert(0, (current_node.set_z, current_node.set_w))
            self.level_to_number_of_node[level_k] += 1
            if current_node.is_complementary:
                self.level_to_number_of_comp[level_k] += 1
            if current_node.is_initial:
                self.level_to_number_of_init[level_k] += 1
            if current_node.is_degenerate:
                self.degen_encount = True
            if len(current_node.set_w) > self.max_size_W:
                self.max_size_W = len(current_node.set_w)
            current_node = current_node.prev_node

    def get_sum_node(self, level_to_nb):
        """
        Get the number of nodes in the path to complementary node.

        :param dict level_to_nb: Number of nodes for each level.
        :returns: res: Number of nodes in the path.
        :rtype: int.

        """
        res = 0
        for k in level_to_nb.keys():
            res += level_to_nb[k]
        return res

    def get_total_node(self):
        """
        Number of nodes in the path to complementary node.

        :param ``NodePathData`` self: The path data.
        :returns: res: Number of nodes in the path.
        :rtype: int.

        """
        return self.get_sum_node(self.level_to_number_of_node)

    def get_total_node_comp(self):
        """
        Number of complementary nodes in the path to complementary node.

        :param ``NodePathData`` self: The path data.
        :returns: Number of complementary nodes in the path.
        :rtype: int.

        """
        return self.get_sum_node(self.level_to_number_of_comp)

    def get_total_node_init(self):
        """
        Number of initial nodes in the path to complementary node.

        :param ``NodePathData`` self: The path data.
        :returns: res_str: Number of initial nodes in the path.
        :rtype: int.

        """
        return self.get_sum_node(self.level_to_number_of_init)

    def __str__(self):
        res_str = "PathData\n"
        res_str += f"Number of node by level: {self.level_to_number_of_node}\n"
        res_str += \
            f"Number of complementary node by level:" \
            f" {self.level_to_number_of_comp}\n"
        res_str += f"Number of initial node by level:" \
                   f" {self.level_to_number_of_init}\n"
        res_str += f"Max number of polynomials in the system:" \
                   f" {self.max_size_W}\n"
        res_str += f"Is degenerate: {self.degen_encount}"
        return res_str


class Node:
    """
    Data structure representing a node of a path in Wilson's algorithm.

    Attributes
    ----------
    pcp: Polynomial Complementarity Problem
        the pcp from which the node is issued.
    set_z: list
        The set of couple (n,j) corresponding to
        the variable x_nj equal to 0 for the node.
    set_w: list
        The set of couple (n,j) corresponding to
        the variable A_nj equal to 0 for the node.
    level: int
        Level of the node.
    xpairs_val: dictionary
        Coordinates above level k (x in S^{z,w}_level(x) ): xpairs_val[(n,i)].
    sys_S: PCP subsystem
        System of equations defining the node.
    coordinates: dictionary
        Coordinates of the Node.
    is_complementary: boolean
        Is the node complementary?
    is_almost_complementary: boolean
        Is the node almost complementary?
    is_initial: boolean
        Is the node initial?
    is_degenerate: boolean
        Is the node degenerate?
    prev_node: Node
        The previous node encountered by the algorithm

    """

    def __init__(self, pcp, set_z, set_w, level, xpairs_val, sys_S,
                 coordinates):
        """
        Creates a complementary node at level 0, from an input PCP.

        """
        self.pcp = deepcopy(pcp)
        self.set_z = set_z
        self.set_w = set_w
        self.level = level
        self.xpairs_val = xpairs_val
        self.sys_S = sys_S
        self.coordinates = coordinates
        # Check complementarity:
        self.prev_node = None
        self.is_complementary = False
        self.is_almost_complementary = False
        self.is_initial = False
        self.is_degenerate = False

        self.check_complementarity()
        # Check degeneracy: The node 0 in the example is degenerate!

    def __str__(self):
        strnode = "Level: {0}\n".format(self.level)
        strnode += "local PCP:\n"
        strnode += self.pcp.__str__()
        strnode += "\n"
        for n in range(self.level + 1, self.pcp.game.n_players):
            for i in self.pcp.game.players_actions[n]:
                strnode += "xpairs_val[({0},{1})] = {2}\n".\
                    format(n, i, self.xpairs_val[(n, i)])
        strnode += "set_z: {0}\n".format(self.set_z)
        strnode += "set_w:{0}\n".format(self.set_w)
        strnode += "System defining the node:\n"
        strnode += self.sys_S.__str__() + "\n"
        strnode += "Coordinates of the node: {0}\n".format(self.coordinates)
        return strnode

    def check_complementarity(self):
        """
        Tells whether node is complementary, , allmost Omega0-complementary \
or initial.

        """
        level = self.level
        omega0level = self.pcp.omega0[level]
        set_z = set(self.set_z)
        set_w = set(self.set_w)
        all_couples = set(
            [(n, i) for (n, i) in self.pcp.couple_to_x.keys() if n <= level])
        z_union_w = set_z.union(set_w)
        card = len(set_z) + len(set_w)
        is_initial = False
        is_complementary = False
        is_almost_complementary = False
        if card == len(all_couples):
            if z_union_w == all_couples:
                is_complementary = True
            if all_couples.difference(z_union_w).issubset(
                    set([(level, self.pcp.omega0[level])])):
                is_almost_complementary = True
            if is_complementary or is_almost_complementary:
                if (level, omega0level) not in set_z:
                    is_initial = True
                    for (n, i) in all_couples:
                        if n == level and i != omega0level:
                            if (n, i) not in set_z:
                                is_initial = False
                                break
        self.is_complementary = is_complementary
        self.is_almost_complementary = is_almost_complementary
        self.is_initial = is_initial
        self.is_degenerate = False

    def check_degeneracy(self, entering_z, entering_w):
        """
        Checks whether the node is degenerate and, if so, \
returns the possible entering pairs in z and w.

        :param list entering_z: The singleton [(n,i)] that has just entered z \
or [] if it was a w that entered.
        :param list entering_w: The singleton [(n,i)] that has just entered w \
or [] if it was a z that entered.
        :returns: is_degenerate: ``True`` if the node is degenerate or \
``False`` if it is non-degenerate.
        :returns: new_binding_z: The list of new pairs that may enter z.
        :returns: new_binding_w: The list of new pairs that may enter w.
        :rtype: Boolean and lists.

        """
        # Try pairs to enter z:
        new_binding_z = entering_z
        possible_z = [(n, i) for (n, i) in self.pcp.couple_to_x.keys()
                      if n <= self.level and (n, i) not in set(
            self.set_z).difference(set(entering_z))]
        for (n, i) in possible_z:
            if (n, i) not in new_binding_z:
                if self.coordinates[self.pcp.couple_to_x[(n, i)]] == 0:
                    new_binding_z.append((n, i))
        # Try pairs to enter w:
        new_binding_w = entering_w
        possible_w = [(n, i) for (n, i) in self.pcp.couple_to_poly.keys()
                      if n <= self.level and (n, i) not in set(
            self.set_w).difference(set(entering_w))]
        for (n, i) in possible_w:
            if (n, i) not in new_binding_w:
                pol = self.pcp.couple_to_poly[(n, i)].substitute(
                    self.coordinates)
                if pol == 0:
                    new_binding_w.append((n, i))
        if len(new_binding_z) + len(new_binding_w) > 1:
            self.is_degenerate = True
        return new_binding_z, new_binding_w

    def normalized_strategy(self):
        """
        Computes the joint mixed strategy corresponding to a \
complementary node.

        :param ``Node`` self: Should be a complementary node.
        :returns: proba: A joint mixed strategy.
        :rtype: List of lists.

        """
        v = self.coordinates
        proba = {}
        for n in range(self.pcp.game.n_players):
            sum_n = 0
            tmp_prob = []
            for j in self.pcp.game.players_actions[n]:
                x = self.pcp.ring(self.pcp.couple_to_x[(n, j)])
                sum_n += v[x]
            for j in self.pcp.game.players_actions[n]:
                x = self.pcp.ring(self.pcp.couple_to_x[(n, j)])
                tmp_prob += [QQbar(v[x] / sum_n)]
            proba[n] = tmp_prob
        return proba

    def get_data_of_path(self):
        """
        Returns data about the path followed to reach self.

        :param ``Node`` self: Current node.
        :returns: node_path_data: Object containing statistics about the path.
        :rtype:  ``NodePathData``.

        """
        node_path_data = NodePathData(self.pcp.game.n_players)
        return node_path_data

    def lift(self, pcp, xpairs_val):
        """
        Lift current complementary node.

        :param ``PolynomialComplementarityProblem`` pcp: \
The pcp from which the node is issued.
        :param dict xpairs_val: Coordinates of node above its level.
        :returns: nextnodeslist: A list containing the possible initial nodes \
at the above level (singleton except in case of degeneracy).
        :rtype: List of Nodes.

        """
        if not self.is_complementary:
            raise WilsonError("Can only lift a complementary node.")
        level = self.level + 1
        x_values_level = {pcp.couple_to_x[(n, i)]: xpairs_val[(n, i)] for
                          (n, i) in pcp.couple_to_x.keys() if n > level}
        subpcp = pcp.substitute(x_values_level, level)
        set_w = deepcopy(self.set_w)
        set_z = deepcopy(self.set_z)
        set_z += [(n, i) for (n, i) in subpcp.couple_to_x.keys() if
                  (n == level) and (i != subpcp.omega0[n])]
        # Try to find w entering set_w
        # Change lift to skip couple of previous level
        possible_next_w = [(n, i) for (n, i) in subpcp.couple_to_x.keys() if
                           n == level]
        no_sol_found = True
        while len(possible_next_w) > 0 and no_sol_found:
            w = possible_next_w.pop(0)
            loc_set_w = set_w + [w]
            subsys = Subsystem(subpcp, set_z, loc_set_w, level, xpairs_val)
            if len(subsys.solutions) > 0:
                no_sol_found = False
                tentativenode = Node(subpcp, set_z, loc_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                list_added_z, list_added_w = \
                    tentativenode.check_degeneracy([], [w])
        # Compute next nodes' list
        if no_sol_found:  # No node found after lifting
            nextnodeslist = []
        else:
            nextnodeslist = []
            degenerated = False
            if len(list_added_z + list_added_w) > 1:
                degenerated = True
            for z in list_added_z:
                loc_set_z = set_z + [z]
                tentativenode = Node(subpcp, loc_set_z, set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                tentativenode.is_degenerate = degenerated
                nextnodeslist += [tentativenode]
            for w in list_added_w:
                loc_set_w = set_w + [w]
                tentativenode = Node(subpcp, set_z, loc_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                tentativenode.is_degenerate = degenerated
                nextnodeslist += [tentativenode]
        return nextnodeslist

    def descend(self, pcp, xpairs_val):
        """
        Descend current initial node.

        :param ``PolynomialComplementarityProblem`` pcp: \
The pcp from which the node is issued.
        :param dict xpairs_val: Coordinates of node above its level.
        :returns: nextnodeslist: A list containing the possible complementary \
nodes at the level below (singleton except in case of degeneracy).
        :rtype: List of Nodes.

        """
        if not self.is_initial:
            raise WilsonError("Can only descend from an initial node.")
        x_values_level = {pcp.couple_to_x[(n, i)]: xpairs_val[(n, i)] for
                          (n, i) in pcp.couple_to_x.keys()
                          if n >= self.level}
        subpcp = pcp.substitute(x_values_level, self.level)
        new_set_z = [(n, i) for (n, i) in self.set_z if n < self.level]
        new_set_w = [(n, i) for (n, i) in self.set_w if n < self.level]
        level = self.level - 1
        if not set(new_set_z).intersection(
                set(new_set_w)):  # Empty intersection
            subsys = Subsystem(subpcp, new_set_z, new_set_w, level, xpairs_val)
            if not subsys.solutions:
                tentativenode = None
            else:
                tentativenode = Node(subpcp, new_set_z, new_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
        else:  # Singleton intersection
            m_j = set(new_set_z).intersection(set(new_set_w))
            if len(m_j) > 1:
                raise WilsonError("Intersection should be a singleton.")
            (m, j) = m_j.pop()
            local_set_z = deepcopy(new_set_z)
            local_set_z.remove((m, j))
            subsys = Subsystem(subpcp, local_set_z, new_set_w, level,
                               xpairs_val)
            # (m,j) should be removed from new_set_w, instead.
            if not subsys.solutions:
                local_set_w = deepcopy(new_set_w)
                local_set_w.remove((m, j))
                subsys = Subsystem(subpcp, new_set_z, local_set_w, level,
                                   xpairs_val)
                if not subsys.solutions:
                    tentativenode = None
                else:
                    tentativenode = Node(subpcp, new_set_z, local_set_w, level,
                                         xpairs_val, subsys,
                                         subsys.solutions[0])
                    tentativenode.prev_node = self
            else:
                tentativenode = Node(subpcp, local_set_z, new_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
        # Check degeneracy of node after descent
        if tentativenode is None:
            nextnodeslist = []
        else:
            nextnodeslist = [tentativenode]
        return nextnodeslist

    def compute_arc(self, prev_node):
        """
        Computes arc leaving current node. Uses previous node to compute it.

        :param ``Node`` self: Current node.
        :param ``Node`` prev_node: Previous node.
        :returns: (arc_set_z, arc_set_w): pair representing the outgoing arc.
        :rtype: pair of lists (of pairs (n,i)).

        """
        # Compute the next arc:
        if self.is_initial:
            if prev_node.is_complementary:
                # Current node results from lift().
                # If almost complementary, Z was unchanged.
                arc_set_z = [(n, i) for (n, i) in self.set_z if
                             not (n, i) in self.set_w]
                arc_set_w = deepcopy(self.set_w)
            else:
                raise WilsonError(
                    "Should not try to traverse an initial"
                    " node reached from the same level!")
        elif self.is_complementary:
            if not prev_node.level > self.level:
                raise WilsonError(
                    "Normally, a complementary node should"
                    " not be traversed in any directions.")
            # We have to find the unique bounded
            # arc leaving current complementary node:
            else:
                m = self.level
                j = self.pcp.omega0[m]
                arc_set_z = deepcopy(self.set_z)
                arc_set_w = deepcopy(self.set_w)
                if (m, j) in self.set_z:
                    arc_set_z.remove((m, j))
                elif (m, j) in self.set_w:
                    arc_set_w.remove((m, j))
                else:
                    raise WilsonError("The current node is not complementary?")
        elif self.is_almost_complementary:
            # Compute the next arc:
            z_inter_w = set(self.set_z).intersection(set(self.set_w))
            (m, j) = z_inter_w.pop()
            if len(z_inter_w) > 0:
                raise WilsonError(
                    "This should not happen with "
                    "an almost-complementary node.")
            if (m, j) in prev_node.set_w:
                arc_set_z = deepcopy(self.set_z)
                arc_set_w = [(n, i) for (n, i) in self.set_w if
                             not (n, i) in self.set_z]
            elif (m, j) in prev_node.set_z:
                arc_set_z = [(n, i) for (n, i) in self.set_z if
                             not (n, i) in self.set_w]
                arc_set_w = deepcopy(self.set_w)
            else:
                raise WilsonError(
                    "Two consecutive nodes should"
                    " have identical z or identical w ")
        else:
            raise WilsonError(
                "If the node is not almost-complementary,"
                " we should not encounter it!")
        if arc_set_z is None:
            arc_set_z = []
        if arc_set_w is None:
            arc_set_w = []
        return arc_set_z, arc_set_w

    def traverse(self, prev_node, xpairs_val):
        """
        Computes next node at same level, given current node and prev_node.

        :param ``Node`` self: Current node.
        :param ``Node`` prev_node: Previous node.
        :param dict xpairs_val: Coordinates of node above its level.
        :returns: nextnodeslist: A list containing the possible complementary \
nodes at the same level (singleton except in case of degeneracy).
        :rtype: List of Nodes.

        """
        nodepcp = self.pcp
        level = self.level
        all_couples = set(
            [(n, i) for (n, i) in nodepcp.couple_to_x.keys() if n <= level])
        # Compute the next arc:
        (arc_set_z, arc_set_w) = self.compute_arc(prev_node)
        poss_new_z = [(m, j) for (m, j) in
                      all_couples.difference(set(self.set_z))]
        poss_new_w = [(m, j) for (m, j) in
                      all_couples.difference(set(self.set_w))]

        nextnodeslist = []
        no_sol_found = True
        while len(poss_new_z) > 0 and no_sol_found:
            z = poss_new_z.pop(0)
            loc_set_z = arc_set_z + [z]
            loc_set_w = arc_set_w
            subsys = Subsystem(nodepcp, loc_set_z, loc_set_w, level,
                               xpairs_val)
            if len(subsys.solutions) > 0:
                tentativenode = Node(nodepcp, loc_set_z, loc_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                nextnodeslist += [tentativenode]
                no_sol_found = False
        while len(poss_new_w) > 0 and no_sol_found:
            w = poss_new_w.pop(0)
            loc_set_z = arc_set_z
            loc_set_w = arc_set_w + [w]
            subsys = Subsystem(nodepcp, loc_set_z, loc_set_w, level,
                               xpairs_val)
            if len(subsys.solutions) > 0:
                tentativenode = Node(nodepcp, loc_set_z, loc_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                nextnodeslist += [tentativenode]
                no_sol_found = False
        # Now get the following node:
        # Caution: list_added_z and list_added_w
        # don't have exactly the same meaning as usual.
        # They should be empty unless the node is degenerate.
        if no_sol_found:
            nextnodeslist = []
        else:
            list_added_z, list_added_w = tentativenode.check_degeneracy([], [])
            degenerated = False
            if len(list_added_z + list_added_w) > 1:
                degenerated = True
            for z in list_added_z:
                loc_set_z = arc_set_z + [z]
                tentativenode = Node(nodepcp, loc_set_z, arc_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                tentativenode.is_degenerate = degenerated
                nextnodeslist += [tentativenode]
            for w in list_added_w:
                loc_set_w = arc_set_w + [w]
                tentativenode = Node(nodepcp, arc_set_z, loc_set_w, level,
                                     xpairs_val, subsys, subsys.solutions[0])
                tentativenode.prev_node = self
                tentativenode.is_degenerate = degenerated
                nextnodeslist += [tentativenode]
        return nextnodeslist

    def already_visited(self, nodeslist):
        """
        Determines whether current node self is present in nodeslist.

        :param list nodeslist: A list of nodes.
        :returns: ``True`` if self has already been visited, ``False`` else.
        :rtype: boolean.

        """
        for node in nodeslist:
            # if len(self.set_z)==len(node.set_z)
            # and len(self.set_w)==len(node.set_w):
            #     if not (set(self.set_z).difference(node.set_z))
            #     and not (set(self.set_w).difference(node.set_w)):
            #         return True
            if len(self.set_z) == len(node.set_z) and\
                    len(self.set_w) == len(node.set_w):
                if not (set(self.set_z).difference(node.set_z)) and\
                        not (set(self.set_w).difference(node.set_w)):
                    if len(self.prev_node.set_z) ==\
                            len(node.prev_node.set_z) and\
                            len(self.prev_node.set_w) ==\
                            len(node.prev_node.set_w):
                        if not (
                                set(self.prev_node.set_z).difference(
                                    node.prev_node.set_z)) and \
                                not (set(self.prev_node.set_w).difference(
                                    node.prev_node.set_w)):
                            return True
        return False
