<h3> PICOCTF '24 </h3>

#### I participated in picoCTF 2024 organized by Carnegie Mellon University with team Fuji_, which took place between March 12, 2024 to March 26, 2024. It was a great solving the challenges and I learnt something new!
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
- Mob psycho
- Endianness-v2

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
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2132d3ae-f386-4e9f-a2b5-8b477ab3e875)


We are to ssh as `ctf-player` to `titan.picoctf.net` at port `50832` with password `84b12bae`

So I just did that and got the flag :)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1ac9aae8-c943-4332-a423-d36682b8cffc)

```
Flag: picoCTF{s3cur3_c0nn3ct10n_07a987ac}
```

#### Commitment Issues
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e0011168-abf8-4f80-b76b-16d0b2a2d8b8)

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
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f95819b9-1da6-49d7-8778-126b3630ab58)

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
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/71de47c9-4c08-4bb2-a1f2-e080abc57022)

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

And my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/General/Binary%20Search/local.py)

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

With that said I wrote a solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/General/Endianness/solve.py)

Here's my solution

```python
from pwn import *

io = remote("titan.picoctf.net", "63041")

io.recvuntil(b"Word: ")
word = io.recvline().strip()

little = [hex(i)[2:] for i in word[::-1]]
little_end = ''.join(little)

big = [hex(i)[2:] for i in word]
big_end = ''.join(big)

io.sendline(little_end.encode())
io.sendline(big_end.encode())

io.recvuntil(b"is: ")
flag = io.recvline()

info(flag)
io.close()
```

#### Dont-you-love-banners
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3474eadd-0527-4b35-82f4-dad9fdf88f2d)

We are given a remote instance to connect to

On doing that I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/668bef9b-2698-4753-a236-217b38764185)

I was confused at this point cause I have no idea what the password is and after trying silly guesses with no luck I decided to brute force

I wrote a script to achieve that this is it here: [brute](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/General/Don't%20You%20Love%20Banners/brute.py)

After running the script I got the password to be `My_Passw@rd_@1234`

Using that worked!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3c4ad114-88eb-4114-a735-9fbf2b4d988a)

After it worked we got 2 questions which was easily solved once you search it up and then finally we spawn into a bash shell

Looking through the file system I couldn't find the flag so I decided to escalate privilege

From doing some manual checks I found out that the `/etc/shadow` file is readable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/54b26647-2c58-477c-b431-c261223a3b87)

We got the root hash which was crackable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/79c6e40c-3123-4086-a4c8-847797fe5d85)

At this point I just switched to user `root` with password `iloveyou`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee6e7917-0936-4f24-b197-990be0455abe)

The flag was in the root directory

```
Flag: picoCTF{b4nn3r_gr4bb1n9_su((3sfu11y_ed6f9c71}
```

#### SansAlpha
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/518276e3-edb0-4663-b610-c70a22fc9c0f)

Connecting to the ssh instance I landed in a restricted shell
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/90b28b82-425b-4cf1-8415-07f83462fbdc)

I can't seem to use some certain words....that's what I thought at first

But after some trial I figured we can't use any characters except some certain symbols and digits

After spending some hours on this I decided to do some research and found this awesome video of LiveOverflow solving a similar challenge [here](https://www.youtube.com/watch?v=6D1LnMj0Yt0)

From that I found out that we can access files using `?` which represents like a wildcard in bash

First I need to know the path to the flag

I used an asterisk `*` on the current path and it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04fc7945-7f08-4e4b-bed1-b3cea7aab2b8)

And using an asterisk on that path showed that the flag is there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d944e0d8-3bf3-4055-8472-a73725e48dbb)

After some while my teammate was able to encode the flag using `base32` 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/65cacb37-a124-4851-bc54-8ad1b5587be4)

Doing that gives the encoded flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b80c1fb-21df-4f67-abe8-42965128c303)

```
/???/???/????32  ~/??????/????.???
```

On decoding the value we got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7e34440b-f0a6-4b53-853b-a3c325a82f63)


```
Flag: picoCTF{7h15_mu171v3r53_15_m4dn355_640b6add}
```

### Forensics 2/7 :~

#### Mob psycho
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/857c8e51-e972-438d-8e11-64624d03ecec)

For this category I really didn't do much just two challenges my team mate solved the other challs there

In this challenge we are given an apk file

After downloading it I just unzipped it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/10742098-4325-474c-b20d-6b34c78ed585)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1de7cc96-5043-4eb1-812e-e3adf2585029)

I tried low hanging fruit things in this case search for a `*.txt` file to see if we can get the flag

Doing that indeed works but the flag was hex encoded which i just decoded
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c2c3a0f-3515-427e-8cfa-c174ebb8c1c4)

```
Flag: picoCTF{ax8mC0RU6ve_NX85l4ax8mCl_5e67ea5e}
```

#### Endianness-v2
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a149261-c72c-405c-81a0-6289bdedb459)

After downloading the file I saw the data is not recognizable by the `file` command
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/02b89b05-578b-4976-864e-0c0b680d4b35)

I uploaded it to cyberchef inorder to view it's hex dump
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/dae95e4b-dde2-40ad-b9d7-bd993c41b9de)

From looking at the first line from the hex dump result I noticed something peculiar

```
00000000  e0 ff d8 ff 46 4a 10 00 01 00 46 49 01 00 00 01  |àÿØÿFJ....FI....|
```

The file seems to a jpeg file but in this case the bytes are flipped 

Here's what I mean

Taking a look at the signature of a valid jpeg file shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04aaa89a-fda9-4973-8303-1901bcb3171f)

```
FF D8 FF E0 00 10 4A 46 49 46 00 01
```

From this we can tell that for every 4 chunks it will basically flip it so that it's in is reverse order

At this point of figuring that I wrote a [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Forensics/Endianess-V2/solve.py) to do the opposite

