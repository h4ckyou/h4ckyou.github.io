with open("sore", "rb") as f:
    binary = f.read()

f.close()

binary = binary.replace(b"\xff\x15\x58\xd3\x27\x00", b'\x90'*6)

with open("patched", "wb") as f:
    f.write(binary)
