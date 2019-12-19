#!/usr/bin/env python3

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

FLAG_POSITION = 0
FLAG_IMMEDIATE = 1
FLAG_RELATIVE = 2

# OPCODE: [args]
# argin = 0, argout = 1
op_info = {
    OPCODE_ADD: [0, 0, 1],
    OPCODE_MULT: [0, 0, 1],
    OPCODE_INPUT: [1],
    OPCODE_OUTPUT: [0],
    OPCODE_JUMP_IF_TRUE: [0, 0],
    OPCODE_JUMP_IF_FALSE: [0, 0],
    OPCODE_LESS_THAN: [0, 0, 1],
    OPCODE_EQUALS: [0, 0, 1],
    OPCODE_RELBASE: [0],
    OPCODE_END: [],
}

class IntCodeVm:
    """ An intcode machine,
    Contains memory, a few registers and opcode implementations
    """
    def __init__(self, mem):
        self.initmem = list(mem)
        self.reset()

    def reset(self):
        self.mem = list(self.initmem)
        self.reg = {
            # Status flags
            "pc_dirty": False,
            "running": True,
            # Program Counter
            "pc": 0,
            # Relative base
            "rbs": 0,
            # Input
            "in": [],
            # Output
            "out": []
        }
        self.ops = {
            OPCODE_ADD: self.op_add,
            OPCODE_MULT: self.op_mult,
            OPCODE_INPUT: self.op_input,
            OPCODE_OUTPUT: self.op_output,
            OPCODE_JUMP_IF_TRUE: self.op_jump_true,
            OPCODE_JUMP_IF_FALSE: self.op_jump_false,
            OPCODE_LESS_THAN: self.op_less_then,
            OPCODE_EQUALS: self.op_equals,
            OPCODE_RELBASE: self.op_relbase,
            OPCODE_END: self.op_end,
        }

    def op_add(self, a1, a2):
        return (a1 + a2,)

    def op_mult(self, a1, a2):
        return (a1 * a2,)

    def op_input(self):
        return (self.reg["in"].pop(0),)

    def op_output(self, a1):
        self.reg["out"].append(a1)
        return ()

    def op_jump_true(self, a1, a2):
        if a1 != 0:
            self.reg["pc"] = a2
            self.reg["pc_dirty"] = True
        return ()

    def op_jump_false(self, a1, a2):
        if a1 == 0:
            self.reg["pc"] = a2
            self.reg["pc_dirty"] = True
        return ()

    def op_less_then(self, a1, a2):
        if a1 < a2:
            return (1,)
        else:
            return (0,)

    def op_equals(self, a1, a2):
        if a1 == a2:
            return (1,)
        else:
            return (0,)

    def op_relbase(self, a1):
        self.reg["rbs"] += a1
        return ()

    def op_end(self):
        self.reg["running"] = False
        return ()


class IntCodeInterpreter(IntCodeVm):
    """ An intcode interpreter
    Parses intcode programs and runs them on an intcode machine
    """
    def __init__(self, program_string):
        intmem = [int(i) for i in program_string.split(",")]
        IntCodeVm.__init__(self, intmem)

    def parse_op(self):
        """ Parse opcode and arguments from current program counter
        We return the opcode along with in/out argument lists
        Arguments are pointers to memory locations
        """
        pc = self.reg["pc"]
        opcode = self.mem[pc] % 100
        flags = self.mem[pc] // 100

        op_args = op_info.get(opcode)
        op_cnt = len(op_args)

        argsin = []
        argsout = []
        for i in range(0, op_cnt):
            f = flags % 10
            flags //= 10

            if f == FLAG_POSITION:
                ptr = self.mem[pc + i + 1]
            elif f == FLAG_IMMEDIATE:
                assert op_args[i] != 1, "Output parameter in immediate mode"
                ptr = pc + i + 1
            elif f == FLAG_RELATIVE:
                ptr = self.mem[pc + i + 1] + self.reg["rbs"]
            else:
                assert False, "Unknown flag value"

            # enlarge memory if we point outside of it
            if ptr >= len(self.mem):
                self.mem += [0] * (2 + ptr - len(self.mem))

            if op_args[i] == 0:
                argsin.append(ptr)
            else:
                argsout.append(ptr)

        return (opcode, argsin, argsout)

    def exec_next_op(self):
        """ Execute intcode operations.
        We lookup known opcodes in the intcode VM and dispatch to the
        corresponding opcode implementation accordingly.

        Opcode implementations operate on values, we handle load/stores to
        memory.
        """

        (opcode, argsin, argsout) = self.parse_op()
        assert(opcode in self.ops)

        # Execute opcode and push results to memory
        output = self.ops[opcode](
                        *[self.mem[a] for a in argsin])
        for i, ptr in enumerate(argsout):
            self.mem[ptr] = output[i]

        # Handle status flags and move PC
        # pc_dirty is set by instructions which modify the program counter
        if self.reg["pc_dirty"]:
            self.reg["pc_dirty"] = False
        else:
            self.reg["pc"] += len(argsin) + len(argsout) + 1

    def push_input(self, val):
        self.reg["in"].append(val)

    def run_gen(self):
        """ Intcode generator, can be used to easily interact with an intcode
        program.

        for output in interpreter.run_gen():
            # Do stuff with output
            ..
            # Push new input
            interpreter.push_input()
        """
        while self.reg["running"]:
            self.exec_next_op()
            while self.reg["out"] != []:
                yield self.reg["out"].pop(0)

    def run(self, argv=None):
        """ Run an intcode program until it exits. You should provide enough
        input in argv
        """
        if argv is not None:
            self.reg["in"] = argv

        while self.reg["running"]:
            self.exec_next_op()
        return self