```python

def swap_chunks(data):
    chunks = []
    swapped_data = ""

    for i in range(0, len(data), 4):
        chunks.append(data[i:i+4])

    lt_idx = chunks[-1]
    chunks = chunks[:-1]
    swapped = b""

    for i in range(len(chunks)):
        swapped += chunks[i][::-1]
            

    return swapped

def main():
    input_file = 'challengefile'
    output_file = 'dump'

    with open(input_file, 'rb') as f:
        file_data = f.read()

    swapped_data = swap_chunks(file_data)


    with open(output_file, 'wb') as f:
        f.write(swapped_data)


if __name__ == "__main__":
    main()
```

Running that script gives a file and on checking the file type shows it's indeed a jpeg file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0e022e03-d569-44c0-929d-5e3e824f6028)

On viewing it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5d7b0f84-b479-4b45-b32d-6b37b583127f)

```
Flag: picoCTF{cert!f1Ed_iNd!4n_s0rrY_3nDian_f72c4bf7}
```











### Reverse Engineering 7/7 :~

#### Packer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6196986d-1c15-4713-85d0-4e2dd763b4f2)

Downloading the binary attached and checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5f04bf33-aea8-4ed6-bcbe-eb0564b5f144)

We see that it's packed with UPX so i just unpacked it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/86aed00a-ab0b-4778-904d-242d5cbeab9d)

Running it shows that it expects a password
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3332d339-bf2d-4648-9a28-88b2ee23e35d)

Since I don't know the password I decided to perform static reversing on the binary to see what it does

Loading it up in Ghidra and decompiling it takes few minutes because the binary is statically linked

But eventually after it does it's thing the main function shows up
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c3e04867-bfbc-4f59-a532-3817bef0ccd4)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d065c119-8925-4049-bb71-5923f4618434)

I didn't bother reading it cause I noticed that it eventually gives the flag which is encoded in hex

```c
puts("Password correct, please see flag: 7069636f4354467b5539585f556e5034636b314e365f42316e34526933535f31613561336633397d")
```

Decoding that hex value gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b136daec-a144-4acb-83a3-684980047209)

```
Flag: picoCTF{U9X_UnP4ck1N6_B1n4Ri3S_1a5a3f39}
```

#### FactCheck
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a03c31cf-3371-437f-882e-bdf89eaa0aeb)

After downloading the binary I checked the file type
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/215ecef2-f4ea-4e1c-a940-3e06d68880f7)

Nothing special there except we're dealing with a 64bits binary which is dynamically linked and not stripped

I ran it to get an overview of what it does but it just exits
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/001a8d42-300f-49ea-9029-a71f92b6e20d)

I used Ghidra to load the binary but then I saw it's a C++ compiled binary then I immediately switched to IDA because it looks really ugly on Ghidra 🥲

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3da09a25-cbd6-4a5d-857b-4f739767b013)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/55175786-0973-496a-b9da-c0524a175745)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/389dba4e-122d-42ec-9083-5403ffcf54af)

So we see some portion of the flag is being stored in memory

I just assummed that it builds up the flag in memory thus I switched to Dynamic Reversing

Loading it up and gdb and disassembling the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5e499d38-daff-4ce9-88ea-a7df357e5dc7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bf3950ae-e3ef-44ae-acfa-d45e992df5e0)

Now I just set a breakpoint right before it calls `ret`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ea11d61-5681-4fe2-85da-3025857f92bd)

Starting the process hits the breakpoint
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3bd2b77e-9077-47e9-a82e-580c83a39009)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a583f5f2-79c5-42da-b9b8-aca0e463c286)

Now I just search for occurrence of `pico & mate` in memory
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9784d445-dcbd-46b7-a794-73ddafa44f13)

With that I got the flag

```
Flag: picoCTF{wELF_d0N3_mate_7d29a538}
```

#### Classic Crackme 0x100
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8a2904f9-ee82-451e-87d1-82d76b620328)

We are given a binary and a remote instance to connect to

Checking the file type of the binary shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/63c10565-ca43-4c1a-a267-c5647cf013ce)

So the same as usual but this type we have debug_info present 

Running the binary to get an overview of what it does shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fab6d7e8-815e-4d93-bc23-49c82984f5d8)

Looks like time we need to get the password 

Loading it up in IDA to decompile it shows this as the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2db4c893-01a7-4472-bc22-b40e9050ed3d)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char input[51]; // [rsp+0h] [rbp-A0h] BYREF
  char output[51]; // [rsp+40h] [rbp-60h] BYREF
  int random2; // [rsp+7Ch] [rbp-24h]
  int random1; // [rsp+80h] [rbp-20h]
  char fix; // [rsp+87h] [rbp-19h]
  int secret3; // [rsp+88h] [rbp-18h]
  int secret2; // [rsp+8Ch] [rbp-14h]
  int secret1; // [rsp+90h] [rbp-10h]
  int len; // [rsp+94h] [rbp-Ch]
  int i_0; // [rsp+98h] [rbp-8h]
  int i; // [rsp+9Ch] [rbp-4h]

  strcpy(output, "lxpyrvmgduiprervmoqkvfqrblqpvqueeuzmpqgycirxthsjaw");
  setvbuf(_bss_start, 0LL, 2, 0LL);
  printf("Enter the secret password: ");
  __isoc99_scanf("%50s", input);
  i = 0;
  len = strlen(output);
  secret1 = 85;
  secret2 = 51;
  secret3 = 15;
  fix = 97;
  while ( i <= 2 )
  {
    for ( i_0 = 0; i_0 < len; ++i_0 )
    {
      random1 = (secret1 & (i_0 % 255)) + (secret1 & ((i_0 % 255) >> 1));
      random2 = (random1 & secret2) + (secret2 & (random1 >> 2));
      input[i_0] = ((random2 & secret3) + input[i_0] - fix + (secret3 & (random2 >> 4))) % 26 + fix;
    }
    ++i;
  }
  if ( !memcmp(input, output, len) )
    printf("SUCCESS! Here is your flag: %s\n", "picoCTF{sample_flag}");
  else
    puts("FAILED!");
  return 0;
}
```

Looking at this we see that our input is going to pass through some sort of encryption scheme which is then eventually compared to the string stored in `output`

We can possibly brute force each character of the expected input since the encryption is deterministic 

But the way I solved this was by using an SMT solver called Z3

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Reverse%20Engineering/Classic%20Crackme%200x100/solve.py)

```python
from z3 import *

