"""Implementation of Porter, Nudelman and Shoam's algorithm.

Class
-----

- Class ``PNS_solver``:
    An instance of the game includes a representation as an hypergraphical
    game, as well as a representation as a polynomial complementarity problem.

Modules' methods
----------------

- ``pns_algo(game)``:
    Solves ``game``, using the PNS algorithm.

- ``supports(domains, sizes)``:
    Computes the list of all joint supports of strategies, of size *sizes*.

- ``allbalancedsupports(domains)``:
    Computes the list of joint supports of strategies of balanced sizes,
    in increasing order of sizes.

- ``balancedpartitions(n, total)``:
    Computes the list of balanced integer partitions of integer *total* in
    *n* parts.

- ``unbalance_partitions(n, total, m)``:
    Computes the list of integer partitions of integer *total* in *n* parts
    where no two elements differ by more than *m*.

- ``allbalancedpartitions(n, total)``:
    Computes the list of balanced integer partitions of integer *m* in *n*
    parts where *m* belongs to the interval [n+1,total].

Detailed description of classes and methods:
--------------------------------------------

"""

from gtnash.util.irda import irda
from gtnash.util.polynomial_complementary_problem import\
    PolynomialComplementaryProblem, Subsystem
from sage.all import Subsets, OrderedPartitions, QQbar
from gtnash.game.normalformgame import NFG
from gtnash.game.hypergraphicalgame import HGG
import itertools


class PNS_solver:
    """Porter, Nudelman and Shoam's solver class, attributes and methods.

    :param AbstractGame game: The game to solve.

    """

    def __init__(self, game):
        """Construction of the PNS-format problem."""
        self.n_players = game.n_players
        self.players_actions = game.players_actions
        self.game = game
        if isinstance(game, NFG):
            hgg = HGG([[0]], [[[0]]], [[0]])  # arbitrary hgg
            self.game_hgg = hgg.convert_to_HGG(game)
        else:
            self.game_hgg = game
        self.all_ordered_support = []
        self.game_pcp = PolynomialComplementaryProblem(game, fact_y=False)
        self.final_support_size = sum(len(a) for a in self.players_actions)
        self.found_support_size = 0
        self.nb_of_support_enumerated = 0
        self.nb_of_subsys_computed = 0

    def launch_pns(self):
        """Executes the PNS algorithm on the current game.

        :returns: Nash equilibrium mixed strategy.
        :rtype: dict.
        """
        self.found_support_size = 0
        self.nb_of_support_enumerated = 0
        self.nb_of_subsys_computed = 0
        self.all_ordered_support = allbalancedsupports(self.players_actions)
        for support_i, current_support in enumerate(self.all_ordered_support):
            self.nb_of_support_enumerated += 1
            support_strat = self.support_to_strategy(current_support)
            support_size = sum(
                [sum(support_strat[n]) for n in range(self.n_players)])
            if support_size == self.n_players:
                supportaslist = [list(k)[0] for k in current_support]
                if self.game_hgg.is_pure_equilibrium(supportaslist):
                    self.found_support_size = support_size
                    return support_strat
            else:
                sub_g = self.game_hgg.get_subgame_fixed_strat(support_strat)
                reduced, z_excluded = irda(sub_g)
                if not z_excluded:
                    set_w = self.create_W_from_support_strat(support_strat)
                    set_wb = self.create_Wb_from_support_strat(support_strat)
                    sub_sys = Subsystem(self.game_pcp, set_wb, set_w,
                                        self.n_players - 1, {})
                    self.nb_of_subsys_computed += 1
                    if len(sub_sys.solutions) > 0:
                        self.found_support_size = support_size
                        return self.normalized_strategy(sub_sys.solutions[0])

    def normalized_strategy(self, solution_dic):
        """Normalizes an unnormalized strategy

        :param dict solution_dic: Unnormalized strategy, associating \
        rational numbers to every variables of the PCP of the game.

        :returns: List of normalized strategies (one for every player).
        :rtype: List of lists.
        """
        proba = {}
        for n in range(self.game_pcp.game.n_players):
            sum_n = 0
            tmp_prob = []
            # range(self.pcp.id_to_nb_act[n]):
            for j in self.game_pcp.game.players_actions[n]:
                x = self.game_pcp.ring(self.game_pcp.couple_to_x[(n, j)])
                sum_n += solution_dic[x]
            # range(self.pcp.id_to_nb_act[n]):
            for j in self.game_pcp.game.players_actions[n]:
                x = self.game_pcp.ring(self.game_pcp.couple_to_x[(n, j)])
                tmp_prob += [QQbar(solution_dic[x] / sum_n)]
            proba[n] = tmp_prob
        return proba

    def create_W_from_support_strat(self, support_strat):
        """Given the support of a strategy, returns the list of pairs \
(*player*, *action*) where *action* belongs to the support of *player*.

        :param list of lists support_strat: *suport_strat[n][n_i]*==1 if \
*n_i* belongs to the support of player *n*.

        :returns: List of pairs *(n,n_a)* belonging to *W*.
        :rtype: List of tuples.
        """
        return [(n, n_a) for n in range(self.n_players)
                for n_i, n_a in enumerate(self.players_actions[n])
                if support_strat[n][n_i] == 1]

    def create_Wb_from_support_strat(self, support_strat):
        """Given the support of a strategy, returns the list of pairs \
(*player*, *action*) where *action* does not belong to the support of *player*.

        :param list of lists support_strat: *suport_strat[n][n_i]*==1 if \
*n_i* belongs to the support of player *n*.

        :returns: List of pairs *(n,n_a)* belonging to *Z*=*Wbar*.
        :rtype: List of tuples.
        """
        return [(n, n_a) for n in range(self.n_players)
                for n_i, n_a in enumerate(self.players_actions[n])
                if support_strat[n][n_i] == 0]

    def support_to_strategy(self, support):
        """Changes the representation of the support of a strategy.

        :param dict support: *support[n]* is the set of actions in the \
support of player *n*.

        :returns: Dictionary of lists of 0 and 1 (1 iff action in the support).
        :rtype: dict.
        """
        return {n: [1 if n_act_i in support[n] else 0 for n_act_i in n_act]
                for n, n_act in enumerate(self.players_actions)}


