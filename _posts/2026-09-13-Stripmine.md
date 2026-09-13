---
title: Strip Mine @ Pwn College
date: 2026-09-13 21:40:00 +0100
categories: [CTF]
tags: [reversing]
math: true
mermaid: true
media_subpath: /assets/posts/2026-09-13-stripmine
image:
  path: stripmine.png
---

## Strip Mine 

### Overview

Hey heyyy 👋🏽

I originally wanted to make a dedicated blog post for a reversing challenge I solved on [pwn.college](https://pwn.college/), but... I got lazy. 😭

This challenge wasn’t graded with points; it was more of a tutorial challenge meant to teach some reversing concepts. Tbh, I’ve forgotten the exact details of the dojo and how the challenge was introduced, but welp. 😂

From what I remember, the challenge is basically a variant of the **“Strip Mine”** game, where the paths and grids are hardcoded into the binary.

So yeah, this is me finally writing about it before I forget even more. 💀


### Source

This is the data structure in use (after reversing it):

```c
00000000 struct grid_t // sizeof=0x1B0
00000000 {
00000000     int score;
00000004     char grid[20][20];
00000194     int x;
00000198     int y;
0000019C     // padding byte
0000019D     // padding byte
0000019E     // padding byte
0000019F     // padding byte
000001A0     node_t *path;
000001A8     size_t steps;
000001B0 };

00000000 struct node_t // sizeof=0x10
00000000 {
00000000     uint8_t bits[8];
00000008     struct node_t *next;
00000010 };
```

And here's the whole program decompilation.

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  char *data; // rax
  char *data_ptr; // rbx
  ssize_t len; // rax
  node_t *path; // rdi
  node_t *next; // rbx
  grid_t game; // [rsp+0h] [rbp-1C8h] BYREF
  unsigned __int64 v10; // [rsp+1B8h] [rbp-10h]

  v10 = __readfsqword(0x28u);
  initialize_game(&game);
  data = malloc(0x10000uLL);
  if ( data )
  {
    data_ptr = data;
    len = read(0, data, 0x10000uLL);
    if ( len > 0 )
    {
      game.path = process_input(data_ptr, len, &game.steps);
      if ( game.path )
      {
        free(data_ptr);
        check_path(&game);
        path = game.path;
        if ( game.path )
        {
          do
          {
            next = path->next;
            free(path);
            path = next;
          }
          while ( next );
          return 0LL;
        }
        else
        {
          return 0LL;
        }
      }
      else
      {
        fwrite("error processing input\n", 1uLL, 0x17uLL, stderr);
        free(data_ptr);
        return 1LL;
      }
    }
    else
    {
      free(data_ptr);
      return 0LL;
    }
  }
  else
  {
    perror("malloc");
    return 1LL;
  }
}


int *__fastcall initialize_game(grid_t *grid)
{
  char *v1; // rax
  char *v2; // rdx
  int *p1; // rax
  int *p2; // rax

  v1 = grid->grid[0];
  do                                            // populates the grid to dots
  {
    v2 = v1 + 20;
    do
      *v1++ = '.';
    while ( v1 != v2 );
    v1 = v2;
  }
  while ( &grid->x != v2 );                     // while v2 isn't equal to the end of 20x20 grid
  p1 = &data1;
  do
  {
    grid->grid[*p1][*(p1 - 1)] = '#';           // write format is data[i] = y, data[i-1] = x
    p1 += 2;
  }
  while ( &data2 != p1 );
  p2 = &data3;
  do
  {
    grid->grid[*p2][*(p2 - 1)] = '$';
    p2 += 2;
  }
  while ( &data4 != p2 );
  grid->x = 0;
  grid->y = 0;
  grid->score = 0;
  return p2;
}

node_t *__fastcall process_input(char *data, __int64 len, _QWORD *steps)
{
  node_t *ptr; // rax
  char *data_ptr; // r12
  __int64 n; // r13
  node_t *root; // r14
  char byte; // dl
  node_t *node; // rbp
  __int64 i; // rbx
  char bit; // dl
  _BYTE nibble[8]; // [rsp+10h] [rbp-48h]
  unsigned __int64 v13; // [rsp+18h] [rbp-40h]

  v13 = __readfsqword(0x28u);
  ptr = 0LL;
  if ( len )
  {
    data_ptr = data;
    n = 0LL;
    root = 0LL;
LABEL_3:
    byte = *data_ptr;
    nibble[0] = *data_ptr >> 4;                 // upper nibble
    nibble[1] = byte & 0xF;                     // lower nibble
    node = ptr;
    i = 0LL;
    while ( 1 )
    {
      ptr = calloc(1uLL, 0x10uLL);
      if ( !ptr )
        break;
      bit = nibble[i];                          // do some bit manipulation of the each nibble
      ptr->bits[0] = bit & 7;
      ptr->bits[1] = (bit & 0xF) >> 3;
      ptr->next = 0LL;
      if ( root )
        node->next = ptr;
      else
        root = ptr;
      ++n;
      ++i;
      node = ptr;
      if ( i == 2 )                             // after two iterations check end of data_ptr
      {
        if ( &data[len] != ++data_ptr )
          goto LABEL_3;
        goto LABEL_12;
      }
    }
  }
  else
  {
    n = 0LL;
    root = 0LL;
LABEL_12:
    *steps = n;
    return root;
  }
  return ptr;
}

