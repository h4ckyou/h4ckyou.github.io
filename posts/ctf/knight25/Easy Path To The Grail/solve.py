def dofight(val: int) -> int:
    value = 0
    for i in range(8):
        value = (val & 1) | (2 * value)
        val >>= 1
    
    return value

def transform(buf: bytes):
    flag = b""
    for i in buf:
        flag += bytes([dofight(i)])
    
    print(flag)


buf = "D2C22A62DEA62CCE9EFA0ECC86CE9AFA4ECC6EFAC6162C3636CC76E6A6BE"
enc = bytes.fromhex(buf)
transform(enc)
