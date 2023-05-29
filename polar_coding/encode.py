import numpy as np
import math


def encode(N, K, message):

    # usecols parameter specifies which column to use 0: N=1024; 1: N=512 ... 7: N=8
    # TODO change column automatically
    reliability_sequence = np.genfromtxt('reliability_sequence.csv', dtype=int, delimiter=';', usecols={6},
                                         skip_header=1, usemask=True).compressed()

    # extracting message bits indexes from reliability sequence
    message_indexes = reliability_sequence[N-K:]

    # creating input vector by inserting message on specified message indexes
    # other indexes will be set to 0 (frozen bits)
    u = np.zeros(N, dtype=int)
    u[message_indexes] = message

    # here starts proper encoding; going from bottom of the tree to top, number of levels equals to log2(N) - 1
    # starting by combining 1 bit with 1 bit, on each level number of combined bits is multiplied by 2
    sequence_len = 1
    tree_depth = int(math.log2(N))
    for x in range(tree_depth - 1, -1, -1):
        for i in range(0, N, 2 * sequence_len):
            first_subchannel = u[i:i + sequence_len]
            second_subchannel = u[i + sequence_len:i + 2 * sequence_len]

            # XOR-ing first_subchannel with second_subchannel, then concatenating the result with second subchannel
            combined_sequence = np.concatenate([(first_subchannel + second_subchannel) % 2, second_subchannel])
            u[i:i + 2 * sequence_len] = combined_sequence

        sequence_len *= 2

    return u
