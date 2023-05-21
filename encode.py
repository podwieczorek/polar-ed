import numpy as np
import math


def encode(N, K, message):
    n = int(math.log2(N))  # exponent

    # usecols parameter specifies which column to use
    reliability_sequence = np.genfromtxt('reliability_sequence.csv', dtype=int, delimiter=';', usecols={6},
                                         skip_header=1,
                                         usemask=True).compressed()

    # extracting message bits indexes from reliability sequence
    message_indexes = reliability_sequence[K:]

    # creating input vector by inserting message on specified message indexes
    # other indexes will be set to 0 (frozen bits)
    u = np.zeros(N, dtype=int)
    u[message_indexes] = message
    # here starts proper encoding; going from bottom of the tree to top, number of levels equals to log2(N) - 1
    # starting by combining 1 bit with 1 bit, on next steps number of combined bits is multiplied by 2
    combined_bits_number = 1
    for tree_depth in range(n - 1, -1, -1):
        # iterating over vector, size step of 2 sub-channels
        for i in range(0, N, 2 * combined_bits_number):
            first_subchannel = u[i:i + combined_bits_number]
            second_subchannel = u[i + combined_bits_number:i + 2 * combined_bits_number]
            # XOR-ing first_subchannel with second_subchannel, then concatenating the result with second subchannel
            combined_sequence = np.concatenate([(first_subchannel + second_subchannel) % 2, second_subchannel])
            u[i:i + 2 * combined_bits_number] = combined_sequence
        combined_bits_number *= 2

    return u
