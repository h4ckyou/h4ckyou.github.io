# rc4.py

def _rc4(key, data):
    output = []
    # initial permutation matrix
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i%len(key)])%256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp

    # prga
    for c in range(len(data)):
        i = (i+1)%256
        j = (j+S[i])%256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp
        K = S[(S[i] + S[j])%256]

        output.append((K ^ data[c]) + 0x01)
    return output

def rc4(key, data):
    #print(data)
    k = [ ord(i) for i in key ]
    d = [ i for i in data ]
    ret =  _rc4(k, d)
    return bytes(ret)


def main():

    print("Enter a file to encrypt: ")
    filename = input("fname> ").split()[0].strip()

    print("Give me a key: ")
    key = input("key> ").split()[0].strip()

    with open(filename, "rb") as f:
        out = rc4(key, f.read())

    fnameenc = f"{filename}.rc4"
    with open(fnameenc, "wb") as f:
        f.write(out)

    print(f"Generated file {fnameenc}")

if __name__ == "__main__":
    main()
