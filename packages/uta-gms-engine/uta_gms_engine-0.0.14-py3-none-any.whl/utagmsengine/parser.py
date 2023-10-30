from xmcda.criteria import Criteria
from xmcda.XMCDA import XMCDA
import csv
import _io
from typing import List, Dict

from .utils.parser_utils import ParserUtils
from .dataclasses import Criterion


class Parser:
    @staticmethod
    def get_performance_table_dict_csv(csvfile: _io.TextIOWrapper) -> Dict[str, Dict[str, float]]:
        """
        Method responsible for getting dict of performances from CSV file

        :param csvfile: python file object of csv file

        :return: Dictionary of performances
        """
        csv_reader = csv.reader(csvfile, delimiter=';')
        gains: List[str] = next(csv_reader)[1:]  # skip gains row
        criteria_ids: List[str] = next(csv_reader)[1:]

        performance_table_list: List[List[float]] = []
        alternative_ids: List[str] = []
        for row in csv_reader:
            performance_list: List[float] = [float(value) for value in row[1:]]
            alternative_id: str = [value for value in row[:1]][0]

            performance_table_list.append(performance_list)
            alternative_ids.append(alternative_id)

        result = {}
        for i in range(len(alternative_ids)):
            result[alternative_ids[i]] = {criteria_ids[j]: performance_table_list[i][j] for j in range(len(criteria_ids))}

        return result

    @staticmethod
    def get_criterion_list_csv(csvfile: _io.TextIOWrapper) -> List[Criterion]:
        csv_reader = csv.reader(csvfile, delimiter=';')

        gains: List[str] = next(csv_reader)[1:]
        criteria_ids: List[str] = next(csv_reader)[1:]

        criteria_objects = []
        for i in range(len(criteria_ids)):
            gain = True if gains[i].lower() == 'gain' else False
            criteria_objects.append(Criterion(criterion_id=criteria_ids[i], gain=gain, number_of_linear_segments=0))

        return criteria_objects

    def get_performance_table_list_xml(self, path: str) -> List[List]:
        """
        Method responsible for getting list of performances

        :param path: Path to XMCDA file (performance_table.xml)

        :return: List of alternatives ex. [[26.0, 40.0, 44.0], [2.0, 2.0, 68.0], [18.0, 17.0, 14.0], ...]
        """
        performance_table_list: List[List[float]] = []
        xmcda: XMCDA = ParserUtils.load_file(path)
        criteria_list: List = self.get_criteria_xml(path)

        for alternative in xmcda.alternatives:
            performance_list: List[float] = []
            for i in range(len(criteria_list)):
                performance_list.append(xmcda.performance_tables[0][alternative][xmcda.criteria[i]])
            performance_table_list.append(performance_list)

        return performance_table_list

    @staticmethod
    def get_alternatives_id_list_xml(path: str) -> List[str]:
        """
        Method responsible for getting list of alternatives ids

        :param path: Path to XMCDA file (alternatives.xml)

        :return: List of alternatives ex. ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        """
        alternatives_id_list: List[str] = []
        xmcda: XMCDA = ParserUtils.load_file(path)

        for alternative in xmcda.alternatives:
            alternatives_id_list.append(alternative.id)

        return alternatives_id_list

    @staticmethod
    def get_criteria_xml(path: str):
        """
        Method responsible for getting list of criteria

        :param path: Path to XMCDA file

        :return: List of criteria ex. ['g1', 'g2', 'g3']
        """
        criteria_list: List = []
        xmcda: XMCDA = ParserUtils.load_file(path)
        criteria_xmcda: Criteria = xmcda.criteria

        for criteria in criteria_xmcda:
            criteria_list.append(criteria.id)

        # Recognition of the type of criteria
        type_of_criterion: List[int] = []
        for i in range(len(criteria_list)):
            if criteria_list[i][0] == 'g':
                type_of_criterion.append(1)
            else:
                type_of_criterion.append(0)

        return type_of_criterion
