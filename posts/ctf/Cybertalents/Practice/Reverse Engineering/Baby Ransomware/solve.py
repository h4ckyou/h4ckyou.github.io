import ctypes
import time
import sys

class Evil:
    def __init__(self, key, enc):
        self.key = key.encode()
        self.enc = enc
        self.size = len(self.key)
        self.array = bytearray(range(0x100))
        self.idx_i = 0
        self.idx_j = 0

        idx_j = 0
        for i in range(0x100):
            idx_j = (self.array[i] + idx_j + self.key[i % self.size]) % 0x100
            self.swap(i, idx_j)

        idx_j = 0
        idx_i = 0

    def swap(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def get_byte(self):
        self.idx_i = (self.idx_i + 1) % 256
        self.idx_j = (self.idx_j + self.array[self.idx_i]) % 256
        self.swap(self.idx_i, self.idx_j)
        pos = self.array[self.idx_i] + self.array[self.idx_j]
        result = self.array[pos & 0xff]
        return result
        
    def decrypt(self):
        size = len(self.enc)
        result = bytearray(size)
        for i in range(size):
            key = self.get_byte()
            value = key ^ self.enc[i]
            result[i] = value
        
        return result

def main():

    if len(sys.argv) != 2:
        print(f"python3 {sys.argv[0]} filename")
        exit(0)

    filename = sys.argv[1]

    with open(filename, "rb") as f:
        enc = f.read()

    libc = ctypes.CDLL("libc.so.6") # msvcrt.dll
    key = "Hell"

    timestamp = 0x5f1c438e
    start = timestamp - 0x10000
    end = timestamp + 0x100000

    for seed in range(start, end):
        libc.srand(seed)

        for i in range(5):
            v3 = libc.rand() % 10
            key += str(v3)

        obj = Evil(key, enc)
        data = obj.decrypt()

        if b"flag" in data:
            print(f"flag: {data.decode()}")
            break

        key = "Hell"


if __name__ == '__main__':
    main()
