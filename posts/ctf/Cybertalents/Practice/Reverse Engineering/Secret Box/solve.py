from PIL import Image

filename = "secret.png"
im = Image.open(filename).convert("RGBA")
p = im.load()
flag = ""

for i in range(0xff):
    px = p[i, 0]
    enc = px[3]

    if enc == 0xff:
        break

    d = enc ^ len(filename)
    flag += chr(d)

print(flag[::-1])
