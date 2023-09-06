<h3> Mr Guesser </h3>

This was a challenge I created for my friends to try out

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