output = "mpknnphjngbhgzydttvkahppevhkmpwgdzxsykkokriepfnrdm"
secret1 = 85
secret2 = 51
secret3 = 15
fix = 97
i = 0

s = Solver()

arr = [BitVec(f'f_{i}', 8) for i in range(len(output))]
tmp = [BitVec(f'f_{i}', 8) for i in range(len(output))]

for v in arr:
    s.add(v > 0x60)
    s.add(v < 0x7f)
          
while i < 3:
    for j in range(len(output)):
        random1 = ((secret1 & (j % 255)) + (secret1 & ((j % 255) >> 1))) 
        random2 = ((random1 & secret2) + (secret2 & (random1 >> 2))) 
        val = (((random2 & secret3) + arr[j] - fix + (secret3 & (random2 >> 4))) % 26 + fix) 
        arr[j] = val

    i += 1

for j in range(len(output)):
    s.add(arr[j] == ord(output[j]))

if s.check() == sat:
    m = s.model()
    inp = ""

    for i in tmp:
        inp += chr(m[i].as_long())
    
    print(inp)
```

One thing to note there is that the constraint I used which let's z3 know the range of value which our input should be is within ascii lowercase letters plus some special characters

Running that generates the a string
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6c315e90-c5d3-4c1e-890f-10b20dcd852f)

We can test it locally
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/88cf8ac1-f897-4f6e-aa3e-1100c607153c)

On the remote instance we can connect to it and send that generated string as the password to get the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d5c4562d-65ae-446d-ab90-7ca23badfea8)

```
Flag: picoCTF{s0lv3_angry_symb0ls_ddcc130f}
```

#### WeirdSnake
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/937f1ffd-3abc-4ce3-b026-f10d9bdd22db)

After downloading the attached file and checking it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a2659bdf-69da-4844-a7ba-1364650d710e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7617084c-10d9-44e2-bc24-85c96af0ba7e)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cc0963aa-8c19-4e68-9030-43d860bb97df)

This is a python bytecode 

Since I wasn't familiar with it I looked at the hint and saw they gave a python library
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9a271787-f9da-4113-aec4-ba451c62da5e)

After I checked it out I saw it's a Disassembler for Python bytecode

From reading the documentation I saw various types of bytecode instructions: [here](https://docs.python.org/3/library/dis.html#python-bytecode-instructions)

I also played with it to see how it works here's an example
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9ef59d5b-e131-4241-ba44-8c12e45ac461)

After I've tried disassembling some various operations I decided to start with reversing the bytecode

First it stores some values into an array called `input_list`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6f8d7c57-52ad-4b0c-bca0-2de674555fcf)

Note that the instruction `LOAD_CONST` pushes the value to the stack, and `STORE_NAME` implements `STACK.pop()` which basically moves the value on the stack to the variable we specified

Next it generates a string which is stored in variable `key_str` with value `J_o3t`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c3a0b80c-48e1-4022-baf9-6a0eb56a9899)

At this point I spent some time trying to understand this:

```
  9         120 LOAD_CONST              36 (<code object <listcomp> at 0x7f704e8a4d40, file "snake.py", line 9>)
            122 LOAD_CONST              37 ('<listcomp>')
            124 MAKE_FUNCTION            0
            126 LOAD_NAME                1 (key_str)
            128 GET_ITER
            130 CALL_FUNCTION            1
            132 STORE_NAME               2 (key_list)

 11     >>  134 LOAD_NAME                3 (len)
            136 LOAD_NAME                2 (key_list)
            138 CALL_FUNCTION            1
            140 LOAD_NAME                3 (len)
            142 LOAD_NAME                0 (input_list)
            144 CALL_FUNCTION            1
            146 COMPARE_OP               0 (<)
            148 POP_JUMP_IF_FALSE      162

 12         150 LOAD_NAME                2 (key_list)
            152 LOAD_METHOD              4 (extend)
            154 LOAD_NAME                2 (key_list)
            156 CALL_METHOD              1
            158 POP_TOP
            160 JUMP_ABSOLUTE          134

Disassembly of <code object <listcomp> at 0x7f704e8a4d40, file "snake.py", line 9>:
  9           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                12 (to 18)
              6 STORE_FAST               1 (char)
              8 LOAD_GLOBAL              0 (ord)
             10 LOAD_FAST                1 (char)
             12 CALL_FUNCTION            1
             14 LIST_APPEND              2
             16 JUMP_ABSOLUTE            4
        >>   18 RETURN_VALUE
```

But basically it will iterate over each character in `key_str` and store it's integer representation to a list `key_list` by using a list comprehension

```python
key_list = [ord(i) for i in key_str]
```

Next it extends the `key_list` till the length is equal that of the `input_list`

```python
while len(key_list) < len(input_list):
    key_list.extends(key_list)
```

The next part is this

```
 15     >>  162 LOAD_CONST              38 (<code object <listcomp> at 0x7f704e8a4df0, file "snake.py", line 15>)
            164 LOAD_CONST              37 ('<listcomp>')
            166 MAKE_FUNCTION            0
            168 LOAD_NAME                5 (zip)
            170 LOAD_NAME                0 (input_list)
            172 LOAD_NAME                2 (key_list)
            174 CALL_FUNCTION            2
            176 GET_ITER
            178 CALL_FUNCTION            1
            180 STORE_NAME               6 (result)

 18         182 LOAD_CONST              39 ('')
            184 LOAD_METHOD              7 (join)
            186 LOAD_NAME                8 (map)
            188 LOAD_NAME                9 (chr)
            190 LOAD_NAME                6 (result)
            192 CALL_FUNCTION            2
            194 CALL_METHOD              1
            196 STORE_NAME              10 (result_text)
            198 LOAD_CONST              40 (None)
            200 RETURN_VALUE

