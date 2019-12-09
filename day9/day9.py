#!/usr/bin/env python3

from itertools import permutations
import sys
import code

from intcode import run_intcode

intcode = sys.argv[1]
init_memmap = [int(i) for i in intcode.split(",")]

computer = run_intcode(init_memmap, [2])

output = []
try:
    while True:
        output.append(next(computer))
except StopIteration as e:
    print(output)
    #code.interact(local=locals())
