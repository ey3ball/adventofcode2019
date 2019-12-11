 #!/usr/bin/env python3

import sys
from intcode import run_intcode

BLACK = 0
WHITE = 1

class Robot:
    TURNS = [(0,-1),(1,0),(0,1),(-1,0)]
    DIRS = ["^", ">", "v", "<"]

    def __init__(self, start_position):
        SIZE = start_position[0] * 2 + 1
        self.current_direction = 0
        self.pos = start_position
        print(SIZE)
        self.ship = [["." for i in range(SIZE)] for j in range(SIZE)]
        self.ship[self.pos[0]][self.pos[1]] = "#"

    def _add_position(self, pos, incr):
        return (pos[0] + incr[0], pos[1] + incr[1])

    def show_panel(self):
        for y in range(len(self.ship[0])):
            for x in range(len(self.ship)):
                if x == self.pos[0] and y == self.pos[1]:
                    sys.stdout.write(self.DIRS[self.current_direction])
                    continue

                if self.ship[x][y] == "#":
                    sys.stdout.write(self.ship[x][y])
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")

    def run_once(self):
        # Step through program and paint
        print(self.pos)
        cur_color = WHITE if self.ship[self.pos[0]][self.pos[1]] == "#" else BLACK
        (color, turn) = self.next(cur_color)
        self.ship[self.pos[0]][self.pos[1]] = "o" if color == BLACK else "#"

        self.turn(turn)

    def next(self, pixel_value):
        pass

    def turn(self, go_right):
        if go_right:
            self.current_direction += 1
        else:
            self.current_direction -= 1

        self.current_direction = self.current_direction % 4
        print(self.TURNS[self.current_direction])

        self.pos = self._add_position(self.pos, self.TURNS[self.current_direction])

class IntCodeRobot(Robot):
    def __init__(self, start_position, memmap):
        Robot.__init__(self, start_position)
        self.argv = []
        self.intcode = run_intcode(memmap, self.argv)
        print("ran")
        self.i = 0


    def next(self, pixel_value):
        self.i += 1
        self.argv.append(pixel_value)
        color = next(self.intcode)
        turn = next(self.intcode)

        return (color, turn)

# Test run
robot = Robot((2,2))
robot.next = lambda x: (1, 0)
robot.run_once()
robot.next = lambda x: (0, 0)
robot.run_once()
robot.next = lambda x: (1, 0)
robot.run_once()
robot.next = lambda x: (1, 0)
robot.run_once()
robot.next = lambda x: (0, 1)
robot.run_once()
robot.next = lambda x: (1, 0)
robot.run_once()
robot.next = lambda x: (1, 0)
robot.run_once()
robot.show_panel()

intcode = sys.argv[1]
init_memmap = [int(i) for i in intcode.split(",")]

intbot = IntCodeRobot((64,64), init_memmap)

try:
    while True:
        intbot.run_once()
except StopIteration as e:
    intbot.show_panel()

ship = intbot.ship

counter = 0
for y in range(len(ship[0])):
    for x in range(len(ship)):
        if ship[x][y] != ".":
            counter += 1
print(counter)
print(intbot.i)
