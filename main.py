import numpy as np
import matplotlib.pyplot as plt
from polar_coding.encode import encode
from polar_coding.decode_SC import decode
from channels.awgn_bpsk_channel import awgn_bpsk_channel
from polar_coding.helper_functions import compute_fails


if __name__ == "__main__":
    N = 256  # codeword length
    K = 120  # message bits

    messages = 1000
    eb_n0_range = [i / 2 for i in range(19)]

    result_ber = dict()
    result_fer = dict()
    for eb_n0 in eb_n0_range:
        ber = 0
        fer = 0

        for _ in range(messages):
            message = np.random.randint(low=0, high=2, size=K)
            encoded_message = encode(N, K, message)
            signal = awgn_bpsk_channel(encoded_message, K, N, eb_n0)
            decoded_message = decode(N, K, signal)

            bit_errors, frame_error = compute_fails(message, decoded_message)
            ber += bit_errors
            fer += frame_error

        result_ber[eb_n0] = ber / (messages * K)
        result_fer[eb_n0] = fer / messages

        print(f'\t{eb_n0}\t|\t{result_ber[eb_n0]:.10f}\t|\t{result_fer[eb_n0]:.10f}')

    ber1 = np.array(list(result_ber.values()))
    plt.plot(eb_n0_range, ber1)
    plt.yscale('log')
    plt.show()
