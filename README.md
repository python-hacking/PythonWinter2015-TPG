# PythonWinter2015-TPG
Command reading, parsing and interpreting

Matrices are input like this:
    [[1 2 3] [1 2 3] [3 2 1] [4 5 6]]

Supported prefix unary operations are '+', '-' and 'T'. 
T stands for 'transpose'. And since it is a keyword, 'T' cannot be a variable name.

Semantics for some operations:

| is concatenation where applicable and bitwise OR in other places.

for example \[\[1 2\] \[1 2\]\] | \[\[3 4\] \[3 4\]\]  --> \[\[1 2 3 4\]\[1 2 3 4\]\].

& is inner product (generalized dot product) or bitwise AND.
