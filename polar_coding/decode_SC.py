import numpy as np
import math


def min_sum(a, b):
    first_element = (1 - 2 * (a < 0))
    second_element = (1 - 2 * (b < 0))
    return first_element * second_element * np.minimum(np.abs(a), np.abs(b))


def g_function(a, b, c):
    return b + (1 - 2 * c) * a


def decode(N, K, received_signal):
    n = int(math.log2(N))
    reliability_sequence = np.genfromtxt('reliability_sequence.csv', dtype=int, delimiter=';', usecols={1},
                                         skip_header=1, usemask=True).compressed()
    frozen_bits_indexes = reliability_sequence[:K]
    beliefs = np.zeros((n + 1, N))
    decoded_bits = np.zeros((n + 1, N), dtype=int)
    node_state_vector = np.zeros((2 * N - 1), dtype=int)

    beliefs[0, :] = received_signal  # Belief of the root node
    node = 0
    depth = 0
    done = False

    while not done:

        if depth == n:  # Leaf node
            if node in frozen_bits_indexes:
                decoded_bits[n, node] = 0
            else:
                decoded_bits[n, node] = 0 if beliefs[n, node] >= 0 else 1
            if node == N - 1:
                done = True
            else:
                node //= 2
                depth -= 1
        else:  # Non-leaf node
            npos = 2 ** depth - 1 + node  # Position of node in node state vector

            if node_state_vector[npos] == 0:  # Step L and go to the left child
                temp = 2 ** (n - depth)
                incoming_beliefs = beliefs[depth, temp * node:temp * (node + 1)]
                a = incoming_beliefs[:temp // 2]
                b = incoming_beliefs[temp // 2:]
                node *= 2
                depth += 1
                temp //= 2
                beliefs[depth, temp * node:temp * (node + 1)] = min_sum(a, b)
                node_state_vector[npos] = 1

            elif node_state_vector[npos] == 1:  # Step R and go to the right child
                temp = 2 ** (n - depth)
                incoming_beliefs = beliefs[depth, temp * node:temp * (node + 1)]
                a = incoming_beliefs[:temp // 2]
                b = incoming_beliefs[temp // 2:]
                incoming_beliefsode = 2 * node
                ldepth = depth + 1
                ltemp = temp // 2
                decoded_bitsn = decoded_bits[ldepth, ltemp * incoming_beliefsode:ltemp * (incoming_beliefsode + 1)] 
                node = node * 2 + 1
                depth += 1
                temp //= 2
                beliefs[depth, temp * node:temp * (node + 1)] = g_function(a, b, decoded_bitsn)
                node_state_vector[npos] = 2

            else:  # Step U and go to the parent
                temp = 2 ** (n - depth)
                incoming_beliefsode = 2 * node
                rnode = 2 * node + 1
                cdepth = depth + 1
                ctemp = temp // 2
                decoded_bitsl = decoded_bits[cdepth, ctemp * incoming_beliefsode:ctemp * (incoming_beliefsode + 1)] 
                decoded_bitsr = decoded_bits[cdepth, ctemp * rnode:ctemp * (rnode + 1)]  
                decoded_bits[depth, temp * node:temp * (node + 1)] = np.concatenate([(decoded_bitsl + decoded_bitsr) % 2, decoded_bitsr])
                node //= 2
                depth -= 1
    message_indexes = reliability_sequence[N - K:]
    return decoded_bits[n, message_indexes]
