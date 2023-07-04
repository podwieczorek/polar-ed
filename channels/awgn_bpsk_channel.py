import numpy as np


def awgn_bpsk_channel(msg, K, N, eb_n0):
    bpsk_symbols = 1 - 2 * msg

    # Calculate noise variance based on eb_n0
    eb_n0_lin = 10 ** (eb_n0 / 10)  # Convert eb_n0 from dB to linear scale
    rate = K / N
    noise_std = np.sqrt(1 / (rate * eb_n0_lin))  # Standard deviation of AWGN

    # Generate AWGN noise samples
    noise = noise_std * np.random.randn(N)

    # Add noise to the transmitted symbols
    signal = bpsk_symbols + noise

    return signal
