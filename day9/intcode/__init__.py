#!/bin/bash

OPCODE_ADD = 1
OPCODE_MULT = 2
OPCODE_END = 99
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_RELBASE = 9

FLAG_POSITION = "0"
FLAG_IMMEDIATE = "1"
FLAG_RELATIVE = "2"

instruction_info = {
    OPCODE_ADD: [0, 0, 1],
    OPCODE_MULT: [0, 0, 1],
    OPCODE_INPUT: [1],
    OPCODE_OUTPUT: [1],
    OPCODE_JUMP_IF_TRUE: [0, 0],
    OPCODE_JUMP_IF_FALSE: [0, 0],
    OPCODE_LESS_THAN: [0, 0, 1],
    OPCODE_EQUALS: [0, 0, 1],
    OPCODE_RELBASE: [0],
    OPCODE_END: [],
}

#intcode = sys.argv[1]
#start_state = [int(i) for i in intcode.split(",")]

def run_intcode(memmap, argv):
    state = list(memmap)

    index = 0
    output = 0
    relative_base = 0
    while True:
        opcode = state[index] % 100
        flags = list(str(state[index]).zfill(5)[:3])
        info = instruction_info.get(opcode)
        length = len(instruction_info.get(opcode)) + 1

        print("op {}".format(state[index:index+length]))
        args = []
        for i in range(1, length):
            flag = flags[-i]

            assert(flag == FLAG_POSITION or flag == FLAG_IMMEDIATE or flag == FLAG_RELATIVE)
            if flag == FLAG_POSITION:
                ptr = state[index + i]
            elif flag == FLAG_IMMEDIATE:
                if info[i-1] == 1:
                    print("Output parameter in immediate mode !!")
                    ptr = state[index + i]
                    #ptr = index + i
                else:
                    ptr = index + i
            elif flag == FLAG_RELATIVE:
                print("relb {} {}".format(state[index+i], relative_base))
                ptr = state[index + i] + relative_base
            else:
                assert(False)

            print(ptr)
            if ptr >= len(state):
                state += [0] * (2 + ptr - len(state))

            args.append(ptr)

        print(args)
        #print([state[arg] for arg in args])

        new_ptr = (False, 0)
        if opcode == OPCODE_ADD:
            state[args[2]] = state[args[0]] + state[args[1]]
        elif opcode == OPCODE_MULT:
            state[args[2]] = state[args[0]] * state[args[1]]
        elif opcode == OPCODE_INPUT:
            print("in {}".format(args[0]))
            state[args[0]] = argv.pop(0)
        elif opcode == OPCODE_OUTPUT:
            yield state[args[0]]
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
        elif opcode == OPCODE_RELBASE:
            print("relbase +={}".format(state[args[0]]))
            #print("relbase +={}".format(state[index+1]))
            relative_base += state[args[0]]
            #relative_base += state[index + 1]
        elif opcode == OPCODE_END:
            break

        if new_ptr[0]:
            index = new_ptr[1]
        else:
            index += length

    return (state, output) 
