from constants import *
from utils import *
from core import *

import pdb
import copy
from functools import reduce

from statesactions import *


############################
## HELPERS

### Return true if the given state object is a goal. Goal is a State object too.
def is_goal(state, goal):
    return len(goal.propositions.difference(state.propositions)) == 0


### Return true if the given state is in a set of states.
def state_in_set(state, set_of_states):
    for s in set_of_states:
        if s.propositions == state.propositions:
            return True
    return False


### For debugging, print each state in a list of states
def print_states(states):
    for s in states:
        ca = None
        if s.causing_action is not None:
            ca = s.causing_action.name
        print(s.id, s.propositions, ca, s.get_g(), s.get_h(), s.get_f())


############################
### Planner 
###
### The planner knows how to generate a plan using a-star and heuristic search planning.
### It also knows how to execute plans in a continuous, time environment.

class Planner():

    def __init__(self):
        self.running = False  # is the planner running?
        self.world = None  # pointer back to the world
        self.the_plan = []  # the plan (when generated)
        self.initial_state = None  # Initial state (State object)
        self.goal_state = None  # Goal state (State object)
        self.actions = []  # list of actions (Action objects)

    ### Start running
    def start(self):
        self.running = True

    ### Stop running
    def stop(self):
        self.running = False

    ### Called every tick. Executes the plan if there is one
    def update(self, delta=0):
        result = False  # default return value
        if self.running and len(self.the_plan) > 0:
            # I have a plan, so execute the first action in the plan
            self.the_plan[0].agent = self
            result = self.the_plan[0].execute(delta)
            if result == False:
                # action failed
                print("AGENT FAILED")
                self.the_plan = []
            elif result == True:
                # action succeeded
                done_action = self.the_plan.pop(0)
                print("ACTION", done_action.name, "SUCCEEDED")
                done_action.reset()
        # If the result is None, the action is still executing
        return result

    ### Call back from Action class. Pass through to world
    def check_preconditions(self, preconds):
        if self.world is not None:
            return self.world.check_preconditions(preconds)
        return False

    ### Call back from Action class. Pass through to world
    def get_x_y_for_label(self, label):
        if self.world is not None:
            return self.world.get_x_y_for_label(label)
        return None

    ### Call back from Action class. Pass through to world
    def trigger(self, action):
        if self.world is not None:
            return self.world.trigger(action)
        return False

    ### Generate a plan. Init and goal are State objects. Actions is a list of Action objects
    ### Return the plan and the closed list
    def astar(self, init, goal, actions):
        plan = []  # the final plan
        open = []  # the open list (priority queue) holding State objects
        closed = []  # the closed list (already visited states). Holds state objects
        ### YOUR CODE GOES HERE

        # open.append(init)
        # current = open[0]
        # parents = {}
        #
        # while not is_goal(current, goal) and len(open) > 0:
        #     open.remove(current)
        #     closed.append(current)
        #
        #     successors = []
        #     for action in actions:
        #         new_propositions = current.propositions | set(action.add_list)
        #         new_propositions = new_propositions.difference(set(action.delete_list))
        #         state = State(new_propositions)
        #         parents[state] = current # may need to double check whether this is being overwritten
        #         state.parent = current
        #         state.g = state.parent.get_g() + action.cost
        #         state.h = self.compute_heuristic(current, goal, actions)
        #         state.causing_action = action
        #         for closed_state in closed:
        #             if len(closed_state.propositions.difference(set(state.propositions))) != 0:
        #                 successors.append(state)
        #
        #     open.extend(successors)
        #     open = sorted(open, key=State.get_f)
        #
        #     current = open[0]
        #
        # if is_goal(current, goal):
        #     node = current
        #     while node != init:
        #         plan.append(node.causing_action)
        #         node = parents[node]
        #
        # print(plan)

        open.append(init)
        current = open[0]

        while not is_goal(current, goal) and len(open) != 0:
            open.remove(current)
            closed.append(current)
            # successors = []

            for action in actions:
                if action.preconditions.issubset(current.propositions):
                    propos = current.propositions | set(action.add_list)
                    propos = propos.difference(set(action.delete_list))
                    state = State(propos)
                    state.parent = current
                    state.causing_action = action
                    state.g = state.parent.g + action.cost
                    state.h = self.compute_heuristic(state, goal, actions)
                    # print("f: " + str(state.get_f()))
                    # is_in_closed = False
                    # for closed_state in closed:
                    #     if len(state.propositions.difference(closed_state[1].propositions)) == 0:
                    #         is_in_closed = True
                    # if not is_in_closed:
                    #     successors.append((state.get_f(), state))
                    if not state_in_set(state, set(closed)) and not state_in_set(state, set(open)):
                        open.append(state)

            # successors = sorted(successors, key=self.get_key)

            # print("successors: " + str(successors))
            # open.extend(successors)
            # print(open)
            open = sorted(open, key=self.get_key)

            # print(open[0])
            # if len(successors) != 0:
            #   current = successors[0]
            # else:
            current = open[0]

        if is_goal(current, goal):
            node = current
            print("Init: " + str(init))
            while node.causing_action is not None:
                print(node)
                plan.append(node.causing_action)
                node = node.parent
                print(plan)

        plan.reverse()

        ### CODE ABOVE
        return plan, closed

    def get_key(self, item):
        return item.get_f()

    ### Compute the heuristic value of the current state using the HSP technique.
    ### Current_state and goal_state are State objects.
    def compute_heuristic(self, current_state, goal_state, actions):
        actions = copy.deepcopy(actions)  # Make a deep copy just in case
        h = 0  # heuristic value to return
        ### YOUR CODE BELOW
        # create dummy actions for start and end
        goal_dummy = Action("goal", list(goal_state.propositions), [], [])
        start_dummy = Action("start", [], list(current_state.propositions), [])
        actions = [start_dummy] + actions + [goal_dummy]

        # construct the graph
        edges = []
        all_preconditions = set()

        for curr in actions:
            effects = set(curr.add_list)
            for action in actions:
                if action != curr:
                    for precondition in action.preconditions:
                        all_preconditions.add(precondition)
                        if precondition in effects:
                            # edges connect effects to preconditions
                            edges.append(Edge(precondition, curr, action))

        # # pruning actions where "start" is not an ancestor
        # nodes = []
        # pruned =[]
        #
        # # NEED A WAY TO ASSOCIATE NODES WITH THEIR EDGES
        # for edge in edges:
        #   curr = edge
        #   while curr.parent is not None:
        #     curr = curr.parent
        #   if curr == start_dummy:
        #     nodes.append(edge.child)
        #     pruned.append(edge)

        # walk the graph
        distances = dict((element, 0) for element in all_preconditions)
        queue = [start_dummy]
        visited = []
        active_effects = set()

        while len(queue) > 0:
            curr = queue.pop()
            visited.append(curr)
            active_effects = active_effects | set(curr.add_list)

            # calculate current value
            pdist = []
            for p in curr.preconditions:
                pdist.append(distances[p])

            curr_val = 0
            if len(pdist) > 0:
                curr_val = max(pdist)

            # update distance hash & add successors to queue
            for edge in edges:
                if edge.parent == curr:
                    distances[edge.name] = curr_val + curr.cost
                    if edge.child not in visited and edge.child.preconditions.issubset(active_effects):
                        queue.append(edge.child)

        for predicate in goal_dummy.preconditions:
            if distances[predicate] > h:
                h = distances[predicate]
        ### YOUR CODE ABOVE
        return h - 1


class Edge():
    def __init__(self, name='', parent=None, child=None):
        self.name = name
        self.parent = parent
        self.child = child

    def __str__(self):
        if self.parent is not None and self.child is not None:
            return "Parent: " + self.parent.name + "\n Fact: " + self.name + "\n Child: " + self.child.name
        elif self.parent is None:
            return "No parent, Fact: " + self.name
        elif self.child is None:
            return "No child, Face: " + self.name

# class Node():
#   def __init__(self, action=None, edges=[]):
#     self.action = action
#     self.name = action.name
#     self.edges = edges
#
#   def add_edge(self, edge):
#     self.edges.append(edge)
#
#   def remove_edge(self, edge):
#     if edge not in self.edges:
#       print("Edge not found")
#     else:
#       self.edges.remove(edge)