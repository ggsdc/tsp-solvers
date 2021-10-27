"""
This class implements common methods for all solving methods
"""


class BaseSolver:
    """ """

    def __init__(self):
        """ """
        self.time = None

    def get_time(self):
        """ """
        return self.time

    def show(self):
        """Has to be implemented in subclass"""
        raise NotImplemented

    def get_best(self):
        """Has to be implemented in subclass"""
        raise NotImplemented

    def run(self):
        """
        Has to be implemented in subclass
        """
        raise NotImplemented
