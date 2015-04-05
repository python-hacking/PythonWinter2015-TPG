#!/usr/bin/python
# coding: utf

import readline
import sys
import tpg
import itertools
import numpy as np

ERROR_CODE = 11
EOF_MESSAGE = "Good bye!"

def minus(x, y=None):
    if y == None:
        return -x
    else:
        return x - y

def plus(x, y=None):
    if y == None:
        return +x
    else:
        return x + y

def make_op(s):
    return {
        '+': plus,
        '-': minus,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
        '&': lambda x,y: x&y,
        '|': lambda x,y: x|y,
    }[s]

class Vector(list):
    def __init__(self, *argp, **argn):
        list.__init__(self, *argp, **argn)

    def __str__(self):
        return "[" + " ".join(str(c) for c in self) + "]"

    def __op(self, a, op):
        try:
            return self.__class__(op(s,e) for s,e in zip(self, a))
        except TypeError:
            return self.__class__(op(c,a) for c in self)

    def __add__(self, a): return self.__op(a, lambda c,d: c+d)
    def __sub__(self, a): return self.__op(a, lambda c,d: c-d)
    def __div__(self, a): return self.__op(a, lambda c,d: c/d)
    def __mul__(self, a): return self.__op(a, lambda c,d: c*d)

    def __and__(self, a):
        try:
            return reduce(lambda s, (c,d): s+c*d, zip(self, a), 0)
        except TypeError:
            return self.__class__(c and a for c in self)

    def __or__(self, a):
        try:
            return self.__class__(itertools.chain(self, a))
        except TypeError:
            return self.__class__(c or a for c in self)

class Matrix(np.matrix):
    pass

class Calc(tpg.Parser):
    r"""

    separator spaces: '\s+' ;
    separator comment: '#.*' ;

    token fnumber: '\d+[.]\d*' float ;
    token number: '\d+' int ;
    token op1: '[|&+-]' make_op ;
    token op2: '[*/]' make_op ;
    token id: '\w+' ;

    START/e -> Operator $e=None$ | Expr/e | $e=None$ ;
    Operator -> Assign ;
    Assign -> id/i '=' Expr/e $Vars[i]=e$ ;
    Expr/t -> Summand/t ( op1/op Summand/f $t=op(t,f)$ )* ;
    Summand/f -> Factor/f ( op2/op Factor/a $f=op(f,a)$ )* ;
    Factor/f -> Compound/f | op1/op Factor/f $f=op(f)$ ;
    Compound/a -> Matrix/a | Vector/a | '\(' Expr/a '\)' | Atom/a ;
    Atom/a ->   id/i ( check $i in Vars$ | error $"Undefined variable '{}'".format(i)$ ) $a=Vars[i]$
              | fnumber/a
              | number/a
              ;
    Vector/$Vector(a)$ -> '\[' '\]' $a=[]$ | '\[' Atoms/a '\]' ;
    Atoms/v -> Atom/a Atoms/t $v=[a]+t$ | Atom/a $v=[a]$ ;
    Matrix/m ->'\[' Vector/m $m=Matrix(m)$  ( Vector/v $ m=np.vstack((m, v)) $)* '\]' ;
    """

calc = Calc()
Vars = {}
PS1 = '--> '

script = None
if len(sys.argv) > 1:
    try:
        script = open(sys.argv[1])
    except Exception as e:
        print >> sys.stderr, e
        exit()

while True:
    if script:
        line = script.readline()
        if not line:
            break
    else:
        try:
            line = raw_input(PS1)
        except EOFError:
            print EOF_MESSAGE
            break
    res = None
    try:
        res = calc(line)
    except tpg.Error as exc:
        print >> sys.stderr, exc
        if script:
            exit(ERROR_CODE)
    if res != None and not script:
        print res

if script:
    print res
