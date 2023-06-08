import math
import numpy as np


def awgn_bpsk_channel(msg, K, N):
    # arbitrary chosen, nest we can make snr_per_bit_db (Eb/N0 in dB) function argument
    snr_per_bit_db = 16
    snr_per_bit = math.pow(10, (snr_per_bit_db / 10))
    rate = K / N
    sigma = math.sqrt(1 / (2 * rate * snr_per_bit))

    # BPSK
    signal = 1 - 2 * msg
    # Generate Gaussian noise
    noise = sigma * np.random.randn(N)
    # Add noise to the signal and return
    return signal + noise