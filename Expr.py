from utils import error


class Const:
    def __init__(self, val):
        self.val = val
        self.type = 'Const'
        self.local_context = {}

    def eval(self, process):
        return self

    # Expr -> (Bool, [(Bool, Expr)])
    def match(self, pattern):
        if pattern.type == self.type:
            return self.val == pattern.val, []
        else:
            return False, []

    def to_str(self, process):
        return self.val


class Symbol:
    def __init__(self, pointer):
        self.pointer = pointer
        self.type = 'Symbol'
        self.local_context = {}

    def eval(self, process):
        if self.pointer in self.local_context:
            result = self.local_context[self.pointer]
        else:
            result = process.context[self.pointer]
        # self.local_context[self.pointer] = result
        result.local_context.update(self.local_context)
        old_expr = result
        new_expr = None
        while old_expr.type == 'Symbol' or old_expr.type == 'Function' and old_expr.name[0].islower():
            new_expr = old_expr.eval(process)
            new_expr.local_context.update(old_expr.local_context)
            if equal(new_expr, old_expr):
                error("Cant match eval symbol")
            else:
                old_expr = new_expr
        # evaled = result.eval(process)
        # return evaled
        return old_expr

    def to_str(self, process):
        res = self.eval(process)
        return res.to_str(process)

    # Expr -> (Bool, [(Bool, Expr)])
    def match(self, pattern):
        return True, [(self.pointer, pattern)]


class Function:
    # String -> [String]
    def __init__(self, name, args, lazy=False):
        self.name = name
        self.args = args
        self.type = 'Function'
        self.local_context = {}

    def eval(self, process):
        if self.name[0].isupper():
            for arg_label in self.args:
                if arg_label in self.local_context:
                    arg_expr = self.local_context[arg_label]
                else:
                    arg_expr = process.context[arg_label]
                arg_expr.local_context.update(self.local_context)
                # arg_expr.eval(process)
            # args = [process.context[arg] for arg in self.args]
            # func_args = [arg.eval(process) for arg in args]
            # new_args_labels = []
            # for arg in func_args:
            #     index = process.index_gen()
            #     process.context.update({index: arg})
            #     new_args_labels.append(index)
            #
            return self
        else:
            if self.name in self.local_context:
                func = self.local_context[self.name]
            else:
                func = process.context[self.name]
            func_args = []
            for arg in self.args:
                if arg in self.local_context:
                    expr = self.local_context[arg]
                    expr.local_context.update(self.local_context)
                    func_args.append(expr)
                else:
                    expr = process.context[arg]
                    expr.local_context.update(self.local_context)
                    func_args.append(expr)

            res = func.eval(func_args, process)
            res.local_context.update(self.local_context)
            return res

    # Expr -> (Bool, [(Bool, Expr)])
    def match(self, pattern):
        if pattern.type == self.type and self.name == pattern.name and len(self.args) == len(pattern.args):
            local_context = [(local_arg, Symbol(pattern_arg)) for local_arg, pattern_arg in
                             zip(self.args, pattern.args)]
            return True, local_context
        else:
            return False, []

    def to_str(self, process):
        res = self.eval(process)
        if res.type == 'Function' and res.name[0].isupper():
            out = res.name + ' ' + str([process.context[arg].to_str(process) for arg in self.args])
            out = ''.join([v for v in out if v != '"' and v != "'" and v != '\\'])
            return out
        elif res.type == 'Function':
            return self.eval(process).to_str(process)
        else:
            return res.to_str(process)


def equal(expr1, expr2):
    if expr1.type == expr2.type == 'Const':
        return expr1.val == expr2.val
    elif expr1.type == expr2.type == 'Symbol':
        return expr1.pointer == expr2.pointer
    elif expr1.type == expr2.type == 'Function':
        return expr1.name == expr2.name and expr1.args == expr2.args
    else:
        return False
