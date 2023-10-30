import pytest

from src.utagmsengine.dataclasses import Criterion
from src.utagmsengine.parser import Parser

from typing import List, Dict


@pytest.fixture()
def performance_table_dict_dummy():
    return {
        'A': {'g1': 26.0, 'g2': 40.0, 'g3': 44.0},
        'B': {'g1': 2.0, 'g2': 2.0, 'g3': 68.0},
        'C': {'g1': 18.0, 'g2': 17.0, 'g3': 14.0},
        'D': {'g1': 35.0, 'g2': 62.0, 'g3': 25.0},
        'E': {'g1': 7.0, 'g2': 55.0, 'g3': 12.0},
        'F': {'g1': 25.0, 'g2': 30.0, 'g3': 12.0},
        'G': {'g1': 9.0, 'g2': 62.0, 'g3': 88.0},
        'H': {'g1': 0.0, 'g2': 24.0, 'g3': 73.0},
        'I': {'g1': 6.0, 'g2': 15.0, 'g3': 100.0},
        'J': {'g1': 16.0, 'g2': 9.0, 'g3': 0.0},
        'K': {'g1': 26.0, 'g2': 17.0, 'g3': 17.0},
        'L': {'g1': 62.0, 'g2': 43.0, 'g3': 0.0}
    }


@pytest.fixture()
def criteria_list_dummy():
    return [
        Criterion(criterion_id='g1', gain=True, number_of_linear_segments=0),
        Criterion(criterion_id='g2', gain=True, number_of_linear_segments=0),
        Criterion(criterion_id='g3', gain=True, number_of_linear_segments=0)
    ]


# @pytest.fixture()
# def performance_table_list_dummy():
#     return [[26.0, 40.0, 44.0],
#             [2.0, 2.0, 68.0],
#             [18.0, 17.0, 14.0],
#             [35.0, 62.0, 25.0],
#             [7.0, 55.0, 12.0],
#             [25.0, 30.0, 12.0],
#             [9.0, 62.0, 88.0],
#             [0.0, 24.0, 73.0],
#             [6.0, 15.0, 100.0],
#             [16.0, 9.0, 0.0],
#             [26.0, 17.0, 17.0],
#             [62.0, 43.0, 0.0]]
#
#
# @pytest.fixture()
# def alternatives_id_list_dummy():
#     return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
#
#
# @pytest.fixture()
# def criteria_list_dummy():
#     return [1, 1, 1]


# def test_get_performance_table_list_xml(performance_table_list_dummy):
#     parser = Parser()
#     performance_table_list: List[List[float]] = parser.get_performance_table_list_xml('performance_table.xml')
#
#     assert performance_table_list == performance_table_list_dummy
#
#
# def test_get_alternatives_id_list_xml(alternatives_id_list_dummy):
#     parser = Parser()
#     alternatives_id_list: List[str] = parser.get_alternatives_id_list_xml('alternatives.xml')
#
#     assert alternatives_id_list == alternatives_id_list_dummy
#
#
# def test_get_criteria_xml(criteria_list_dummy):
#     parser = Parser()
#
#     criteria_list: List[str] = parser.get_criteria_xml('performance_table.xml')
#
#     assert criteria_list == criteria_list_dummy


def test_get_performance_table_dict_csv(performance_table_dict_dummy):
    parser = Parser()
    with open('../tests/files/alternatives.csv', 'r') as csvfile:
        performance_table_dict: Dict[str, Dict[str, float]] = parser.get_performance_table_dict_csv(csvfile)

    assert performance_table_dict == performance_table_dict_dummy


def test_get_criterion_list_csv(criteria_list_dummy):
    parser = Parser()
    with open('../tests/files/alternatives.csv', 'r') as csvfile:
        criteria_list: List[Criterion] = parser.get_criterion_list_csv(csvfile)

    assert criteria_list == criteria_list_dummy

