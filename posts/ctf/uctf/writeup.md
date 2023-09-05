<h3> UCTF 2023 </h3>

I played this ctf with my friends

Here's the writeup to the challengs I solved:

### Web
-  E Corp
-  htaccess
-  Captcha1 The Missing Lake
-  MongoDB NoSQL Injection

### Cryptography
- Noql

### Pwn
- Moedo

### Misc
- OTP (Onion Transfer Protocol)


### Web

#### E Corp
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e71ca47b-2df7-48be-9a92-52dbbbedd6aa)

From the challenge description we can immediately tell this would be some sort of SSRF

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/53621409-426b-413f-bb7d-b8d2076b6ad4)

We have 4 various blog post

Clicking it just shows some word
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cdaa45ff-4bc7-4a69-af13-5d456b2ea8ed)

Looking at the request made when I click on a blog post shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e2aeadb-e991-407e-9fc9-de1dae9b4c5f)

We have a `POST` request to `/api/view.php`

And the parameter passed is this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/de85eb59-70ae-422b-95e0-9046403faf55)

It is using a `file` wrapper to view the content of `/posts/Azita`

With this we can basically read local files from disk 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6cb54c6-7e8a-4353-90e3-7ea3a536c427)

```r
curl -s -X POST "https://ecorpblog.uctf.ir/api/view.php" -H "Content-Type: application/json" -d '{"post":"file:///etc/passwd"}' | jq .post -r
```

But how would that help us in accessing the internal domain?

Well since it uses `file` wrapper it's safe to assume we can also make use of other wrappers in this case it will be `http`

With that said we should be able to access the internal domain `http://admin-panel.local`

Doing that works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ca1ad5f7-096d-4067-8b3d-08669c628713)

```r
curl -s -X POST "https://ecorpblog.uctf.ir/api/view.php" -H "Content-Type: application/json" -d '{"post":"http://admin-panel.local"}' | jq .post -r
```

Here's the flag

```
Flag: uctf{4z174_1n_urm14}
```

#### Htaccess
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/56adf216-bb38-4497-a090-38d51feab049)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7e3b3c26-d017-4374-8d61-c8138fe0a285)

So there are two htaccess rules placed on two portions of the flag

We need to bypass them inorder to get the flag

The first one is this:

```
RewriteEngine On
RewriteCond %{HTTP_HOST} !^localhost$
RewriteRule ".*" "-" [F]
```

What this rule enforce is basically that if the `Host` header isn't `localhost` we won't be able to access the file

So to bypass this we can just change the `Host` header to `localhost`

This is what happens if we fail to bypass and try to read the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b9cb159e-7257-4d18-a687-1327a9289eb2)

Cool so let's bypass that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a03e6ab-ca72-4b56-8d2a-9467161a1a40)

```r
curl -H "Host: localhost" http://htaccess.uctf.ir/one/flag.txt
```

We get the first portion of the flag

```
uctf{Sule_
```

For the second rule:

```
RewriteEngine On
RewriteCond %{THE_REQUEST} flag
RewriteRule ".*" "-" [F]
```

It checks if the request body contains the string `flag` 

If it does then we will get 403 error

Here's a sample
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/18ca5089-ef40-4032-87cb-b89d01a06d39)

So to bypass this we can just url encode the string `flag` in the url search bar 

And what will happen is that the htaccess check will return False but where as on the server side it will get decoded to `flag` and we get access to it

This solution was given to me by @0xvenus

First I urlencoded `flag` then used it as the file name in the url
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6de8e1a8-13a0-4242-af01-ea1aa06fa2a7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aefe0048-9e87-4026-bf53-8a1fc6aa5ef9)

```
curl htaccess.uctf.ir/two/%66%6c%61%67.txt;echo
```

We can now join the two portion of the flag 

```
Flag: uctf{Sule_Dukol_waterfall}
```

#### Captcha1 | the Missing Lake 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e89c51b0-3c8c-45c6-968c-5251a3ee51a9)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/84eeb99d-7440-44c3-88a7-bce6647b9352)

