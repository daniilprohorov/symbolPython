import re
import matplotlib.pyplot as plt
import subprocess
from Process import Process
from Expr import Const, Symbol, Function
import sys
from parser import splitWithBrackets

sys.setrecursionlimit(10000)

p = Process()


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


def equalBuildInConst_func(x, y):
    if x.val == y.val:
        return Const(1)
    else:
        return Const(0)


def equalBuildInSymbol_func(x, y):
    if x.pointer == y.pointer:
        return Const(1)
    else:
        return Const(0)


list2const = ['Const', 'Const']
list1const = ['Const']
p.symbol("a0", "a0")
p.symbol("b0", "b0")
p.symbol("a1", "a1")
p.symbol("b1", "b1")
p.symbol("a2", "a2")
p.symbol("b2", "b2")
p.symbol("a3", "a3")
p.symbol("b3", "b3")
p.symbol("a4", "a4")
p.symbol("b4", "b4")
p.const("true", 1)
p.const("false", 0)
p.const("fake", 0)
p.define("add", [["a0", "b0"]], ["fake"], True, add_func, ['Const', 'Const', 'Const'])
p.define("mul", [["a1", "b1"]], ["fake"], True, mul_func, ['Const', 'Const', 'Const'])
p.define("neg", [["a2"]], ["fake"], True, neg_func, ['Const', 'Const'])
p.define("equalBuildInConst", [["a3", "b3"]], ["fake"], True, equalBuildInConst_func, ['Const', 'Const', 'Const'])
p.define("equalBuildInSymbol", [["a4", "b4"]], ["fake"], True, equalBuildInSymbol_func, ['Symbol', 'Symbol', 'Const'])

filename = "prg"
lastLine = ""

def printPoints(lst):
    x_lst = [x for y1, y2, x in lst]
    y1_lst = [y1 for y1, y2, x in lst]
    y2_lst = [y2 for y1, y2, x in lst]
    print(y1_lst)
    print(y2_lst)
    plt.plot(x_lst, y1_lst)
    plt.plot(x_lst, y2_lst)
    plt.show()

def getLastLine():
    with open(filename, "r") as f:
        lns = [line for line in f]
        return lns[-2]


lastLine = re.sub(r'\n', '', getLastLine())
if re.search(r'print', lastLine):
    last = re.split(r'print', lastLine)[1]
    # n_last = re.sub(r'\\"', '"', last[2:-1])
    n_last = last[2:-1]
    output = n_last.split(',')
    output.insert(0, "./testState-exe")
    out = subprocess.Popen(output,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    if stderr:
        print("internal Error")
    else:
        n_stdout = str(stdout)
        out = ''.join([v for v in n_stdout[1:] if v != '"' and v != "'" and v != '\\' and v != 'n'])

        printPoints(eval(out))
else:
    p.text_define()
    result = p.eval('main')
    print(result.to_str(p))
