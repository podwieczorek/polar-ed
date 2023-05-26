import numpy as np
from polar_coding.encode import encode
from polar_coding.decode_SC import decode

if __name__ == "__main__":
    N = 8  # codeword length
    K = 4  # message bits

    # generating random binary message of size K
    message = np.random.randint(low=1, high=2, size=K)
    encoded_message = encode(N, K, message)
    print(encoded_message)
    decoded_message = decode(N, K, encoded_message)
    print(decoded_message)
