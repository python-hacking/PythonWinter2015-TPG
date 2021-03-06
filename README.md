# PythonWinter2015-TPG
Command reading, parsing and interpreting

__Usage__:

* For interactive prompt simply run caalc.py.
* For batch execution supply your command file as an argument. The output is the result of the last operation executed. (Beware that assignment operator has no value, so if you want to see contents of a variable, just say it's name in the last command).
Execution of this script

```
var = 3 * 4
var
```
will yield 12.

__Matrices__ are input like this:

```
[[1 2 3] [1 2 3] [3 2 1] [4 5 6]]
```

Supported __prefix unary operations__ are '+', '-' and 'T'.
T stands for 'transpose'. And since it is a keyword, 'T' cannot be a variable name.
```
v = T ---[3 4 5] # v is a  3 x 1 vector (-3 -4 -5)^T.
```

__Semantics__ for some operations:

| is concatenation where applicable and bitwise OR in other places. For example
```
[[1 2] [1 2]] | [[3 4] [3 4]]
```
results in ``` [[1 2 3 4][1 2 3 4]]```.

& is inner product (generalized dot product) or bitwise AND.


For __regression testing__ launch runtests.py.
