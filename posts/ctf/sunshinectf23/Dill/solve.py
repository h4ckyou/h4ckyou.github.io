#!/usr/bin/python3

encrypted = 'bGVnbGxpaGVwaWNrdD8Ka2V0ZXRpZGls'
mapping = [5, 1, 3, 4, 7, 2, 6, 0]
prefix = "sun{"
suffix = "}"

enc = [encrypted[i:i+4] for i in range(0, len(encrypted), 4)]
r = [0]*8

for idx, value in enumerate(mapping):
    r[value] = enc[idx]

r = ''.join(r)
flag = prefix + r + suffix

print(f"Flag: {flag}")
