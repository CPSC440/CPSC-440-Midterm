from core.bit_converter import pretty_print_bin, bin_list_to_hex_str
from core.alu import encode_twos_complement, add, sub, decode_twos_complement
from core.m_extension import mul, div
from core.f_extension import fadd_f32
import struct

def float_to_bits(f):
    """Helper to get bit representation of a float for testing."""
    s = struct.pack('>f', f)
    return [int(b) for b in ''.join(f'{i:08b}' for i in s)]

def bits_to_float(b):
    """Helper to convert bit list back to float."""
    s = ''.join(map(str, b))
    i = int(s, 2)
    return struct.unpack('>f', i.to_bytes(4, 'big'))[0]

def main():
    print("--- Two's Complement & ALU Demo ---")
    val_a, val_b = 13, -7
    a_bits = encode_twos_complement(val_a)['bits']
    b_bits = encode_twos_complement(val_b)['bits']

    print(f"{val_a} -> {pretty_print_bin(a_bits)}")
    print(f"{val_b} -> {pretty_print_bin(b_bits)}")

    add_res = add(a_bits, b_bits)
    add_val = decode_twos_complement(add_res['result'])
    print(f"{val_a} + {val_b} = {add_val} (Flags: N={add_res['N']}, Z={add_res['Z']}, C={add_res['C']}, V={add_res['V']})")

    print("\n--- M Extension Demo ---")
    mul_res = mul(a_bits, b_bits)
    mul_val = decode_twos_complement(mul_res['rd_bits'])
    print(f"{val_a} * {val_b} = {mul_val} (Low 32 bits)")
    print("Multiplication Trace:")
    for line in mul_res['trace'][:3]: print(f"  {line}")
    print("  ...")

    div_a, div_b = -7, 3
    div_a_bits = encode_twos_complement(div_a)['bits']
    div_b_bits = encode_twos_complement(div_b)['bits']
    div_res = div(div_a_bits, div_b_bits)
    q_val = decode_twos_complement(div_res['q_bits'])
    r_val = decode_twos_complement(div_res['r_bits'])
    print(f"\n{div_a} / {div_b} = Q: {q_val}, R: {r_val}")

    print("\n--- F Extension Demo ---")
    f_a, f_b = 1.5, 2.25
    f_a_bits = float_to_bits(f_a)
    f_b_bits = float_to_bits(f_b)
    print(f"Adding {f_a} (0x{bin_list_to_hex_str(f_a_bits)[2:]}) and {f_b} (0x{bin_list_to_hex_str(f_b_bits)[2:]})")

    fadd_res = fadd_f32(f_a_bits, f_b_bits)
    fadd_val = bits_to_float(fadd_res['res_bits'])
    print(f"Result: {fadd_val:.2f} (0x{bin_list_to_hex_str(fadd_res['res_bits'])[2:]})")
    for line in fadd_res['trace']: print(f"  {line}")


if __name__ == "__main__":
    main()