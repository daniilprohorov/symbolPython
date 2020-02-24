from Expr import Const, Symbol, Function
from Definition import Define
from Text import text_to_index, const_or_symbol
from parser import parse


class Process:
    # Dict[String, [Expr]]
    context = {}

    # Int
    global_counter = 0

    main_func = 'main'

    def __init__(self, context=None):
        if context:
            self.context = context

    def index_gen(self):
        index = 'i' + str(self.global_counter)
        self.global_counter += 1
        return index

    def const(self, key: str, const: int):
        expr = Const(const)
        self.context.update({key: expr})

    def symbol(self, key: str, symbol: str):
        expr = Symbol(symbol)
        self.context.update({key: expr})

    # выражение функция, не объявление!
    def func(self, key: str, func: str, args: [str]):
        expr = Function(func, args)
        self.context.update({key: expr})

    def define(self, key: str, args_list: [[str]], results: [str], build_in=False, build_in_func=None, types=[]):
        args_expr = [[self.context[arg] for arg in args] for args in args_list]
        results_expr = [self.context[result] for result in results]
        func = Define(args_expr, results_expr, build_in, build_in_func, types, key)
        self.context[key] = func

    def text_define(self):
        functions = parse()
        for name in functions:
            body = functions[name]
            args_text_list = body.args
            args_out = []
            local_args_dict = {}
            for argsText in args_text_list:
                local_args = []
                for arg_t in argsText:
                    if type(arg_t) == list:
                        index = text_to_index([arg_t], {}, self)
                        local_args_dict[index[0]] = index[0]
                        local_args.append(index[0])

                    elif arg_t in self.context:
                        index = arg_t
                        local_args_dict[arg_t] = index
                        local_args.append(index)
                    else:
                        index = const_or_symbol(arg_t, self)
                        local_args_dict[arg_t] = index
                        local_args.append(index)
                args_out.append(local_args)
            results = text_to_index(body.block, local_args_dict, self)
            self.define(name, args_out, results)

    def eval(self, key: str, args: [str] = []):
        func = self.context[key]
        args_expr = [self.context[arg] for arg in args]
        return func.eval(args_expr, self)
