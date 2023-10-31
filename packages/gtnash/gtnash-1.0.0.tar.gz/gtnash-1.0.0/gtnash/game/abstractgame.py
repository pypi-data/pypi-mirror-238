from abc import ABC, abstractmethod


class AbstractGame(ABC):
    """This is the abstract game class from which all other classes derive.
    """
    @property
    def n_players(self):
        """Number of players of input game (@property).

        :param object self: Input game object.

        :returns: self._n_play, the number of players of self.
        :rtype: int.
        """
        return self._n_play

    @n_players.setter
    def n_players(self, n_play):
        self._n_play = n_play

    @property
    def players_actions(self):
        """Actions of every players of input game (@property).

        :param object self: Input game object.

        :returns: self._players_act, the actions of each player of self.
        :rtype: list of lists.
        """
        return self._players_act

    @players_actions.setter
    def players_actions(self, players_act):
        self._players_act = players_act

    @property
    def utilities(self):
        """Utilities of every players of input game (@property).

        :param object self: Input game object.

        :returns: self._util, utilities of every actions/players of self.
        :rtype: list of lists.
        """
        return self._util

    @utilities.setter
    def utilities(self, util):
        self._util = util

    @abstractmethod
    def expected_utilities(self):
        pass

    @abstractmethod
    def is_equilibrium(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def read_GameFile(self):
        pass

    @abstractmethod
    def write_GameFile(self):
        pass

    # @abstractmethod
    # def convert_to_HGG(self):
    #     pass
