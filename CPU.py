from typing import List


def makeFlags(num: int) -> List[bool]:
    flags = []
    for i in range(11, 5, -1):
        if num & (2 ** i) == 0:
            flags.append(False)
        else:
            flags.append(True)
    return flags


class nandCPU:
    def __init__(self):
        self.regA = 0
        self.regD = 0
        self.ram = [0] * 16384
        self.screen = [0] * 8192
        self.ip = 0

    def ALU(self, flags: List[bool], x: int, y: int) -> int:
        if flags[0]:  # zx
            x = 0
        if flags[1]:  # nx
            x = ~ x
        if flags[2]:  # zy
            y = 0
        if flags[3]:  # ny
            y = ~ y
        # print(y)
        # print(x)
        if flags[4]:
            out = x + y
        else:
            out = x & y
        if flags[5]:
            out = ~ out
        return out

    def doInstruction(self, instruction: int):
        a = instruction & 32768
        if instruction & 32768 == 0:
            self.A_Instruction(instruction)
        else:
            self.C_Instruction(instruction)

    def A_Instruction(self, num: int):  # instruct format: 0vvv vvvv vvvv vvvv
        num = num & 32767  # use bitmask to remove first bit
        self.regA = num
        self.ip += 1

    def getMem(self) -> int:
        if self.regA < 16384:
            return self.ram[self.regA]
        elif self.regA < 24576:
            return self.screen[self.regA - 16384]
        elif self.regA == 24576:
            return 0  # TODO make keyboard work

    def storeMem(self, num: int):
        if self.regA < 16384:
            self.ram[self.regA] = num
        elif self.regA < 24576:
            self.screen[self.regA - 16384] = num

    def C_Instruction(self, num: int):  # 1 1 1 a   c1 c2 c3 c4   c5 c6 d1 d2   d3 j1 j2 j3
        if num & 4096 == 0:  # use bitmask to get a
            y = self.regA
            print("y = A")
        else:
            y = self.getMem()
            print("y = M")
        flags = makeFlags(num)
        ans = self.ALU(flags, self.regD, y)
        if 2 ** 3 & num > 0:
            print("stored in mem")
            self.storeMem(ans)
        if 2 ** 4 & num > 0:
            print("stored in D")
            self.regD = ans
        if 2 ** 5 & num > 0:
            print("stored in A")
            self.regA = ans
        shouldJump = False
        if (1 & num > 0) and (ans > 0):
            shouldJump = True
        if (2 & num > 0) and (ans == 0):
            shouldJump = True
        if (4 & num > 0) and (ans < 0):
            shouldJump = True
        print(shouldJump)
        if shouldJump:
            self.ip = self.regA
        else:
            self.ip += 1

# c = nandCPU()
# c.regA=10
# c.doInstruction(19)
# print(a)
