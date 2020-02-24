from exprClass import Expr
from utils import error
from Definition import Define
from parser import parse
import re


class DefFunc:

    def __init__(self, context={}):
        self.globalCounter = 0
        self.context = context

    def index_gen(self):
        index = 'i' + str(self.globalCounter)
        self.globalCounter += 1
        return index

    def const(self, key: str, const: int):
        expr = Expr(self)
        expr.const(const)
        self.context.update({key: expr})

    def symbol(self, key: str, symbol: str):
        expr = Expr(self)
        expr.symbol(symbol)
        self.context.update({key: expr})

    # выражение функция, не объявление!
    def func(self, key: str, func: str, args: [str]):
        expr = Expr(self)
        expr.function(func, args)
        self.context.update({key: expr})

    def define(self, key: str, args: [[str]], res: [str], buildIn=False, buildInFunc=None):
        argsExpr = [[self.context[arg] for arg in argsList] for argsList in args]
        resExpr = [self.context[r] for r in res]
        func = Define(argsExpr, resExpr, buildIn, buildInFunc, key)
        self.context[key] = func

    def eval(self, key: str, args: [str] = []):
        func = self.context[key]
        argsExpr = [self.context[arg] for arg in args]
        return func.eval(argsExpr, self)

    def constOrSymbol(self, val: str):
        match = re.match('[-+]?[\d]+', val)
        index = self.index_gen()
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
            elif type(blockText) is str:
                block = blockText
                if block in localArgsDict:
                    blockOut.append(localArgsDict[block])
                elif block in self.context:
                    blockOut.append(block)
                else:
                    index = self.constOrSymbol(block)
                    blockOut.append(index)
            else:
                index = self.index_gen()
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
            argsOut = []
            localArgsDict = {}
            for argsText in argsTextList:
                localArgs = []
                for argT in argsText:
                    if type(argT) == list:
                        index = self.blockToIndex([argT], {})
                        localArgsDict[index[0]] = index[0]
                        localArgs.append(index[0])

                    elif argT in self.context:
                        index = argT
                        localArgsDict[argT] = index
                        localArgs.append(index)
                    else:
                        index = self.constOrSymbol(argT)
                        localArgsDict[argT] = index
                        localArgs.append(index)
                argsOut.append(localArgs)
            blockTextList = body.block
            blocksOut = self.blockToIndex(blockTextList, localArgsDict)
            self.define(name, argsOut, blocksOut)

    def patternMatch(self, exprP: Expr, exprE: Expr, localContext, context):
        if exprP.isConst and exprE.isConst:
            if exprP.val == exprE.val:
                return (True, localContext)
            else:
                return (False, localContext)
        # If symbol, everything is OK
        elif exprP.isConst:
            if exprE.isSymbol:
                newExprE = context[exprE.symbolVal]
                if newExprE != exprE:
                    return self.patternMatch(exprP, newExprE, localContext, context)
                else:
                    return (False, localContext)
            elif exprE.isFunc:
                key = exprE.funcKey
                args = exprE.args
                newExprE = self.eval(key, args)
                if newExprE != exprE:
                    return self.patternMatch(exprP, newExprE, localContext, context)
                else:
                    return (False, localContext)

            print('wow, big problems in match, man')

        elif exprP.isSymbol:
            localContext[exprP.symbolVal] = exprE
            return (True, localContext)
        elif exprP.isFunc and exprE.isFunc:
            if exprP.funcKey == exprE.funcKey:
                for argPstring, argEstring in zip(exprP.args, exprE.args):
                    argP = context[argPstring]
                    argE = context[argEstring]
                    (res, newContext) = self.patternMatch(argP, argE, localContext, context)
                    if res:
                        localContext.update(newContext)
                    else:
                        return (False, {})
                return (True, localContext)
            else:
                return (False, localContext)
        else:
            # if not working, maybe we need to eval  exprE.
            return (False, localContext)










