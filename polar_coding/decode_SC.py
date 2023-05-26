import numpy as np
import math


def decode(N, K, encoded_message):
    reliability_sequence = np.genfromtxt('reliability_sequence.csv', dtype=int, delimiter=';', usecols={7},
                                         skip_header=1, usemask=True).compressed()
    frozen_bits_indexes = reliability_sequence[:K]

    u = encoded_message

    # here starts decoding
    sequence_len = N//2
    tree_depth = int(math.log2(N))
    for x in range(1, tree_depth+1, 1):
        for i in range(0, N, 2 * sequence_len):
            first_subchannel = u[i:i + sequence_len]
            second_subchannel = u[i + sequence_len:i + 2 * sequence_len]
            combined_sequence = np.concatenate([(first_subchannel + second_subchannel) % 2, second_subchannel])
            u[i:i + 2 * sequence_len] = combined_sequence

        sequence_len //= 2

    return u
