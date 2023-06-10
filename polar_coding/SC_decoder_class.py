from polar_coding.helper_functions import min_sum, g_function
import numpy as np
import math


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
        self.node_state_vector = np.zeros((2 * N - 1), dtype=int)
        self.frozen_bits_indexes = self.reliability_sequence[:N-K]

    def handle_leaf_node(self, node):
        n = int(math.log2(self.N))
        # checking if leaf node is frozen, frozen bit will always be 0
        if node in self.frozen_bits_indexes:
            self.decoded_bits[n, node] = 0
        else:
            self.decoded_bits[n, node] = 0 if self.beliefs[n, node] >= 0 else 1

    def do_step_l(self, node, depth, node_position):
        temp = 2 ** (self.n - depth)

        incoming_beliefs = self.beliefs[depth, temp * node:temp * (node + 1)]
        incoming_beliefs_part1 = incoming_beliefs[:temp // 2]
        incoming_beliefs_part2 = incoming_beliefs[temp // 2:]

        node *= 2
        depth += 1
        temp //= 2
        self.beliefs[depth, temp * node:temp * (node + 1)] = min_sum(incoming_beliefs_part1, incoming_beliefs_part2)
        self.node_state_vector[node_position] = 1

    def do_step_r(self, node, depth, node_position):
        temp = 2 ** (self.n - depth)

        incoming_beliefs = self.beliefs[depth, temp * node:temp * (node + 1)]
        incoming_beliefs_part1 = incoming_beliefs[:temp // 2]
        incoming_beliefs_part2 = incoming_beliefs[temp // 2:]

        incoming_beliefs_node = 2 * node
        ldepth = depth + 1
        ltemp = temp // 2
        decoded_bitsn = self.decoded_bits[ldepth, ltemp * incoming_beliefs_node:ltemp * (incoming_beliefs_node + 1)]
        node = node * 2 + 1
        depth += 1
        temp //= 2

        self.beliefs[depth, temp * node:temp * (node + 1)] = \
            g_function(incoming_beliefs_part1, incoming_beliefs_part2, decoded_bitsn)
        self.node_state_vector[node_position] = 2

    def do_step_u(self, node, depth):
        temp = 2 ** (self.n - depth)
        incoming_beliefs_node = 2 * node
        rnode = 2 * node + 1
        cdepth = depth + 1
        ctemp = temp // 2

        decoded_bits_left = self.decoded_bits[cdepth, ctemp * incoming_beliefs_node:ctemp * (incoming_beliefs_node + 1)]
        decoded_bits_right = self.decoded_bits[cdepth, ctemp * rnode:ctemp * (rnode + 1)]
        self.decoded_bits[depth, temp * node:temp * (node + 1)] = np.concatenate(
            [(decoded_bits_left + decoded_bits_right) % 2, decoded_bits_right])

    def get_decoded_message(self):
        message_indexes = self.reliability_sequence[self.N - self.K:]
        return self.decoded_bits[self.n, message_indexes]
