from exprClass import Expr
from argsClass import Args
from funcClass import Func
from processClass import DefFunc
import sys

sys.setrecursionlimit(100000)

constTest = Expr()
constTest.const(1)
c = constTest.eval({}, {}, [])

symbolTest = Expr()
symbolTest.symbol("a")
s = symbolTest.eval({"a": constTest}, {}, [])
print()

def add_func(x, y):
    xv = x.val
    yv = y.val
    v = xv + yv
    new_expr = Expr()
    new_expr.const(v)
    return new_expr

def mul_func(x, y):
    xv = x.val
    yv = y.val
    v = xv * yv
    new_expr = Expr()
    new_expr.const(v)
    return new_expr

def neg_func(x):
    xv = x.val
    v = -xv
    new_expr = Expr()
    new_expr.const(v)
    return new_expr

p = DefFunc()
p.const("a1", 5)
p.const("b1", 6)
p.symbol("a", "a")
p.symbol("b", "b")
p.const("true", 1)
p.const("false", 0)
p.const("fake", 0)
p.define("add", [["a", "b"]], ["fake"], True, add_func)
p.define("mul", [["a", "b"]], ["fake"], True, mul_func)
p.define("neg", [["a"]], ["fake"], True, neg_func)
p.parseContext()
lol = p.eval('factorial', ["a1"])
print("lol")
#
# p.func("sub_neg", "neg", ["b"])
# p.func("sub_add", "add", ["a", "sub_neg"])
# p.define("sub", [["a", "b"]], ["sub_add"])
#
# p.define("if", [["true", "a", "b"], ["false", "a", "b"]], ["a", "b"])
#
#
# p.symbol("n", "n")
# p.const("1", 1)
# p.const("2", 2)
# p.const("0", 0)
# p.const("5", 5)
# p.func("sb", "sub", ["n", "1"])
# p.func("self", "factorial", ["sb"])
# p.func("fact", "mul", ["n", "self"])
# p.define("factorial", [["0"], ["n"]], ["1", "fact"])

