#!/usr/bin/python3

from collections import Counter

def check_password(code):
    codestr = str(code)

    if len(codestr) != 6:
       return 2

    previous = 0
    seq = ""
    seqs = []
    for i in codestr:
        if int(i) < previous:
            return 3

        if len(seq) == 0 or i == str(seq[-1]):
            seq += i
        else:
            seqs.append(len(seq))
            seq = i

        previous = int(i)

    seqs.append(len(seq))
    
    if 2 in seqs:
        return 0
    else:
        return 4

assert(check_password(112233) == 0)
assert(check_password(123444) == 4)
assert(check_password(111133) == 0)
#assert(check_password(123789) == 1)

valid = 0
for code in range(235741, 706948+1):
    if check_password(code) == 0:
        valid += 1

print(valid)
