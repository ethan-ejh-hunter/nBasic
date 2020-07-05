possibleOperations = ["0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-1", "A-1", "D+A", "D-A", "A-D",
                      "D&A", "D|A", "M", "!M", "-M", "M+1", "M-1", "D+M", "D-M", "M-D", "D&M", "D|M"]
operationOpcode = ["0101010", "0111111", "0111010", "0001100", "0110000", "0001101", "0110001", "0001111", "0110011",
                   "0011111", "0110111", "0001110", "0110010", "0000010", "0010011", "0000111", "0000000", "0010101",
                   "1110000", "1110001", "1110011", "1110111", "1110010", "1000010", "1010011", "1000111", "1000000",
                   "1010101"]
translateFromOperations = ["1+D", "1+A", "A+D", "A&D" "A|D", "1+M", "M+D", "M&D", "M|D"]
translateToOperations = ["D+1", "A+1", "D+A", "D&A" "D|A", "M+1", "D+M", "D&M", "D|M"]
possibleJumps = ["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
jumpsOpcode = ["001", "010", "011", "100", "101", "110", "111"]
print(len(operationOpcode))
print(len(possibleOperations))


def translateLine(line: str) -> str:
    if line[0] == "@":
        unparsed = line[1:]
        parsedNum = int(unparsed)
        unpaddedBinaryNumber = bin(parsedNum)
        paddedBinaryNumber = unpaddedBinaryNumber[2:].zfill(16)  # remove inital 0b at begin of string
        return paddedBinaryNumber
    else:
        command = "111"
        statement = getStatement(line)
        if "=" in statement:
            operation = getOperation(statement)
            equality = getEquality(statement)
        else:
            equality = None
            operation = statement
        operation = translateOperation(operation)  # this fixes problems such as not having '1+A' recognized as 'A+1'
        command += getOperationOpcode(operation)
        print(command)
        jumpVals = getJumpValues(line)
        if equality is not None:
            command += generateEqualityOpcode(equality)
        else:
            command += "000"
        print(command)
        if jumpVals is not None:
            command += generateJumpOpcode(jumpVals)
        else:
            command += "000"
        print(command)
        return command


def generateJumpOpcode(jumpVals):
    if jumpVals in possibleJumps:
        loc = possibleJumps.index(jumpVals)
    else:
        raise SyntaxError("jump " + jumpVals + " does not exist")
    return jumpsOpcode[loc]


def generateEqualityOpcode(equality: str) -> str:
    print(equality)
    command = ""
    if "A" in equality:
        command = "1"
    else:
        command = "0"
    if "D" in equality:
        command = command + "1"
    else:
        command = command + "0"
    if "M" in equality:
        command = command + "1"
    else:
        command = command + "0"
    return command


def getOperation(statement: str) -> str:
    if "=" in statement:
        loc = statement.find("=")
        return statement[loc + 1:]
    else:
        return statement


def translateOperation(operation: str) -> str:
    if operation in translateFromOperations:
        loc = translateFromOperations.index(operation)
        return translateToOperations[loc]
    else:
        return operation


def getOperationOpcode(operation: str) -> str:
    if operation in possibleOperations:
        loc = possibleOperations.index(operation)
    else:
        raise SyntaxError("operation " + operation + " does not exist")
    return operationOpcode[loc]


def getStatement(line: str) -> str:
    if ";" in line:
        loc = line.find(";")
        return line[:loc]
    else:
        return line


def getEquality(statement: str) -> str:
    if "=" in statement:
        loc = statement.find("=")
        return statement[:loc]
    else:
        return None


def getJumpValues(line: str) -> str:
    if ";" in line:
        loc = line.find(";")
        return line[loc + 1:]
    else:
        return None


def assembleArray(lines):
    returnFile = []
    for line in lines:
        strippedLine = line.strip()
        if not strippedLine == "":
            returnFile.append(translateLine(strippedLine))
    return returnFile
