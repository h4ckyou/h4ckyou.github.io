<h3> ForeverCTF  </h3>

<h3> Challenge Solved: </h3>

__P.S I'll be updating since I haven't really solved all the challs and the ctf is running forever ¯\_(ツ)_/¯__ </h3>

## Web
- Start at the Source 
- Cookies
- Baby SQLi 
- Local File Inclusion 
- XSS
- Server Side Request Forgery
- Command Injection
- SQLi

## Binary Exploitation
- uint64_t
- Tricky Indices
- Overflow
- Jump
- Shelly Sells Shells
- Params
- Canary in a Coal Mine
- ROP
- Get my GOT
- Leak
- ret2libc
- Printf
- Resolve
- Signals

## Reverse Engineering
- strings
- xor
- Simple Checker
- gdb

## Cryptography
- All Your Base Are Belong To Us
- Zeros and Ones
- All Greek To Me
- DEADBEEF
- Bookwork
- RSA
- Bad Parameters

## Forensics
- Met A Data
- Not Very Significant Message
- Redacted
- Magic
- Zipped
- Dr. Doom's Devious Deletion Dilemma

 ## Miscellaneous
 - Nested Zip

 ## Networking
 - HTTP Objects


### Web 8/8:~

#### Start at the Source 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f400d2ca-8e7c-4a86-a5ec-69bc518ac1a3)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7b6d1659-e78e-4543-b57b-0e6281ea98e4)

Checking the page source gives the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64baed16-debe-4ab9-92f0-86c0c02aa6a1)

```
Flag: utflag{1_l1ke_h1de_&_seek}
```

#### Cookies
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fd8cf95b-efa0-4030-a47a-6291128d8802)

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee338b71-afba-479a-930f-391337b4e2d6)

Checking the cookies available shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/065ebe70-f27a-470d-afd8-11058b418ff4)

I set the `isCookieMonster` to `true` 

And on refreshing the page I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/014558e8-f397-4b56-9b1b-e0efde833614)

```
Flag: utflag{c0ngrat5_tak3_a_byt3}
```

#### Baby SQLi 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df6e5bd9-c271-4b02-94f9-072422f05541)

We are given this:

```sql
INSERT INTO users(username, password, email) VALUES ('admin', 'utflag{*****************}', 'contact@isss.io');
```

So this means the value stored in column `password` will contain the flag

Moving over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1e403fcc-299a-4c23-9812-d88128aa21ef)

Searching for a valid mail returns the username it belongs to 
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/127159644/252477232-b98b35f8-b8c5-4956-a915-3eadf423d87c.png)

But a non valid mail turns an empty array
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f162a2c0-5c01-4cb6-99fe-3004a81b62b7)

When I inject a single quote `'` it returns error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ccdc987c-86eb-49fb-a0d8-6b8fa9de11e7)

But using `--` comments it and no error is shown
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/79fd4c7f-423f-44f1-9927-04bca149728d)

This means that the web server is vulneable to SQL Injection

We can also tell from the Challenge name 😉

Since only a single table is available and the flag is in the password column. I will use a `union` query to get that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6221124d-4394-42c3-a4b5-912586b3b50e)

```
Payload: ' union select password from users --
```

And I got the flag

```
Flag: utflag{wow_lets_unionize}
```

