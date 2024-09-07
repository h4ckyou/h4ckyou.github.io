#!/usr/bin/python2.7
import random
import sys

def get_seed(current_x, current_time):
    start = current_time - 0x100
    end = current_time + 0x100

    for sd in range(start, end):
        random.seed(sd)
        x = random.randint(0, 400000000)
        if x == current_x:
            return sd


def predict(seed):
    output = ''
    random.seed(seed)

    for i in range(99*2 + 2):
        x = random.randint(0, 400000000)
        output += str(x) + ' '
    
    print(output)

    
def main():
    cx = int(sys.argv[1])
    ct = int(sys.argv[2])
    seed = get_seed(cx, ct)
    predict(seed)


if __name__ == '__main__':
    main()