So we are to provide the captcha 300 times before we get the flag

The session cookie is provided
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/074ca712-6663-4cae-95fc-a2e8052ad184)

On each page refresh the value of the image changes
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/011c164f-7bb5-47ad-85ba-054f26382a1a)

We can submit those words from the image manually but what's the fun there 🙂

This is my approach in solving this challenge:
- First I'll need to get the current captcha from the image so that I can send the first captcah request with it's value
- Using tesseract which is an OCR tool I can extract the text from the image
- Then do a while loop to repeat the process till the capcha check is completed

That sounds easy writing **that** but the script took me some good amount of time debugging 😂

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/uctf/web/Captcha1/solve.py) and I must admit it takes about 12minutes (I should learn to optimize my coding ikr)

But after running the script I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0bcca4c7-5e8d-47b7-97ac-14130aadc5be)

And back on the web page I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0a7edada-b61b-4fab-b4c0-34b8d2c9a07c)

```
Flag: UCTF{7h3_m1551n6_l4k3}
```

#### MongoDB NoSQL Injection
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b772a480-0009-4b97-8133-7299c55c2bf7)

From the challenge name we can tell we will be doing NoSQL Injection

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3593ab49-4297-403d-86c0-9243e8442ff3)

We have a login page but since no credential was giving let us try bypass it using NoSQL Injection

I used burp to intercept the login request
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/15a311ff-124d-446b-89b0-3cb5ade06d90)

Failed login request just redirects to `/login`

Notice the header
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7b7848bf-df6e-4bc2-b54e-43909cf8e081)

It's running Express server which is like NodeJS and usually the database that runs on NodeJS is MongoDB

Also because of this we can pass the parameters in form of json
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/19231513-689d-45b3-8f74-fe503e1102e2)

We can see that on forwarding the request it works 

To check for NoSQL Injection I used the not equal `$ne` parameter 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b1d8f98f-ccd9-4d1d-8fd8-cdec64d86ea4)

```r
{"username":{"$ne":"uche"},"password":{"$ne":"uche"}}
```

What that does is to tell the MongoDB that the value of `username` is not equal to `uche` which is True because the database doesn't have any username as `uche` also the same applies to the password

With that the login will be successfull

By intercepting the login request and modifying it to that payload I was able to bypass the login page
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0dc5ac97-3fd6-458a-bfa6-27a9d4381b96)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/86bda8f4-1e90-4c28-8b25-c7b6ff6089f6)

In the home page we can search for a user

But when I tried searching for some names it didn't return any result

There's a `/users` endpoint but that gives this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6fd12f6-87fc-4713-a03a-e506477237d5)

So we need to find a way to get the users

We can take advantage of the NoSQL injection to dump the users from the username column

The way to do it is by using regular expression

So basically this:

```r
{"username":{"$regex":"^"},"password":{"$ne":"uche"}}
```

That will return True and get us logged in because `^` is a wildcard which basically checks if any of the users in the column first character is any value

Next we can try:

```r
{"username":{"$regex":"^a"},"password":{"$ne":"uche"}}
```

This will check is any of the user in the column is starting from `a` if that returns True i.e gets us logged in

Then we can check for the second character

```r
{"username":{"$regex":"^ab"},"password":{"$ne":"uche"}}
```

Basically we will keep doing that and eventually end up dumping the users

So now that we know that we can go ahead doing it manually but scripting it saves time

Here's the dump [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/uctf/web/NoSQL/solve.py) 

If you check the script you will see commentated section of the code that's so because while I was trying to solve this I was over complicating things lol

Anyways basically the script will dump the users
![1](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0abeee0b-3c8a-4b11-b198-719d8ee02b79)
![2](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7f823cb0-0850-426f-a462-a193556bb5f5)

Now that we have the list of users this is where I started over complication things

I assumed the flag would be any of the users password

So I made a function to get the password length of each users

It's just doing this regex

```
{"username":{each_users},"password":{"$regex":"[a-zA-Z0-9]{1}"}}
```

Basically that will check is the length of the user password is 1 if it is then it will return True and get us logged in

