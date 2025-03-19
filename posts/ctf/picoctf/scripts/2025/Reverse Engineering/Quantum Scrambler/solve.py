import ast

def unscramble(L):
    i = len(L)
    while i > 2:
        L[i - 1].pop()
        split_point = len(L[i - 2]) - len(L[i - 1]) 
        L.insert(i - 1, L[i - 2][split_point:])
        L[i - 2] = L[i - 2][:split_point]
        i -= 1
    return L

# hey don't mind my ass code
def get_hex(L):
    res = []
    for i in L:
        for j in i:
            if j:
                res.append(int(j,16)) 
        
    return res

enc = ast.literal_eval(open("output.txt").read())
orig = unscramble(enc)

flag = get_hex(orig)
print(bytes(flag)) 