def balancedpartitions(n, total):
    """ Computes the list of balanced partitions of total in n parts: \
    [k_1,...,k_n] such that k_1+...+k_n=total.

    :param int n: The number of elements in the partition.
    :param int total: The total to decompose.

    :returns: The list of decompositions [k_1,...,k_n] such that \
    k_1+...+k_n=total and [k_i-k_j]<=1, for all i,j.
    :rtype: List of lists of integers.
    """
    return [part for part in OrderedPartitions(total, n)
            if max(part) - min(part) <= 1]


def unbalance_partitions(n, total, m):
    """ Computes the list of unbalanced partitions of total in n parts: \
    [k_1,...,k_n] such that k_1+...+k_n=total.

    :param int n: The number of elements in the partition.
    :param int total: The total to decompose.
    :param int m: maximal discrepancy between elements in the partition.

    :returns: The list of decompositions [k_1,...,k_n] such that \
    k_1+...+k_n=total and [k_i-k_j]=m, for all i,j.
    :rtype: List of lists of integers.
    """
    return [part for part in OrderedPartitions(total, n)
            if max(part) - min(part) == m]


def allbalancedpartitions(n, total):
    """Computes all balanced partitions of m in n parts, where n<=m<=total.

    :param int n: The number of elements in the partition.
    :param int total: The total to decompose.

    :returns: The list of decompositions [k_1,...,k_n] such that \
    k_1+...+k_n=total and [k_i-k_j]<=m, for all i,j,n<=m<=total.
    :rtype: List of lists of integers.
    """
    allparts = []
    for m in range(n, total + 1):
        for ecar in range(m - (n - 1)):
            allparts += unbalance_partitions(n, m, ecar)
    return allparts


def supports(domains, sizes):
    """ Computes all supports of given sizes of a list of domains.

    :param list of lists domains: the list of full supports of all strategies.
    :param list of int sizes: the sizes of the partial supports.

    :returns: All supports of joint strategies of prescribed sizes.
    :rtype: list of lists.
    """
    list_of_subsets = []
    for i in range(len(domains)):
        list_of_subsets.append(Subsets(domains[i], sizes[i]))
    supports_it = itertools.product(*list_of_subsets)
    return supports_it


def allbalancedsupports(domains):
    """ Computes all balanced supports in increasing \
sizes for a list of domains.

    :param list of lists domains: the list of full supports of all strategies.

    :returns: All balanced supports of joint strategies, by increasing sizes.
    :rtype: list of lists.
    """
    n = len(domains)
    total = sum([len(domains[i]) for i in range(n)])
    abp = allbalancedpartitions(n, total)
    iterlist = []
    for i in range(len(abp)):
        iterlist.append(supports(domains, abp[i]))
    allbalancedsupports_it = itertools.chain(*iterlist)
    return allbalancedsupports_it


def pns_algo(game):
    """Solves *game*, using the PNS algorithm.

    :param AbstractGame game: The game to solve

    :returns: Nash equilibrium mixed strategy.
    :rtype: dict.
    """
    pns_solve = PNS_solver(game)
    return pns_solve.launch_pns()
