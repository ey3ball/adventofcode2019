#!/usr/bin/env python3

from intcode import IntCodeInterpreter
import sys

PCK_ADDR = 0
PCK_X = 1
PCK_Y = 2

with open("day23.txt", "r") as f:
    program = f.readline().strip()

_nics = [IntCodeInterpreter(program) for i in range(0, 50)]

nics = []
for i, nic in enumerate(_nics):
    nic.push_input(i)
    nic.__dict__.update({'i': i})
    nics.append((nic, nic.run_gen()))

old_nat = [-1, -1]
nat = []
delivered = []

while True:
    idle = True
    for nic, nic_gen in nics:
        packet = []
       
        starved = False
        for i in range(0,3):
            out = next(nic_gen)
            if out == None:
                starved = True
                break
            idle = False
            packet.append(out)

        if starved:
            continue
        print(packet)
        if packet[PCK_ADDR] <= 49:
            nics[packet[PCK_ADDR]][0].push_input(packet[PCK_X])
            nics[packet[PCK_ADDR]][0].push_input(packet[PCK_Y])

        if packet[PCK_ADDR] == 255:
            nat = [packet[PCK_X], packet[PCK_Y]]
            #print("Received packet for 255")
            #print(packet)
            #sys.exit(0)

    if idle and nat != []:
        print("nat {}".format(nat))
        if nat != [] and nat[1] == old_nat[1]:
            print(nat)
            sys.exit(0)
        else:
            old_nat = nat
        nics[0][0].push_input(nat[0])
        nics[0][0].push_input(nat[1])
