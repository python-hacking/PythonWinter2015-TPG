#!/usr/bin/python
# coding: utf

import readline
import sys
import tpg
import itertools
import numpy as np

ERROR_CODE = 11
EOF_MESSAGE = "Good bye!"

number_types = (type(1.), type(1))

def transpose(x):
    if type(x) in number_types:
        return x
    return x.transpose()

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
        'T': transpose,
        '+': plus,
        '-': minus,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
        '&': lambda x,y: x&y,
        '|': lambda x,y: x|y,
    }[s]

class BadOperandsError(Exception):
    def __str__(self):
        return "Bad operands!"

class Matrix(np.matrix):
    def __str__(self):
        if self.shape[0] == 1:
            return self.getA1().__str__()
        elif self.shape[1] == 1:
            return "T " + self.getA1().__str__()
        else:
            return self.getA().__str__()

    def __and__(self, rhs):
        try:
            if self.shape == rhs.shape:
                return np.inner(self, rhs).getA1()[0]
            else:
                raise BadOperandsError()
        except AttributeError:
            return super(np.matrix, self).__and__(int(rhs))

    def __or__(self, rhs):
        try:
            return np.hstack((self, rhs))
        except ValueError: # incompatible dimensions
            pass
        try:
            return super(np.matrix, self).__or__(int(rhs))
        except TypeError:
            raise BadOperandsError()

# In case we'll want vector product or something..
# Anyway, keeping this class looks like a good idea
# because this way the grammar is cleaner
class Vector(Matrix):
    pass

class Calc(tpg.Parser):
    r"""

    separator spaces: '\s+' ;
    separator comment: '#.*' ;

    token fnumber: '\d+[.]\d*' float ;
    token number: '\d+' int ;
    token op1: '[|&+-T]' make_op ;
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
