#!/usr/bin/env python3

import sys

OPCODE_ADD = 1
OPCODE_MULT = 2
OPCODE_END = 99
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8

FLAG_POSITION = "0"
FLAG_IMMEDIATE = "1"

intcode = sys.argv[1]
start_state = [int(i) for i in intcode.split(",")]

state = list(start_state)


intruction_len = {
    OPCODE_ADD: 4,
    OPCODE_MULT: 4,
    OPCODE_INPUT: 2,
    OPCODE_OUTPUT: 2,
    OPCODE_JUMP_IF_TRUE: 3,
    OPCODE_JUMP_IF_FALSE: 3,
    OPCODE_LESS_THAN: 4,
    OPCODE_EQUALS: 4,
    OPCODE_END: 1,
}

index = 0
argv = 5
output = 0
while True:
    opcode = state[index] % 100
    flags = list(str(state[index]).zfill(5)[:3])
    length = intruction_len.get(opcode)
    #print("New instructions {}".format(index))
    #print("{} {} {} {}".format(
    #    state[index], state[index+1], state[index+2], state[index+3]))

    # Force position mode for output instructions
    #if opcode == OPCODE_ADD:
    #    flags[0] = "0"
    #elif opcode == OPCODE_MULT:
    #    flags[0] = "0"
    #elif opcode == OPCODE_OUTPUT:
    #    flags[2] = "0"

    print(opcode)
    args = []
    for i in range(1, length):
        flag = flags[-i]

        assert(flag == FLAG_POSITION or flag == FLAG_IMMEDIATE)
        if flag == FLAG_POSITION:
            args.append(state[index + i])
        elif flag == FLAG_IMMEDIATE:
            args.append(index + i)
        else:
            assert(False)
    print(args)

    new_ptr = (False, 0)
    if opcode == OPCODE_ADD:
        state[args[2]] = state[args[0]] + state[args[1]]
    elif opcode == OPCODE_MULT:
        state[args[2]] = state[args[0]] * state[args[1]]
    elif opcode == OPCODE_INPUT:
        state[args[0]] = argv
    elif opcode == OPCODE_OUTPUT:
        output = state[args[0]]
    elif opcode == OPCODE_JUMP_IF_TRUE:
        if state[args[0]] != 0:
            new_ptr = (True, state[args[1]])
    elif opcode == OPCODE_JUMP_IF_FALSE:
        if state[args[0]] == 0:
            new_ptr = (True, state[args[1]])
    elif opcode == OPCODE_LESS_THAN:
        if state[args[0]] < state[args[1]]:
            state[args[2]] = 1
        else:
            state[args[2]] = 0
    elif opcode == OPCODE_EQUALS:
        if state[args[0]] == state[args[1]]:
            state[args[2]] = 1
        else:
            state[args[2]] = 0
    elif opcode == OPCODE_END:
        break

    if new_ptr[0]:
        index = new_ptr[1]
    else:
        index += length

print("out: {}".format(output))

print("init: {}".format(start_state))
print("end: {}".format(state))
