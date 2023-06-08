import numpy as np


def compute_fails(expected, decoded):
    bit_errors = np.sum(expected != decoded)
    frame_error = int(bit_errors > 0)
    return bit_errors, frame_error