Disassembly of <code object <listcomp> at 0x7f704e8a4df0, file "snake.py", line 15>:
 15           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                16 (to 22)
              6 UNPACK_SEQUENCE          2
              8 STORE_FAST               1 (a)
             10 STORE_FAST               2 (b)
             12 LOAD_FAST                1 (a)
             14 LOAD_FAST                2 (b)
             16 BINARY_XOR
             18 LIST_APPEND              2
             20 JUMP_ABSOLUTE            4
        >>   22 RETURN_VALUE

```

This is equivalent to doing

```python
result = [a ^ b for a, b in zip(input_list, key_list)]

result_text = ''.join(map(chr, result))
```

At this point we can get tell what this bytecode does is to decrypt the input_list using xor with the key as the key_str

I decided to just reimplement that but then I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/00e00bea-f6bc-4532-93f8-bbc560b1d531)

```python
input_list = [4, 54, 41, 0, 112, 32, 25, 49, 33, 3, 0, 0, 57, 32, 108, 23, 48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 106, 123, 89, 87, 18, 62, 47, 10, 78]
key_str = "J_o3t"

r = ''

for i in range(len(input_list)):
    xr = ord(key_str[i % len(key_str)]) ^ input_list[i]
    r += chr(xr)

print(r)
```

That doesn't work? 

Luckily because xor is reversible I decided to retrieve the key since we know the plaintext should start with `picoCTF` and we've got the ciphertext
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bc278b21-3a0e-4875-8a88-2ff60dce8e4d)

Cool the key should be `t_Jo3`

Using that worked....here's the solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Reverse%20Engineering/Weird%20Snake/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0cf883d8-2a62-408c-adee-305a4e9a263a)

```
Flag: picoCTF{N0t_sO_coNfus1ng_sn@ke_516dfaee}
```

#### WinAntiDbg0x100

This series of Windows Antidebug Challenges are not currently in picogym

But since I do have the files saved I'll go on ahead with the solution

I'll only be writing about WinAntiDbg0x100-0x200 I wasn't able to run the 3rd one on my host due to some DLL file missing so my teammate did that instead

For the first one we are given this set of files
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ea6db12-3fdd-4968-b1a6-2f924f856b00)

If we try to run it we get an error saying it needs to be run in a debugger
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/86693466-90f1-4181-b7c0-7195ebb7b53e)

Loading it up in IDA we can generate the pseudocode 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7d570d8-5f0e-4297-9a12-ba1e79a9a606)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a22baf4f-4150-4e18-8106-8b45b33742d8)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char Block; // [esp+0h] [ebp-8h]
  char Blocka; // [esp+0h] [ebp-8h]
  WCHAR *lpOutputString; // [esp+4h] [ebp-4h]

  if ( (unsigned __int8)sub_401130() )
  {
    OutputDebugStringW("\n");
    OutputDebugStringW("\n");
    sub_4011B0();
    if ( sub_401200() )
    {
      OutputDebugStringW(
        L"### Level 1: Why did the clever programmer become a gardener? Because they discovered their talent for growing a"
         " 'patch' of roses!\n");
      sub_401440(7);
      if ( IsDebuggerPresent() )
      {
        OutputDebugStringW(L"### Oops! The debugger was detected. Try to bypass this check to get the flag!\n");
      }
      else
      {
        sub_401440(11);
        sub_401530(dword_405404);
        lpOutputString = (WCHAR *)sub_4013B0(dword_405408);
        if ( lpOutputString )
        {
          OutputDebugStringW(L"### Good job! Here's your flag:\n");
          OutputDebugStringW(L"### ~~~ ");
          OutputDebugStringW(lpOutputString);
          OutputDebugStringW(L"\n");
          OutputDebugStringW(L"### (Note: The flag could become corrupted if the process state is tampered with in any way.)\n\n");
          j_j_free(lpOutputString);
        }
        else
        {
          OutputDebugStringW(L"### Something went wrong...\n");
        }
      }
    }
    else
    {
      OutputDebugStringW(L"### Error reading the 'config.bin' file... Challenge aborted.\n");
    }
    free(::Block);
  }
  else
  {
    sub_401060((char *)lpMultiByteStr, Block);
    sub_401060("### To start the challenge, you'll need to first launch this program using a debugger!\n", Blocka);
  }
  OutputDebugStringW(L"\n");
  OutputDebugStringW(L"\n");
  return 0;
}
```

From reading the code I could tell that this would open up the file `config.bin` performs some operation on it then makes sure we aren't running the executable in a debugger using the windows `IsDebuggerPresent` [api](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-isdebuggerpresent) 

So that should "prevent" us from using a debugger but we can easily bypass this

Remember that the eax/rax holds the return value from a called function

From the disassembly that handles that check I saw this:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c077a05-1f52-4f4e-bf01-3bc8f03a15ba)

```
call    ds:IsDebuggerPresent
test    eax, eax
jz      short loc_CB161B
```

From that we can see that after the call to `IsDebuggerPresent` it checks if the `eax` register is `0` and if it is we should get to the function that prints the flag

There are two ways I could go about this

First I set a breakpoint at `test eax, eax` then modified the eax register which was set to `1` to `0` which bypasses the check

But then the program exited immediately and made me not able to even get the flag

That's not an issue because if we take a look at the output tab we should see the flag there
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/79297dd9-db41-4149-8099-c9864c29b5bf)

The next way to go about this is to directly patch the `jz` opcode to a `jnz`

To do that in IDA click on the opcode then go to:

```
Edit --> Patch Program --> Assemble
```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cba79b29-106a-45a7-ae01-36cbf906c0af)

Now I just replaced that with then pressed `Ok --> Cancel`

```
jnz      short loc_CB161B
``` 

Now time to save the patched binary 

```
Edit --> Patch Porgram --> Apply Patch to input file
```

With that the executable should be able to run bypassing the debugger check

Here's how it looked here after running the newly patched executable in IDA
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9f997cf2-0070-4343-ad8a-c8de37ca22e5)

```
Flag: picoCTF{d3bug_f0r_th3_Win_0x100_e70398c9}
```

#### WinAntiDbg0x200

Same type of file given again
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ef1e0c2b-bbb6-431f-b5d7-49bd7071f464)

If we try to run it we get this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f4170e6f-5554-4f56-8889-de7a68866137)

This time around we need to run it as admin

