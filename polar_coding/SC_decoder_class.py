from polar_coding.helper_functions import min_sum, g_function
from enum import IntEnum
import numpy as np
import math


class NodeState(IntEnum):
    not_visited = 0
    after_l_step = 1
    after_r_step = 2


class PolarDecoder:
    def __init__(self, N, K):
        self.n = int(math.log2(N))
        column = 10 - self.n
        self.reliability_sequence = np.genfromtxt('reliability_sequence.csv', dtype=int, delimiter=';',
                                                  usecols={column}, skip_header=1, usemask=True).compressed()
        self.K = K
        self.N = N
        self.beliefs = np.zeros((self.n + 1, N))
        self.decoded_bits = np.zeros((self.n + 1, N), dtype=int)
        # node_state_vector is long one dimensional array, it stores state of every node in the tree
        # starting from top of the tree to the bottom, the indexing look like this:
        # [root, level1_node0, level1_node1, level2_node0 ... level{n}_node{n-1}]
        # node_state_vector[2 ** current_depth - 1 + node_index] indicates in what state currently visited node is
        self.node_state_vector = np.zeros((2 * N - 1), dtype=int)
        self.frozen_bits_indexes = self.reliability_sequence[:N - K]

    def handle_leaf_node(self, node):
        # checking if leaf node is frozen, frozen bit will always be 0
        if node in self.frozen_bits_indexes:
            self.decoded_bits[self.n, node] = 0
        else:
            self.decoded_bits[self.n, node] = 0 if self.beliefs[self.n, node] >= 0 else 1

    def do_step_l(self, node, depth, node_position):
        current_index = 2 ** (self.n - depth)

        incoming_beliefs = self.beliefs[depth, current_index * node:current_index * (node + 1)]
        incoming_beliefs_part1 = incoming_beliefs[:current_index // 2]
        incoming_beliefs_part2 = incoming_beliefs[current_index // 2:]

        # going to left child
        node *= 2
        depth += 1
        current_index //= 2

        self.beliefs[depth, current_index * node:current_index * (node + 1)] = \
            min_sum(incoming_beliefs_part1, incoming_beliefs_part2)
        self.node_state_vector[node_position] = NodeState.after_l_step

    def do_step_r(self, node, depth, node_position):
        current_index = 2 ** (self.n - depth)

        incoming_beliefs = self.beliefs[depth, current_index * node:current_index * (node + 1)]
        incoming_beliefs_part1 = incoming_beliefs[:current_index // 2]
        incoming_beliefs_part2 = incoming_beliefs[current_index // 2:]

        incoming_beliefs_node = 2 * node
        left_node_depth = depth + 1
        left_node_index = current_index // 2
        incoming_decoded_bits = self.decoded_bits[left_node_depth, left_node_index * incoming_beliefs_node:
                                                                   left_node_index * (incoming_beliefs_node + 1)]
        # going to right child
        node = node * 2 + 1
        depth += 1
        current_index //= 2

        self.beliefs[depth, current_index * node:current_index * (node + 1)] = \
            g_function(incoming_beliefs_part1, incoming_beliefs_part2, incoming_decoded_bits)
        self.node_state_vector[node_position] = NodeState.after_r_step

    def do_step_u(self, node, depth):
        current_index = 2 ** (self.n - depth)
        left_child = 2 * node
        right_child = 2 * node + 1
        parent_depth = depth + 1
        parent_index = current_index // 2

        decoded_bits_left = self.decoded_bits[parent_depth, parent_index * left_child:parent_index * (left_child + 1)]
        decoded_bits_right = self.decoded_bits[parent_depth, parent_index * right_child:parent_index * (right_child + 1)]
        self.decoded_bits[depth, current_index * node:current_index * (node + 1)] = np.concatenate(
            [(decoded_bits_left + decoded_bits_right) % 2, decoded_bits_right])

    def get_decoded_message(self):
        message_indexes = self.reliability_sequence[self.N - self.K:]
        return self.decoded_bits[self.n, message_indexes]
