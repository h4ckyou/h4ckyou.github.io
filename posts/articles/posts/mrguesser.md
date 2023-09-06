<h3> Mr Guesser </h3>

This was a challenge I created for my friend to try out

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e7a29534-d2e2-42df-ab09-de56415895eb)

I provided the server source code:

```python
#!/usr/bin/python3
from random import randint

flag = b"IDAN{[REDACTED]}"
guess = randint(1, 500_000_000_000)
print("Enter the secret number to gain the treasure: ")
counter = 0
try:       
    while counter < 40:
        inp = int(input("Secret Number: "))
        if inp == guess:
            print(f"Weldone you guessed my secret \n Have your flag: {flag}")
            break
        elif inp > guess:
            print("Lower")
        else: 
            print("Higher")       
        counter += 1
        print(f"You have {40 - counter} chances left")
except Exception as e:
    print(f"Got '{e}'. \nPlease enter a valid number.")
```

The idea is that you need to guess a random number generated within the range of 1 to 500,000,000,000

And we have just 40 chances i.e the amount of guess we can make

If our input number is greater than the random number the server tells us "Lower" else if our input number is lower the server tells us "Higher"

We can approach brute force if we have unlimited amount of trials or if the number generated will likely return a smaller number within the range of our guess

Of cause we can't know that because each time we connect to the server the number is randomly generated

And approaching brute force won't work but if there is a chance that the number generated would be within the range of our guess iimit then we can maybe try brute force?

Anyways that's not an efficient way to solving this because brute forcing this high dataset would take a lot of time even if we had unlimited guess

So let's apply an Algorithm here

From the challenge description we can tell this is some sort of Algorithm question and `yes` I made it cause I'm learning DSA so just to test what I know I made the chall 🙂

The best algorithm to use here is Binary Search Algorithm

Incase you don't know what that is I made a note when learning it.

You can check it out [here](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/programming/Learning/Data%20Structures%20and%20Algorithm/Binary%20Search%20Algorithm.md)

I won't explain what the algorithm does cause I did already in the above link

So here's my solve script

```python
from pwn import *
context.log_level = 'info'
from warnings import filterwarnings
filterwarnings("ignore")

host, port = "0.tcp.eu.ngrok.io", 19972

io = remote(host, port)

def binarySearch(N):
    left, right = 0, N

    for i in range(30):
        try:
            while left <= right:
                middle = left + (right - left) // 2

                io.recvuntil("Secret Number:")
                io.sendline(str(middle))
                recv = io.recvline().decode().strip()

                if recv == "Lower":
                    right = middle - 1

                elif recv == "Higher":
                    left = middle + 1

                else:
                    recv = io.recvline()
                    return recv.decode()
        except Exception as e:
            return "Error"

N = 500_000_000_000

result = binarySearch(N)
print(result)
```

After running the script I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dd61587e-5279-4291-af1a-9e83b8216e33)

It took just `16.032` seconds
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/61a97445-ebbb-405f-aafe-f9eb1b5f79b2)

Imagining brute forcing how long it would take??

Anyways that's all for today!

Btw the person who I gave to solve this solved it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee147702-71db-4fcb-a701-b8eb7d8f60f0)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cfc68b53-467a-4d08-9636-58d4021ee590)
