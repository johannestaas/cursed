'''
cursed.version

For simple python version checks.
'''
import sys

PY26 = sys.version_info[:2] <= (2, 6)
PY27 = sys.version_info[:2] == (2, 7)
PY3 = sys.version_info[0] == 3
