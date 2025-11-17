import unittest
from core.alu import add, sub, encode_twos_complement, decode_twos_complement
from core.bit_converter import int_to_bin_list

class TestALU(unittest.TestCase):
    def test_twos_complement_codec(self):
        self.assertEqual(decode_twos_complement(encode_twos_complement(13)['bits']), 13)
        self.assertEqual(decode_twos_complement(encode_twos_complement(-13)['bits']), -13)
        self.assertEqual(decode_twos_complement(encode_twos_complement(0)['bits']), 0)
        self.assertTrue(encode_twos_complement(2**31)['overflow'])
    
    def test_add_overflow(self):
        a = int_to_bin_list(0x7FFFFFFF, 32)
        b = int_to_bin_list(1, 32)
        res = add(a, b)
        self.assertEqual(decode_twos_complement(res['result']), -2147483648)
        self.assertEqual(res['V'], 1)
        self.assertEqual(res['C'], 0)
        self.assertEqual(res['N'], 1)
        self.assertEqual(res['Z'], 0)

    def test_sub_overflow(self):
        a = encode_twos_complement(-2147483648, width=32)['bits']
        b = encode_twos_complement(2, width=32)['bits']
        res = sub(a, b)
        self.assertEqual(decode_twos_complement(res['result']), 2147483647)
        self.assertEqual(res['V'], 1)
        self.assertEqual(res['C'], 1)
        self.assertEqual(res['N'], 0)
        self.assertEqual(res['Z'], 0)

    def test_add_negatives(self):
        a = encode_twos_complement(-1)['bits']
        b = encode_twos_complement(-1)['bits']
        res = add(a, b)
        self.assertEqual(decode_twos_complement(res['result']), -2)
        self.assertEqual(res['V'], 0)
        self.assertEqual(res['C'], 1)
        self.assertEqual(res['N'], 1)
        self.assertEqual(res['Z'], 0)
    
    def test_add_to_zero(self):
        a = encode_twos_complement(13)['bits']
        b = encode_twos_complement(-13)['bits']
        res = add(a, b)
        self.assertEqual(decode_twos_complement(res['result']), 0)
        self.assertEqual(res['V'], 0)
        self.assertEqual(res['C'], 1)
        self.assertEqual(res['N'], 0)
        self.assertEqual(res['Z'], 1)

if __name__ == '__main__':
    unittest.main()