I opened IDA but with admin privilege this time around then loaded the executable to it

On generating the pseudocode I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/13364580-df13-44a5-b91e-83d6364dffa1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9d7c0a60-155b-4729-b38a-8d5e04c5ee58)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa027a1f-069a-455d-ba79-247bb55c2d98)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char Block; // [esp+0h] [ebp-Ch]
  char Blockb; // [esp+0h] [ebp-Ch]
  char Blocka; // [esp+0h] [ebp-Ch]
  HANDLE hObject; // [esp+4h] [ebp-8h]
  WCHAR *lpOutputString; // [esp+8h] [ebp-4h]

  if ( !sub_4012F0() )
  {
    sub_401910(
      "[ERROR] There are permission issues. This program requires debug privileges and hence you might want to run it as an Admin.\n",
      Block);
    sub_401910("Challenge aborted. Please run this program as an Admin. Exiting now...\n", Blockb);
    exit(255);
  }
  hObject = CreateMutexW(0, 0, L"WinAntiDbg0x200");
  if ( !hObject )
  {
    sub_401910("[ERROR] Failed to create the Mutex. Exiting now...\n", Block);
    exit(255);
  }
  if ( GetLastError() == 183 )
  {
    if ( argc != 2 )
    {
      sub_401910("[ERROR] Expected an argument\n", Block);
      exit(48879);
    }
    v3 = atoi(argv[1]);
    if ( DebugActiveProcess(v3) )
      exit(0);
    exit(48879);
  }
  sub_401910((char *)lpMultiByteStr, Block);
  if ( (unsigned __int8)sub_401600() )
  {
    OutputDebugStringW("\n");
    OutputDebugStringW("\n");
    sub_401400();
    if ( sub_401450() )
    {
      OutputDebugStringW(
        L"### Level 2: Why did the parent process get a promotion at work? Because it had a \"fork-tastic\" child process "
         "that excelled in multitasking!\n");
      sub_401090(3);
      if ( (unsigned __int8)sub_4011D0() && IsDebuggerPresent() )
      {
        sub_401090(1);
        sub_401180(dword_40509C);
        lpOutputString = (WCHAR *)sub_401000(dword_4050A0);
        if ( lpOutputString )
        {
          OutputDebugStringW(L"### Good job! Here's your flag:\n");
          OutputDebugStringW(L"### ~~~ ");
          OutputDebugStringW(lpOutputString);
          OutputDebugStringW(L"\n");
          OutputDebugStringW(L"### (Note: The flag could become corrupted if the process state is tampered with in any way.)\n\n");
          j_j_free(lpOutputString);
        }
        else
        {
          OutputDebugStringW(L"### Something went wrong...\n");
        }
      }
      else
      {
        OutputDebugStringW(L"### Oops! The debugger was detected. Try to bypass this check to get the flag!\n");
      }
    }
    else
    {
      OutputDebugStringW(L"### Error reading the 'config.bin' file... Challenge aborted.\n");
    }
    free(::Block);
  }
  else
  {
    sub_401910("### To start the challenge, you'll need to first launch this program using a debugger!\n", Blocka);
  }
  CloseHandle(hObject);
  OutputDebugStringW(L"\n");
  OutputDebugStringW(L"\n");
  return 0;
}
```

Looking at the code I noticed this line:

```c
if ( (unsigned __int8)sub_4011D0() && IsDebuggerPresent() )
```

And the function `sub_4011D0()` basically trys to create a child process
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/71a697d5-4f10-4fe0-960f-86a1717343c9)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/69ecba64-5f6d-45c2-bcc0-641b8950c28e)

The program comparism checks if the value returned from calling `sub_4011D0()` is `1` and if `IsDebuggerPresent()` returns `1` then we get the "error debugging message"

Ok now that we know this we just need to make sure it doesn't meet this check

Looking at the assembly representation I saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3472020d-5d8e-43f1-8f03-4fa4f30729b5)

```
push    offset aLevel2WhyDidTh ; "### Level 2: Why did the parent process"...
call    ds:OutputDebugStringW
push    3
call    sub_401090
add     esp, 4
call    sub_4011D0
movzx   edx, al
test    edx, edx
jnz     short loc_401832

call    ds:IsDebuggerPresent
test    eax, eax
jz      short loc_401847

loc_401847: ; get flag :)
push    1
call    sub_401090
add     esp, 4
mov     eax, dword_40509C
```

Ok the assembly looks pretty good and this are the two main parts:

```
part1:
    call    sub_4011D0
    movzx   edx, al
    test    edx, edx
    jnz     short loc_401832

part2:
    call    ds:IsDebuggerPresent
    test    eax, eax
    jz      short loc_401847
