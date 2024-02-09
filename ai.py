from __future__ import absolute_import, division, print_function
import copy
import random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.


class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        # TODO: complete this
        return all(v is None for v in self.children)
        # pass

# AI agent. Determine the next move.


class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions:
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move
    # note for myself: current_state returns a deep copy

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):

        if depth == 0 or node == None:
            # print("Node is none or depth = 0.")
            return

        # current_node = node
        current_state = copy.deepcopy(node.state)
        current_simulator = Game(*node.state)

        if (depth % 2) != 0:
            # Player makes a move
            for direction in [0, 1, 2, 3]:
                if current_simulator.move(direction):
                    tmp_child = Node(
                        current_simulator.current_state(), CHANCE_PLAYER)
                    node.children.append(tmp_child)
                else:
                    node.children.append(None)
                current_simulator.set_state(*current_state)
        else:
            # Computer places a tile
            hist = set()
            possible_cases = len(current_simulator.get_open_tiles())
            while len(hist) != possible_cases:
                # for i in range(len(current_simulator.get_open_tiles())):
                current_simulator.place_random_tile()
                if (', '.join(str(e) for col in current_simulator.current_state()[0] for e in col)) not in hist:
                    tmp_child = Node(
                        current_simulator.current_state(), MAX_PLAYER)
                    node.children.append(tmp_child)
                    hist.add(
                        (', '.join(str(e) for col in current_simulator.current_state()[0] for e in col)))
                current_simulator.set_state(*current_state)

            # for i in range(len(current_simulator.get_open_tiles())):
            #     current_simulator.place_random_tile()
            #     tmp_child = Node(
            #         current_simulator.current_state(), MAX_PLAYER)
            #     node.children.append(tmp_child)
            #     current_simulator.set_state(*current_state)

        # print(f"Building tree at depth {depth}.")
        # print(f"At node state: {node.state}, children: {node.children}")

        for i in range(len(node.children)):
            self.build_tree(node.children[i], depth - 1)

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None, depth=3):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0
        if node.is_terminal():
            # print(
            #     f"-- At depth {depth}, node state: {node.state}, expectimax returned: {node.state[1]}")
            return (None, node.state[1])
        elif node.player_type == MAX_PLAYER:
            value, best_direction, curr_direction = 0, 0, -1
            for c in node.children:
                curr_direction += 1
                if c is not None:
                    c_expectimax = self.expectimax(c, depth - 1)[1]
                    best_direction = curr_direction if c_expectimax > value else best_direction
                    value = max(value, c_expectimax)
            # print(
            #     f"-- At depth {depth}, node state: {node.state}, expectimax (1) returned: {(best_direction, value)}")
            return (best_direction, value)
        else:  # CHANCE_PLAYER
            value, count = 0, 0
            for c in node.children:
                if c is not None:
                    value += self.expectimax(c, depth - 1)[1]
                    count += 1
            # print(
            #     f"-- At depth {depth}, node state: {node.state}, expectimax (2) returned: {(None, value / count)}")
            return (None, value / count)

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        return random.randint(0, 3)
