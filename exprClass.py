class Expr:

    def __init__(self):
        self.func = None
        self.args = None
        self.val = None
        self.symbolVal = None
        self.key = None
        self.keyArgs = None
        self.isFunction = False
        self.isConst = False
        self.isSymbol = False
        self.isKey = False

    def function(self, func):
        self.func = func
        self.isFunction = True

    def const(self, val):
        self.val = val
        self.isConst = True

    def symbol(self, symbol):
        self.symbolVal = symbol
        self.isSymbol = True

    def key(self, key: str, keyArgs: [str]):
        self.key = key
        self.keyArgs = keyArgs
        self.isKey = True

    def eval(self, context, args):
        if self.isConst:
            return self
        elif self.isSymbol:
            return self
        elif self.isFunction:
            cArgs = self.args.args

            new_expr = self.func.eval(context, args)
            return new_expr
        elif self.isKey:
            context.update(args)
            if self.key in context:
                block = context[self.key]
                return block.eval()
            else:
                return self
