#!/usr/bin/env python3

FINAL_POSITION = 4086
DECK_SIZE = 10007

DEAL_INC="deal with increment "
NEW_STACK="deal into new stack"
CUT="cut "

def parse(l):
    if l.startswith(DEAL_INC):
        return (deal, [int(l[len(DEAL_INC):])])
    elif l.startswith(NEW_STACK):
        return (new_stack, [])
    elif l.startswith(CUT):
        return (cut, [int(l[len(CUT):])])
    else:
        sys.stderr.write("Parse error ! {}\n".format(l))

def new_stack(params):
    a,b = params
    return (-a, -b - 1)

def cut(params, n):
    a,b = params
    return (a, b - n)

def deal(params, n):
    a,b = params
    return (n * a, n * b)

with open("day22_i.txt") as f:
    shuffle = [parse(l) for l in f.readlines()]

ab = (1, 0)
for op, arg in shuffle:
    ab = op(ab, *arg)
    ab = (ab[0] % DECK_SIZE, ab[1] % DECK_SIZE)
print(ab)

print((ab[0] * 2019 + ab[1]) % DECK_SIZE)
