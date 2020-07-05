import Rom
import assembler
import preprocessor


def run(fileName):
    lines = []
    if fileName:
        with open(fileName) as file:
            for line in file:
                lines.append(line.strip())
    prep = preprocessor.Preprocessor
    a = prep(readFileName=None, lines=lines)
    a.preprocess()
    preprocessed = a.preprocessed
    assembled = assembler.assembleArray(preprocessed)
    print(assembled)
    converted = []
    for i in assembled:
        converted.append(int(i, 2))
    rom = Rom.ROM(converted)
    rom.startEmulation()


run("basic.txt")
