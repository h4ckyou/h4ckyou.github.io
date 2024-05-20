<h3> Cyberfest CTF 2024 </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a995235f-ae7c-4340-b0d7-330901a9afc2)

Hello 👋, I participated in this CTF with team `!ethical` as `0x1337`

I'll be giving writeups to some of the challenges which I solved

<h3> Challenge Solved </h3>


## General
- Do you read
- Say Hello
- Do you read 2
  
## Cryptography
- ByteOps

## Web
- Troll

## Reverse Engineering
- Sore
- Finding Nunlock

## Misc
-  Hip Hip HIp!


Not pretty much so let's get to it 😉


### Do you read
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7959b41a-de7b-4146-9201-ee1f00422abe)

It's clearly referring to the main page of the site, so I went over there, viewed page source and got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6c201e0-13fd-4808-a3b9-badccb7f643e)

```
Flag: ACTF{dont_skip_cutscenes}
```

### Say Hello
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/be74af8b-ed43-46af-a222-6c28f729d021)

Head over to their accounts, follow them go back to the ctf platform then submit `Yes` :)

```
Flag: Yes
```

### Do you read 2
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/191d940a-9684-4c31-bdbb-f9d80926837b)

Just submit that 

```
Flag: actf{i_did_not_skip_this_cutscene}
```

### ByteOps
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0ad226af-f00a-4817-a6c3-60e48b466e40)

Ohh this challenge was pretty easy but I spent some time on it

First I downloaded the attached file and on checking it's content I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/93bf8cb5-364b-4e23-8b32-3fcc6fa9a7d5)

```
6182665f351415600b57005b5f80fd
```

I started thinking this was some sort of hex value 💀

Well after trying I got back to the challenge and read the "description"

```
Our contact says Nuk deployed a contract using EIP-3855 .

The hexcode calldata of a transaction that will not revert is said to be the key.
```

I am not a Web3 person but from reading this I knew it was related to Web3

Ok time for some research, first thing I had to search what was "EIP-3855" meant
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7754334c-1a98-41ea-9fde-ae88047fb5dc)

Most of what I was seeing was just "PUSH0 instruction"

I tried to learn about "EIP" but didn't succeed as I could not find any where to get a general basic of what it is

Now i decided to work back with what I have

From reading [this](https://ethereum-magicians.org/t/eip-3855-push0-instruction/7014/2) it made me conclude that the hex value given as the challenge is a bytecode because the links based on "EIP-3855" was referencing opcode (operational code) and instructions, you can also use the challenge name to conclude your assumption is right (`Byteops`)

Now that I know this I had to find a way to decompile the bytecode

Searching it up on google gave [this](https://ethervm.io/decompile) and trying to use it worked

```c
contract Contract {
    function main() {
        var var0 = 0x8266;
        // Unhandled termination
    }
}

label_0000:
	0000    61  PUSH2 0x8266
	0003    5F  5F
	// Stack delta = +1
	// Outputs[1] { @0000  stack[0] = 0x8266 }
	// Block terminates

	0004    35    CALLDATALOAD
	0005    14    EQ
	0006    15    ISZERO
	0007    60    PUSH1 0x0b
	0009    57    *JUMPI
	000A    00    *STOP
	000B    5B    JUMPDEST
	000C    5F    5F
	000D    80    DUP1
	000E    FD    *REVERT
```

Ok good now we decompiled it what next?

Well we need to understand what it does and each opcode has the operation it performs so I searched for the opcode 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0d9793fc-379e-4ad8-8606-56f70de6dbda)





































