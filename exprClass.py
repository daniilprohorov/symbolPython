class Expr:

    def __init__(self, process):
        self.args = None
        self.val = None
        self.symbolVal = None
        self.funcKey = None
        self.isConst = False
        self.isSymbol = False
        self.isFunc = False
        self.process = process

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
            onlyArgsVals = False
            if self.funcKey in context:
                func = context[self.funcKey]
            elif argsValues:
                onlyArgsVals = True
            else:
                return self
            # TODO: Problem with lazy is here

            # newArgsVals = []
            # for i, arg in enumerate(self.args):
            #     index = None
            #     if arg in argsDict:
            #         index = argsDict[arg]
            #         val = argsValues[index]
            #         newArgsVals.append(val)
            #     elif arg in context:
            #         fromContext = context[arg]
            #         newArgsVals.append(fromContext)
            #
            # return func.eval(newArgsVals, self.process)



            newArgsVals = []
            for i, arg in enumerate(self.args):
                index = None
                if arg in argsDict:
                    index = argsDict[arg]
                    if onlyArgsVals:
                        evaluated = index
                    else:
                        evaluated = argsValues[index].eval(context, argsDict, argsValues)
                    # argsValues[index] = evaluated
                    newArgsVals.append(evaluated)
                    # newArgsVals = [argsValues[argsDict[a]] for a in self.args]
                elif arg in context:
                    fromContext = context[arg]
                    # local import
                    from Definition import Define

                    if isinstance(fromContext, Expr):
                        if fromContext.funcKey and fromContext.funcKey[0].isupper():
                            evaluated = fromContext
                        else:
                            evaluated = fromContext.eval(context, argsDict, argsValues)
                    elif isinstance(fromContext, Define):
                        # evaluated = fromContext.eval(argsValues, self.process)
                        # evaluated = fromContext
                        evaluated = argsValues[fromContext].eval(context, argsDict, argsValues)

                    newArgsVals.append(evaluated)
                    # newArgsVals = argsValues

            if onlyArgsVals:
                self.args = newArgsVals
                return self
            else:
                return func.eval(newArgsVals, self.process)

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