```

For the first part, after it calls the `sub_4011D0` function it sets `edx` to the value returned by the called function and it's stored in the `al` register, then it checks if `edx` is zero and finally it jumps if not zero to the function that handles the "error message" else it moves on to the `IsDebuggerPresent` check

From this we know that edx must equal 0 for we to bypass this check

For this I set a breakpoint at the `test edx, edx` instruction then I start the process

To set a breakpoint in IDA we can just click on `F2` at the instruction we want to break at or just right click and choose `add breakpoint`

Doing that I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac777e18-6259-4514-a2f8-cdeca6540b25)

Looking at the "General Registers" tab we see that `EDX` currently is `1`

So we need to patch that opcode from a `jnz --> jz` which is basically saying jump to the isdebugger check if edx is not zero

The next part is what we did in the previous `WinAntiDbg0x100` challenge

Just patch `jz --> jnz`

With that said after doing that I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a80d8c84-7e28-4620-942b-72c464690675)

```
Flag: picoCTF{0x200_debug_f0r_Win_c6db2768}
```

### Web 10/10 :~

#### Elements
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8fa4cc9a-f87f-4b71-bb7e-f6f6d52c64c5)

I actually wasn't the one who solved this but I helped in writing the solve script since our solution takes quite some time before exfiltrating the flag

You can read up on how to solve it here and the other web challenges: [solution](https://krill-x7.github.io/2024/03/27/PicoCTF.html)

And here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Web/Elements/solve.py)

Basically what it does is to brute force the flag character by character using the xss payload which causes the chrome browser to crash once the character being guessed is right

If it crashes, the python script itself stops and I couldn't figure a way to make it continue when the "server instance" isn't reachable which means the chrome browser crashed

So because of that I actually had to do manual changing of the index and updating the known flag character leaked

It was quite a bit of pain but after about ~3hours from guessing the right words and brute force we got the flag

```
Flag: picoCTF{little_alchemy_was_the_0g_game_does_anyone_rememb3r_9889fd4a}
```

### Cryptography 4/5 :~

#### Interencdec
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d1cef18-d367-46d5-a1e7-7d88c79209f2)

After downloading the attached file and checking it I saw it was base64 encoded
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0149b059-fb8d-41b9-9ada-a94f8e347296)

I decoded it using the cli tool and got another base64 encoded value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed2acfaf-b699-44c5-aa2b-588e63cc5587)

On further decoding gives a value which seems to be shifted
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/05bb8a30-b235-4ca2-8311-9327b7263969)

I then used dcodefr caesar cipher [decoder](https://www.dcode.fr/caesar-cipher) to get the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d01d7599-0982-4a7e-acbb-59146e54be4b)

```
Flag: 	picoCTF{caesar_d3cr9pt3d_a47c6d69}
```

#### Custom encryption
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/82434bb9-35d3-45d5-ab9c-7994390531fc)

We are given a python file and the encoded flag

```python
from random import randint
import sys


def generator(g, x, p):
    return pow(g, x) % p


def encrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(((ord(char) * key*311)))
    return cipher


def is_prime(p):
    v = 0
    for i in range(2, p + 1):
        if p % i == 0:
            v = v + 1
    if v > 1:
        return False
    else:
        return True


def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text


def test(plain_text, text_key):
    p = 97
    g = 31

    if not is_prime(p) and not is_prime(g):
        print("Enter prime numbers")
        return
    
    a = randint(p-10, p)
    b = randint(g-10, g)
    # a = 89
    # b = 27
    print(f"a = {a}")
    print(f"b = {b}")

    u = generator(g, a, p)
    v = generator(g, b, p)
    key = generator(v, a, p)
    b_key = generator(u, b, p)

    shared_key = None

    if key == b_key:
        shared_key = key
    else:
        print("Invalid key")
        return
    
    semi_cipher = dynamic_xor_encrypt(plain_text, text_key)
    cipher = encrypt(semi_cipher, shared_key)
    print(f'cipher is: {cipher}')


if __name__ == "__main__":
    # message = sys.argv[1]
    test(message, "trudeau")
```

Here's the encoded flag file content

```
a = 89
b = 27
cipher is: [33588, 276168, 261240, 302292, 343344, 328416, 242580, 85836, 82104, 156744, 0, 309756, 78372, 18660, 253776, 0, 82104, 320952, 3732, 231384, 89568, 100764, 22392, 22392, 63444, 22392, 97032, 190332, 119424, 182868, 97032, 26124, 44784, 63444]
```

I'll go through what the encryption scheme is

First it imports two python modules

```python
from random import randint
import sys
```

Then it calls function `test` passing the first argument which is the message as the first parameter and the second parameter is the key

```python
if __name__ == "__main__":
    message = sys.argv[1]
    test(message, "trudeau")
```

Here's the test function code

```python
def test(plain_text, text_key):
    p = 97
    g = 31
    if not is_prime(p) and not is_prime(g):
        print("Enter prime numbers")
        return
    a = randint(p-10, p)
    b = randint(g-10, g)
    print(f"a = {a}")
    print(f"b = {b}")
    u = generator(g, a, p)
    v = generator(g, b, p)
    key = generator(v, a, p)
    b_key = generator(u, b, p)
    shared_key = None
    if key == b_key:
        shared_key = key
    else:
        print("Invalid key")
        return
    semi_cipher = dynamic_xor_encrypt(plain_text, text_key)
    cipher = encrypt(semi_cipher, shared_key)
    print(f'cipher is: {cipher}')
```

So it stores two prime number in variable `p & g` and makes sure they are prime

Next it generates `a, b `which are random number between `(p-10) & p` and `(g-10) & g` respectively

We are given the value of `a & b`

It calls function `generator` passing `g, a & p` as the parameter where the result is stored in variable `u` and the same is done with with `g, b, p` which is stored in `v`

Here's what the `generator` function does

```python
def generator(g, x, p):
    return pow(g, x) % p
```

Basically what that does is to take the power of `g` to `x` modded with `p` i.e `(g ** x) mod p`

And it generates `u, v, key & b_key`

This is actually a known cryptography implementation called [Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)

But here we are given just the private exponent 

Still we can calculate `u & v`

```python
a, b = 89, 27
p, g = 97, 31

u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)

assert key == b_key
shared_key = key
```

Back to the code it calls function `dynamic_xor_encrypt` passing the `message & text_key` as the parameter

Here's what it does

```python
def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text
```

So it basically just performs a xor operation but this time it reverses the message string which is then xored

After that it generates a cipher which is the value return from calling function `cipher` passing the xored value and the shared key as the parameter

Here's what the function does

```python
def encrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(((ord(char) * key*311)))
    return cipher
```

For each character in the "xored value" it multiplies it by `key*311`

And the result is appended to a cipher list and returned to us

Now how to solve this?

Since we know the key and xor key we can just reverse the process used to encrypt the flag

First we need to deal with the `encrypt` function

```
cipher = char * (key*311)
```

To recover `char` we can simply do this

```
char = cipher // (key*311)
```

Ok that's the first step and with we should retreive the xored value

Now how do we reverse xor?

Well xor is reversible by this

```
a ^ b == c
a ^ c == b
b ^ a == a
```

We can just make use of this commutative property of xor to retrieve the plaintext

```
xored = plaintext ^ key
plaintext = xored ^ key
```

With that said here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Cryptography/Custom%20Encryption/solve.py)

```python
def generator(g, x, p):
    return pow(g, x) % p

