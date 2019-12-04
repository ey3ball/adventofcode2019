#!/usr/bin/python3

from collections import Counter

def check_password(code):
    codestr = str(code)
    digits = [int(number) for number in codestr]
    [(_, max_repeats)] = Counter(digits).most_common(1)

    if max_repeats <= 1:
        return 1

    if len(codestr) != 6:
       return 2

    previous = 0
    for i in codestr:
        if int(i) < previous:
            return 3

        previous = int(i)

    return 0

assert(check_password(111111) == 0)
assert(check_password(223450) == 3)
assert(check_password(123789) == 1)

valid = 0
for code in range(235741, 706948+1):
    if check_password(code) == 0:
        valid += 1

print(valid)
