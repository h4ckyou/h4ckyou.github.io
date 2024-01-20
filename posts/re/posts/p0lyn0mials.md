<h3> Reverse Engineering </h3>

### Chall
    - CTF: Attack CTF
    - Name: S0Lving_p0lyn0mials_OR_bRuteF0rcing

We're given a python file 
![image](https://user-images.githubusercontent.com/113513376/222312353-4416326d-6715-4dff-9302-535f36df72f4.png)

```
def my_function(x):
    return pow(x,3)+10*pow(x,2)+x*7 + 6

plaintext = "AtHackCTF{}"

cipher = []
for i in plaintext : 
   cipher.append(my_function(ord(i)))
print("cipher = " ,cipher)
```

Looking at the code we can tell what it does:

```
1. Creates a function which does a mathematical calculation
2. Stores the value `AtHackCTF{}` in variable plaintext
3. Then it loops through each character of plaintext 
4. It then calls the math function using the numerical value of the looped character as an argument
```

Running it creates an array of the encrypted value
![image](https://user-images.githubusercontent.com/113513376/222312807-c9e06fcb-2fd7-46c0-902a-bf86e3bc7cd3.png)

We're given the flag but in its encrypted form
![image](https://user-images.githubusercontent.com/113513376/222312923-ed981882-e643-442a-96b0-b4bfbdf8526a.png)

So with this the idea is to reverse it

And how it can be done is by looping through the numerical value of range about 300 then check if the cipher is equal to the value of the math function calculated

If it is then it should print the number and get its corresponding ascii value

Doing it manually isn't fun so i'll write a script to do that for me
![image](https://user-images.githubusercontent.com/113513376/222314523-4d11d9e0-95ac-4d6c-91c7-0f20dc679722.png)

```
def solve(cipher):
    for i in range(300):
        if (cipher == pow(i,3)+10*pow(i,2)+i*7 + 6):
            return chr(i)

cipher = [317336, 1696274, 425598, 1007448, 1069008, 1340288, 346128, 663858, 392496, 2013024, 734808,
 1233758, 1268616, 1069008, 1233758, 948296, 142008, 1653936, 948296, 516368, 133974, 1612308, 1133024, 
 948296, 392496, 1739328, 1452776, 948296, 641264, 133974, 497274, 1783104, 1268616, 1452776, 1199544,
 948296, 1531158, 133974, 1377114, 1918824, 1452776, 133974, 1414608, 1268616, 1007448, 1377114, 1653936,
 948296, 556008, 619188, 948296, 1037924, 619188, 1739328, 1696274, 1133024, 392496, 133974, 1612308, 1069008, 
 1268616, 1452776, 1199544, 290184, 47064, 2110256]

flag = []

for num in cipher:
    decode = solve(num)
    flag.append(decode)

print("".join(flag))
```

Running it gives the flag
![image](https://user-images.githubusercontent.com/113513376/222314631-deb142f4-e5a7-4769-8875-683198c8f207.png)


