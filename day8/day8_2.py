#!/usr/bin/env python3

import sys

IMAGE_SIZE = 25*6

with open("day8.txt") as f:
    pixels = [int(i) for i in f.readline().strip()]

layers = [pixels[i*IMAGE_SIZE:(i+1)*IMAGE_SIZE]
          for i in range(0, len(pixels) // IMAGE_SIZE)]

def blend_pixels(top, bottom):
    if top != 2:
        return top
    else:
        return bottom

decoded = layers[0]
for image in layers:
    decoded = [blend_pixels(decoded[i],image[i]) for i in range(0, IMAGE_SIZE)]

for (i, p) in enumerate(decoded):
    if p == 0:
        sys.stdout.write(" ")
    else:
        sys.stdout.write(".")

    if (i+1) % 25 == 0:
        sys.stdout.write("\n")


for i in range(0, 7):
    print(decoded[i*25:(i+1)*25])
