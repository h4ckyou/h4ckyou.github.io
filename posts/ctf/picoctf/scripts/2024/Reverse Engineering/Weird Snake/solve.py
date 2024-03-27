input_list = [4, 54, 41, 0, 112, 32, 25, 49, 33, 3, 0, 0, 57, 32, 108, 23, 48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 106, 123, 89, 87, 18, 62, 47, 10, 78]
key_str = "t_Jo3"

r = ''

for i in range(len(input_list)):
    xr = ord(key_str[i % len(key_str)]) ^ input_list[i]
    r += chr(xr)

print(r)
