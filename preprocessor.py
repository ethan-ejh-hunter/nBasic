import re
from typing import List

findNameRegex = "[a-zA-Z]\\w*\\("
getCenterRegex = "\\([a-zA-Z]\\w*(,[a-zA-Z]\\w*)*\\)"
getParamsCenterRegex = '\\(([a-zA-Z0-9]\\w*(,[a-zA-Z0-9]\\w*)*)|()\\)'
print(getParamsCenterRegex)
looksLikeMacroRegex = "[a-zA-Z]\\w*\\(([a-zA-Z0-9]\\w*(,[a-zA-Z0-9]\\w*)*)|()\\)"


class Macro:
    def __init__(self, name, data=[], args=[]):
        self.name = name
        self.data = data
        self.args = args

    def __eq__(self, other):
        if other.name is self.name:
            return True
        else:
            return False


class Context:
    def __init__(self, variables=[], constants=[], labels=[]):
        self.variables = None
        self.constants = None
        self.labels = None


class Var:
    def __init__(self, name, location):
        self.location = location
        self.name = name

    def __eq__(self, other):
        if other.name is self.name:
            return True
        else:
            return False


class aList:
    def __init__(self, num, locations):
        self.num = num
        self.locations = locations

    def __eq__(self, other):
        if other.num is self.num:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.num < other.num:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.num > other.num:
            return True
        else:
            return False


class Const:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        if other.name is self.name:
            return True
        else:
            return False


def replaceInString(string, listToFind, listToReplace) -> str:
    for (find, replace) in zip(listToFind, listToReplace):
        string = re.sub(find, replace, string)
    return string


def replaceInList(list, listToFind, listToReplace) -> List[str]:
    newLines = []
    for line in list:
        lineWithReplace = replaceInString(line, listToFind, listToReplace)
        newLines.append(lineWithReplace)
    return newLines


