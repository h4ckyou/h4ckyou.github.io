![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7aeb95aa-ffab-4b19-a785-f81b6b247c4c)<h3> Cyberfest CTF 2024 </h3>

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
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0d9793fc-379e-4ad8-8606-56f70de6dbda)

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

Well we need to understand what it does and each opcode has the operation it performs so I searched for the opcode list and got [this](https://ethervm.io/#82)

Before diving into the bytecode we can see that some portion was decompiled correctly and it defines a contract `Contract` where the `main` function stores a value `0x8266` in variable `var0`

At this point of seeing it I went back to the challenge and read the description

```
The hexcode calldata of a transaction that will not revert is said to be the key.
````

This looks like the right input to this challenge so I tried it but unfortunately it didn't work

I did spam lot of it though 💀

Now let's understand what the bytecode does

First I'll write what each opcode translates too

```
PUSH2 - Pushes a 2-byte value onto the stack
CALLDATALOAD - Reads a (u)int256 from message data
EQ - (u)int256 equality
ISZERO - (u)int256 is zero
PUSH1 - Pushes a 1-byte value onto the stack
JUMPI - conditional jump if condition is truthy
STOP - Halts execution of the contract
JUMPDEST - Metadata to annotate possible jump destinations
PUSH0 - Shanghai hardfork, EIP-3855: pushes 0 onto the stack
DUP1 - clones the last value on the stack
REVERT - Byzantium hardfork, EIP-140: reverts with return data
```

Harmed with this instruction let's translate what it does

- First it pushes a 2 byte value onto the stack then pushes 0 to the stack

At this point let's visualize the stack as an array, then it should hold this:

```
[0x8266, 0x0]
```

- Next it reads an unsigned int from the message data
- Then it compares our input with the value on the stack (i presume)
- If it's equal it stops else it reverts

Ok pretty straight forward we just need to provide the value that would make the contract not to revert, and for that to happen the value oughts to be `0x8266`

But when I submitted that as flag it wasn't working

I then decided to work with this dynamically, basically seeing how it works during runtime

Searching for how I could achieve that lead me to [evm_playground](https://www.evm.codes/playground)

This is how it looks like
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b82f9fd9-97a5-447f-a803-5f883dd7ad21)

So I change the default bytecode there to the one we have
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d43c9858-bc5b-4105-947e-a4e4df2b9546)

One thing to note there is that the `Calldata` form is where we pass in input as hex in this case the value we want to check

First i tried using the value it's compared to which is `0x8266`

Starting it's execution shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/997f2adc-77e4-435f-befa-180d86c15261)

We can click on `next instruction`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bb513182-fdef-4eea-807c-54b546dad3ae)

After the `CALLDATALOAD` instruction we see our given value has multiple 0's
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cdc0139f-2466-496e-aa05-d6c720ff4d5a)

I don't really know how i can say this but i think it's just like how memory address are when it uses msb to represent data

Like in this case `CALLDATALOAD` reads an unsigned 256 bits int

When I checked the size of `(u)int256` in solidity I got it to be `2^256-1`

If you compute that and compare it with the length of the value we have you should see this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b92348fd-b1da-4844-854d-dc50cad5a81f)

This means it's just alligned based on the size of the data type

When we continue the execution it will hit `REVERT` because of course the values aren't equal
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/837368f9-ab18-487a-a5b0-5713a82e1af3)

So here's the value I used

```
0x0000000000000000000000000000000000000000000000000000000000008266
```

Using that the execution hits `STOP` which means this is the expected value

We can then submit that :)

```
Flag: ACTF{0x0000000000000000000000000000000000000000000000000000000000008266}
```

### Troll
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/813b37d2-c052-41b1-9409-a985da23ed3d)

This challenge was pretty much created due to a rant about why there were no very trivial challs 😄

-- We asked for it...

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/556e5bef-06ac-475e-9f40-82560a35c2d3)

-- He delivered

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d9d5495d-0005-430c-ba29-660c3f0b4e75)

Now let's get to it

Going to the attached url doesn't show anything
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/06a284fe-3cf2-4578-b303-18ded56c4fdc)

Viewing page source reveals nothing also
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/656d4fa2-8066-4589-8928-8cf54c83afaf)

On checking `/robots.txt` reveals this path
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2553da28-c96a-4164-8013-64a04d587682)

Trying to access it downloads an attachment
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2e4d146f-b9cb-46b5-b7a4-42446281d5cf)

The file downloaded was a rust compiled executable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fa517406-19be-4799-8b70-a95fd382d1cd)

I ran it and got this message
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed67c45d-d9cb-41bd-bac8-1832c5429af3)

At this point when solving it I actually had to `CTRL+C` because during the prequal there was a rev chall which would logout the current session so I thought it was the same but luckily it wasn't

Strings & grepping for the flag pattern reveals the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/be496a23-5c1d-4200-add1-d079346cdc04)

```
Flag: aCtF{robotTxt_and_strings_as_requested}
```

For the last two webs I wasn't the one who solved it but my teammate, incase you are wondering what the solution is here's the payload used:

--- Mystique

```
//note I renamed most of the obfuscated variables for better understanding. 

onSubmit, the login() function is called which sets the following varaibles.

- publicKey stores a JSEncrypt key object gotten from the setPublicKey() function.
    - The setPublicKey() function stores a PEM key in the key variable.
    - creates a new JSEncrypt object and stores it in the jsEncryptedKey variable.
    - it finally uses the .setPublicKey() method on the JSEncrypt object to the set the public key to the PEM key above.

- randomText stores a randomText generated by the generateRandomText() function
    - I don't this is really important

- encryptedData stores the encrypted data returned from the encryptData() function which takes publicKey and randomText as arguments
    - The encryptData function stores the result of concatinating 'user' + randomText in a variable data. 
    - encrypts the data using the publicKey.encrypt() method

- sendEncryptedData makes a POST request to the /Flag endpoint with the encryptedData as argument.
    - before the request is sent, the encryptedData is url-encoded

[+] Steps to recreate
    In your console, run the following . .
        - var key = '-----BEGIN PUBLIC KEY-----\n MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0ziDyee9fICsEJ5ebGyv\n N1toEnOGBwYQrehsuOfkNXm4BKoBgiSXJGAeU/+4JeXrkaX7pejDF1loZvKXFIfA\n RaaNIqDbsZfIYPB0nMpaYrXreO6R+7jyWN6a0uPTOyaYYlCdhLRjciV8w7PBcO/e\n iVzCajZSp+uNqlVz3s83o+LOl0B/RLNNUPrUjwvj7s4dattJhtKLts1mC1V7aHcL\n JquS5E2OqAzps2DzVJ1sezHmvJGw9/8+58AMwqFTwixP37+FhuAbNGUN5DHRUjSK\n zscmDAgE+HN+GPwOx6ynpVmrubqWsZ0CL14mxtfVYNUBopI/BACZYdn2B/Eze1ay\n uQIDAQAB\n -----END PUBLIC KEY-----\n'
        - var jsEncryptedKey = new JSEncrypt()
        - jsEncryptedKey.setPublicKey(key)
        - sendEncryptedData(jsEncryptedKey.encrypt("admin"+generateRandomText())
```

--- Daredevil
```
sendEncryptedData(encryptData(key,"admin:' or password like *"))

checking the source code, we need to send the user and password seperated by ':' encrypted.

sendEncryptedData(encryptData(setPublicKey(), "admin:admin")) 

when you send the above in your browser console, you should get "Invalid Username or password" as the response. 

but when you send this instead, 

sendEncryptedData(encryptData(key,"admin' and password like '%'--:admin"))

we get the following response "Login for admin' and password like '%'-- not allowed", so we can guess the password like that.
```

### Finding nulock 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6d7d2808-87fc-427a-adf1-14d8a71ddec2)

This was the first reverse engineering challenge, and we were given an apk file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/879edf55-dc4a-4cd5-8def-d02c99aa7e90)

First thing I tried was to unzip the file, grep for the flag, convert the dex files to jar using `dex2jar`, decompile the converted dex file using `jd-gui`

Doing that I didn't really get anything and `jd-gui` decompilation was a bit off

So I tried using an online [decompiler](https://www.decompiler.com/)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f27807bc-1b9d-4e35-a29c-171ecd8bda4d)

Next i downloaded the zip file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e1d2da91-b134-4e92-8595-7f5f5890b7a0)

Unzipping it and opening in vscode should give this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0546674f-029b-4b31-8f79-5af3e04c2914)

Looking through the classes i saw `Payload.java` which looked interesting

Viewing it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c00628aa-dd8a-4be1-b408-27c9ba2a6e08)

We can right away tell we should decode that

I just copied and paste that array to python interpreter then converted them to `chr`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6c7ef4ee-319b-439e-9c1a-2f6ccf069e71)

That gives error and that's because it isn't in the printable range for example `-5` isn't a printable value

To fix this we need to `AND` it with `255 == 0xff` which is equivalent to `% 256` and that would make each value there in the printable range
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b7423d26-bc55-47aa-8305-6756837dd86b)

With that we get the flag

```
Flag: ACTF{Dynamic_Analysis_h0s7_R3v3al5}
```

