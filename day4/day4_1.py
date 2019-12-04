#!/usr/bin/python3

from collections import Counter

def check_password(code):
    codestr = str(code)

    if len(codestr) != 6:
       return 2

    previous = 0
    two = False
    for i in codestr:
        if int(i) < previous:
            return 3
        if int(i) == previous:
            two = True

        previous = int(i)

    if two:
        return 0
    else:
        return 4

assert(check_password(111111) == 0)
assert(check_password(223450) != 0)
assert(check_password(123789) != 0)

valid = 0
for code in range(235741, 706948+1):
    if check_password(code) == 0:
        valid += 1

print(valid)