class Preprocessor:
    def getName(self, line: str) -> str:
        if "(" in line:
            nameAndParenth = re.search(findNameRegex, line)
            if nameAndParenth is None:
                self.error("improper macro definition (ex of correct: macro abc("
                           "a1,a2)")
            name = nameAndParenth.group()[:-1]
            return name
        else:
            self.error("Macro def has no left parenthases")

    def getArgs(self, line: str) -> List[str]:
        line = line.replace(" ", "")
        left = line.find("(")
        right = line.find(")")
        verifiedArgs = line[1 + left:right]
        allArgs = verifiedArgs.split(",")
        setArgs = set(allArgs)
        if not len(allArgs) == len(setArgs):
            self.error("macro def has args with the same name")
        return allArgs

    def getParams(self, line: str) -> List[str]:
        line = line.replace(" ", "")
        left = line.find("(")
        right = line.find(")")
        verifiedArgs = line[1 + left:right]
        allArgs = verifiedArgs.split(",")
        setArgs = set(allArgs)
        if not len(allArgs) == len(setArgs):
            self.error("macro def has args with the same name")
        return allArgs

    def looksLikeMacro(self) -> bool:
        found = re.search(looksLikeMacroRegex, self.currentLine)
        if found:
            return True
        else:
            return False

    def getNextLine(self):
        self.loc += 1
        if self.loc >= len(self.lines):
            self.currentLine = "EOF"
        else:
            self.currentLine = self.lines[self.loc].strip()

    def resetLoc(self):
        self.currentLine = self.lines[0]
        self.loc = 0

    def error(self, errorStr: str):
        raise SyntaxError("Error on line " + str(self.loc) + ": " + errorStr + " curLine = " + self.currentLine)

    def findMacros(self) -> List[str]:
        clean = []
        while self.currentLine != "EOF":
            if self.splitLine[0] is "macro":
                restOfLine = self.currentLine[4:]
                name = self.getName(restOfLine)
                args = self.getArgs(restOfLine)
                print(name)
                print(args)
                data = []
                self.getNextLine()
                while self.currentLine != "endMacro":
                    if self.currentLine == "EOF":
                        self.error("expected endMacro, found EOF")
                    data.append(self.currentLine)
                    self.getNextLine()
                self.definedMacros.append(Macro(name, data, args, 0))
            else:
                clean.append(self.currentLine)
            self.getNextLine()
        return clean

    def findMacro(self, name: str, numArgs: int):
        for i in self.definedMacros:
            if i.name == name and i.type == "macro" and len(i.args) == numArgs:
                return i
        return None

    def replaceCurrentLine(self, lines):
        linesP1 = self.lines[:self.loc]
        linesP2 = self.lines[self.loc + 1:]
        self.lines = linesP1 + lines + linesP2
        self.loc -= 1

    def deleteCurrentLine(self):
        linesP1 = self.lines[:self.loc]
        linesP2 = self.lines[self.loc + 1:]
        self.lines = linesP1 + linesP2
        self.loc -= 1

    def inlineMacros(self) -> List[str]:
        numInlinedMacros = 0
        while self.currentLine != "EOF":
            if self.looksLikeMacro():
                name = self.getName(self.currentLine)
                params = self.getParams(self.currentLine)
                macro = self.findMacro(name, len(params))
                if macro is None:
                    self.error("no function found with that name and number of arguments")
                else:
                    linesFromFunct = macro.data
                    if macro.args:
                        newLines = replaceInList(linesFromFunct, macro.args, params)
                    else:
                        newLines = linesFromFunct
                    newLines = ["inlinedMacro " + str(numInlinedMacros)] + newLines + ["endInlinedMacro"]
                    self.replaceCurrentLine(newLines)
            self.getNextLine()
        return self.lines

    def constant(self):
        while self.currentLine != "EOF":
            self.splitLine = self.currentLine.split()
            if self.splitLine[0] is "const":
                restOfLine = self.splitLine[1:]
                self.deleteCurrentLine()
                if len(restOfLine) == 2:
                    name = restOfLine[0]
                    num = restOfLine[1]
                    try:
                        parsedNum = int(num)
                    except ValueError:
                        self.error("the value of the constant must be an integer")
                    if not name.isalnum():
                        self.error("the name of the constant can be comprised only of alphanumerics")
                    if name.isdigit():
                        self.error("the name of the constant cannot be all numbers")
                    if not name[0].isalpha():
                        self.error("the name of the constant must begin with a letter")
                    if name in self.definedConst:
                        self.error("duplicate constant names: that's a no-no")
                    self.currentContext.consts.append(Const(name, parsedNum))
                else:
                    self.error("const must have exactly 2 arguments afterwards")
            self.getNextLine()

    def findLabel(self):
        while self.currentLine != "EOF":
            self.splitLine = self.currentLine.split()
            if self.splitLine[0] is "label":
                name = self.splitLine[1].strip()
                if not name.isalnum():
                    self.error("the name of the label can be comprised only of alphanumerics. Label name: " + name)
                if name.isdigit():
                    self.error("the name of the label cannot be all numbers. Label name: " + name)
                if not name[0].isalpha():
                    self.error("the name of the label must begin with a letter")
                if name in self.definedVars:
                    self.error("duplicate label/variable names: that's a no-no")
                self.currentContext.vars.append(Var(name, self.loc))
                self.deleteCurrentLine()
            self.getNextLine()

    def list(self):
        while self.currentLine != "EOF":
            self.splitLine = self.currentLine.split()
            if self.splitLine[0] is "list":
                list = self.splitLine[1:]
                name = list[0]
                if len(list) < 2:
                    self.error("list must have at least 1 element. Name: " + name)
                if not name.isalnum():
                    self.error("the name of the variable can be comprised only of alphanumerics. Name: " + name)
                if name.isdigit():
                    self.error("the name of the variable cannot be all numbers. Name: " + name)
                if not name[0].isalpha():
                    self.error("the name of the variable must begin with a letter. Name: " + name)
                if name in self.definedVars:
                    self.error("duplicate variable names: that's a no-no. Name: " + name)
                self.currentContext.definedVars.append(name)
                self.currentContext.varLocation.append(str(self.nextVarLocation))
                self.nextVarLocation += 1
                list = list[1:]
                for i in list:
                    if i in self.lists:
                        loc = self.lists.index(i)
                        self.lists[loc].locations.append(self.nextVarLocation)
                    else:
                        self.lists.append(aList(i, [self.nextVarLocation]))
                    self.nextVarLocation += 1
                self.deleteCurrentLine()
            self.getNextLine()

    def var(self):
        while self.currentLine != "EOF":
            self.splitLine = self.currentLine.split()
            if self.splitLine[0] is "var":
                name = self.splitLine[1].strip()
                if not name.isalnum():
                    self.error("the name of the variable can be comprised only of alphanumerics. Name: " + name)
                if name.isdigit():
                    self.error("the name of the variable cannot be all numbers. Name: " + name)
                if not name[0].isalpha():
                    self.error("the name of the variable must begin with a letter. Name: " + name)
                if name in self.definedVars:
                    self.error("duplicate variable names: that's a no-no. Name: " + name)
                self.currentContext.vars.append(Var(name, self.nextVarLocation))
                self.nextVarLocation += 1
                self.deleteCurrentLine()
            self.getNextLine()

    def include(self):
        while self.currentLine != "EOF":
            self.splitLine = self.currentLine.split()
            if self.splitLine[0] is "include":
                restOfLine = self.splitLine[1].strip()
                linesP1 = self.lines[:self.loc]
                linesP2 = self.lines[self.loc + 1:]
                with open(restOfLine, "r") as file:
                    lines = []
                    for line in file:
                        lines.append(line.strip())
                self.lines = linesP1 + lines + linesP2
            self.getNextLine()

    def evaluateCompileTimeArithmetic(self):
        commands = []
        for i in self.lines:
            if i[0] is "@":
                if "+" in i or "-" in i:
                    num = eval(i[1:])
                    commands.append("@" + str(num))
                else:
                    commands.append(i)
            else:
                commands.append(i)
        return commands

    def dealWith16BitWeirdness(self):
        commands = []
        for i in self.lines:
            if i[0] is "@":
                num = int(i[1:])
                if num > 32767:  # i.e. uses last bit of 16 bit number
                    commands.append("@32767")
                    if num is 32768:
                        commands.append("A=A+1")
                    else:
                        commands.append("D=A+1")
                        leftOver = num - 32768
                        commands.append("@" + str(leftOver))
                        commands.append("A=A+D")
                else:
                    commands.append(i)
            else:
                commands.append(i)
        return commands

    def writeLists(self):
        self.listNums, self.listLocations = (list(t) for t in zip(*sorted(zip(self.listNums, self.listLocations))))
        commands = []
        prev = -1
        containsPartialNum = False
        for i, locs in zip(self.listNums, self.listLocations):
            if i == 0:
                commands.append("D=0")
            elif i == 1:
                commands.append("D=1")
                prev = 1
            elif prev + 1 == i:
                commands.append("D=D+1")
            else:
                commands.append("@" + str(i))
                commands.append("D=A")
                prev = i
            for j in locs:
                commands.append("@" + str(j))
                commands.append("M=D")
        return commands

    def doOperation(self, function):
        self.resetLoc()
        return function()

    def __init__(self, readFileName: str = None, writeFileName: str = None, lines=None):
        self.mainContext = Context()
        self.currentContext = self.mainContext
        self.contexts = []
        self.loc = 0
        self.splitLine = []
        self.nextVarLocation = 0
        self.definedMacros = []
        self.inMacro = False
        if writeFileName:
            writeFile = open(writeFileName, 'w')
        self.lines = []
        if lines:
            self.lines = lines
        if readFileName:
            with open(readFileName) as file:
                for line in file:
                    self.lines.append(line.strip())

    def preprocess(self):
        self.doOperation(self.include)  # find include statements, add to file
        self.lines = self.doOperation(self.findMacros)  # find macros in file
        self.doOperation(self.inlineMacros)  # inline
        self.doOperation(self.findLabel)  # find instances of label
        self.doOperation(self.var)  # find instances of var
        self.doOperation(self.list)  # find instances of list
        self.lines = replaceInList(self.lines, self.definedVars,
                                   self.varLocation)  # replace instances of name of list or var
        self.doOperation(self.constant)  # do constants stuff
        self.lines = replaceInList(self.lines, self.definedConst, self.constValues)  # replace constants
        self.lines = self.evaluateCompileTimeArithmetic()  # do arithmatic at compile-time

        if len(self.listNums) > 0:
            self.lines = self.writeLists() + self.lines
        self.lines = self.dealWith16BitWeirdness()  # deal with a reg not being able to store full 16 bit value

        cleanedSpaces = []
        for parsed in self.lines:
            if parsed != " " and parsed != '':
                cleanedSpaces.append(parsed)
        self.preprocessed = cleanedSpaces


preprocessor = Preprocessor("program.txt")
print(preprocessor.lines)
preprocessor.preprocess()
print(preprocessor.lines)
