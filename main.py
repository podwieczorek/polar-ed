import numpy as np
from polar_coding.encode import encode
from polar_coding.decode_SC import decode
from channels.awgn_bpsk_channel import awgn_bpsk_channel

if __name__ == "__main__":
    N = 16  # codeword length
    K = 8  # message bits

    # generating random binary message of size K
    message = np.random.randint(low=1, high=2, size=K)
    print(message)
    encoded_message = encode(N, K, message)
    signal = awgn_bpsk_channel(encoded_message, K, N)
    decoded_message = decode(N, K, encoded_message)
    print(decoded_message)
