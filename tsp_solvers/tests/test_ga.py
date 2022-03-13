import random
from unittest import TestCase
from tsp_solvers.tests.const import (
    GA_V10_COST,
    GA_V10_GENES,
    GA_V100_COST,
    GA_V100_GENES,
)
from tsp_solvers import Graph
from tsp_solvers import GeneticAlgorithm

# TODO: define tests for each method
#  use random.seed to be able to get the same results every time.


class GATestCase(TestCase):
    def setUp(self):
        super().setUp()
        random.seed(42)
        self.g = Graph()

    def tearDown(self):
        super().tearDown()
        pass

    def test_ga_10(self):
        self.g.create_graph_from_json("./tsp_solvers/tests/data/10v.json")
        ga = GeneticAlgorithm(self.g, 200, 100, 0.1, 120, "nearest")
        ga.run()
        self.assertListEqual(ga.best_genes, GA_V10_GENES)
        self.assertEqual(ga.best_cost, GA_V10_COST)

    def test_ga_100(self):
        self.g.create_graph_from_json("./tsp_solvers/tests/data/100v.json")
        ga = GeneticAlgorithm(self.g, 200, 100, 0.1, 120, "nearest")
        ga.run()
        self.assertListEqual(ga.best_genes, GA_V100_GENES)
        self.assertEqual(ga.best_cost, GA_V100_COST)
