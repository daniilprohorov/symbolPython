from exprClass import Expr
from argsClass import Args
from Definition import Define
from processClass import DefFunc
import sys

sys.setrecursionlimit(100000)


def add_func(x, y, p):
    xv = x.val
    yv = y.val
    v = xv + yv
    new_expr = Expr(p)
    new_expr.const(v)
    return new_expr

def mul_func(x, y, p):
    xv = x.val
    yv = y.val
    v = xv * yv
    new_expr = Expr(p)
    new_expr.const(v)
    return new_expr

def neg_func(x, p):
    xv = x.val
    v = -xv
    new_expr = Expr(p)
    new_expr.const(v)
    return new_expr

def print_func(x, p):
    s = x.toString()
    print(s)
    new_expr = Expr(p)
    new_expr.const(0)
    return new_expr

p = DefFunc()
p.const("a1", 1)
p.const("b1", 6)
p.const("k", 12)
p.const("one", 1)
p.const("two", 2)
p.symbol("a", "a")
p.symbol("b", "b")
p.symbol("c", "c")
p.const("true", 1)
p.const("false", 0)
p.const("fake", 0)
p.define("add", [["a", "b"]], ["fake"], True, add_func)
p.define("mul", [["a", "b"]], ["fake"], True, mul_func)
p.define("neg", [["a"]], ["fake"], True, neg_func)
p.define("print", [["a"]], ["fake"], True, print_func)

# p.func("mul1", "mul", ["a", "b"])
# p.func("mul2", "mul", ["one", "two"])
# p.func("sub1", "sub", ["c", "two"])
# p.func("sub2", "sub", ["one", "mul2"])
p.parseContext()
lol = p.eval('main')
print(lol.toString())

# lol = p.patternMatch(p.context['sub1'], p.context['sub2'], {})
# print(lol)
