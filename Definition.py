from Expr import equal, Symbol
from utils import error


class Define:
    # аргументы как указатели
    # [[Expr]] -> [Expr] -> Bool -> PythonFunc -> [String] -> String
    def __init__(self, list_args, list_blocks, build_in=False, func=None, build_in_types=[], label='unknown'):
        if build_in:
            self.types = build_in_types
            self.list_args = list_args
            self.list_blocks = list_blocks
        else:
            self.types = [typ.pointer for typ in list_args[0]] + [list_blocks[0].pointer]
            self.list_args = list_args[1:]
            self.list_blocks = list_blocks[1:]

        self.build_in = build_in
        self.build_in_func = func
        self.label = label
        self.type = 'Def'
        self.local_context = {}

    # [String] -> Process -> Expr
    def eval(self, args_values, process):
        new_args = self.args_eval(args_values, self.types[:-1], process)
        matched, block, local_context = self.pattern_match(new_args, process)
        if matched:
            if self.build_in:
                return self.build_in_func(*new_args)
            else:
                block.local_context.update(local_context)
                # if block.type == self.types[-1] == 'Function' and block.name[0].isupper():
                #     return block
                # else:
                result = block.eval(process)
                return result

        else:
            print('PROBLEM!! NOT ENOUGH VARIANTS IN PATTERN MATCHING')

    def to_str(self, process):
        return self.label

    # [Expr] -> [String] -> Process -> [Expr]
    def args_eval(self, args, types, process):
        new_args = []
        for arg, typ in zip(args, types):
            old_arg = arg
            while old_arg.type != typ and typ != 'Symbol':
                new_arg = old_arg.eval(process)
                if equal(new_arg, old_arg):
                    error("Cant evaluate")
                else:
                    old_arg = new_arg
            new_args.append(old_arg)

        return new_args

    # [Expr] -> (Bool, Expr)
    def pattern_match(self, args, process):
        big_context_list = []
        matched = False
        matched_block = None
        for args_p, block_p in zip(self.list_args, self.list_blocks):
            matched = True
            big_context_list = []
            for expr_p, expr in zip(args_p, args):
                match_bool, local_context = self.match(expr_p, expr, process)

               #############

                old_expr = expr
                # while expr.type == 'Function' and expr_p.type == 'Function' and expr.name[0].islower():
                while expr.type == 'Function' and expr_p.type == 'Function':
                    new_expr = old_expr.eval(process)
                    match_bool, local_context = self.match(expr_p, new_expr, process)
                    if not match_bool and equal(new_expr, old_expr):
                        break
                        error("Cant match")
                    elif new_expr.type == 'Function' and match_bool and new_expr.name[0].isupper():
                        break
                    elif new_expr.type != 'Function' and match_bool:
                        break
                    else:
                        old_expr = new_expr

                #################

                if match_bool:
                    big_context_list += local_context
                else:
                    matched = False
                    break
            if matched:
                matched_block = block_p
                break
        if matched:
            local_context = {key: expr for key, expr in big_context_list}
            return True, matched_block, local_context
        else:
            return False, None, local_context

    def match(self, expr_p, expr, process):
        if expr_p.type == 'Const':
            return self.match_const(expr_p, expr, process)
        elif expr_p.type == 'Symbol':
            return self.match_symbol(expr_p, expr, process)
        elif expr_p.type == 'Function':
            return self.match_func(expr_p, expr, process)
        else:
            return False, []

    def match_const(self, const_p, expr, process):
        if expr.type == 'Const':
            return const_p.match(expr)
        elif expr.type == 'Symbol':
            new_expr = expr.eval(process)
            if equal(expr, new_expr):
                return False, []
            else:
                return self.match_const(const_p, new_expr, process)
        elif expr.type == 'Function':
            new_expr = expr.eval(process)
            if equal(expr, new_expr):
                return False, []
            else:
                return self.match_const(const_p, new_expr, process)

    def match_symbol(self, symbol_p, expr, process):
        if expr.type == 'Symbol':
            if expr.pointer == symbol_p.pointer:
                return True, [(expr.pointer, expr.eval(process))]
        return symbol_p.match(expr)
        # return symbol_p.match(expr)

    def match_func(self, func_p, expr, process):
        if expr.type == 'Const':
            return False, []
        elif expr.type == 'Symbol':
            new_expr = expr.eval(process)
            if equal(expr, new_expr):
                return False, []
            else:
                return self.match_func(func_p, new_expr, process)
        elif expr.type == 'Function':
            # Bool, [(Bool, Expr)]
            matched, local_context = func_p.match(expr)
            if matched:
                # TODO: Maybe add local context to global context is not the best idea)
                # process.context.update(local_context)
                args_expr = [process.context[arg_str] for arg_str in func_p.args]
                matched_args = [new_expr for key, new_expr in local_context]
                m_list = []
                for arg, m_arg in zip(args_expr, matched_args):
                    m_list.append(self.match(arg, m_arg, process))
                if all([m for m, dict_m in m_list]):
                    return True, [(pair[0], pair[1].eval(process)) for dict_m in m_list for pair in dict_m[1]]
                else:
                    return False, []

            else:
                return False, []
