from typing import Tuple, List, Dict

from pulp import LpVariable, LpProblem, LpMaximize, lpSum, GLPK
from collections import defaultdict


class SolverUtils:

    @staticmethod
    def calculate_solved_problem(
            performance_table_list: List[List[float]],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            alternative_id_1: int = -1,
            alternative_id_2: int = -1,
            show_logs: bool = False,
    ) -> LpProblem:
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems

        :param performance_table_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param alternative_id_1: used only in calculation for hasse graphs
        :param alternative_id_2: used only in calculation for hasse graphs
        :param show_logs: default None

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict, u_list
        )

        u_list = [sorted(lp_var_list, key=lambda var: float(var.name.split("_")[-1])) for lp_var_list in u_list]

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i]:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        u_list_of_characteristic_points: List[List[LpVariable]] = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][float(characteristic_points[i][j])])
            u_list_of_characteristic_points.append(pom[:])

        # Monotonicity constraint
        for i in range(len(u_list)):
            for j in range(1, len(u_list[i])):
                if criteria[i]:
                    problem += u_list[i][j] >= u_list[i][j - 1]
                else:
                    problem += u_list[i][j - 1] >= u_list[i][j]

        # Bounds constraint
        for i in range(len(u_list)):
            for j in range(1, len(u_list[i]) - 1):
                if criteria[i]:
                    problem += u_list[i][-1] >= u_list[i][j]
                    problem += u_list[i][j] >= u_list[i][0]
                else:
                    problem += u_list[i][0] >= u_list[i][j]
                    problem += u_list[i][j] >= u_list[i][-1]

        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) == lpSum(right_side)

        if alternative_id_1 >= 0 and alternative_id_2 >= 0:
            left_alternative: List[float] = performance_table_list[alternative_id_2]
            right_alternative: List[float] = performance_table_list[alternative_id_1]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, Dict[int, List[LpVariable]]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_higher_than_{j}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])
                    variable_2_name: str = f"v_{j}_higher_than_{i[0]}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])
                    pom_dict[j] = pom[:]

            alternatives_binary_variables[i[0]] = pom_dict

        indifferences_dict = {}
        for k in indifferences:
            if k[0] not in indifferences_dict:
                indifferences_dict[k[0]] = [k[1]]
            else:
                indifferences_dict[k[0]].append(k[1])

            if k[1] not in indifferences_dict:
                indifferences_dict[k[1]] = [k[0]]
            else:
                indifferences_dict[k[1]].append(k[0])

        for k in indifferences_dict:
            for i in indifferences_dict[k]:
                differ = set(indifferences_dict[i]) - set(indifferences_dict[k]) - set([k])
                indifferences_dict[k] = indifferences_dict[k] + list(differ)

        big_M: int = 1e20
        for worst_best in worst_best_position:
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:
                    checked = 0
                    for k in indifferences_dict:
                        if k == worst_best[0] and (i in indifferences_dict[k]):
                            problem += alternatives_binary_variables[worst_best[0]][i][0] == 0
                            problem += alternatives_binary_variables[worst_best[0]][i][1] == 0
                            checked = 1
                    if checked == 0:
                        problem += lpSum(alternatives_variables[worst_best[0]]) - lpSum(
                            alternatives_variables[i]) + big_M * alternatives_binary_variables[worst_best[0]][i][
                                       0] >= epsilon
                        problem += lpSum(alternatives_variables[i]) - lpSum(
                            alternatives_variables[worst_best[0]]) + big_M * alternatives_binary_variables[worst_best[0]][i][
                                       1] >= epsilon
                        problem += alternatives_binary_variables[worst_best[0]][i][0] + \
                                   alternatives_binary_variables[worst_best[0]][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2]

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in u_list_dict[i]:
                if_characteristic = 0

                for z in range(len(u_list_of_characteristic_points[i])):
                    if u_list_dict[i][j].name == u_list_of_characteristic_points[i][z].name:
                        if_characteristic = 1
                        break

                if if_characteristic == 0:
                    point_before = 0
                    point_after = 1
                    while characteristic_points[i][point_before] > float(
                            u_list_dict[i][j].name.split("_")[-1]) or float(u_list_dict[i][j].name.split("_")[-1]) > \
                            characteristic_points[i][point_after]:
                        point_before += 1
                        point_after += 1
                    value = SolverUtils.linear_interpolation(float(u_list_dict[i][j].name.split("_")[-1]),
                                                             characteristic_points[i][point_before], u_list_dict[i][
                                                                 float(characteristic_points[i][point_before])],
                                                             characteristic_points[i][point_after], u_list_dict[i][
                                                                 float(characteristic_points[i][point_after])])

                    problem += u_list_dict[i][j] == value

        problem += epsilon

        problem.solve(solver=GLPK(msg=show_logs))

        return problem

    @staticmethod
    def calculate_the_most_representative_function(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            show_logs: bool = False,
    ) -> LpProblem:
        """
        Main method used in getting the most representative value function.

        :param performance_table_list:
        :param alternatives_id_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None

        :return problem:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        delta: LpVariable = LpVariable("delta")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i] == 1:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        # Monotonicity constraint
        for i in range(len(u_list)):
            for j in range(1, len(u_list[i])):
                if criteria[i] == 1:
                    problem += u_list[i][j] >= u_list[i][j - 1]
                else:
                    problem += u_list[i][j - 1] >= u_list[i][j]

        # Bounds constraint
        for i in range(len(u_list)):
            for j in range(1, len(u_list[i]) - 1):
                if criteria[i] == 1:
                    problem += u_list[i][-1] >= u_list[i][j]
                    problem += u_list[i][j] >= u_list[i][0]
                else:
                    problem += u_list[i][0] >= u_list[i][j]
                    problem += u_list[i][j] >= u_list[i][-1]

        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) == lpSum(right_side)

        necessary_preference: Dict[str, List[str]] = SolverUtils.get_necessary_relations(
            performance_table_list=performance_table_list,
            alternatives_id_list=alternatives_id_list,
            preferences=preferences,
            indifferences=indifferences,
            criteria=criteria,
            worst_best_position=worst_best_position,
            number_of_points=number_of_points,
        )

        for i in range(len(alternatives_id_list) - 1):
            for j in range(i + 1, len(alternatives_id_list)):
                name_i = alternatives_id_list[i]
                name_j = alternatives_id_list[j]
                pom1 = []
                pom2 = []
                for k in range(len(performance_table_list[i])):
                    pom1.append(u_list_dict[k][float(performance_table_list[i][k])])
                    pom2.append(u_list_dict[k][float(performance_table_list[j][k])])
                sum_i = lpSum(pom1[:])
                sum_j = lpSum(pom2[:])

                if (name_i not in necessary_preference and name_j in necessary_preference and name_i in
                    necessary_preference[name_j]) or \
                        (name_i in necessary_preference and name_j in necessary_preference and name_i in
                         necessary_preference[name_j] and name_j not in necessary_preference[name_i]):
                    problem += sum_j >= sum_i + epsilon
                elif (name_j not in necessary_preference and name_i in necessary_preference and name_j in
                      necessary_preference[name_i]) or \
                        (name_i in necessary_preference and name_j in necessary_preference and name_j in
                         necessary_preference[name_i] and name_i not in necessary_preference[name_j]):
                    problem += sum_i >= sum_j + epsilon
                elif (name_i not in necessary_preference and name_j not in necessary_preference) or \
                        (name_i not in necessary_preference and name_j in necessary_preference and name_i not in
                         necessary_preference[name_j]) or \
                        (name_j not in necessary_preference and name_i in necessary_preference and name_j not in
                         necessary_preference[name_i]) or \
                        (name_i in necessary_preference and name_j not in necessary_preference[
                            name_i] and name_j in necessary_preference and name_i not in necessary_preference[name_j]):
                    problem += sum_i <= delta + sum_j
                    problem += sum_j <= delta + sum_i

        # Worst and Best position
        alternatives_variables: List[List[LpVariable]] = []
        for i in range(len(performance_table_list)):
            pom = []
            for j in range(len(u_list_dict)):
                pom.append(u_list_dict[j][performance_table_list[i][j]])
            alternatives_variables.append(pom[:])

        alternatives_binary_variables: Dict[int, Dict[int, LpVariable]] = {}
        all_binary_variables = {}
        for i in worst_best_position:
            pom_dict = {}
            for j in range(len(performance_table_list)):
                pom = []
                if i[0] != j:
                    variable_1_name: str = f"v_{i[0]}_higher_than_{j}"
                    if variable_1_name not in all_binary_variables:
                        variable_1: LpVariable = LpVariable(variable_1_name, cat='Binary')
                        pom.append(variable_1)
                        all_binary_variables[variable_1_name] = variable_1
                    else:
                        pom.append(all_binary_variables[variable_1_name])
                    variable_2_name: str = f"v_{j}_higher_than_{i[0]}"
                    if variable_2_name not in all_binary_variables:
                        variable_2: LpVariable = LpVariable(variable_2_name, cat='Binary')
                        pom.append(variable_2)
                        all_binary_variables[variable_2_name] = variable_2
                    else:
                        pom.append(all_binary_variables[variable_2_name])
                    pom_dict[j] = pom[:]

            alternatives_binary_variables[i[0]] = pom_dict

        indifferences_dict = {}
        for k in indifferences:
            if k[0] not in indifferences_dict:
                indifferences_dict[k[0]] = [k[1]]
            else:
                indifferences_dict[k[0]].append(k[1])

            if k[1] not in indifferences_dict:
                indifferences_dict[k[1]] = [k[0]]
            else:
                indifferences_dict[k[1]].append(k[0])

        for k in indifferences_dict:
            for i in indifferences_dict[k]:
                differ = set(indifferences_dict[i]) - set(indifferences_dict[k]) - set([k])
                indifferences_dict[k] = indifferences_dict[k] + list(differ)

        big_M: int = 1e20
        for worst_best in worst_best_position:
            for i in range(len(performance_table_list)):
                if i != worst_best[0]:
                    checked = 0
                    for k in indifferences_dict:
                        if k == worst_best[0] and (i in indifferences_dict[k]):
                            problem += alternatives_binary_variables[worst_best[0]][i][0] == 0
                            problem += alternatives_binary_variables[worst_best[0]][i][1] == 0
                            checked = 1
                    if checked == 0:
                        problem += lpSum(alternatives_variables[worst_best[0]]) - lpSum(
                            alternatives_variables[i]) + big_M * alternatives_binary_variables[worst_best[0]][i][
                                       0] >= epsilon
                        problem += lpSum(alternatives_variables[i]) - lpSum(
                            alternatives_variables[worst_best[0]]) + big_M * alternatives_binary_variables[worst_best[0]][i][
                                       1] >= epsilon
                        problem += alternatives_binary_variables[worst_best[0]][i][0] + \
                                   alternatives_binary_variables[worst_best[0]][i][1] <= 1

            pom_higher = []
            pom_lower = []
            for j in alternatives_binary_variables[worst_best[0]]:
                pom_higher.append(alternatives_binary_variables[worst_best[0]][j][0])
                pom_lower.append(alternatives_binary_variables[worst_best[0]][j][1])
            problem += lpSum(pom_higher) <= worst_best[1] - 1
            problem += lpSum(pom_lower) <= len(performance_table_list) - worst_best[2]

        problem += big_M * epsilon - delta

        problem.solve(solver=GLPK(msg=show_logs))

        return problem

    @staticmethod
    def get_necessary_relations(
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            criteria: List[bool],
            worst_best_position: List[List[int]],
            number_of_points: List[int],
            show_logs: bool = False
    ) -> Dict[str, List[str]]:
        """
        Method used for getting necessary relations.

        :param performance_table_list:
        :param alternatives_id_list:
        :param preferences:
        :param indifferences:
        :param criteria:
        :param worst_best_position:
        :param number_of_points:
        :param show_logs: default None

        :return necessary:
        """
        necessary: Dict[str, List[str]] = {}
        for i in range(len(performance_table_list)):
            for j in range(len(performance_table_list)):
                if i == j:
                    continue

                problem: LpProblem = SolverUtils.calculate_solved_problem(
                    performance_table_list=performance_table_list,
                    preferences=preferences,
                    indifferences=indifferences,
                    criteria=criteria,
                    worst_best_position=worst_best_position,
                    number_of_points=number_of_points,
                    alternative_id_1=i,
                    alternative_id_2=j,
                    show_logs=show_logs
                )

                if problem.variables()[0].varValue <= 0:
                    if alternatives_id_list[i] not in necessary:
                        necessary[alternatives_id_list[i]] = []
                    necessary[alternatives_id_list[i]].append(alternatives_id_list[j])

        return necessary

    @staticmethod
    def create_variables_list_and_dict(performance_table: List[list]) -> Tuple[List[list], List[dict]]:
        """
        Method responsible for creating a technical list of variables and a technical dict of variables that are used
        for adding constraints to the problem.

        :param performance_table:

        :return u_list, u_list_dict: ex. Tuple([[u_0_0.0, u_0_2.0], [u_1_2.0, u_1_9.0]], [{26.0: u_0_26.0, 2.0: u_0_2.0}, {40.0: u_1_40.0, 2.0: u_1_2.0}])
        """
        u_list: List[List[LpVariable]] = []
        u_list_dict: List[Dict[float, LpVariable]] = []

        for i in range(len(performance_table[0])):
            row: List[LpVariable] = []
            row_dict: Dict[float, LpVariable] = {}

            for j in range(len(performance_table)):
                variable_name: str = f"u_{i}_{float(performance_table[j][i])}"
                variable: LpVariable = LpVariable(variable_name)

                if performance_table[j][i] not in row_dict:
                    row_dict[float(performance_table[j][i])] = variable

                flag: int = 1
                for var in row:
                    if str(var) == variable_name:
                        flag: int = 0
                if flag:
                    row.append(variable)

            u_list_dict.append(row_dict)

            row: List[LpVariable] = sorted(row, key=lambda var: float(var.name.split("_")[-1]))
            u_list.append(row)

        return u_list, u_list_dict

    @staticmethod
    def calculate_direct_relations(necessary: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Method for getting only direct relations in Hasse Diagram
        :param necessary:
        :return direct_relations:
        """
        direct_relations: Dict[str, List[str]] = {}
        # first create the relation list for each node
        for node1, relations in necessary.items():
            direct_relations[node1] = sorted(relations)
        # then prune the indirect relations
        for node1, related_nodes in list(direct_relations.items()):  # make a copy of items
            related_nodes_copy: List[str] = related_nodes.copy()
            for node2 in related_nodes:
                # Check if node2 is also related to any other node that is related to node1
                for other_node in related_nodes:
                    if other_node != node2 and other_node in direct_relations and node2 in direct_relations[other_node]:
                        # If such a relationship exists, remove the relation between node1 and node2
                        related_nodes_copy.remove(node2)
                        break
            direct_relations[node1] = sorted(related_nodes_copy)  # sort the list

        return direct_relations

    @staticmethod
    def get_alternatives_and_utilities_dict(
            variables_and_values_dict,
            performance_table_list,
            alternatives_id_list,
    ) -> Dict[str, float]:
        """
        Method for getting alternatives_and_utilities_dict

        :param variables_and_values_dict:
        :param performance_table_list:
        :param alternatives_id_list:

        :return sorted_dict:
        """

        utilities: List[float] = []
        for i in range(len(performance_table_list)):
            utility: float = 0.0
            for j in range(len(performance_table_list[i])):
                variable_name: str = f"u_{j}_{performance_table_list[i][j]}"
                utility += round(variables_and_values_dict[variable_name], 4)

            utilities.append(round(utility, 4))

        utilities_dict: Dict[str, float] = {}
        # TODO: Sorting possibly unnecessary, but for now it's nicer for human eye :)
        for i in range(len(utilities)):
            utilities_dict[alternatives_id_list[i]] = utilities[i]
        sorted_dict: Dict[str, float] = dict(sorted(utilities_dict.items(), key=lambda item: item[1]))

        return sorted_dict

    @staticmethod
    def calculate_characteristic_points(
            number_of_points,
            performance_table_list,
            u_list_dict,
            u_list
    ) -> List[List[float]]:
        """
        Method for calculating characteristic points

        :param number_of_points:
        :param performance_table_list:
        :param u_list_dict:
        :param u_list:

        :return characteristic_points:
        """
        columns: List[Tuple[float]] = list(zip(*performance_table_list))
        worst_values: List[float] = [min(col) for col in columns]
        best_values: List[float] = [max(col) for col in columns]
        characteristic_points: List[List[float]] = []

        for i in range(len(worst_values)):
            pom = []
            if number_of_points[i] != 0:
                for j in range(number_of_points[i]):
                    x = worst_values[i] + (j / (number_of_points[i] - 1)) * (best_values[i] - worst_values[i])
                    if x not in u_list_dict[i]:
                        new: str = f"u_{i}_{x}"
                        variable: LpVariable = LpVariable(new)
                        new: Dict[float, LpVariable] = {x: variable}
                        u_list_dict[i].update(new)
                        u_list[i].append(variable)
                    pom.append(x)
                characteristic_points.append(pom[:])
            else:
                for j in range(len(performance_table_list)):
                    if float(performance_table_list[j][i]) not in pom:
                        pom.append(float(performance_table_list[j][i]))
                pom.sort()
                characteristic_points.append(pom[:])
        return characteristic_points

    @staticmethod
    def linear_interpolation(x, x1, y1, x2, y2) -> float:
        """Perform linear interpolation to estimate a value at a specific point on a straight line"""
        result = y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return result

    @staticmethod
    def get_criterion_functions(
            variables_and_values_dict,
            criteria
    ) -> Dict[str, List[Tuple[float, float]]]:
        """
        Method responsible for getting criterion functions

        :param variables_and_values_dict:
        :param criteria:
        :return:
        """
        criterion_functions: Dict[str, List[Tuple[float, float]]] = defaultdict(list)

        criterion_ids: List[str] = []
        for crit in criteria:
            criterion_ids.append(crit.criterion_id)

        for key, value in variables_and_values_dict.items():
            if key.startswith('u'):
                first_part, x_value = key.rsplit('_', 1)
                _, i = first_part.rsplit('_', 1)

                criterion_functions[criterion_ids[int(i)]].append((float(x_value), value))

        for key, values in criterion_functions.items():
            criterion_functions[key] = sorted(values, key=lambda x: x[0])

        return dict(criterion_functions)
