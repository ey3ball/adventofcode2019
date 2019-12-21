#!/usr/bin/env python3

from intcode import IntCodeAscii
import sys

with open("day21.txt", "r") as f:
    program = f.readline().strip()

droid = IntCodeAscii(program)
droid_gen = droid.run_gen()

droid.send_line("NOT C T")
droid.send_line("AND D T")
droid.send_line("OR T J")
droid.send_line("NOT B T")
droid.send_line("AND D T")
droid.send_line("OR T J")
droid.send_line("NOT A T")
droid.send_line("OR T J")
droid.send_line("WALK")

droid.run()
print(droid.reg["out"])

#for line in droid_gen:
#    print(line)
