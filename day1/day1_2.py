#/usr/bin/python

def fuel_required(mass):
    required = int(mass / 3) - 2

    return required + fuel_required(required) if required >= 0 else 0

total_fuel = 0
with open("day1_1.txt", "r") as f:
    modules_fuel = [fuel_required(int(m))  for m in f.readlines()]

    total_fuel += sum(modules_fuel)

print(total_fuel)
