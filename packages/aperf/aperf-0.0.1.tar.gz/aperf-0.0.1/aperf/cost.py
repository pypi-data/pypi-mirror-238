#!/usr/bin/env python3

###############################################################################
# Copyright 2022 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import logging
import matplotlib.pyplot as plt
import statistics

from collections import defaultdict


class FuncCost():
    def __init__(self, name="", level=0, duration=0, start_time=0,
                 end_time=0) -> None:
        self.name = name
        self.level = level
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time

    def parse(self, line):
        data = line.strip().split(',')
        if len(data) < 5:
            return
        self.level = int(data[0])
        self.name = data[1]
        self.duration = int(data[2])
        self.start_time = int(data[3])
        self.end_time = int(data[4])


class TaskCost():
    def __init__(self, name) -> None:
        self.name = name
        self.func_costs = defaultdict()

    def add(self, func_cost):
        if func_cost.name in self.func_costs:
            print("Duplicate name {}".format(func_cost.name))
        self.func_costs[func_cost.name] = func_cost

    def get_func_cost(self, func_name):
        return self.func_costs.get(func_name, None)

    def total(self):
        """total task time cost in milliseconds

        Returns:
            _type_: _description_
        """
        total_cost = 0.0
        for _, func_cost in self.func_costs.items():
            if func_cost.level == 1:
                total_cost += func_cost.duration
        return total_cost / 1e6

    def max(self):
        # multi-node tree to find leaf node
        pass

    def min(self):
        pass

    def max_k(self):
        pass

    def min_k(self):
        pass

    def large_than(self):
        pass


class TotalCost():
    def __init__(self) -> None:
        self.task_cost_dict = defaultdict(list)

    def add(self, task_cost):
        self.task_cost_dict[task_cost.name].append(task_cost)

    def draw_task_cost(self, task_name):
        task_costs = self.task_cost_dict.get(task_name, None)
        if task_costs:
            costs = [task_cost.total() for task_cost in task_costs]
            logging.debug(costs)
            mean, std = self.task_cost_mean(
                task_name), self.task_cost_std(task_name)
            fig, ax = plt.subplots()
            ax.plot(costs)
            plt.text(0.6, 0.9, "mean:{:.2f}, std:{:.2f}".format(
                mean, std), transform=ax.transAxes)
            plt.ylabel("time(ms)")
            plt.show()

    def task_cost_mean(self, task_name):
        task_costs = self.task_cost_dict.get(task_name, None)
        costs = []
        if task_costs:
            costs = [task_cost.total() for task_cost in task_costs]
        return statistics.fmean(costs)

    def task_cost_std(self, task_name):
        task_costs = self.task_cost_dict.get(task_name, None)
        costs = []
        if task_costs:
            costs = [task_cost.total() for task_cost in task_costs]
        return statistics.stdev(costs)

    def max(self):
        # multi-node tree to find leaf node
        pass

    def min(self):
        pass

    def max_k(self):
        pass

    def min_k(self):
        pass

    def large_than(self):
        pass
