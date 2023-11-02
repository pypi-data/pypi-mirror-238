import os
import re

import coverage

from agent_config import AgentConfig
from .footprint_model import FootprintModel
from .scanner.file_scanner import FileScanner

PYTHON_FILES_REG = r"^[^.#~!$@%^&*()+=,]+\.pyw?$"


class FootprintService(object):

    def __init__(self, agent_config: AgentConfig):
        self.agent_config = agent_config

    def _get_top_relative_path(self, filepath):
        start = os.getcwd()
        start = os.path.abspath(start)
        return os.path.relpath(filepath, start)

    def _is_match(self, method, line_num):
        is_match = method.position[0] < line_num <= method.endPosition[0]

        if method.position[0] == method.endPosition[0]:
            is_match = method.position[0] <= line_num <= method.endPosition[0]

        return is_match

    def _lines_to_methods(self, file_signature, covered_lines):
        line_methods = {}
        for line_num in covered_lines:
            if file_signature["line_map"].get(line_num):
                method = file_signature["line_map"].get(line_num)
                line_methods[method.uniqueId] = method
                continue
            if not file_signature["sorted"]:
                file_signature["file_data"].methods = sorted(file_signature["file_data"].methods,
                                                             key=lambda method: method.position[0], reverse=True)
                file_signature["sorted"] = True
            for method in file_signature["file_data"].methods:
                if self._is_match(method, int(line_num)):
                    line_methods[method.uniqueId] = method
                    file_signature["line_map"][line_num] = method
                    break
        return list(line_methods.values())

    def get_footprints_array(self, coverage_data: coverage.CoverageData):
        files_signatures = {}
        file_scanner = FileScanner()
        footprints = []
        for filename in coverage_data.measured_files():
            covered_lines = coverage_data.lines(filename)
            if not re.match(PYTHON_FILES_REG, os.path.split(filename)[1]):
                continue
            file_signature = files_signatures.get(filename)
            if not file_signature:
                file_data = file_scanner.calculate_file_signature(filename, self._get_top_relative_path(filename))
                file_signature = {"file_data": file_data, "line_map": {}, "sorted": False}
                files_signatures[filename] = file_signature
            covered_methods = self._lines_to_methods(file_signature, covered_lines)

            if covered_methods:
                file_footprints = [method.uniqueId for method in
                                   covered_methods]
                footprints.extend(file_footprints)
        return footprints

    def get_footprints_model(self, coverage_data: coverage.CoverageData, start_time: int, end_time: int):
        footprints = self.get_footprints_array(coverage_data)
        footprint_model = FootprintModel(self.agent_config, footprints, start_time, end_time)
        return footprint_model
