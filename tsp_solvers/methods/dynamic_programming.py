from tsp_solvers.methods.base import BaseSolver


class DynamicProgramming(BaseSolver):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.distance_matrix = self.graph.get_distance_matrix()
        self.starting_city = 0
        self.total_cities = self.graph.number_vertices

        self.end_state = (1 << self.total_cities) - 1

        self.memo = [
            [None for _col in range(1 << self.total_cities)]
            for _row in range(self.total_cities)
        ]

        self.shortest_path = []
        self.min_path_cost = float("inf")

    def run(self):
        self._init_memo()

        for num_element in range(3, self.total_cities + 1):
            for subset in self._init_combination(num_element):
                if self._is_not_in_subset(self.starting_city, subset):
                    continue

                for next_destination in range(self.total_cities):
                    if (
                        next_destination == self.starting_city
                        or self._is_not_in_subset(next_destination, subset)
                    ):
                        continue

                    state = subset ^ (1 << next_destination)
                    min_distance = float("inf")
                    for end_destination in range(self.total_cities):
                        if (
                            end_destination == self.starting_city
                            or end_destination == next_destination
                            or self._is_not_in_subset(end_destination, subset)
                        ):
                            continue

                        new_distance = (
                            self.memo[end_destination][state]
                            + self.distance_matrix[end_destination][next_destination]
                        )
                        if new_distance < min_distance:
                            min_distance = new_distance

                    self.memo[next_destination][subset] = min_distance

        self._calculate_min_cost()
        self._calculate_shortest_path()

    def _init_memo(self):
        for destination in range(self.total_cities):
            if destination == self.starting_city:
                continue

            self.memo[destination][
                1 << self.starting_city | 1 << destination
            ] = self.distance_matrix[self.starting_city][destination]

    def _calculate_min_cost(self):
        for i in range(self.total_cities):
            if i == self.starting_city:
                continue

            distance = self.memo[i][self.end_state]

            if distance < self.min_path_cost:
                self.min_path_cost = distance

    def _calculate_shortest_path(self):
        state = self.end_state

        for i in range(1, self.total_cities):
            best_index = -1
            best_distance = float("inf")

            for j in range(self.total_cities):
                if j == self.starting_city or self._is_not_in_subset(j, state):
                    continue

                new_distance = self.memo[j][state]

                if new_distance <= best_distance:
                    best_index = j
                    best_distance = new_distance

            self.shortest_path.append(best_index)
            state = state ^ (1 << best_index)

        self.shortest_path.append(self.starting_city)
        self.shortest_path.reverse()

    def _init_combination(self, num_element):
        subset_list = []
        self._init_full_combination(0, 0, num_element, self.total_cities, subset_list)
        return subset_list

    def _init_full_combination(
        self, subset, at, num_element, total_cities, subset_list
    ):
        elements_left_to_pick = total_cities - at
        if elements_left_to_pick < num_element:
            return

        if num_element == 0:
            subset_list.append(subset)

        else:
            for i in range(at, total_cities):
                subset |= 1 << i
                self._init_full_combination(
                    subset, i + 1, num_element - 1, total_cities, subset_list
                )
                subset &= ~(1 << i)

    @staticmethod
    def _is_not_in_subset(element, subset):
        return ((1 << element) & subset) == 0

    def get_best(self):
        print("\nDynamic programming:")
        print(f"Best solution: {self.min_path_cost}")
        print(f"Best path: {self.shortest_path}")
