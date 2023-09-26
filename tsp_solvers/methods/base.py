"""
This class implements common methods for all solving methods
"""


class BaseMethod:
    """ """

    def __init__(self):
        """ """
        self.time = None
        self.cost = 0

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

    def get_solution_value(self):
        return self.cost

    def get_solution_time(self):
        return self.time
