import unittest

import CPU


class TestCPU(unittest.TestCase):
    myCPU = CPU.nandCPU()

    def test_ALU(self):
        self.assertEqual(self.myCPU.ALU([False, False, False, False, False, False], 1, 1), 1)
        self.assertEqual(self.myCPU.ALU([False, False, False, False, True, False], 1, 1), 2)
        self.assertEqual(self.myCPU.ALU([True, False, False, False, True, False], 1, 1), 1)
        self.assertEqual(self.myCPU.ALU([True, False, True, False, True, False], 1, 1), 0)
        self.assertEqual(self.myCPU.ALU([False, False, True, True, True, False], 1, 1), 0)
        self.assertEqual(self.myCPU.ALU([False, False, True, True, True, False], 0, 1), -1)
        self.assertEqual(self.myCPU.ALU([False, True, False, False, True, True], 0, 1), -1)
        self.assertEqual(self.myCPU.ALU([False, True, False, False, True, True], 5, 1), 4)
        self.assertEqual(self.myCPU.ALU([True, True, False, True, True, True], 5, 1), 2)
        self.assertEqual(self.myCPU.ALU([True, True, False, True, True, True], 5, 100), 101)

    def test_A_Instruction(self):
        self.myCPU.A_Instruction(int(bin(50), 2))
        self.assertEqual(self.myCPU.regA, 50)
        self.myCPU.A_Instruction(int(bin(9999), 2))
        self.assertEqual(self.myCPU.regA, 9999)

    def test_makeFlags(self):
        self.assertEqual(CPU.makeFlags(2688), [True, False, True, False, True, False])
        self.assertEqual(CPU.makeFlags(1856), [False, True, True, True, False, True])
        self.assertEqual(CPU.makeFlags(3520), [True, True, False, True, True, True])

    def test_several(self):
        self.myCPU.A_Instruction(100)
        self.myCPU.C_Instruction(60881)
        self.assertEqual(self.myCPU.ip, 100)
        self.assertEqual(self.myCPU.regD, 101)


if __name__ == '__main__':
    unittest.main()
