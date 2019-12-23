#!/usr/bin/env python3

import sys

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

print("Deck shuffler equation : {} * x + {} [{}]".format(ab[0], ab[1], DECK_SIZE))
print("Position of card 2019 after shuffling a small deck : {}".format(
        ((ab[0] * 2019 + ab[1]) % DECK_SIZE)))


print("Upping the ante")
DECK_SIZE=119315717514047
SHUFFLE_COUNT=101741582076661
FINAL_POS=2020

print("New deck size : {}".format(DECK_SIZE))
ab = (1, 0)
for op, arg in shuffle:
    ab = op(ab, *arg)
    ab = (ab[0] % DECK_SIZE, ab[1] % DECK_SIZE)

print("1xDeck shuffler equation : {} * x + {} [{}]".format(ab[0], ab[1], DECK_SIZE))
inv = (pow(ab[0], -1, mod=DECK_SIZE), (-ab[1] % DECK_SIZE))
print("Inverse equation : -  {} * {}".format(inv[1], inv[0]))

print("Position of card 2019 after shuffling a big deck once : {}".format(
        ((ab[0] * FINAL_POS + ab[1]) % DECK_SIZE)))
pos = (ab[0] * 2019 + ab[1]) % DECK_SIZE
ant = ((pos + inv[1]) * inv[0]) % DECK_SIZE
print("Trying to revert ? {}".format(ant))
pos = (ab[0] * pos + ab[1]) % DECK_SIZE
print("Twice : {}".format(pos))
ant = ((pos + inv[1]) * inv[0]) % DECK_SIZE
ant = ((ant + inv[1]) * inv[0]) % DECK_SIZE
print("Revert twice: {}".format(ant))

def rev(pos, it, ab):
    r = (pow((1 - ab[0]), -1, DECK_SIZE) * ab[1]) % DECK_SIZE
    a_n = pow(ab[0], -it, mod=DECK_SIZE)
    inv = ((pos - r) * a_n + r) % DECK_SIZE
    return inv

print("Trying to generic revert twice ? {}".format(rev(15965746545382, 2, ab)))

# Finally
print("Trying to revert ? {}".format(rev(2020, SHUFFLE_COUNT, ab)))
