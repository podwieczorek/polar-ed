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


# min sum function, a and b are beliefs received from parent node
# return value is a belief send to child node
# if a and b are vectors the function applies the min sum coordinate wise
def min_sum(a, b):
    first_element = (1 - 2 * (a < 0))
    second_element = (1 - 2 * (b < 0))
    return first_element * second_element * np.minimum(np.abs(a), np.abs(b))


# repetition code operation
# a and b are vectors of beliefs, received from parent node
# c is a vector of decoded bits, received from left child node
def g_function(a, b, c):
    return b + (1 - 2 * c) * a