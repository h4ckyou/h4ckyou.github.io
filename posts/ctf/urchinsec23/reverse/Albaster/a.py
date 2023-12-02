# int __fastcall b(int a1)
# {
#   return putchar(10 * (a1 / 10 % 10) + a1 % 10);
# }


def b(num):
    a = (num % 10 + ((num // 10) % 10) * 10);
    return a

# def brute(i):
#     var = []
    
#     while i > 0:
#         incase = i
        # var.append(b(int(i) + int(i / 100) * -100))
#         i = i // 100

#         if chr(var[0]) == 'u' and chr(var[1]) == 'r':
#             print(f'Found: [{incase}]')
#             break

#         print(''.join(chr(i) for i in var))
    
# for i in range(7448979809417343555, 9999999999999999999):
#     brute(i)

var = []
i = 0x989FE854689F4DBD

while i > 0:
    var.append(b(int(i) + int(i / 100) * -100))
    i = i // 100

sus = [61, 80, 20, 92, 42, 26, 64, 77, 99, 10]
print(''.join(chr(i) for i in sus))

# import string

# charset = string.ascii_letters

# for char in charset:
#     eqn = ord(char) % 10 + ((ord(char) // 10) % 10) * 10
#     print(eqn)
