with open('enc', 'rb') as f:
    encrypted_data = f.read()

keystream = bytes.fromhex("89ce75b9bb093f2d3b90034c15e43d04bc3d6bbd99dc0b13a02c50be4ed7560b31462f736a1d65f1befcec67fa")
decrypted = ""

for i in range(len(encrypted_data)):
    ct = encrypted_data[i] - 1
    print(chr(ct ^ keystream[i % len(keystream)]), end='')
