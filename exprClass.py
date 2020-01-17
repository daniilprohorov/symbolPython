class Expr:

    def __init__(self):
        self.args = None
        self.val = None
        self.symbolVal = None
        self.funcKey = None
        self.isConst = False
        self.isSymbol = False
        self.isFunc = False

    def const(self, val):
        self.val = val
        self.isConst = True

    def symbol(self, symbol):
        self.symbolVal = symbol
        self.isSymbol = True

    def function(self, funcKey, args: [str]):
        self.funcKey = funcKey
        self.args = args
        self.isFunc = True

    def eval(self, context, argsDict, argsValues):
        if self.isConst:
            return self
        elif self.isSymbol:
            if self.symbolVal in argsDict:
                i = argsDict[self.symbolVal]
                return argsValues[i]
            elif self.symbolVal in context:
                return context[self.symbolVal]
            else:
                return self
        elif self.isFunc:
            # вычисляем аргументы, которые strict
            func = context[self.funcKey]
            # strict_args = [label for label, p in self.args if p == "strict"]
            newArgsVals = []
            for i, arg in enumerate(self.args):
                index = None
                if arg in argsDict:
                    index = argsDict[arg]
                    evaluated = argsValues[index].eval(context, argsDict, argsValues)
                    # argsValues[index] = evaluated
                    newArgsVals.append(evaluated)
                    # newArgsVals = [argsValues[argsDict[a]] for a in self.args]
                elif arg in context:
                    evaluated = context[arg].eval(context, argsDict, argsValues)
                    # argsValues[i] = evaluated
                    newArgsVals.append(evaluated)
                    # newArgsVals = argsValues

            return func.eval(context, newArgsVals)

    def toString(self):
        if self.isConst:
            return str(self.val)
        elif self.isSymbol:
            return str(self.symbolVal)
        else:
            return self.funcKey



def expr_equals(expr1: Expr, expr2: Expr):
    if expr1.isConst and expr2.isConst:
        return expr1.val == expr2.val
    elif expr1.isSymbol and expr2.isSymbol:
        return expr1.symbolVal == expr2.symbolVal
    elif expr1.isFunc and expr2.isFunc:
        return expr1.funcKey == expr2.funcKey and expr1.args == expr2.args
    else:
        False









