#!/usr/bin/env python3 

from collections import Counter
import sys

def parse_line(l):
    [ins, out] = l.split(" => ")

    ins = ins.split(", ")
    ins = [component.split(" ") for component in ins]
    ins =  {chemical: int(qty)
           for [qty, chemical] in ins}

    out = out.strip().split(" ")

    return (out, ins)

with open(sys.argv[1]) as f:
    chemicals = {out[1]: { "in": ins, "out": int(out[0]) }
                 for out, ins in [parse_line(l) for l in f.readlines()]}


def required_ore(fuel_qty):
    spare = Counter()

    required = Counter()
    required["FUEL"] = fuel_qty
    while True:
        #print("Requirements {}".format(dict(required)))

        if len(required) == 1 and "ORE" in required:
            break

        next_required = Counter()
        for component, qty in required.items():
            #print("Need {} x {}".format(component, qty))

            if component == "ORE":
                next_required["ORE"] += qty
                continue

            # First check if we can use some spare chemicals
            if spare[component] > 0:
                use_spare = min(spare[component], qty)
                qty -= use_spare
                spare[component] -= use_spare
                #print("Took {} from storage".format(use_spare))

            assert qty >= 0
            if qty == 0:
                continue

            # Find the reaction that generates component,
            # add add necessary reagents to requirements
            gen_qty = chemicals[component]["out"]
            gen_requirements = chemicals[component]["in"]
            reaction_count = ((qty - 1) // gen_qty) + 1
            #print("Gen {} from {} x {}".format(reaction_count * gen_qty, reaction_count, chemicals[component]))

            spare_qty = (reaction_count * gen_qty) - qty
            if spare_qty:
                #print("Add {} x {} to storage".format(component, spare_qty))
                spare[component] += spare_qty

            for reagent, reagent_qty in gen_requirements.items():
                next_required[reagent] += reaction_count * reagent_qty
                #print(reagent, next_required[reagent])

        required = next_required

    return required["ORE"]

TARGET = 1000000000000
baseline = required_ore(1)

print("1 FUEL <= {} ORE".format(baseline))

estimate_fuel = TARGET // baseline
actual_ore = required_ore(estimate_fuel)

if actual_ore > TARGET:
    fuel_range = [0, estimate_fuel]
else:
    fuel_range = [estimate_fuel, estimate_fuel * 2]

while True:
    if fuel_range[1] - fuel_range[0] <= 1:
        break

    try_fuel = (fuel_range[0] + fuel_range[1]) // 2
    actual_ore = required_ore(try_fuel)
    if actual_ore > TARGET:
        fuel_range = [fuel_range[0], try_fuel]
    else:
        fuel_range = [try_fuel, fuel_range[1]]

print("{} FUEL <= {} ORE".format(fuel_range[0], required_ore(fuel_range[0])))
