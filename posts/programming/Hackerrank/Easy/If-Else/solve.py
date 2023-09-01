#!/bin/python3
import math
import os
import random
import re
import sys


if __name__ == '__main__':
    n = int(input().strip())

    check1 = [x for x in range(1, 101, 2)]
    check2 = [y for y in range(2, 6, 2)]
    check3 = [z for z in range(6, 21, 2)]
    check4 = [i for i in range(0, 101, 2)]

    # If n is odd, print Weird
    for val1 in check1:
        if n == val1:
            print('Weird')
            break
    
    # If n is even and in the inclusive range of 2 to 5, print Not Weird
    for val2 in check2:
        if n == val2:
            print('Not Weird')
            break
    
    # If n is even and in the inclusive range of 6 to 20, print Weird
    for val3 in check3:
        if n == val3:
            print('Weird')
            break
    
    # If n is even and greater than 20, print Not Weird
    for val4 in check4:
        if n == val4 and n > 20:
            print('Not Weird')
            break
