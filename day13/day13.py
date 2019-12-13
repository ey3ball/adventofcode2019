#!/usr/bin/env python3

from itertools import groupby
from intcode import IntCodeInterpreter
from collections import OrderedDict
import sys
import time
import os

"""
This solution is convoluted because of a BUG I only discovered after finishing
it. The Intcode VM uses a generator to yield output data.

Since the output from the game produces threee consecutive values at a time, I
decided it would be a good opportunity to give itertools.groupby a try.

Sadly groupby in order to group inputs by 3, groupby implementation has to
access the 4th element in the following loop :

for _, group in groupby(enumerate(gen), key=lambda e: e[0] // 3):

This means my loop is always one move behind which is one I ended up
reverse-engineering the ball movement in order to predict its next position ...
"""

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

def wall(tile):
    if tile == WALL or tile == BLOCK:
        return True
    else:
        return False

def bump(pos, vec, tiles):
    # Side bump
    side = (pos[0] + vec[0], pos[1])
    if wall(tiles[side]):
        if tiles[side] == BLOCK:
            tiles[side] = 0
        return bump(pos, (-vec[0], vec[1]), tiles)

    # Top bump
    top = (pos[0], pos[1] + vec[1])
    if wall(tiles[top]):
        if tiles[top] == BLOCK:
            tiles[top] = 0
        return bump(pos, (vec[0], -vec[1]), tiles)

    # Diag bump
    diag = (pos[0] + vec[0], pos[1] + vec[1])
    if wall(tiles[diag]):
        if tiles[diag] == BLOCK:
            tiles[diag] = 0
        return bump(pos, (-vec[0], -vec[1]), tiles)

    return (pos[0] + vec[0], pos[1] + vec[1])

def predict_next_ball_pos(prev, cur, tiles):
    tiles = dict(tiles)

    dx = cur[0] - prev[0]
    dy = cur[1] - prev[1]

    return bump(cur, (dx, dy), tiles)

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
step = 0
interpreter.push_input(0)
interpreter.push_input(0)
for _, group in groupby(enumerate(gen), key=lambda e: e[0] // 3):
    update = [g[1] for g in group]
    pushed = ""

    if update[2] == CURSOR and pos is None:
        pos = update[0]

    if update[2] == BALL:
        if ball is not None:
            next_pos = predict_next_ball_pos(ball, (update[0], update[1]), tiles)
            tiles[next_pos] = "P"
            if pos - next_pos[0] >= 1:
                #pushed = "left"
                if next_pos[0] != 1:
                    interpreter.push_input(-1)
                    pos -= 1
                else:
                    interpreter.push_input(0)
            elif pos - next_pos[0] == 0:
                # ball is just above us, don't move
                if next_pos[1] != 19:
                    interpreter.push_input(next_pos[0] - ball[0])
                    pos += next_pos[0] - ball[0]
                else:
                    interpreter.push_input(0)
            elif pos - next_pos[0] <= -1:
                #pushed = "right"

                if next_pos[0] != 36:
                    interpreter.push_input(1)
                    pos += 1
                else:
                    interpreter.push_input(0)

        ball = (update[0], update[1])

    if update[0] == -1:
        screen_ok = True
        score = update[2]

    tiles[(update[0], update[1])] = update[2]
    if screen_ok:
        #os.system("tput clear")
        print(step)
        printt(tiles)

        time.sleep(0.01)
        #input("")

        step += 1
