#!/usr/bin/env python3

from collections import Counter

IMAGE_SIZE = 25*6

with open("day8.txt") as f:
    pixels = [int(i) for i in f.readline().strip()]

images = [pixels[i*IMAGE_SIZE:(i+1)*IMAGE_SIZE]
          for i in range(0, len(pixels) // IMAGE_SIZE)]

corruption_status = [(counter[0], counter)
                     for counter in (Counter(i) for i in images)]

corruption_status.sort(key=lambda x: x[0])

print(corruption_status)
best = corruption_status[0]
print(best[1][1] * best[1][2])
