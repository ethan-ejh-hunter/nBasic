import unittest

import assembler


class MyTestCase(unittest.TestCase):
    def test_A_Instruction(self):
        self.assertEqual(assembler.translateLine("@124"), "0000000001111100")

    def test_Store_Instructions(self):
        self.assertEqual(assembler.translateLine("M=1"), "1110111111001000")
        self.assertEqual(assembler.translateLine("D=M"), "1111110000010000")
        self.assertEqual(assembler.translateLine("D=D-A"), "1110010011010000")
        self.assertEqual(assembler.translateLine("M=D+M"), "1111000010001000")
        self.assertEqual(assembler.translateLine("M=M+1"), "1111110111001000")

    def test_Jump_Instructions(self):
        self.assertEqual(assembler.translateLine("0;JMP"), "1110101010000111")
        self.assertEqual(assembler.translateLine("D;JGT"), "1110001100000001")


if __name__ == '__main__':
    unittest.main()
