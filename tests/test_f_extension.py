from core.f_extension import fadd_f32
from core.bit_converter import hex_str_to_bin_list, bin_list_to_hex_str

def test_fadd():
    print("--- Testing FADD ---")
    
    f_a_bits = hex_str_to_bin_list("0x3FC00000", width=32)
    f_b_bits = hex_str_to_bin_list("0x40100000", width=32)
    expected_hex = "0x40700000"
    
    res = fadd_f32(f_a_bits, f_b_bits)
    result_hex = bin_list_to_hex_str(res['res_bits'])
    
    assert result_hex == expected_hex, f"Test 1 Failed: 1.5 + 2.25 Expected {expected_hex}, Got {result_hex}"

    f_one = hex_str_to_bin_list("0x3F800000", width=32)
    expected_two = "0x40000000"
    
    res2 = fadd_f32(f_one, f_one)
    result_hex2 = bin_list_to_hex_str(res2['res_bits'])
    
    assert result_hex2 == expected_two, f"Test 2 Failed: 1.0 + 1.0 Expected {expected_two}, Got {result_hex2}"

    print("FADD tests passed!")

if __name__ == '__main__':
    test_fadd()