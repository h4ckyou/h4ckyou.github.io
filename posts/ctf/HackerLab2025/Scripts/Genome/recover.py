import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

repertoire = './'
encrypted_files = [file for file in os.listdir(repertoire) if file.endswith('.sika')]
encrypted_files.sort()

# Initialize the key with the first byte of each encrypted file
key = bytearray(16)
for i, encrypted_file in enumerate(encrypted_files):
    with open(os.path.join(repertoire, encrypted_file), 'rb') as f:
        encrypted_data = f.read()
        key[i] = encrypted_data[0]  # Populate first bytes from each file's first byte

# Brute-force the last three key bytes
found_key = None
with open(os.path.join(repertoire, 'flag.txt.sika'), 'rb') as f:
    encrypted_data = f.read()
    for possible_byte1 in range(256):
        for possible_byte2 in range(256):
            for possible_byte3 in range(256):
                key[2] = possible_byte1
                key[14] = possible_byte2
                key[15] = possible_byte3
                cipher = AES.new(bytes(key), AES.MODE_ECB)
                try:
                    decrypted_data = cipher.decrypt(encrypted_data[1:])
                    if decrypted_data.startswith(b'fake'):
                        found_key = key[:]
                        print(f"Found matching key: {found_key.hex()}")
                        break
                except ValueError:
                    continue
            if found_key:
                break
        if found_key:
            break

if not found_key:
    print("No matching key found.")
else:
    os.makedirs('out', exist_ok=True)
    for encrypted_file in encrypted_files:
        with open(os.path.join(repertoire, encrypted_file), 'rb') as f:
            encrypted_data = f.read()
            cipher = AES.new(bytes(found_key), AES.MODE_ECB)
            decrypted_data = cipher.decrypt(encrypted_data[1:]) 
            try:
                decrypted_data = unpad(decrypted_data, AES.block_size)
            except ValueError:
                print(f"Warning: {encrypted_file} may not have valid padding.")
            output_path = os.path.join('out', encrypted_file.replace('.sika', '.txt'))
            with open(output_path, 'wb') as o:
                o.write(decrypted_data)
    print("Decryption completed.")
