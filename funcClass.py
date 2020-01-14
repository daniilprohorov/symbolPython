from exprClass import Expr
from argsClass import Args


class Func:
    list_args = None
    list_blocks = None

    # аргументы как указатели
    def __init__(self, list_args: [Args], list_blocks: [Expr], buildIn=False, func=None):
        self.list_args = list_args
        self.list_blocks = list_blocks
        self.build_in = buildIn
        self.build_in_func = func

    def eval(self, context, argsValues=None):
        for args, block in zip(self.list_args, self.list_blocks):
            indexes = []
            for i, arg in enumerate(args.args):
                if arg.isConst:
                    indexes.append(i)
                else:
                    continue

            if indexes:
                for i in indexes:
                    argsValues[i] = argsValues[i].eval(context, argsValues)

            if all([args.args[i].val == argsValues[i].val for i in indexes]):

                if self.build_in:
                    new_args = []
                    for arg in argsValues:
                        new_args.append(arg.eval(context, argsValues))
                    return self.build_in_func(*argsValues)

                if block.isConst:
                    return block
                elif block.isSymbol:
                    # TODO: добавить контекст
                    symbol = block.symbolVal
                    for i, arg in enumerate(args.args):
                        if arg.isSymbol and symbol == arg.symbolVal:
                            return argsValues[i]

                elif block.isFunction:
                    return block.eval(context, argsValues)

            else:
                continue



        # if self.block.isConst:
        #     return self.block.val
        # elif self.block.isSymbol:
        #     # TODO: добавить контекст
        #     symbol = self.block.symbolVal
        #     for i, arg in enumerate(self.args):
        #         if arg.isSymbol and symbol == arg.symbolVal:
        #             return argsValues[i]
        #
        # elif self.block.isFunction:

            # for arg in context:
            #    if symbol == arg.symbolVal:
            #        return argsValues[i]
