#!/usr/bin/env python3

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

def new_stack(stack):
    return list(reversed(stack))

def cut(stack, n):
    return stack[n:] + stack[:n]

def deal(stack, n):
    new_stack = [-1] * len(stack)
    for i in range(0, len(stack)):
        new_stack[i*n % len(stack)] = stack[i]
    return new_stack

assert cut(list(range(0,10)), 3) == [3,4,5,6,7,8,9,0,1,2] 
assert cut(list(range(0,10)), -3) == [7,8,9,0,1,2,3,4,5,6] 
assert new_stack(list(range(0,10))) == [9,8,7,6,5,4,3,2,1,0] 
assert deal(list(range(0,10)), 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3] 

with open("day22_i.txt") as f:
    shuffle = [parse(l) for l in f.readlines()]
print(shuffle)

stack = list(range(0,10007))
for op, arg in shuffle:
    stack = op(stack, *arg)
    if -1 in stack:
        print(op, arg)
        print("wtf")
        break

assert(sorted(stack) == list(range(0,10007)))

for i, card in enumerate(stack):
    if card == 2019:
        print(i)
