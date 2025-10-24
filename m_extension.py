from .alu import add
from .bit_converter import zero_extend, int_to_bin_list, decode_twos_complement, sign_extend, encode_twos_complement, pretty_print_bin, invert

def mul(rs1_bits, rs2_bits):

    trace = []
    width = 32

    multiplicand = sign_extend(rs1_bits, width * 2)
    product = zero_extend(rs2_bits, width * 2)

    trace.append(f"Initial: P={decode_twos_complement(product)}, M={decode_twos_complement(multiplicand)}")

    for i in range(width):
        step_trace = f"step {i + 1}: "
        if product [-1] == 1:
            add_res = add(product[:width], multiplicand[:width])
            upper_product = add_res['result']
            product = upper_product + product[width:]
            step_trace += f"P+=M. P={decode_twos_complement(product)}. "

        product = [product[0]] + product[:-1]
        step_trace += f"Arithmetic right shift. P={decode_twos_complement(product)}"
        trace.append(step_trace)

    full_product_val = decode_twos_complement(product)
    low_32_val = decode_twos_complement(product[width:])
    overflow = full_product_val != low_32_val

    return {
        'rd_bits': product[width:],
        'overflow': overflow,
        'trace': trace
    }

def div(rs1_bits, rs2_bits):

    trace = []
    width = 32
    dividend_val = decode_twos_complement(rs1_bits)
    divisor_val = decode_twos_complement(rs2_bits)

    if divisor_val == 0:
        return {'q_bits': [-1]*width, 'r_bits': rs1_bits, 'trace': ["Division by zero"]}
    if dividend_val == -2**(width - 1) and divisor_val == -1:
        return {'q_bits': rs1_bits, 'r_bits': [0]*width, 'trace': ["Overflow case"]}
    
    dividend_pos = int_to_bin_list(abs(dividend_val), width)
    divisor_pos = int_to_bin_list(abs(divisor_val), width)

    quotient = [0]*width
    remainder = zero_extend(dividend_pos, width)

    divisor_64 = zero_extend(divisor_pos, width * 2)
    remainder_64 = zero_extend(remainder, width * 2)

    trace.append(f"Initial: R={pretty_print_bin(remainder_64)}, D={pretty_print_bin(divisor_64)}")

    for i in range(width):
        remainder_64 = remainder_64[1:] + [0]
        trace.append(f"Step {i + 1}: Shift left R. R={pretty_print_bin(remainder_64)}")

        original_rem = remainder_64[:]
        sub_res = add(remainder_64, invert(divisor_64))
        sub_res = add(sub_res['result'], int_to_bin_list(1, width * 2))
        remainder_64 = sub_res['result']

        if remainder_64[0] == 1:
            quotient = quotient[1:] + [0]
            remainder_64 = original_rem
            trace.append(f"Step {i+1} (Restore): R < 0. Set q_bit=0. Restore R.")
        else:
            quotient = quotient[1:] + [1]
            trace.append(f"Step {i+1} (Subtract): R >= 0. Set q_bit=1.")
    
    if (dividend_val < 0) != (divisor_val < 0):
        quotient = encode_twos_complement(-decode_twos_complement(quotient))['bits']
    if dividend_val < 0:
        remainder_64 = encode_twos_complement(-decode_twos_complement(remainder_64))['bits']

    return {
        'q_bits': quotient,
        'r_bits': remainder_64[width:],
        'trace': trace
    }