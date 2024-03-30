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





































































### Web 10/10 :~

#### Elements
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8fa4cc9a-f87f-4b71-bb7e-f6f6d52c64c5)

I actually wasn't the one who solved this but I helped in writing the solve script since our solution takes time before exfiltrating the flag

You can read up on how to solve it here: [solution]()




















