import numpy as np


def compute_fails(expected, decoded):
    bit_errors = np.sum(expected != decoded)
    frame_error = int(bit_errors > 0)
    return bit_errors, frame_error


def check_for_exceptions(n, k):
    if n <= k:
        raise Exception('N should be greater than K')
    if n == 16:
        raise Exception('No reliability sequence found for N=16')