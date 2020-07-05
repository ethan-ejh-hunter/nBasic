import CPU


class ROM:
    def __init__(self, ROM):
        self.cpu = CPU.nandCPU()
        self.rom = ROM
        self.actualLength = len(ROM)
        amountToAdd = 32768 - self.actualLength
        self.rom += [0] * amountToAdd
        self.cpu.ip = 0

    def startEmulation(self):
        for i in range(0, self.actualLength):
            currentInstruction = self.rom[self.cpu.ip]
            self.cpu.doInstruction(currentInstruction)
        print(1)