def decrypt(cipher, shared_key):
    semi_cipher =  ""
    for value in cipher:
        semi_cipher += chr(value // (shared_key * 311))

    return semi_cipher

def xor_pwn(enc, key):
    pt = ""
    k_len = len(key)

    for idx, val in enumerate(enc[::-1]):
        k_chr = key[idx % k_len]
        d_chr = chr(ord(k_chr) ^ ord(val))
        pt += d_chr
    
    print(pt[::-1])

a, b = 89, 27
p, g = 97, 31

u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)

assert key == b_key
shared_key = key

cipher = [33588, 276168, 261240, 302292, 343344, 328416, 242580, 85836, 82104, 156744, 0, 309756, 78372, 18660, 253776, 0, 82104, 320952, 3732, 231384, 89568, 100764, 22392, 22392, 63444, 22392, 97032, 190332, 119424, 182868, 97032, 26124, 44784, 63444]
semi_cipher = decrypt(cipher, shared_key)
flag = xor_pwn(semi_cipher[::-1], "trudeau")
```

Running it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/54c4321c-5a7b-4e0f-aa92-079d98cc6301)

```
Flag: picoCTF{custom_d2cr0pt6d_dc499538}
```

#### C3
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5bbc7699-0354-4e59-9827-f161ac8ebcc9)

We are given a python file and a ciphertext
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/eaca6fac-36c0-4210-a130-bca695fd824c)

```python
import sys
chars = ""
from fileinput import input
for line in input():
  chars += line

lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

out = ""

prev = 0
for char in chars:
  cur = lookup1.index(char)
  out += lookup2[(cur - prev) % 40]
  prev = cur

sys.stdout.write(out)
```

Ok basically this code will iterate through our input and get the index of the current character in the lookup1 string, then it subtracts the index with the prev variable which is set to 0 initially and is modded by 40. The result is used as the index to get the character specified at the string lookup2 and finally it updates the variable `prev` to the current index `cur`

We can easily reverse this process

```python
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

ciphertext = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"

out = ""

prev = 0
for char in ciphertext:
    cur = lookup2.index(char)
    out += lookup1[(cur + prev) % 40]
    prev = (cur + prev) % 40

print(out)
```

Running that gives another python code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04de7fae-e860-40dc-b9b0-87730702e162)

```python
#asciiorder
#fortychars
#selfinput
#pythontwo

chars = ""
from fileinput import input
for line in input():
    chars += line
b = 1 / 1

for i in range(len(chars)):
    if i == b * b * b:
        print chars[i] #prints
        b += 1 / 1
```

Hmm nothing sus there

I just stored the result obtained from the first reversed operation and used that for this new python code retrieved

And that gave me the word which is the flag

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Cryptography/C3/solve.py)

```python
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

ciphertext = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"

out = ""

prev = 0
for char in ciphertext:
    cur = lookup2.index(char)
    out += lookup1[(cur + prev) % 40]
    prev = (cur + prev) % 40

chars = out
b = 1 / 1

r = ""

for i in range(len(chars)):
    if i == b * b * b:
        r += chars[i] 
        b += 1 / 1

print(r)
```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/235701c2-ab74-4ba6-86f7-445bc522691e)

```
Flag: picoCTF{adlibs}
```

#### Rsa Oracle
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3b898e7f-efef-4035-89df-1b02885112e9)

We are given an encoded password and secret file with also a remote instance to connect to

Checking the given files shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c8277a05-2dbe-41f3-b49d-8947b88ce8b2)

From the challenge hint we know that we are meant to decrypt the AES encrypted file (secret.enc) but it needs a password

So the password file given is actually the encrypted password also that means we would need to get the plaintext form of the encrypted password

Now that we know that let's connect to the remote instance
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d01200ac-5123-4153-9ddf-40028a668780)

On connecting to it i saw that this is a service which encrypts and decrypts values for us

We can try to encrypt a word
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c2c423d2-33a2-4691-8088-dc4be7848f67)

Here i encrypted `pwn` and the ciphertext is `2047850252706091840405479775769742652500446636392769116787296844217713229548194309699205024040158803529449603571974932458613731680043863948321059171243239`

Let's decrypt it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4641f65a-9ddd-4ba0-a32c-edaa04b366f6)

Ok nice we can encrypt and decrypt 

So bascially this is an oracle because it's offering to decrypt any ciphertext we give it

And we know that it implements RSA 

For the encryption/decryption part of RSA it computes this:

```
## Encryption
ct = (m ^ e) mod n

## Decryption
m = (ct ^ d) mod n
```

When we try to decrypt the ciphertext we get this error 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f2e78bef-755e-400b-a3ba-49db97e0822b)

So no easy win :)

Now how do we exactly trick this oracle to give me the flag?

I made some research and found [this](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-1/)

So here's how to craft the ciphertext

First we already know that the server computes `m = (ct ^ d) mod n and ct = (m ^ e) mod n`

Because the server check that we don’t ask for the decryption of the flag, you can’t give it the ciphertext right away, we need to modify it in a way to trick the server into thinking it’s something else 

The modification must be carefully chosen so that we can revert the process once we get the response of the server

For instance, we can’t just add one and expect to subtract 1 from the output

The trick is the multiply the ciphertext with another ciphertext `ct2` from which we know the plaintext

```
ct2 = (2 ^ e) mod n
```

Now the new ciphertext that you will send to the server will be:

```
C = ct * ct2
  = (m ^ e) * (2 ^ e)
  = ((2m) ^ e)
  = 2m^e
```

The server will give you back:

```
pt = (2(C ^ e) ^ d) mod n
   = 2*m
```

Now we just divide `pt` by 2 and that's the password

You must choose a small value because the computations are made modulo n, so if the result gets too big we wont be able to know the real value

With that said I wrote a solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/picoctf/scripts/2024/Cryptography/RSA%20Oracle/solve.py)

```python
from pwn import *
from Crypto.Util.number import long_to_bytes
from warnings import filterwarnings

io = remote("titan.picoctf.net", 61923)
filterwarnings("ignore")

io.sendline("E")
io.sendline(p8(0x2))
io.recvuntil("n) ")

