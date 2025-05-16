from pwn import *
import struct

MAZE_SIZE = 30
CELL_SIZE = 0x10

exe = ELF("./tunnel", checksec=False)

def read_cell(addr):
    data = exe.read(addr, CELL_SIZE)
    return struct.unpack("IIII", data)

def read_coord(coord):
    x, y, z = coord
    addr = exe.sym["maze"] + (x * MAZE_SIZE * MAZE_SIZE * CELL_SIZE) + (y * MAZE_SIZE * CELL_SIZE) + (z * CELL_SIZE)
    return read_cell(addr)

START = 0
OPEN = 1
CLOSED = 2
FINISH = 3

def get_adj(pos):
    x, y, z = pos
    options = []
    if x > 0: options.append((x-1, y, z))
    if x < MAZE_SIZE - 1: options.append((x+1, y, z))
    if y > 0: options.append((x, y-1, z))
    if y < MAZE_SIZE - 1: options.append((x, y+1, z))
    if z > 0: options.append((x, y, z-1))
    if z < MAZE_SIZE - 1: options.append((x, y, z+1))
    return options

def solve():
    start = (0, 0, 0)
    stack = [(start, [start])]
    visited = set()

    while stack:
        pos, path = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)

        _, _, _, typ = read_coord(pos)
        if typ == FINISH:
            return path

        for adj in get_adj(pos):
            if adj in visited:
                continue
            _, _, _, adj_type = read_coord(adj)
            if adj_type == OPEN or adj_type == FINISH:
                stack.append((adj, path + [adj]))

    return None 

path = solve()

solution = ""
for i in range(1, len(path)):
    prev = path[i-1]
    cur = path[i]
    dx, dy, dz = cur[0]-prev[0], cur[1]-prev[1], cur[2]-prev[2]
    if dx == 1: solution += "R"
    elif dx == -1: solution += "L"
    elif dy == 1: solution += "F"
    elif dy == -1: solution += "B"
    elif dz == 1: solution += "U"
    elif dz == -1: solution += "D"

print(solution)
