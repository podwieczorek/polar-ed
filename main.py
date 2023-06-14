import numpy as np
import matplotlib.pyplot as plt
from polar_coding.encode import encode
from polar_coding.decode_SC import decode
from channels.awgn_bpsk_channel import awgn_bpsk_channel
from polar_coding.helper_functions import compute_fails


if __name__ == "__main__":
    N = 1024  # codeword length
    K = 100  # message bits

    messages = 10000
    # eb_n0_range = [0, 0.5, 1.0 .. 9.0]
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

        print(f'\t{eb_n0}\t|\t{result_ber[eb_n0]:.10f}\t|\t{result_fer[eb_n0]:.8f}')

    # changing BER and FER result values from dict to np array
    ber_values = np.array(list(result_ber.values()))
    fer_values = np.array(list(result_fer.values()))

    # plotting BER and FER vs Eb/N0 curves
    plt.plot(eb_n0_range, ber_values, 'b', label='BER')
    plt.plot(eb_n0_range, fer_values, 'r', label='FER')
    plt.title('BER and FER vs Eb/N0 in BPSK AWGN channel')
    plt.suptitle(f'messages={messages}, N={N}, K={K}')
    plt.xlabel('Eb/N0[dB]')
    plt.legend()
    plt.yscale('log')
    plt.show()
