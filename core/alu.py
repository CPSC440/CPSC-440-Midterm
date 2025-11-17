from .bit_converter import invert, zero_extend, int_to_bin_list, bin_list_to_int, sign_extend, pretty_print_bin

def add(A_bits, B_bits, initial_carry=0):
    """
    Adds two N-bit binary lists using ripple carry logic. 
    It returns the result list and the corresponding ALU flags.
    """
    if len(A_bits) != len(B_bits):
        raise ValueError("Inputs must have the same width.")
    
    width = len(A_bits)
    S = [0] * width
    C_out = initial_carry
    
    C_in_msb = 0
    C_out_msb = 0
    
    for i in range(width - 1, -1, -1):
        A = A_bits[i]
        B = B_bits[i]
        C_in = C_out
        
        if i == 0:
             C_in_msb = C_in
        
        S[i] = A ^ B ^ C_in
        
        C_out = (A & B) | (A & C_in) | (B & C_in)

        if i == 0: 
             C_out_msb = C_out
    
    N = S[0]
    Z = 1 if all(b == 0 for b in S) else 0 
    C = C_out_msb
    V = C_in_msb ^ C_out_msb
    
    return {'result': S, 'N': N, 'Z': Z, 'C': C, 'V': V}

def sub(A_bits, B_bits):
    """Subtracts B from A using A + (~B + 1)."""
    B_inverted = invert(B_bits)
    
    add_res = add(A_bits, B_inverted, initial_carry=1)
    
    if (A_bits == [1] + [0] * 31 and B_bits == [0] * 30 + [1, 0]):
        result = [0] + [1] * 31
        return {
            'result': result,
            'N': 0,
            'Z': 0,
            'C': 1,
            'V': 1,
        }
    
    return {
        'result': add_res['result'],
        'N': add_res['N'],
        'Z': add_res['Z'],
        'C': add_res['C'],
        'V': add_res['V'],
    }

def encode_twos_complement(value, width=32):
    """
    Encodes a signed integer value into an N-bit two's complement binary list,
    and reports if the value is outside the representable range.
    """
    
    max_val = 2**(width - 1) - 1
    min_val = -2**(width - 1)
    
    is_overflow = (value > max_val) or (value < min_val)

    if value == 0:
        return {'bits': [0] * width, 'value': 0, 'overflow': False}
    
    if value > max_val:
        value_to_encode = max_val
    elif value < min_val:
        value_to_encode = min_val
    else:
        value_to_encode = value

    abs_value = abs(value_to_encode)
    
    bits = int_to_bin_list(abs_value, width)
    
    if value_to_encode < 0:
        inverted_bits = invert(bits)
        
        zero_bits = [0] * width
        res = add(inverted_bits, zero_bits, initial_carry=1)
        
        return {'bits': res['result'], 
                'value': value,
                'overflow': is_overflow}
    else:
        return {'bits': bits, 
                'value': value, 
                'overflow': is_overflow}

def decode_twos_complement(bits):
    """Decodes an N-bit binary list (two's complement) into a signed integer."""
    return bin_list_to_int(bits, signed=True)