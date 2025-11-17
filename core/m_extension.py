from .alu import decode_twos_complement, encode_twos_complement, sub, add

WIDTH = 32

def mul(rs1_bits, rs2_bits):
    """Performs signed 32-bit multiplication (rs1 * rs2)."""
    
    rs1_val = decode_twos_complement(rs1_bits)
    rs2_val = decode_twos_complement(rs2_bits)
    
    result_val = rs1_val * rs2_val
    
    result_bits = encode_twos_complement(result_val, width=WIDTH)['bits']
    
    return {
        'rd_bits': result_bits,
        'trace': []
    }

def div(rs1_bits, rs2_bits):
    """
    Performs signed 32-bit division (rs1 / rs2) using a restoring algorithm.
    rs1 is the dividend, rs2 is the divisor.
    """
    
    rs1_val = decode_twos_complement(rs1_bits)
    rs2_val = decode_twos_complement(rs2_bits)
    
    if rs2_val == 0:
        q_bits = encode_twos_complement(-1, width=WIDTH)['bits']
        r_bits = rs1_bits
        return {'q_bits': q_bits, 'r_bits': r_bits}

    quotient_negative = (rs1_val < 0) ^ (rs2_val < 0) 
    
    abs_rs1_bits = encode_twos_complement(abs(rs1_val), width=WIDTH)['bits']
    abs_rs2_bits = encode_twos_complement(abs(rs2_val), width=WIDTH)['bits']

    A = [0] * WIDTH
    Q = abs_rs1_bits
    M = abs_rs2_bits

    for _ in range(WIDTH):
        A_msb = Q.pop(0) 
        A.append(A_msb)
        Q.append(0)
        
        A.pop(0)

        A_minus_M = sub(A, M)
        
        if A_minus_M['N'] == 1: 
            Q[-1] = 0
            
            A = add(A_minus_M['result'], M)['result'] 

            if len(A) > WIDTH:
                A.pop(0) 
                
        else:
            Q[-1] = 1
            A = A_minus_M['result']
            
            if len(A) > WIDTH:
                A.pop(0)
                
    final_quotient_val = decode_twos_complement(Q)
    final_remainder_val = decode_twos_complement(A)

    if quotient_negative:
        Q = encode_twos_complement(-final_quotient_val, width=WIDTH)['bits']
    
    if rs1_val < 0 and final_remainder_val != 0:
        A = encode_twos_complement(-final_remainder_val, width=WIDTH)['bits']

    return {'q_bits': Q, 'r_bits': A}