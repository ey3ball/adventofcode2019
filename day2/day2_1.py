#!/bin/bash

import sys

OPCODE_ADD = 1
OPCODE_MULT = 2
OPCODE_END = 99

intcode = sys.argv[1]
start_state = [int(i) for i in intcode.split(",")]

state = list(start_state)
for i in range(0, int(len(start_state) / 4)):
    index = i * 4
    opcode = state[index]
    arg1 = state[index + 1]
    arg2 = state[index + 2]
    out = state[index + 3]

    if opcode == OPCODE_ADD:
        state[out] = state[arg1] + state[arg2]
    elif opcode == OPCODE_MULT:
        state[out] = state[arg1] * state[arg2]
    elif opcode == OPCODE_END:
        break

print("init: {}".format(start_state))
print("end: {}".format(state))
