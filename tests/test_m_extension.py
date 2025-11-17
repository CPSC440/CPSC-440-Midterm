from core.m_extension import mul, div
from core.alu import decode_twos_complement, encode_twos_complement

def test_mul():
    print("--- Testing MUL ---")
    
    rs1_10 = encode_twos_complement(10, width=32)['bits']
    rs2_5 = encode_twos_complement(5, width=32)['bits']
    res1 = mul(rs1_10, rs2_5)
    assert decode_twos_complement(res1['rd_bits']) == 50, "Test 1 Failed: 10 * 5 != 50"

    rs1_13 = encode_twos_complement(13, width=32)['bits']
    rs2_neg7 = encode_twos_complement(-7, width=32)['bits']
    res2 = mul(rs1_13, rs2_neg7)
    assert decode_twos_complement(res2['rd_bits']) == -91, "Test 2 Failed: 13 * -7 != -91"

    print("MUL tests passed!")

def test_div():
    print("\n--- Testing DIV ---")
    
    rs1_10 = encode_twos_complement(10, width=32)['bits']
    rs2_3 = encode_twos_complement(3, width=32)['bits']
    res1 = div(rs1_10, rs2_3)
    assert decode_twos_complement(res1['q_bits']) == 3, "Test 1 Q Failed: 10 / 3 != 3"
    assert decode_twos_complement(res1['r_bits']) == 1, "Test 1 R Failed: 10 % 3 != 1"

    rs1_neg7 = encode_twos_complement(-7, width=32)['bits']
    rs2_3 = encode_twos_complement(3, width=32)['bits']
    res2 = div(rs1_neg7, rs2_3)
    assert decode_twos_complement(res2['q_bits']) == -2, "Test 2 Q Failed: -7 / 3 != -2"
    assert decode_twos_complement(res2['r_bits']) == -1, "Test 2 R Failed: -7 % 3 != -1"

    rs1_1 = encode_twos_complement(1, width=32)['bits']
    rs2_0 = encode_twos_complement(0, width=32)['bits']
    res3 = div(rs1_1, rs2_0)
    assert decode_twos_complement(res3['q_bits']) == -1, "Test 3 Q Failed: Division by Zero should return -1"
    
    print("DIV tests passed!")

if __name__ == '__main__':
    test_mul()
    test_div()