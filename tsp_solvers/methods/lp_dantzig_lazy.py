import re
from datetime import datetime

from gurobipy import GRB
import gurobipy as gp
from pulp import LpProblem, LpMinimize, GUROBI, value

from tsp_solvers.methods.lp_dantzig import LinearIntegerDantzig

import logging

logger = logging.getLogger(__name__)


class LinearIntegerDantzigLazy(LinearIntegerDantzig):
    def __init__(self, graph, max_time, plot=False):
        super().__init__(graph, max_time, plot=plot)
        self.model = LpProblem("TSP problem (DFJ lazy)", LpMinimize)

    def run(self):
        start_time = datetime.utcnow()
        received_status = self.model.solve(
            GUROBI(
                msg=True,
                timeLimit=self.max_time,
                mip=True,
                LazyConstraints=1,
            ),
            callback=gurobi_callback,
        )

        travels = self.travel.vfilter(lambda v: value(v)).keys_tl()

        start = travels[0][0]
        end = travels[0][1]
        travels = travels[1:]
        temp = [start]
        while travels:
            for travel in travels:
                if travel[0] == end:
                    start = travel[0]
                    end = travel[1]
                    temp.append(start)
                    travels.remove(travel)
                    break
        self.solution = self.solution = [
            self.graph.vertices_collection[idx] for idx in temp
        ]
        self.cost = self.graph.get_cost(self.solution)
        self.time = datetime.utcnow() - start_time


def gurobi_callback(model, where):
    if where == GRB.Callback.MIPSOL:
        try:
            eliminate_subtours(model)
        except Exception as e:
            logger.error(f"Exception occurred in MIPSOL callback: {e}")
            model.terminate()


def eliminate_subtours(model):
    vars_list = model.getVars()

    def get_indexes(variable_name):
        pattern = r"Travel_\((-?\d+),_(-?\d+)\)"
        match = re.match(pattern, variable_name)
        if match:
            # Extract the matched numbers from the groups
            x = int(match.group(1))
            y = int(match.group(2))
            return (x, y)

    vars = {var.index: get_indexes(var.VarName) for var in vars_list}
    vars_reverse = {v: k for k, v in vars.items()}
    values = {var.index: model.cbGetSolution(var) for var in vars_list}

    edges = [v for k, v in vars.items() if values[k] > 0.5]

    unvisited = list(set(value for tpl in vars.values() for value in tpl))
    cycles = []

    while unvisited:
        temp_cycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            temp_cycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges if i == current and j in unvisited]

        cycles.append(temp_cycle)

    obj_value = model.cbGet(GRB.Callback.MIPSOL_OBJ)
    obj_bst = model.cbGet(GRB.Callback.MIPSOL_OBJBST)
    obj_bnd = model.cbGet(GRB.Callback.MIPSOL_OBJBND)

    if obj_bnd == -1e100:
        globals()["best_bnd"] = obj_bnd
        return

    if len(cycles) == 1:
        return

    # cycle = cycles[0]
    for cycle in cycles:
        edges_on_cycle = [(x, y) for x, y in zip(cycle, cycle[1:] + [cycle[0]])]
        model.cbLazy(
            gp.quicksum(vars_list[vars_reverse[edge]] for edge in edges_on_cycle)
            <= len(cycle) - 1
        )

    globals()["best_bnd"] = obj_bnd
