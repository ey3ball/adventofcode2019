#/usr/bin/python

with open("day1_1.txt", "r") as f:
    modules_fuel = [int(int(m)/3) - 2  for m in f.readlines()]

    print(sum(modules_fuel))