ct1 = int(io.recvline().decode())
ct2 = 2575135950983117315234568522857995277662113128076071837763492069763989760018604733813265929772245292223046288098298720343542517375538185662305577375746934
C = ct1 * ct2
# print(ct1)
# print(ct2)

io.sendline("D")
io.sendline(str(C))

io.recvuntil(": ")
pt = long_to_bytes(int((io.recvline().decode().split()[-1]), 16) // 2)
print(f"AES Password: {pt}")

io.close()
```

Running that we get the aes key which we can then go ahead decrypting `secret.enc`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8aec393e-bf44-4406-bbda-89892d500b18)

```
Flag: picoCTF{su((3ss_(r@ck1ng_r3@_24bcbc66}
```

### Binary Exploitation 9/10 :~

#### Format String 0
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0506f1f6-1ff2-4cc9-9f3b-8a3db3629c17)

We are given a binary and the source code with a remote instance to connect to

Downloading the attached file and checking the source shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a723603-c0a6-4f19-b172-4883ddb79c99)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/23fc13a4-6cfc-4dc5-bd2f-ec5731c31300)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d72b18cc-6926-478d-8e5b-bd6bae054728)

Since this was the first challenge in this category I felt lazy to read the source code but i saw some interesting things just by looking at it
- The flag is opened and stored in a global variable
- We have have a prompt where we need to choose the right bugger and if we meet certain condition we get another prompt which allows us choose another burger

Ok that doesn't make much sense but looking at the part where we select a burger i saw this

```c
#define BUFSIZE 32

char choice1[BUFSIZE];
scanf("%s", choice1);
char *menu1[3] = {"Breakf@st_Burger", "Gr%114d_Cheese", "Bac0n_D3luxe"};
if (!on_menu(choice1, menu1, 3)) {
    printf("%s", "There is no such burger yet!\n");
    fflush(stdout);
} else {
    int count = printf(choice1);
    if (count > 2 * BUFSIZE) {
        serve_bob();

```


First we read in the choice using `scanf` and it's stored in the buffer `choice1` then it stores some burgers in the `menu1` array and if our input is among the buffer array then it calls `printf` on our choice and then it saves the return value from calling printf to an integer variable `count` then checks if `count` is greater than `2 * BUFSIZE`. If the check returns True then it calls the `server_bob` function

There are two vulnerabilities here:
- Buffer overflow
- Format String Bug

The first one is when it receives our input, we can see that when it calls `scanf` it doesn't specify to number of bytes to read in which causes the overflow since the choice buffer can only hold up just 32 bytes

So at this point of knowing that I basically just decided to spam 'A's
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f6f3a240-4430-4189-84e9-a37c222539b5)

It also worked remotely
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/872832c7-1d8c-43de-a841-8eb644c08491)

But looking back at the challenge this is probably not a good way to solve this even though it works

So let me talk about the second vuln which is format string bug

I saw that when it wants to store the result of printf to variable count, printf would print out our choice without using a format specifier

That's what leads to the format string bug

But how exactly do we leverage that when it eventually checks if the count is greater than 64 (2 * 32)

Since we are meant to choose from the menu I noticed that `menu1[1]` has a format specifier in it

```
Gr%114d_Cheese
```

In other words when printf is called it would also do `printf(%114d)`

And the return value from calling [printf](https://man7.org/linux/man-pages/man3/printf.3.html#RETURN_VALUE) is the number of characters printed (excluding the null byte used to end output to strings).

So when `%114d` is passed to printf the number of bytes returned would be `114`

We can check this out by making a dummy script --> compiling it and setting a breakpoint after printf is called

```c
#include <stdio.h>

int main(){
    char value[32];
    scanf("%s", value);
    int count = printf(value);
    printf("\nsize: %d\n", count);

    return 0;
}
```

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e30e2e1c-e110-4b87-8144-7e7fd1fc829a)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a29076c7-bc3e-4329-a866-f9d1d44f0227)

We can see that `rax` is `0x72 == 144` and that's greater than `64` with that we can get us to the next function `serve_bob`

Doing that works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a7ce57f5-1f93-49e1-bdbd-6b80f058874a)

Now for the next function it's also similar

```c
char choice2[BUFSIZE];
scanf("%s", choice2);
char *menu2[3] = {"Pe%to_Portobello", "$outhwest_Burger", "Cla%sic_Che%s%steak"};
if (!on_menu(choice2, menu2, 3)) {
    printf("%s", "There is no such burger yet!\n");
    fflush(stdout);
} else {
    printf(choice2);
    fflush(stdout);
}
```

We just choose `menu[2]` which then does `printf(%s%s%s)` 

But is that meant to give the flag? 

Rather how did we get the flag initially with the buffer overflow

Well I didn't say this at first but there's a function which handle signals

```c
void sigsegv_handler(int sig) {
    printf("\n%s\n", flag);
    fflush(stdout);
    exit(1);
}

signal(SIGSEGV, sigsegv_handler);
```

In this case once the program sees a SIGSEGV signal it would call the handler function which helps us print the flag

That's why the buffer overflow when caused produces a SIGSEGV signal which we then got the flag

To see this we can try it in a debugger and cause an overflow

I set a breakpoint at the point where `server_patrick` function wants to return
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7be06560-8631-4271-be9b-3728279ab33f)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a8c25440-2de4-4470-b52d-fd8335bfa281)

If we move to next instruction we would see that we triggered the SIGSEGV signal
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/21d305bc-34f3-4fdc-b112-d56ba53b8091)

But how exactly can we acheive a SIGSEGV signal with this uncontrollable format string bug

Here's how it's possible, remember that the choice two would do `printf(%s%s%s)`

And what printf would interpret is that:
- Print the string stored in the pointer at the first offset i.e 0xffffffff -> "test"...... so print "test"

But what if that address pointer is invalid what happens? Well the SIGSEGV signal is triggered

So now that we know that, we just choose it and hope the address at the first offset is invalid

Doing that I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a7f1a688-04aa-4da4-8af0-662987f4cd84)

```
Flag: picoCTF{7h3_cu570m3r_15_n3v3r_SEGFAULT_63191ce6}
```












































































