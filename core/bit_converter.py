def int_to_bin_list(integer, width):
    """Converts a non-negative integer to a binary list of a fixed width."""
    bin_str = bin(integer)[2:]
    padded_str = bin_str.zfill(width)
    return [int(bit) for bit in padded_str]

def hex_str_to_bin_list(hex_str, width=32):
    """Converts a hex string (e.g., '0x3F800000') into an N-bit binary list."""
    if hex_str.lower().startswith('0x'):
        hex_str = hex_str[2:]
    
    try:
        val = int(hex_str, 16)
    except ValueError:
        raise ValueError(f"Invalid hex string: {hex_str}")

    bin_str = bin(val)[2:].zfill(width)
    
    return [int(bit) for bit in bin_str]

def bin_list_to_int(bits, signed=False):
    width = len(bits)
    val = 0
    for bit in bits:
        val = (val * 2) + bit
    if signed and bits[0] == 1:
        val -= (1 << width)
    return val

def bin_list_to_hex_str(bits):
    """Converts a binary list into a hex string with '0x' prefix."""
    bin_str = "".join(map(str, bits))
    val = int(bin_str, 2)
    return f"0x{val:0{len(bits)//4}X}"

def pretty_print_bin(bits):
    return '_'.join(''.join(map(str, bits[i:i+4])) for i in range(0, len(bits), 4))

def invert(bits):
    return [1 - bit for bit in bits]

def sign_extend(bits, width):
    return [bits[0]] * (width - len(bits)) + bits

def zero_extend(bits, width):
    if len(bits) >= width:
        return bits
    return [0] * (width - len(bits)) + bits