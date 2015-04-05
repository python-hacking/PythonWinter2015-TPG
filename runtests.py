#!/usr/bin/python
""" Usage: pass fully qualified path to caalc.py
or don't pass anything if you have it in the current dir. """

import os
import sys
import subprocess

file_suffix = ".txt"
expected_suffix = ".expected"
null_file = open("/dev/null", "w")

caalc_path = sys.argv[1] if len(sys.argv) > 1 else os.environ["PWD"] + "/caalc.py"
src_root = os.environ["PWD"] + "/tests"

class WrongAnswerException(Exception):
    pass

# FIXME: unused
class RuntimeErrorException(Exception):
    pass

def do_test(filename):
    caalc_out = subprocess.check_output(['python', caalc_path, filename], stderr=null_file)
    expected_out = open(filename + expected_suffix).read()
    if caalc_out.split() != expected_out.split():
        raise WrongAnswerException("caalc error: WA")

failed = []
for root, dirs, files in os.walk(src_root):
    lst = [root + '/' + i for i in files if i.endswith(file_suffix)]
    for src_file in lst:
        try:
            print src_file
            do_test(src_file)
            print "\tOK"
        except Exception as e:
            failed += [src_file]
            print "\tFAILED!"
            print e

print "\n=======RESULTS======="
print len(failed), "tests failed"
print failed
null_file.close()
