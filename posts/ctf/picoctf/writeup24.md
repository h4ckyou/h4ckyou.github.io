<h3> PICOCTF '24 </h3>

#### Description: This was a fun ctf that took place from March 12 to March 26, 2024. I played with team *Fuji_*
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b697be8a-2adb-48f3-8260-1db8ddfd8e69)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/87b20483-b9c6-4cde-97b1-8abc8ee6cc32)


**I'll be giving writeup to challenges I solved**

<h3> Challenge Solved </h3>

## General Skills
- Super SSH
- Commitment Issues
- Time Machine
- Blame Game
- Collaborative Development
- Binhexa
- Binary Search
- Endianness
- Dont-you-love-banners
- SansAlpha

## Forensics
- Scan Surprise
- Verify
- CanYouSee
- Secret of the Polyglot
- Mob psycho
- Endianness-v2
- Blast from the past
- Dear Diary

## Reverse Engineering
- Packer
- FactCheck
- Classic Crackme 0x100
- WeirdSnake
- WinAntiDbg0x100
- WinAntiDbg0x200
- WinAntiDbg0x300

## Web 
- Elements

## Cryptography
- Interencdec
- Custom encryption
- C3
- Rsa Oracle

## Binary Exploitation
- Format String 0
- Heap 0
- Format String 1
- Heap 1
- Heap 2
- Heap 3
- Format  String 2
- Format String 3
- Babygame 03

### General Skills 10/10 :~

#### Super SSH
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6baf5964-a045-4fd8-9e09-b75809b7cf4f)


We are to ssh as `ctf-player` to `titan.picoctf.net` at port `50832` with password `84b12bae`

So I just did that and got the flag :)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1ac9aae8-c943-4332-a423-d36682b8cffc)

```
Flag: picoCTF{s3cur3_c0nn3ct10n_07a987ac}
```

#### Commitment Issues
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/15c45383-53ca-49c9-ab78-515cf046c0f0)

We are given a zip file and after unzipping it showed a git directory in the `./drop-in` directory
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6b7213b9-3563-4f2f-a95d-8d2494f69969)

Going over there shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/daa04493-61f4-4cfb-a987-cb4be2c8220d)

From the challenge description we know the message was already deleted 

So I checked the git logs
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/079a61dd-5fc9-4c26-a3ea-df65d1984750)

The commit `87b85d7dfb839b077678611280fa023d76e017b8` was responsible in the creation of the flag

I checked it and got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2fd81a96-e134-4e7b-9da6-da9c634e1af5)

```
Flag: picoCTF{s@n1t1z3_ea83ff2a}
```

#### Time Machine
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/18cb8d91-570c-47ca-bcad-029791f60309)

We are given a zip file and after unzipping it showed a git directory in the `./drop-in` directory (same as the previous challenge)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/34c90ea7-fc66-40ae-a05b-6644d6f5370b)

Going over there shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b8b9041-b081-4111-8aa2-2a4675589451)

I just did the same thing I did before :)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bb11fda3-97ac-4ffa-9b6f-ed2a4086eb95)

```
Flag: picoCTF{t1m3m@ch1n3_186cd7d7}
```

#### Blame Game
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e37948d1-ad2a-4780-b7ed-7b01748022cc)

Same as the previous ones
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ea6af638-e302-4ad5-be19-1a0f19fb40d1)

But this time around when I checked the git log it was much
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/26530660-0a32-4f24-8ad6-e94200a4ce2f)

I checked from the first commit and saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d908167e-e479-4715-910f-f7bb294ba50a)

The flag was in the author field

```
Flag: picoCTF{@sk_th3_1nt3rn_d2d29f22}
```

#### Collaborative Development
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6ad2886e-892a-4843-a1c1-a6c75d574318)

Same as the previous one again
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a1da72d6-f217-444d-9565-ca07db00de79)

In the git directory the python code there just prints out some word
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1393fa25-9396-41c4-9b77-b1dccd94adcf)

