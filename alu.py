from .bit_converter import invert, int_to_bin_list, bin_list_to_int

def _full_adder(a, b, c_in):
    s = (a ^ b) ^ c_in
    c_out = (a & b) | (c_in & (a ^ b))
    return s, c_out

def add(bits_a, bits_b):
    width = len(bits_a)
    result = [0] * width
    c_in = 0
    for i in range(width - 1, -1, -1):
        result[i], c_in = _full_adder(bits_a[i], bits_b[i], c_in)


    N = result[0]
    Z = 1 if all(b == 0 for b in result) else 0
    C = c_in
    V = (bits_a[0] == bits_b[0]) and (result[0] != bits_a[0])

    return {'result': result, 'N': N, 'Z': Z, 'C': C, 'V': V}

def sub(bits_a, bits_b):
    width = len(bits_a)
    one = int_to_bin_list(1, width)

    b_inv = invert(bits_b)
    b_neg_res = add(b_inv, one)
    b_neg = b_neg_res['result']

    res = add(bits_a, b_neg)

    res['C'] = 1 - res['C']
    return res

def encode_twos_complement(value, width=32):
    min_val, max_val = -2**(width-1), 2**(width-1) - 1
    overflow = not (min_val <= value <= max_val)

    if value >= 0:
        bits = int_to_bin_list(value, width)
    else:
        pos_bits = int_to_bin_list(abs(value), width)
        inv_bits = invert(pos_bits)
        one = int_to_bin_list(1, width)
        add_res = add(inv_bits, one)
        bits = add_res['result']
    
    return {'bits': bits, 'overflow': overflow}

def decode_twos_complement(bits):
    return bin_list_to_int(bits, signed=True)