We can keep incrementing the values till we get a False return

But when I ran it I noticed the password length are all the same for the users
![3](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6134f03c-cee1-4c42-aa43-e3ce3c179109)

So it's likely the password are hashes that's why it's the same

Therefore it's of no use (i spent so many hours on this lool)

After this I decided to check the web out and saw the search user function which I had forgotten about
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8ff9caf3-258f-48ee-9af0-86007e8c4957)

I searched for the users I have and got their individual role

Right now it doesn't work I guess the server is overloaded
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac8e29a8-13f8-4ccb-9fe9-3b96290c51be)

But user `decre127` profile had the flag in his `ID` column

Just to confirm I ran the script again and saw that the users changed so that's why it didn't return any value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e757bbd9-5d05-462d-ad41-399ba83275a3)

Searching the first user returned it's value
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f00d22eb-1afa-491a-8f81-f25f6a51836e)

So just search for all the users the one whose role is `admin` holds the flag :P

### Cryptography

#### Noql
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/82f14208-4242-4832-8d08-4cb3a529d8a6)

We are given an attached file to download with the key which is base64 encoded

Checking the attached file showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/49c10754-9fc1-495e-9536-ff6874a9de63)

The first thing I noticed was the first 6 bytes `gAAAAA` 

That's Fernet encryption and I knew cause I did something similar before and when ever something is encrypted using Fernet Cipher the first 6 bytes are `gAAAAA`

I wrote a script to decrypt it

```python
from cryptography.fernet import Fernet

key = b"CT0cgUTU7gBBvA3DOk4H30JMQSFwNm-viqZm9eDwPK8="
token = open('noql.txt', 'r').read()

f = Fernet(key)
d = f.decrypt(token)

print(d.decode())
```

Running it gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b0709d9f-264b-4b53-9d37-aa7c92969044)

```
Flag: ucf{urum_noql}
```

### Pwn

#### Moedo
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6387b487-e9f0-4e3e-86b0-834f0f817e52)

This was a begineer pwn challenge and the source code was provided

Here's the source [code](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/uctf/pwn/moedo/src.c)

Reading the source code we can see the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e288aa81-e7ad-45ab-a48c-b9afa076ce68)

What it does is this:
- It sets the user and group id to two corresponding variables
- Then the value stored in variable `moeness` is the value returned when the `check_moe` function is called passing the user id as the argument
- A pointer `custom_chant` stores the value of the environment variable `MOE_CHANT`
- The array `chant` holds a set of characters
- It checks if the argument count is less than 2 and errors out this means this program will require an argument
- If a value is in the `custom_chant` variable it will then use `strcpy` to copy the value to the array chant
- Then it will print out the uid, gid and the moeness (this in hex)
- It compares the value stored in `moeness` with the expected `moeness` value which is `0x30e`
  ![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f3c48feb-8b89-4c31-91f3-06b63cbabb20)
- If that checks returns false it returns error else it sets our `userid` and `groupid` to `0` calls `execve` on our input which is basically command execution


Here's the `check_moe` function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4088dbad-a56e-48e5-ba2e-8c397ccf7bc3)

What that basically does is to like convert our user id to a moe value 

So what's the vulnerability with the code?

Well this:

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8bb18a40-6353-448f-9f75-707754274574)

It uses `strcpy` to copy the value of the `MOE_CHANT` environment variable to the `chant` array

And the chant array can only hold some amount of bytes since it already has some value stored in it

```c
char chant[] = "Moe Moe Kyun!";
```

The use of `strcpy` cause a buffer overflow 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a4819641-03ce-4c4d-8ac4-a8858486ad51)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bab46dfa-bc85-470f-a813-870886ea197b)

Let us test this out

First I compiled it because no binary was provided just the source code :P
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4a499ad6-0ad3-4c88-94a2-a00514b55aa7)

```
➜  Moedo gcc src.c -no-pie -o src
```

Now I can cause a segfault
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c5c234b4-d38a-4712-9e57-1478a797483f)

