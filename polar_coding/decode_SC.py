from polar_coding.SC_decoder_class import PolarDecoder
import math


def decode(N, K, received_signal):
    decoder = PolarDecoder(N, K)
    decoder.beliefs[0, :] = received_signal

    n = int(math.log2(N))
    node = 0
    depth = 0
    done = False

    while not done:
        if depth == n:  # handling leaf node
            decoder.handle_leaf_node(node)
            # if handled leaf node was the last one, decoding is done
            if node == N - 1:
                done = True
            else:
                node //= 2
                depth -= 1
        else:   # handling non-leaf node
            # node position in node state vector
            node_position = 2 ** depth - 1 + node

            if decoder.node_state_vector[node_position] == 0:  # Step L and go to the left child
                decoder.do_step_l(node, depth, node_position)
                node *= 2
                depth += 1

            elif decoder.node_state_vector[node_position] == 1:  # Step R and go to the right child
                decoder.do_step_r(node, depth, node_position)
                node = node * 2 + 1
                depth += 1

            else:  # Step U and go to the parent
                decoder.do_step_u(node, depth)
                node //= 2
                depth -= 1
    return decoder.get_decoded_message()
