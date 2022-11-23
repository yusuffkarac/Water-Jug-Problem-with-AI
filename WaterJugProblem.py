# coding=utf-8

from __future__ import print_function

import time
from simpleai.search.viewers import BaseViewer

from simpleai.search.models import SearchProblem

from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, \
    uniform_cost


class WaterJugProblem(SearchProblem):
    ''' Water Jug Problem '''

    def __init__(self):
        # (current jug1, current jug2, current jug 3)
        super(WaterJugProblem, self).__init__(initial_state=(0, 0, 0))
        # ******* I ASSIGNED THESE VALUES FOR TESTING*******
        self.c1 = 8
        self.c2 = 5
        self.c3 = 3

        self.t1 = 4
        self.t2 = 4
        self.t3 = 0
        # ******* PLEASE UNCOMMENT THESE ROWS FOR INPUT DATA *******

        # self.c1 = int(input("Type capacity 1:"))
        # self.c2 = int(input("Type capacity 2:"))
        # self.c3 = int(input("Type capacity 3:"))

        # self.t1 =int(input("Type target 1:"))
        # self.t2 = int(input("Type target 2:"))
        # self.t3 = int(input("Type target 3:"))

    def actions(self, s):
        self._actions = [
            ################ fill the jug ################

            ('fill 1',),
            ('fill 2',),
            ('fill 3',),

            ################ empty jug ################
            ('empty 1',),
            ('empty 2',),
            ('empty 3',),

            ################ ****fill one to another*** ################

            ('j1 to j2',),
            ('j1 to j3',),

            ('j2 to j1',),
            ('j2 to j3',),

            ('j3 to j1',),
            ('j3 to j2',)

        ]
        '''Possible actions from a state.'''
        # we try to generate every possible state and then filter those
        # states that are valid
        return [a for a in self._actions if self._is_valid(self.result(s, a))]

    def _is_valid(self, s):

        return 0 <= s[0] <= self.c1 and 0 <= s[1] <= self.c2 and 0 <= s[2] <= self.c3

    def result(self, state, action):
        next_state = list(state)

        ## Fill actions
        if action[0] == 'fill 1':
            next_state[0] = self.c1

        elif action[0] == 'fill 2':
            next_state[1] = self.c2

        elif action[0] == 'fill 3':
            next_state[2] = self.c3

        ## Empty actions
        elif action[0] == 'empty 1':
            next_state[0] = 0

        elif action[0] == 'empty 2':
            next_state[1] = 0

        elif action[0] == 'empty 3':
            next_state[2] = 0



        # Pour one to another actions
        elif action[0] == 'j1 to j2':
            next_state[0] = max(0, state[0] - (self.c2 - state[1]))
            next_state[1] = min(state[0] + state[1], self.c2)


        elif action[0] == 'j1 to j3':
            next_state[0] = max(0, state[0] - (self.c3 - state[2]))
            next_state[2] = min(state[0] + state[2], self.c3)


        # *********
        elif action[0] == 'j2 to j1':
            next_state[0] = min(state[0] + state[1], self.c1)
            next_state[1] = max(0, state[1] - (self.c1 - state[0]))


        elif action[0] == 'j2 to j3':
            next_state[1] = max(0, state[1] - (self.c3 - state[2]))
            next_state[2] = min(state[1] + state[2], self.c3)

            # *********

        elif action[0] == 'j3 to j1':
            next_state[0] = min(state[0] + state[2], self.c1)
            next_state[2] = max(0, state[2] - (self.c1 - state[0]))

        elif action[0] == 'j3 to j2':
            next_state[1] = min(state[1] + state[2], self.c2)
            next_state[2] = max(0, state[2] - (self.c2 - state[1]))

        return tuple(next_state)

    def cost(self, state, action, state2):

        return 1

    def is_goal(self, state):
        return state == (self.t1, self.t2, self.t3)


total_costs = {}
use_memory = {}


def test_function(algo, problem, viewer, depth_limit=None, graph_search=True):
    print("*********************************************************\n\n")
    print("Graph search?:" + str(graph_search))
    if algo == "bfs":
        tic = time.perf_counter()
        print("BFS")
        result = breadth_first(problem, graph_search=graph_search, viewer=viewer)
        toc = time.perf_counter()
    elif algo == "ucs":
        tic = time.perf_counter()
        print("UCS")
        result = uniform_cost(problem, graph_search=graph_search, viewer=viewer)
        toc = time.perf_counter()

    elif algo == "dfs":
        tic = time.perf_counter()
        print("DFS")
        result = depth_first(problem, graph_search=graph_search, viewer=viewer)
        toc = time.perf_counter()

    elif algo == "dls":
        tic = time.perf_counter()
        print("DLS")
        result = limited_depth_first(problem, depth_limit=depth_limit, graph_search=graph_search, viewer=viewer)
        toc = time.perf_counter()

    elif algo == "ids":
        tic = time.perf_counter()
        print("IDS")
        result = iterative_limited_depth_first(problem, graph_search=graph_search, viewer=viewer)
        toc = time.perf_counter()

    print("Resulting Path:")
    for i in range(len(result.path())):
        print(f"{i}  . ", result.path()[i])
    print("Total Cost:", result.cost)
    total_costs[algo] = result.cost
    use_memory[algo] = viewer.stats['max_fringe_size']

    print("Viewer Stats:")
    print(viewer.stats)
    print("Runtime:", toc - tic)


my_viewer = BaseViewer()

problem = WaterJugProblem()
print(f"Capacity: ({problem.c1}, {problem.c2}, {problem.c3})")
print(f"Target: ({problem.t1}, {problem.t2}, {problem.t3})")
print("Initial Satate: ", problem.initial_state)
print("******* Uninformed Search Algorithms *******\n\n")

test_function("bfs", problem, my_viewer)
test_function("ucs", problem, my_viewer)
test_function("dfs", problem, my_viewer)
test_function("dls", problem, my_viewer, depth_limit=15)
test_function("ids", problem, my_viewer)

print("\n\n******** COSTS BY ORDER ********* ")
for w in sorted(total_costs, key=total_costs.get, ):
    print("Cost of", w, ":", total_costs[w])

print("\n\n******** MEMORY USAGE BY ORDER********* ")

for m in sorted(use_memory, key=use_memory.get, ):
    print(m, "memory usage is", use_memory[m])
