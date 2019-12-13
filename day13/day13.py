#!/usr/bin/env python3

from itertools import groupby
from intcode import IntCodeInterpreter
from collections import OrderedDict
import sys
import time
import os

with open("day13.txt", "r") as f:
    program = f.readline().strip()

interpreter = IntCodeInterpreter(program)
interpreter.mem[0] = 2
gen = interpreter.run_gen()

screen_ok = False

WALL = 1
BLOCK = 2
CURSOR = 3
BALL = 4
PADDLE = 3

def predict_next_ball_pos(prev, cur, tiles):
    dx = cur[0] - prev[0]
    dy = cur[1] - prev[1]

    pred_x = cur[0] + dx
    pred_y = cur[1] + dy
    next_tile = tiles[(pred_x, pred_y)]
    if next_tile == BLOCK:
        pred_y = cur[1] - dy
    if next_tile == WALL:
        pred_x = cur[0] - dx

    return (pred_x, pred_y)

def printt(tiles):
    for (x, y), tile in tiles.items():
        #print(x, y)
        if (x == 0):
            sys.stderr.write("\n")
        sys.stderr.write(str(tile) if tile != 0 else " ")
    sys.stderr.write("\n")

score = 0
tiles = OrderedDict()
pos = None
ball = None
screen_ok = False
for _, group in groupby(enumerate(gen), key=lambda e: e[0] // 3):
    update = [g[1] for g in group]
    pushed = ""
    #print(update)
    if update[2] == CURSOR:
        pos = update[0]

    if update[2] == BALL:
        if ball is not None:
            next_pos = predict_next_ball_pos(ball, (update[0], update[1]), tiles)

            if pos - next_pos[0] >= 1:
                pushed = "left"

                if next_pos[0] != 1:
                    interpreter.push_input(-1)
            elif pos - next_pos[0] == 0:
                if next_pos[1] != 19:
                    interpreter.push_input(next_pos[0] - ball[0])
            elif pos - next_pos[0] <= -1:
                pushed = "right"

                if next_pos[0] != 36:
                    interpreter.push_input(1)
            #elif pos - next_pos[0] == 0:
            #    interpreter.push_input(update[0] - ball[0])

        ball = (update[0], update[1])

    if update[0] == -1:
        screen_ok = True
        score = update[2]

    tiles[(update[0], update[1])] = update[2]
    if screen_ok:
        os.system("tput clear")
        print(ball[0])
        print(pushed)
        printt(tiles)
        input("")

#try:
#    interpreter.run()
#except:
#    print(interpreter.reg["out"])
#
#xs = interpreter.reg["out"][0::3]
#ys = interpreter.reg["out"][1::3]
#tile = interpreter.reg["out"][2::3]
#
#for i in range(len(xs)):
#    if tile[i] == 0:
#        if (xs[i], ys[i]) in tiles:
#            del tiles[(xs[i], ys[i])]
#    else:
#        tiles[(xs[i], ys[i])] = tile[i]
#    #if tile[i] == 2:
#    #    block += 1
#    #    print(xs[i], ys[i], tile[i])
#
#print(tiles)
