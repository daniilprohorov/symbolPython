from exprClass import Expr
from utils import error
from funcClass import Func
from parser import parse
import re


class DefFunc:

    def __init__(self, context={}):
        self.globalCounter = 0
        self.context = context

    def indexGen(self):
        index = 'i' + str(self.globalCounter)
        self.globalCounter += 1
        return index

    def const(self, key: str, const: int):
        expr = Expr()
        expr.const(const)
        self.context.update({key: expr})

    def symbol(self, key: str, symbol: str):
        expr = Expr()
        expr.symbol(symbol)
        self.context.update({key: expr})

    # выражение функция, не объявление!
    def func(self, key: str, func: str, args: [str]):
        expr = Expr()
        expr.function(func, args)
        self.context.update({key: expr})

    def define(self, key: str, args: [[str]], res: [str], buildIn=False, buildInFunc=None):
        argsExpr = [[self.context[arg] for arg in argsList] for argsList in args]
        resExpr = [self.context[r] for r in res]
        func = Func(argsExpr, resExpr, buildIn, buildInFunc)
        self.context[key] = func

    def eval(self, key: str, args: [str] = []):
        func = self.context[key]
        argsExpr = [self.context[arg] for arg in args]
        return func.eval(self.context, argsExpr)

    def constOrSymbol(self, val: str):
        match = re.match('[-+]?[\d]+', val)
        index = self.indexGen()
        if match:
            self.const(index, int(val))
        else:
            self.symbol(index, val)
        return index

    def blockToIndex(self, blockTextList, localArgsDict):
        blockOut = []
        for blockText in blockTextList:
            if len(blockText) == 1:
                block = blockText[0]
                if block in localArgsDict:
                    blockOut.append(localArgsDict[block])
                elif block in self.context:
                    blockOut.append(block)
                else:
                    index = self.constOrSymbol(block)
                    blockOut.append(index)
            else:
                index = self.indexGen()
                nameOfFunc = blockText[0]
                argsIndexes = [self.blockToIndex([block], localArgsDict)[0] for block in blockText[1:]]
                self.func(index, nameOfFunc, argsIndexes)
                blockOut.append(index)
        return blockOut

    def create(self):
        pass

    def parseContext(self):
        functions = parse()
        for name in functions:
            body = functions[name]
            argsTextList = body.args
            # if argsTextList == [[]]:
            #     blockTextList = body.block
            #     blocksOut = self.blockToIndex(blockTextList, localArgsDict)
            #     self.symbol(name, blocksOut[0])
            # else:
            argsOut = []
            localArgsDict = {}
            for argsText in argsTextList:
                localArgs = []
                for argT in argsText:
                    if argT in self.context:
                        index = argT
                        localArgsDict[argT] = index
                        localArgs.append(index)
                    else:
                        index = self.constOrSymbol(argT)
                        localArgsDict[argT] = index
                        localArgs.append(index)
                argsOut.append(localArgs)
            # TODO: исправить тут костыль
            blockTextList = body.block
            blocksOut = self.blockToIndex(blockTextList, localArgsDict)
            self.define(name, argsOut, blocksOut)