Checking the git log shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dbf779c1-a5d1-4836-ab83-c007f5970bdd)

So the flag isn't there

On noticing that we are in the main branch I decided to see if there are other branch

Checking it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/66b80390-a9e0-4837-919a-46e17581dd8e)

I switched to `feature/part-1`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d656d670-7496-49d1-82bd-727e1b0adb58)

We can see that it had one portion of the flag

I repeated this process for the two branches left 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c08003f0-b407-40a0-9537-684d60079cc0)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/24a2e941-7838-463b-bc18-1910fe66868a)

With that I just concatenated the 3 portions of the flag to form the full flag

```
Flag: picoCTF{t3@mw0rk_m@k3s_th3_dr3@m_w0rk_2c91ca76}
```

#### Binhexa
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0e81658e-00fe-4162-9abd-708b58bf8886)

We are given a remote instance to connect to

After connecting to it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/54fc7ff3-c16e-4e04-a06a-ed534ef40920)

So we'll be given two binary numbers and we are to perform various operations on it 6 times

Also the operations to be performed changes
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a98a80d9-05c9-4b99-b22d-4ed236005f8c)

Tbh during this ctf I solved this manually since the number of times we get question are just 6

I can't redo it here cause it's stressfull and i'm too lazy to write a script now :(

But the process was that i received the two binary string convert them to integer with python `int(binary, 2)` then perform the operation expected and send the result as a binary string

With that on the 6th trial I got the flag

```
Flag:
```

#### Binary Search
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/05190373-3744-42e8-9bc6-09b867672a86)

Reading the description we know that we need to guess a number with 1000 possibilities and we have just 10 trials

The challenge already hinted to use an Algorithm called Binary Search

We are given an attachment to download and on downloading it we see this bash script
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/643f4d6d-5ef7-4b9b-ad30-e44b1e7c9c78)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ad544fe1-e9dc-4a23-91b7-8cdc6926f8ce)


```sh
#!/bin/bash

# Generate a random number between 1 and 1000
target=$(( (RANDOM % 1000) + 1 ))

echo "Welcome to the Binary Search Game!"
echo "I'm thinking of a number between 1 and 1000."

# Trap signals to prevent exiting
trap 'echo "Exiting is not allowed."' INT
trap '' SIGQUIT
trap '' SIGTSTP

# Limit the player to 10 guesses
MAX_GUESSES=10
guess_count=0

while (( guess_count < MAX_GUESSES )); do
    read -p "Enter your guess: " guess

    if ! [[ "$guess" =~ ^[0-9]+$ ]]; then
        echo "Please enter a valid number."
        continue
    fi

    (( guess_count++ ))

    if (( guess < target )); then
        echo "Higher! Try again."
    elif (( guess > target )); then
        echo "Lower! Try again."
    else
        echo "Congratulations! You guessed the correct number: $target"

        # Retrieve the flag from the metadata file
        flag=$(cat /challenge/metadata.json | jq -r '.flag')
        echo "Here's your flag: $flag"
        exit 0  # Exit with success code
    fi
done

# Player has exceeded maximum guesses
echo "Sorry, you've exceeded the maximum number of guesses."
exit 1  # Exit with error code to close the connection
```

So let's go over what it does:
- It generates a number between 1-1000
- It initilizes our maximum guess and guess counter to 10 and 0 respectively
- In a while loop where the condition checks if the guess counter is less than and equal to the maximum guess:
  - It reads in our input and checks if it's an integer using regex
  - Increments the guess counter by 1
  - If our guess is equal to the random generated number we get the flag
  - If our guess is less than the random generated number we get an error telling us that the target number is higher than our input
  - If our guess is greater than the random generated number we get an error telling us that the target number is lower than our input
- Once the while loop meets the condition it exits

Now that we are aware of what it does exactly we need to figure a way to guess the target value under the limited search sapce