__int64 __fastcall check_path(grid_t *game)
{
  node_t *path; // rax
  __int64 i; // rdx
  __int64 steps; // rbp
  int y; // ecx
  int x; // edi
  int current_score; // esi
  __int64 pos; // rcx
  unsigned int coord_x; // esi
  unsigned int coord_y; // ecx

  path = game->path;
  if ( path )
  {
    for ( i = 1LL; ; ++i )
    {
      steps = i - 1;
      if ( path->bits[1] )
      {
        y = game->y;
        x = game->x;
        if ( game->grid[y][x] == '$' )
        {
          current_score = game->score + 1;
          game->score = current_score;
          game->grid[y][x] = '.';
          if ( current_score > 15 )
          {
            game_win();
            return __printf_chk(1LL, "score: %d  --  took %ld steps\n", game->score, steps);
          }
        }
        path = path->next;
      }
      else
      {
        pos = path->bits[0];
        coord_x = game->x + x_axis[pos];
        coord_y = game->y + y_axis[pos];
        if ( coord_y > 0x13 || coord_x > 0x13 || game->grid[coord_y][coord_x] == '#' )
        {
          puts("\nCOLLAPSE!!");
          return __printf_chk(1LL, "score: %d  --  took %ld steps\n", game->score, steps);
        }
        game->x = coord_x;
        game->y = coord_y;
        path = path->next;
      }
      if ( !path )
        break;
    }
    steps = i;
  }
  else
  {
    steps = 0LL;
  }
  return __printf_chk(1LL, "score: %d  --  took %ld steps\n", game->score, steps);
}

unsigned __int64 game_win()
{
  int v0; // eax
  int *v1; // rax
  char *v2; // rax
  int v3; // eax
  int *v4; // rax
  char *v5; // rax
  int *v6; // rax
  char *v7; // rax
  _BYTE v9[136]; // [rsp+0h] [rbp-98h] BYREF
  unsigned __int64 v10; // [rsp+88h] [rbp-10h]

  v10 = __readfsqword(0x28u);
  v0 = open("/flag", 0);
  if ( v0 < 0 )
  {
    v1 = __errno_location();
    v2 = strerror(*v1);
    __printf_chk(1LL, "\n  ERROR: Failed to open the flag -- %s!\n", v2);
    if ( geteuid() )
    {
      puts("  Your effective user id is not 0!");
      puts("  You must directly run the suid binary in order to have the correct permissions!");
    }
    exit(-1);
  }
  v3 = read(v0, v9, 0x80uLL);
  if ( v3 <= 0 )
  {
    v4 = __errno_location();
    v5 = strerror(*v4);
    __printf_chk(1LL, "\n  ERROR: Failed to read the flag -- %s!\n", v5);
    exit(-1);
  }
  if ( write(1, v9, v3) <= 0 )
  {
    v6 = __errno_location();
    v7 = strerror(*v6);
    __printf_chk(1LL, "\n  ERROR: Failed to write the flag -- %s!\n", v7);
    exit(-1);
  }
  puts("\n");
  return __readfsqword(0x28u) ^ v10;
}
```

### Solve

For my solution, I ended up treating the maze like a graph and exploring it using Breadth-First Search (BFS) to find the path through the hardcoded grid.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from collections import deque

exe = context.binary = ELF('stripmine', checksec=False)
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def init():
    global io

    io = start()

def generatePath(path):
    result = bytearray()

    for pos in path:
        lower_bit = pos
        upper_bit = 0
        upper_nibble = (upper_bit << 3) | lower_bit

        lower_bit = 0
        upper_bit = 1
        lower_nibble = (upper_bit << 3) | lower_bit

        byte = (upper_nibble << 4) | lower_nibble
        result.append(byte)

    return bytes(result)


def solve():

    points_x = bytes.fromhex("00 00 00 00 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF")
    points_y = bytes.fromhex("FF FF FF FF FF FF FF FF 00 00 00 00 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 00 FF FF FF FF")

    x_axis = [struct.unpack("<i", points_x[i:i+4])[0] for i in range(0, len(points_x), 4)]
    y_axis = [struct.unpack("<i", points_y[i:i+4])[0] for i in range(0, len(points_y), 4)]

    grid = [
        [0,0,2,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,2,0,0,0,0,0,0,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,2,0,0,0,0,2,1,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,2,0,0,0,0,0,1,1,1,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,2,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],
        [0,0,1,1,1,1,2,1,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,2,0,1,1,0,0,0,0,0,0,0,2,0],
        [0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
        [0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,2],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,2,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    rows, cols = len(grid), len(grid[0])

    def bfs(start_x, start_y):
        q = deque()
        q.append((start_x, start_y, []))
        visited = set()
        visited.add((start_x, start_y))

        while q:
            x, y, path = q.popleft()

            for pos in range(8):
                nx, ny = x + x_axis[pos], y + y_axis[pos]
                if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                    if grid[ny][nx] == 1:
                        continue
                    new_path = path + [pos]
                    if grid[ny][nx] == 2: 
                        grid[ny][nx] = 1
                        return nx, ny, new_path
                    q.append((nx, ny, new_path))
                    visited.add((nx, ny))

        return None  


    start_x, start_y = 0, 0
    win_path = b""

    while True:
        result = bfs(start_x, start_y)
        if not result:
            break
        start_x, start_y, path = result
        print(f"Reached food at ({start_x}, {start_y}) with moves {path}")
        win_path += generatePath(path)
    
    io.send(win_path)

    io.interactive()


def main():
    
    init()
    solve()
    

if __name__ == '__main__':
    main()
```

And.. that's all :)

