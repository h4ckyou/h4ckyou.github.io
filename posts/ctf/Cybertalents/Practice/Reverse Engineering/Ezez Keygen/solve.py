"""
It's a x64bits executable which is stripped

The program expects the serial and username from the user

It makes sure the user equals "4dminUser31337"

Then it calls the check() function passing the user and the serial as the arguemnt

The check function does some checks:
- Makes sure the user length is not greater than 30 and the serial length is not greater than 100
- The user length equals this: slen / 3 + slen % 3 (where slen is the serial length)
- Compares the generated value from calling the generate() function against the user

The generate function does this:
- Takes an argument which is the serial value
- Iterates through the length of the value while incrementing the iterate by 3
- Checks every last byte of each chunk of the serial value if it equals (- or +)
- If the value of the serial format equals (+) then it sets v2 to 1 else it sets v2 to 0
- The first two bytes of the serial chunk is then converted to an integer
- Then it computes the final value which is 2 multiplied by the converted chunk integer added with v2

HOW TO SOLVE?

First i'll get the list of length of key that could work for the user then i'll generate a fake serial key to work with

user = "4dminUser31337"
for i in range(100):
    op = i // 3 + i % 3
    if op == len(user):
        print(i)
    
The result was:
- 38
- 40
- 42

This means those are the possible length of the right serial key

To solve i just do the encryption in it's reverse operation!
"""

user = "4dminUser31337"
key = ""

for i in range(len(user)):
    cur = ord(user[i])
    fmt = ""
    # check if value is even because if it is then a1[i + 2] == '-' and v2 is equals 0 else 1
    if (cur % 2 == 0):
        fmt = "-"
    else:
        fmt = "+"
        cur -= 1 # 2 * strtol(nptr, 0LL, 16) + v2
    
    val = cur // 2
    key += hex(val)[2:] + fmt


print(key)
