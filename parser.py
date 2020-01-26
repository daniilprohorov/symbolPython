import re
from utils import error

def prgList():
    filename = "prg"
    funcSymbol = "@"
    with open(filename, "r") as f:
        prgFile = f.read()
        newLinesDel = prgFile.replace('\n', "")
        multSpaceDel = re.sub(' +', ' ', newLinesDel)
        leftBracketSpaceDel = re.sub(r'\( ', '(', multSpaceDel)
        rightBracketSpaceDel = re.sub(r' \)', ')', leftBracketSpaceDel)
        backNewLines = rightBracketSpaceDel.replace(funcSymbol, '\n' + funcSymbol)
        result = [line for line in backNewLines.split('\n') if line != '']
        return result

def appendLast(n, lst, val):
    if n == 0:
        lst.append(val)
    else:
        appendLast(n-1, lst[-1], val)

def splitWithBrackets(line):
    acc = ""
    splitedList = []
    bracketsCount = 0
    for ch in line:
        if ch == '(':
            appendLast(bracketsCount, splitedList, [])
            bracketsCount += 1
            # acc.append([])
        elif ch == ')':
            if acc != '':
                appendLast(bracketsCount, splitedList, acc)
                acc = ''
            if bracketsCount > 0:
                bracketsCount -= 1
            else:
                error("Brackets order error")
        elif ch == ' ':
            appendLast(bracketsCount, splitedList, acc)
            acc = ""
        else:
            acc += (ch)

    if acc != '':
        appendLast(bracketsCount, splitedList, acc)
        acc = ''
    return splitedList

def splitListByEqual(lst):
    a = []
    b = []
    flag = "A"
    for el in lst:
        if el == '=':
            flag = "B"
            continue

        if flag == "A":
            a.append(el)
        else:
            b.append(el)
    return (a, b)



class PreFunc:
    def __init__(self, name: str, args: [str], block: [str]):
        self.name = name
        self.args = [args]
        self.block = [block]

    def addPattern(self, args: [str], block: [str]):
        self.args.append(args)
        self.block.append(block)

def preParse(lines):
    preParsed = [splitWithBrackets(ln)[1:] for ln in lines]
    splited = [splitListByEqual(l) for l in preParsed]
    context = {}
    for fst, snd in splited:
        name = fst[0]
        args = fst[1:]
        block = snd
        if name in context:
            context[name].addPattern(args, block)
        else:
            p = PreFunc(name, args, block)
            context[fst[0]] = p

    return context


def parse():
    result = preParse(prgList())
    return result

lol = parse()
print(parse())

