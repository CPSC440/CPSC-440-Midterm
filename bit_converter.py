def int_to_bin_list(val, width):
    if val < 0:
        val = (1 << width) + val
    bits = []
    for i in range(width):
        bits.append(val % 2)
        val //= 2
    return bits[::-1]

def bin_list_to_int(bits, signed=False):
    width = len(bits)
    val = 0
    for bit in bits:
        val = (val * 2) + bit
    if signed and bits[0] == 1:
        val -= (1 << width)
    return val

def bin_list_to_hex_str(bits):
    hex_map = "0123456789ABCDEF"
    hex_str = "0x"
    for i in range(0, len(bits), 4):
        n_bits = bits[i:i+4]
        value = bin_list_to_int(n_bits)
        hex_str += hex_map[value]
    return hex_str

def pretty_print_bin(bits):
    return '_'.join(''.join(map(str, bits[i:i+4])) for i in range(0, len(bits), 4))

def invert(bits):
    return [1 - bit for bit in bits]

def sign_extend(bits, width):
    return [bits[0]] * (width - len(bits)) + bits

def zero_extend(bits, width):
    return [0] * (width - len(bits)) + bits