```
➜  Moedo export MOE_CHANT=$(python2 -c print" 'A'*1000")
➜  Moedo ./src lol
UID: 1094795585 - GID: 1094795585 - Moe: 41414141
You're not moe enough!
[2]    125693 segmentation fault  ./src lol
➜  Moedo
```

Cool now we have confirmed the buffer overflow

What we should think of now is on how to exploit this?

Well we basically just need to meet the if condition done on the value of `moeness`

Since this will turn to be variables on the stack,

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58b6af1b-1044-4728-8500-195f4df67015)

We can calculate the offset between the `chant` and `moeness` variables

With that we will be able to overwrite the value stored in `moeness`

To get the offset we can maybe look it up in gdb
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4a26a145-4f1f-45eb-b700-9cf483907e00)

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2e80dc1a-1c50-4052-b04a-75a7beade69f)

Or just check ghidra stack layout
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/648d5671-bef6-4548-84d1-663107599fbf)

The offset is `0x2e - 0x14 = 26`

So with 26 bytes we will get the moeness variable and on more input we would overwrite it's content

Let's check it out
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b8982e4c-bd2a-499d-ad19-1c243e83e616)

Cool it works

Now we just need to overwrite it to the expected moeness value which is `0x30e`

```c
#define MOE_ENOUGH 0x30e
```

The hex form will be `\x0e\x03` doing that worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5da43065-6203-4b82-9f85-2b30b2f422fc)

But we get an issue returned from `setuid` and that's because it's trying to set the user id to `0` which is for the root user and we are not root

We can just change permission and set the binary to have the suid perm
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5da4ceac-198f-44a9-9e9c-88e5ebec3d6a)

And now if we run it again we should have command execution as root
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1613fece-64e7-4767-8a1f-aa5df2417b52)

All we need now is to do the same thing on the server but unfortunately there's no python on the server :(

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8b12d266-fdc5-4d7e-8628-6f5981632380)

I then used `printf` since it was available on the remote server
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7a8779a0-0be6-4c07-9b89-22c71c19fce4)

```
export MOE_CHANT="AAAAAAAAAAAAAAAAAAAAAAAAAA$(printf '\x0e\x03')"
```

Here's the flag

```
Flag: uctf{m45h1r0_d1dn7_61v3_up}
```

### Misc

####  OTP (Onion Transfer Protocol) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/80d2167f-0b97-4e9d-a921-1637a15e4098)

I was writing on this challenge and was almost done but suddenly my firefox crashed (it's been happening recently I have just few tabs open 😕) and I didn't save this github edit progress 😭

Starting afresh is a bit of pain so I will just give the TDLR of it

We are given a host running ftp via the tor network proxy

Connecting to it normally won't work so we need to setup a proxy where when we use ftp it will be passed via the tor network proxy

It can be configured by using starting tor service and using tor network which by default runs on port 9050 i think then add that in our proxychain config file as socks5 proxy

Then we should be able to connect to ftp!

The ftp contained 5000 directories all having different names and the same file in each directory

The file name was `flag.txt` but it contained a fake flag

Each of the directory had the same size so if you thought of just filtering the one of different size that won't work (but congrats on thinking of that xD)

You might also maybe think of downloading all the files and grepping for the flag but that's stressfull considering network speed and the amount of time it will take before it downloads :)

There was a hidden file which had the keyword: `Think of IFUM!!!` 

At first that seemed weird but after few minutes I figured that a directory started with `IFUM` and on downloading the file in that directory lead to another hint 

I have forgotten the word :( but it was also among a directory then that one contained the flag

That's all for this ctf and the challenge I did 😜

Here's the writeup to other challs solved by some of the team mates I played with:

[Sensei](https://github.com/SENSEIXENUS2/Ctf-writeupsScripts/blob/main/UctfWriteups/Writeup.md) [gr33p](https://gr33pp.github.io/posts/urmia-ctf-2023/writeup)

Btw `Captcha2` was among the web challenge though it was solved, Sensei beat me in writing an auto solve script 😭

Do so to check the two writeups 

Thanks for reading (　-_･)σ - - - - - - - 
