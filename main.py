from exprClass import Expr
from argsClass import Args
from funcClass import Func


def add_func(x, y):
    xv = x.val
    yv = y.val
    v = xv + yv
    new_expr = Expr()
    new_expr.const(v)
    return new_expr


def neg_func(x):
    xv = x.val
    v = -xv
    new_expr = Expr()
    new_expr.const(v)
    return new_expr


neg_const = Expr()
neg_const.const(0)
arg_neg = Expr()
arg_neg.symbol("a")
arguments1_neg = Args([arg_neg])
neg = Func([arguments1_neg], [neg_const], True, neg_func)

add_const = Expr()
add_const.const(0)
arg_add_1 = Expr()
arg_add_1.symbol("a")
arg_add_2 = Expr()
arg_add_2.symbol("b")
arguments1_add = Args([arg_add_1, arg_add_2])
add = Func([arguments1_add], [add_const], True, add_func)


block1 = Expr()
block1.symbol("b")
block2 = Expr()
block2.symbol("a")

arg11 = Expr()
arg11.const(0)
arg21 = Expr()
arg21.symbol("a")
arg31 = Expr()
arg31.symbol("b")

arg12 = Expr()
arg12.const(1)
arg22 = Expr()
arg22.symbol("a")
arg32 = Expr()
arg32.symbol("b")

arguments1 = Args([arg11, arg21, arg31])
arguments2 = Args([arg12, arg22, arg32])
if_func = Func([arguments1, arguments2], [block1, block2])

lol1 = Expr()
lol1.const(1)
lol2 = Expr()
lol2.const(10)
lol3 = Expr()
lol3.const(7)

a = if_func.eval([], [lol1, lol2, lol3])

t1 = Expr()
t1.const(10)
t2 = Expr()
t2.const(6)
l = add.eval([], [t1, t2])


print()
# fib 0 = 1
# fib 1 = 1
# fib n = n + fib (n-1)
