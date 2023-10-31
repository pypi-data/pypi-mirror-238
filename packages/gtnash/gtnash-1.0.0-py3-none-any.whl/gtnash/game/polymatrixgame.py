from gtnash.game.hypergraphicalgame import HGG


class PMG(HGG):
    """Polymatrix game class, attributes and methods.
    This class heritates from the *hypergraphicalgames class*.

    :param list of lists players_actions: Actions of every players of
        the polymatrix game.
    :param list of lists of lists utilities: Utilities of every players of
        input game. *utilities[g][n][a]* is the local utility of
        player *n* in local game *g* if the local joint action's index is *a*.
    :param list of lists hypergraph: List of sublist containing
        all the players' indices of all local games. *hypergraph[g]* is
        the list of players' indices involved in local game *g*.

    """

    def __init__(self, players_actions, utilities, hypergraph):
        """Polymatrix game constructor.
        """
        if HGG.is_PMG(HGG(players_actions, utilities, hypergraph)):
            super().__init__(players_actions, utilities, hypergraph)
        else:
            print('It is not a polymatrix game, please use HGG class')

    def read_GameFile(self, file_path):
        """Using a .hgg game file (polymatrix games are specific
        hypergraphical games), creates the corresponding utilities table.

        .. WARNING::

            Note that currently the order of players is the reverse of
            that in the utilities table (Player 1 in the .nfg file is the
            "last" player in the utilites table).

        :param string file_path: Path of the .nfg file to read.

        :returns: A polymatrix game.
        :rtype: list of lists of integers.
        """
        util_table_hgg = HGG.read_GameFile(self, file_path)
        util_table = PMG(util_table_hgg.players_actions,
                         util_table_hgg.utilities,
                         util_table_hgg.hypergraph)
        return util_table
