import sys
from PIL import Image

def prob(s_img, msg, d_img):
	im = Image.open(s_img).convert("RGBA")
	p = im.load()
	c = 0
	msg = map(lambda x: ord(x) ^ len(d_img), msg[::-1])
	
	for i in range(0, len(msg)):
		enc = msg[i]
		p[c, 0] = (p[c, 0][0], p[c, 0][1], p[c, 0][2], enc)
		c += 1
	im.save(d_img)


if len(sys.argv) != 4:
	print(f"{sys.argv[0]} \"orignal.png\" \"secret message\" \"secret.png\"")
	exit()

prob(sys.argv[1], sys.argv[2], sys.argv[3])