To do that I implemented an algorithm called [Binary Search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

It's basically an algorithm used to find the position of a value in a sorted array and it's time complexity is `O(log n)`

To test my solution I ran it locally

Here's the edited script

```bash
#!/bin/bash

# Generate a random number between 1 and 1000
target=689

echo "Welcome to the Binary Search Game!"
echo "I'm thinking of a number between 1 and 1000."

# Limit the player to 10 guesses
MAX_GUESSES=10
guess_count=0

while (( guess_count < MAX_GUESSES )); do
    read -p "Enter your guess: " guess

    if ! [[ "$guess" =~ ^[0-9]+$ ]]; then
        echo "Please enter a valid number."
        continue
    fi

    (( guess_count++ ))

    if (( guess < target )); then
        echo "Higher! Try again."
    elif (( guess > target )); then
        echo "Lower! Try again."
    else
        echo "Congratulations! You guessed the correct number: $target"

        # Retrieve the flag from the metadata file
        flag="fake_flag_for_testing"
        #flag=$(cat /challenge/metadata.json | jq -r '.flag')
        echo "Here's your flag: $flag"
        exit 0  # Exit with success code
    fi
done

# Player has exceeded maximum guesses
echo "Sorry, you've exceeded the maximum number of guesses."
exit 1  # Exit with error code to close the connection
```

And my solve script

```python
from pwn import *

context.log_level = 'debug'

io = process("./guessing_game.sh")

io.recvline()

def binarySearch(N):
    left, right = 0, N

    io.recvline()

    while left <= right:
        middle = left + (right - left) // 2

        io.sendline(str(middle))
        
        recv = io.recvline().decode().split()[0]

        if recv == "Lower!":
            right = middle - 1

        elif recv == "Higher!":
            left = middle + 1

        else:
            recv = io.recvline()
            return recv.decode()


N = 1000

binarySearch(N)

io.interactive()
```

Running it works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e927bc5f-1d02-4eaa-8c63-6c4be4cbd142)

Now I need to do the same remotely

But pwntools was always hanging
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cf278520-7784-486c-a0c2-300260f2caca)

Because the number of guesses we can make is just 10 I decided to do it manually 😢
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6e2e77e3-5e1d-49a6-9fcd-b825333a9ff8)

We see that the target value is lower than our input, so we set the new right pointer to `middle - 1` and update the new middle value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cf2d4aa8-b8fe-4632-b365-b9c86db90f4a)

Now it's higher so we set the left pointer to `middle + 1` and update the new middle value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9fc56703-cdb7-45b1-8627-ad0f7fe7a112)

Lower so we set the right pointer to `middle - 1` and update the new middle value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cafb7ca9-93dd-449c-a8b1-34b45b44b70d)

Hopefully you get the point...following the algorithm eventually made me get the right value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b16ca357-fa12-4bf7-a331-b0f50e8e742c)

```
Flag: picoCTF{g00d_gu355_6dcfb67c}
```

#### Endianness
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6664aaad-85e2-4e15-ba32-33154d51acfa)

We are given a download file and after downloading it I saw it's a C program
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f6490b6d-cd3d-4411-af59-166798b5d266)

The code is pretty much but the basic idea about it is that we will be given a word and we need to submit the little and big endian representation of the word

What is Endian? Endian refers to the order in which bytes are stored for multi-byte data types such as integers or floating-point numbers. There are two primary ways to represent these values in memory:
- Little Endian: The least significant byte (LSB) is stored at the lowest memory address, with the remaining bytes stored in increasing order of significance.
- Big Endian: The most significant byte (MSB) is stored at the lowest memory address, with the remaining bytes stored in decreasing order of significance.



















































### Web 10/10 :~

#### Elements
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8fa4cc9a-f87f-4b71-bb7e-f6f6d52c64c5)

I actually wasn't the one who solved this but I helped in writing the solve script since our solution takes time before exfiltrating the flag

You can read up on how to solve it here: [solution]()





















