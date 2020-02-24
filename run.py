from Process import Process
from Expr import Const, Symbol, Function
import sys
sys.setrecursionlimit(10000)

def add_func(x, y):
    xv = x.val
    yv = y.val
    v = xv + yv
    new_expr = Const(v)
    return new_expr


def mul_func(x, y):
    xv = x.val
    yv = y.val
    v = xv * yv
    new_expr = Const(v)
    return new_expr


def neg_func(x):
    xv = x.val
    v = -xv
    new_expr = Const(v)
    return new_expr


p = Process()
# p.const("a1", 1)
# p.const("b1", 6)
# p.const("k", 12)
# p.const("one", 1)
# p.const("two", 2)
list2const = ['Const', 'Const']
list1const = ['Const']
p.symbol("a0", "a0")
p.symbol("b0", "b0")
p.symbol("a1", "a1")
p.symbol("b1", "b1")
p.symbol("a2", "a2")
p.symbol("b2", "b2")
p.const("true", 1)
p.const("false", 0)
p.const("fake", 0)
p.define("add", [["a0", "b0"]], ["fake"], True, add_func, ['Const', 'Const', 'Const'])
p.define("mul", [["a1", "b1"]], ["fake"], True, mul_func, ['Const', 'Const', 'Const'])
p.define("neg", [["a2"]], ["fake"], True, neg_func, ['Const', 'Const'])

p.text_define()
lol = p.eval('main')
print(lol.to_str(p))
