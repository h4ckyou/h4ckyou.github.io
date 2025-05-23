import hashlib

output_bin = bytes.fromhex("E3 9D 8F 77 30 76 78 00 16 E2 7B E3 B3 16 07 25 43 36 9B E1 DA A7 1F 66 09 05 D2 18 8E 21 5D 62 52 66 E4 72 79 C3 30 62 E3 B1 D3 01 3C F3 3B CF A4 E7 15 1F 82 E8 D2 68 F8 B1 B7 06 31 AB 1B 7A 74 AF A6 5E 03 0F 88 3F 04 B7 15 C3 6F 58 64 42 2E EB F4 95 FA D7 75 11 D2 70 F2 7C FB B9 0D 03 30 1F 99 1E 5F FB 1A 35 F3 F0 93 18 10 DD 7B D5 F2 71 A4 DA FD D6 DC 51 DC F0 A9 02 20 FA 41 3F 31 F9 AF 13 D2 BE 6C 40 60 C2 18 82 67 4B 69 05 27 EB BA 85 B3 D4 73 16 C5 76 BB 77 E0 B9 5B 42 3A 12 9F 07 0B A0 5D 33 A7 E5 C8 12 02 D7 63 C4 E5 FF 45 1E F3 C7 D9 1E 9A E7 F5 53 2E 96 7D 8E F5 EC EE 05 F3 97 D5 51 7B C2 0D 20 A0 58 6C 51 22 EC F6 84 FA CB 71 01 CF 77 BB 76 FA F1 04 4E 72 0F 87 57 50 FA 00 31 BA F7 C6 1E A0 0F 28 D2 F8 FE 46 0E B8 D7 93 40 CE BE B6 43 6C 7E AE D4 33 E9 ED 1B 59 DC 75 93 2E AF 1A 8A 7A 0A 64 53 22 E0 EE C1 BE 45 90 FA 75 AF A6 6A EB B9 11 0B 91 CF 8C B4 98 A3 52 3A 31 03 7F 1B 0A 94 7A 62 3E E6 57 0F B4 85 70 84 8F A4 B7 0C 6D EC 4B 3F 7C D6 EE 01 59 4D D5 45 61 97 09 C3 78 5F E7 A5 DA E7 F6 C1 B9 C8 7E 17 DF 6B A7 7D AE FD 04 42 3E 03 CB 04 44 FD 04 35 BA EF 8A 1F 11 98 28 C2 F8 FE 49 19 FD D6 51 A4 36 B9 A9 43 66 FD 47 3E 3D F5 FB 57 55 50 96 5A 7C 87 5B 93 68 58 71 4C 26 AE FE 94 FA D4 69 10 C2 C6 7A 75 EB B7 6B 21 B0 E6 72 12 42 FB 52 26 BC F7 94 1F 43 D7 60 C0 F9 F0 41 5C E7 85 DA 4A C9 B9 A9 17 72 F9 54 6D 2F F3 E1 57 43 47 86 41 CD 4A 16 86 25 0A 61 E6 EA FA F5 94 A8 C9 75 19 96 76 B3 38 F8 F0 06 0B 3E 07 85 14 54 A3 52 35 A7 A3 94 B9 CA D7 7D D1 54 3A 56 19 A7 85 DF 41 DC F0 AC 0D 64 F5 4D 28 2F BC FE 02 59 1E 83 5A 7B 91 5B 84 7C 43 61 40 31 E1 F4 95 FA D1 75 11 C5 25 BE FA 0E 00 04 0C 26 14 28 DE 54 AF 16 25 F3 F5 25 D3 11 DD 7C C0 F5 FF 41 5C B1 C4 D1 5D DD B9 AB 17 68 F9 00 47 10 F9 AF 03 55 53 85 46 2E 87 08 97 29 49 6A 48 33 FA 59 48 F4 89 3E 41 96 F5 4D 8C 2B 93 6B 68 52 6C EB 77 31 8F 72 50 D3 83 E6 7A 63 B4 08 A1 97 93 24 7C DD A5 B3 24 AF D0 C5 63 00 9C 2E 4D 5C 9C 8F 77 33 3E F4 35 0E F2 3B E3 09 2A 05 25 43 8E 9A E1 DA A7 10 63 B7 05 D2 18 8A 99 90 9D 52 66 EB 77 31 8F 72 50 D3 83 E6 7A 63 B4 08 A1 9C 93 24 7C DD A5 B2 24 B7 C0 85 63 00 9C 2E 4D 5C 9C 8F 77 30 3E F5 35 1F E2 7B E3 09 2A 04 25 67 9E DA E1 DA A7 10 63 B6 05 D2 18 8E 99 61 62 44 66 EB 77 31 8F 83 AF ED 81 E6 7A 63 B4 08 A1 97 93 24 7C DD A5 B3 24 8B D0 C5 63 10 9C 2F 4D 5C 8C CF 77 30 3E F5 35 0E E2 7B E3 09 2A 05 25 5C 8E 9A E1 CA A7 11 63 B6 25 92 18 8E 99 61 62 52 66 EB 77 31 8F 72 50 F8 83 E6 7A 73 B4 09 A1 97 B3 64 7C DD A5 B3 24 AF D0 C5 63 00 9C 2E 4D 6E 9C 8F 77 20 3E F4 35 0E C2 3B E3 09 2A 05 25 43 8E 9A E1 DA A7 10 63 B6 76 BA 7D E2 F5 4F 03 21 0B EB 28 54 F7 1B 24 D3 E5 8A 1B 04 B4 6E CD F6 F4 0A 10 B8 CB B3 7B F0 B2 B6 10 5F EF 5A 2C 2E E8 8F 28 55 5A 94 41 6F E2 24 86 67 4E 05 25 6D FD E3 8C AE C6 72 63 98 76 A6 6A FA F8 03 62 7C 15 83 04 45 FD 06 31 B1 83 C8 0E 06 CC 7C A1 97 93 24 7C DD A5 B3 24 AF D0 C5 63 00 9C 2E 4D 5C 9C 8F 77 30 3E F5 35 0E E2 7B E3 09 2A 05 25 43 8E 9A E1 DA A7 10 63 B6 05 D2 18 8E 99 61 62 52 66 EB 77 31 8F 72 50 D3 83 E6 7A 63 B4 08 A1 8C 93 24 7C DC A5 B3 24 A9 D0 C5 63 00 9C 2E 4D 95 99 3C F4 25 AA F5 C0 85 D7 95 84 E7 A4 7A 2D 0B 3D 3E 28 7A 15 1A 83 99 C2 4D 95 88 01 38 78 4E 7E B9 03 8E 4F F2 C7 30 2E 8A 23 3E C0 AC 46 B8 67 F2 A2 A1 A5 F7 D5 40 BA A8 4C 1B 4F AB 9A 40 04 00 00")
output_bin_len = 1088
n = output_bin_len - 64

payload = output_bin[:n]
expected_hash = output_bin[n:n+64]

with open("names.txt", "r") as f:
    usernames = [line.strip() for line in f if line.strip()]

with open("langs.txt", "r") as f:
    langs = [line.strip()[:5] for line in f if line.strip()]

hostname = "pc-COMPTA"

for uname in usernames:
    for lang in langs:
        key_material = uname + hostname + lang
        key = hashlib.sha512(key_material.encode()).digest()

        decrypted = bytes([b ^ key[i % 64] for i, b in enumerate(payload)])
        digest = hashlib.sha512(decrypted).digest()

        if digest == expected_hash:
            print(f"USERNAME={uname}, HOSTNAME={hostname}, LANG={lang}")
            with open("shellcode.bin", "wb") as f:
                f.write(decrypted)
            exit(0) 
