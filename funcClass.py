from exprClass import Expr
from typing import Dict
from argsClass import Args


class Func:
    list_args = None
    list_blocks = None

    # аргументы как указатели
    def __init__(self, list_args: [[Expr]], list_blocks: [Expr], buildIn=False, func=None, label="unknown"):
        self.list_args = list_args
        self.list_blocks = list_blocks
        self.build_in = buildIn
        self.build_in_func = func
        self.label = label

        # self.argsDict = {arg: i for args in self.list_args for i, arg in enumerate(args)}

    # def eval(self, context, argsValues):
    #     for args, block in zip(self.list_args, self.list_blocks):
    #         argsValuesList = []
    #         const_args = [arg for arg in args if arg.isConst]
    #         argsDict = {arg.toString(): i for i, arg in enumerate(args)}
    #
    #         for const in const_args:
    #             key = argsDict[const.toString()]
    #             currentArg = argsValues[key]
    #             if currentArg.isConst:
    #                 newExpr = Expr()
    #                 newExpr.const(currentArg.val)
    #                 argsValuesList.append(newExpr)
    #             else:
    #                 currentArg = currentArg.eval(context, argsDict, argsValues)
    #                 if currentArg.isConst:
    #                     newExpr = Expr()
    #                     newExpr.const(currentArg.val)
    #                     argsValuesList.append(newExpr)
    #                 else:
    #                     print("Pattern match error")
    #                     return None
    #
    #         if [v.val for v in const_args] != [v.val for v in argsValuesList]:
    #             continue
    #         else:
    #             if self.build_in:
    #                 # args.update(const_args)
    #                 evaledArgs = [v.eval(context, argsDict, argsValues) for v in args]
    #                 return self.build_in_func(*evaledArgs)
    #             else:
    #                 # args.update(const_args)
    #                 return block.eval(context, argsDict, argsValues)

    def eval(self, argsValues, p):
        matched = False
        localContextGlobal = {}
        for args, block in zip(self.list_args, self.list_blocks):
            argsDict = {arg.toString(): i for i, arg in enumerate(args)}
            matchFlags = []
            localContextGlobal = {}
            for arg, argV in zip(args, argsValues):
                res, localContext = p.patternMatch(arg, argV, {}, p.context)
                if res:
                    localContextGlobal.update(localContext)
                    matchFlags.append(res)
                else:
                    matchFlags.append(res)
            if all(matchFlags):
                matched = True
                break
            else:
                continue
        if matched:
            p.context.update(localContextGlobal)
            if self.build_in:
                evaledArgs = [v.eval(p.context, argsDict, argsValues) for v in args]
                evaledArgs.append(p)
                return self.build_in_func(*evaledArgs)
            else:
                # args.update(const_args)
                return block.eval(p.context, argsDict, argsValues)
        else:
            print('PROBLEM!! NOT ENOUGH VARIANTS IN PATTERN MATCHING')








            # def changeLabels(self, labels_list):
    #     newArgs = []
    #     for labels, block in zip(labels_list, self.list_blocks):
    #         tmp = dict()
    #         for (new, tp) in labels:
    #             tmp2 = Expr()
    #             if type(new) is str:
    #                 tmp2.symbol(new)
    #             elif type(new) is int:
    #                 tmp2.const(new)
    #             tmp[new] = tmp2
    #         newArgs.append(tmp)
    #         newArgsBlock = []
    #         for lb in labels:
    #             newArgsBlock.append(lb)

            # block.args = newArgsBlock

            # self.list_args = newArgs











