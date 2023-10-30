from typing import List, Dict, Optional, Tuple

from pulp import LpProblem

from .utils.solver_utils import SolverUtils
from .utils.dataclasses_utils import DataclassesUtils
from .dataclasses import Preference, Indifference, Criterion, DataValidator, Position


class Solver:

    def __init__(self, show_logs: Optional[bool] = False):
        self.name = 'UTA GMS Solver'
        self.show_logs = show_logs

    def __str__(self):
        return self.name

    def get_hasse_diagram_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
            positions: Optional[List[Position]] = []
    ) -> Dict[str, List[str]]:
        """
        Method for getting hasse diagram dict

        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects
        :param positions: List of Position objects

        :return direct_relations:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)
        DataValidator.validate_positions(positions, performance_table_dict)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        refined_linear_segments: List[int] = DataclassesUtils.refine_linear_segments(
            criterions=criteria
        )

        refined_worst_best_position: List[List[int]] = DataclassesUtils.refine_positions(
            positions=positions,
            performance_table_dict=performance_table_dict
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        necessary_preference = SolverUtils.get_necessary_relations(
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
            preferences=refined_preferences,
            indifferences=refined_indifferences,
            criteria=refined_gains,
            worst_best_position=refined_worst_best_position,
            number_of_points=refined_linear_segments,
            show_logs=self.show_logs
        )

        direct_relations: Dict[str, List[str]] = SolverUtils.calculate_direct_relations(necessary_preference)

        for alternatives_id in alternatives_id_list:
            if alternatives_id not in direct_relations.keys():
                direct_relations[alternatives_id] = []

        return direct_relations

    def get_representative_value_function_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
            positions: Optional[List[Position]] = []
    ) -> Tuple[Dict[str, float], Dict[str, List[Tuple[float, float]]]]:
        """
        Method for getting The Most Representative Value Function

        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects
        :param positions: List of Position objects

        :return:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)
        DataValidator.validate_positions(positions, performance_table_dict)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        refined_linear_segments: List[int] = DataclassesUtils.refine_linear_segments(
            criterions=criteria
        )

        refined_worst_best_position: List[List[int]] = DataclassesUtils.refine_positions(
            positions=positions,
            performance_table_dict=performance_table_dict
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        problem: LpProblem = SolverUtils.calculate_the_most_representative_function(
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
            preferences=refined_preferences,
            indifferences=refined_indifferences,
            criteria=refined_gains,
            worst_best_position=refined_worst_best_position,
            number_of_points=refined_linear_segments,
            show_logs=self.show_logs
        )

        variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in problem.variables()}

        criterion_functions: Dict[str, List[Tuple[float, float]]] = SolverUtils.get_criterion_functions(
            variables_and_values_dict=variables_and_values_dict,
            criteria=criteria,
        )

        alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
            variables_and_values_dict=variables_and_values_dict,
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
        )

        return alternatives_and_utilities_dict, criterion_functions
