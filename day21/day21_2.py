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

droid.send_line("NOT J T")
droid.send_line("AND J T")
droid.send_line("OR E T")
droid.send_line("OR H T")
droid.send_line("AND T J")

droid.send_line("NOT B T")
droid.send_line("AND D T")
droid.send_line("OR T J")
droid.send_line("NOT A T")
droid.send_line("OR T J")

droid.send_line("RUN")

droid.run()
print(droid.reg["out"])

#for line in droid_gen:
#    print(line)
