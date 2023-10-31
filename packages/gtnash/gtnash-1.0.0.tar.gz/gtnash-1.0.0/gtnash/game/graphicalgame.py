from gtnash.game.hypergraphicalgame import HGG
import re
import shlex
import numpy as np


class GG(HGG):
    """
    A class used to represented the utilities table and the joint
    actions of the players associated to them

    Methods
    -------
    read_GameFile(file_path)
        Using a game describe in a .gg, create the utilities table
        corresponding to it.
    write_GameFile(file_path)
        Given a utilities table write the game in a .gg file

    """

    def __init__(self, players_actions, utilities, hypergraph):
        """
        Parameters
        ----------
        players_actions: list
            List of sublist of every actions of each player
        utilities: list
            List of the utility of each players
        hypergraph: array
            List of sublist containing all the players of each local play

        """
        if HGG.is_GG(HGG(players_actions, utilities, hypergraph)):
            super().__init__(players_actions, utilities, hypergraph)
        else:
            print('It is not a graphical game, please used HGG class')

    def read_GameFile(self, file_path):
        """
        Using a game describe in a .gg, create the utilities table
        corresponding to it.
        Note that currently the player order is reverse in the GG
        (The player 1 in the gg file
        is the "last" player of the UtilitesTable)

        Parameters
        ----------
        file_path: String
            Path of the file .gg to read

        Return
        ----------
        GG
            Graphical game in the file

        """
        # Read file
        file_read = open(file_path, 'r')
        content = file_read.read()
        content_list = content.split('"', 2)
        if content_list[0] != 'GG 0 R ':
            print('Ce fichier n est pas reconnu')
        else:
            game_info = content_list[2]
            game_info_bis = game_info.split(game_info.split('\n{')[0])[1]
            file_read.close()
            iterTest = re.finditer('{(.*?)}', game_info)
            p_actions = []
            # Get the name and actions of the players
            for i, s in enumerate(iterTest):
                # Pas très sur du calcul de p_actions
                if i == 1:
                    p_actions = [int(str_int) for str_int in
                                 shlex.split(s.group(1))]
            # Création de la liste de liste hypergraph
            iterTest = re.finditer('\n{1,}{(.*?)}',
                                   (game_info.split("\n{1,}")[0]).replace(',',
                                                                          ''))
            hypergraph = []
            for i, s in enumerate(iterTest):
                sublist_hypergraph = [int(sub_int) for sub_int in
                                      s.group(1).strip('\n').split(" ") if
                                      sub_int]
                hypergraph.append(sublist_hypergraph)
                # Création de la liste de liste de liste des utilités
            utilities = []
            iterTest = re.finditer('}\n(.*?)\n', game_info_bis)
            # Get the string of payoff, an iterator is use but there
            # is only 1 element to iterate on
            for i, s in enumerate(iterTest):
                sublist_utilites = [int(sub_int) for sub_int in
                                    s.group(1).strip('\n').split(" ") if
                                    sub_int]
                n_players = len(hypergraph[i])
                # Initialize the list of utility
                subsublist_utilities = []
                for j in range(n_players):
                    if hypergraph[i][j] == i:
                        subsublist_utilities.append(sublist_utilites)
                    else:
                        subsublist_utilities.append(
                            list(np.zeros(len(sublist_utilites))))
                # According to the way the utility are written
                # in the nfg file get for each player their utility
                utilities.append(subsublist_utilities)
            # Reverse the order of the players of each utility and
            # the order of the players action so that they
            # correspond to the order used in utilitiesTabl
            p_actions.reverse()
            # Generate list of actions like [[0,1,2][0,1][0,1,2,4]]
            # (for 3 player where one they have 3,2 and 4 actions)
            players_actions = [[j for j in range(p_actions[i])] for i in
                               range(len(p_actions))]
            self.players_actions = players_actions
            self.utilities = utilities
            self.hypergraph = hypergraph
            util_table = GG(self.players_actions, self.utilities,
                            self.hypergraph)
            return util_table

    def write_GameFile(self, file_path):
        """
        Given the current graphical game write the game in a .gg file

        Parameters
        ----------
        file_path: string
            Path and name of the file to write
        """
        # Get the number of players and their number of actions
        # n_players = len(self.players_actions)
        p_actions = [len(subl) for subl in self.players_actions]
        # Get all the joint actions
        jact = [self.local_normalformgames[i].joint_actions for i in
                range(len(self.hypergraph))]
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
        # Create a string that correspond to the utility of
        # the player to write in the gg file
        gamedescript = "nothing"
        playernames = "{"
        nb_actions = "{"
        for n_p, n_act in enumerate(p_actions):
            playernames += f' "Player {n_p}"'
            nb_actions += f" {n_act}"
            if n_p == len(p_actions) - 1:
                playernames += " }"
                nb_actions += " }"
        # Create the prologue of the file
        writeligne = f'GG 0 R "{gamedescript}" {playernames} {nb_actions}'
        fileTestwrite = open(file_path + '.gg', "w+")
        fileTestwrite.write(writeligne + "\n")
        # Create the rest
        for index_hyper_edge, hyper_edge in enumerate(hyperg):
            str_hyper_edge = "{"
            for play in hyper_edge:
                str_hyper_edge += f' {play}'
            str_hyper_edge += ' }\n'
            fileTestwrite.write(str_hyper_edge)
            str_utilities = ""
            for j in range(len(hyperg[index_hyper_edge])):
                if hyperg[index_hyper_edge][j] == index_hyper_edge:
                    index_begin = len(hyperg[index_hyper_edge]) - j - 1
            for index_uti in range(
                    len(payoffwrite[index_hyper_edge]) // len(hyper_edge)):
                uti = payoffwrite[index_hyper_edge][
                    index_uti * len(hyper_edge) + index_begin]
                str_utilities += f'{int(uti)} '
            fileTestwrite.write(str_utilities + "\n")
        fileTestwrite.close()
