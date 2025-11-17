from .bit_converter import int_to_bin_list, bin_list_to_int, bin_list_to_hex_str, zero_extend
from .alu import add

EXP_WIDTH = 8
FRAC_WIDTH = 23
BIAS = 127

def _unpack_f32(bits):
    """Extracts sign, exponent, and fraction from a 32-bit list."""
    sign = bits[0]
    exp = bits[1:1+EXP_WIDTH]
    frac = bits[1+EXP_WIDTH:]
    return {'s': sign, 'e': exp, 'f': frac}

def _repack_f32(s, e, f):
    """Combines sign, exponent, and fraction back into a 32-bit list."""
    return [s] + e + f

def fadd_f32(a_bits, b_bits):
    """Simulates float32 addition."""
    trace = []
    
    a = _unpack_f32(a_bits)
    b = _unpack_f32(b_bits)
    
    exp_a = bin_list_to_int(a['e'])
    exp_b = bin_list_to_int(b['e'])
    
    if exp_a == 0 and all(bit == 0 for bit in a['f']):
        return {'res_bits': b_bits, 'flags': {}, 'trace': trace}
    if exp_b == 0 and all(bit == 0 for bit in b['f']):
        return {'res_bits': a_bits, 'flags': {}, 'trace': trace}
    
    sig_a = [1] + a['f']
    sig_b = [1] + b['f']
    
    if exp_a < exp_b:
        exp_a, exp_b = exp_b, exp_a
        sig_a, sig_b = sig_b, sig_a
        a, b = b, a

    shift = exp_a - exp_b
    if shift > 0:
        sig_b = [0] * shift + sig_b
        if len(sig_b) > 24:
            sig_b = sig_b[:24]
    
    sig_a = zero_extend(sig_a, 24)
    sig_b = zero_extend(sig_b, 24)
    
    res_exp_val = exp_a
    res_s = a['s']

    if a['s'] == b['s']:
        add_res = add(sig_a, sig_b)
        res_sig = add_res['result']
        
        if add_res['C'] == 1:
            res_sig = [1] + res_sig[:-1]
            res_exp_val += 1
    else:
        val_a = bin_list_to_int(sig_a)
        val_b = bin_list_to_int(sig_b)
        
        if val_a >= val_b:
            res_val = val_a - val_b
            res_s = a['s']
        else:
            res_val = val_b - val_a
            res_s = b['s']
        
        if res_val == 0:
            return {'res_bits': [0] * 32, 'flags': {}, 'trace': trace}
            
        res_sig = int_to_bin_list(res_val, 24)
    
    if all(bit == 0 for bit in res_sig):
        return {'res_bits': [0] * 32, 'flags': {}, 'trace': trace}
    
    while len(res_sig) > 0 and res_sig[0] == 0:
        res_sig = res_sig[1:] + [0]
        res_exp_val -= 1
    
    if len(res_sig) >= 24:
        res_f = res_sig[1:24]
    else:
        res_f = res_sig[1:] + [0] * (23 - len(res_sig) + 1)
    
    if len(res_f) > 23:
        res_f = res_f[:23]
    elif len(res_f) < 23:
        res_f = res_f + [0] * (23 - len(res_f))
    
    res_exp = int_to_bin_list(res_exp_val, EXP_WIDTH)
    
    result_bits = _repack_f32(res_s, res_exp, res_f)
    return {'res_bits': result_bits, 'flags': {}, 'trace': trace}

