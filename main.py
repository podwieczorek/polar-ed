import numpy as np
from encode import encode

if __name__ == "__main__":
    N = 16  # codeword length
    K = 8  # message bits

    # generating random binary message of size K
    message = np.random.randint(low=0, high=2, size=K)
    encoded_message = encode(N, K, message)

    print(message)
    print(encoded_message)
