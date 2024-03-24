### New Jersey 2024 CTF

#### It was fun and I only focused on solving the Binary Exploitation & Reverse Engineering challenges. I played with `THE TOMATO DUDES`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e465014d-57ac-44c0-957e-7adf914b3089)

Currently the scoreboard is hidden though the ctf is over so i can't see our position nor each user point

#### Challenges Solved:
  - Humble Beginnings (reverse)
  - Password Manager (reverse)
  - Searching-Through-Vines (pwn)
  - Math Test (reverse)
  - The Heist 1 (reverse)
  - Running On Prayers (pwn)
  - Stage Left (pwn)
  - Postage (pwn)
  - The Heist 2 (reverse)

Out of this I was able to do 8/9 from this category
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/23b098bb-9f86-409b-8dee-1f9d7cb18f4e)

So let's start...

##### Humble Beginning
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1d690764-40c6-41a8-9eaa-09e1aff297de)

So our goal is to find the crypto wallet address

After downloading the executable I loaded it up in IDA and generated the pseudocode

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7f1e3de0-234a-4349-8f65-0c6bb73a818c)

At this line:

```c
sub_140001010(v4, "mxnhCEkuBogW3E7XAEzNmaq6eZqW3zgEuu");
```

It's calling function `sub_140001010` passing `v4` which is the first argument we pass to the executable as the first parameter and some weird string as the second parameter

Using that as the address worked

```
Flag: jctf{mxnhCEkuBogW3E7XAEzNmaq6eZqW3zgEuu}
```


