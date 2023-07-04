![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/df7bddc4-0a78-4b23-9c71-412e590135e1)<h3> BattleCTF Prequal 2023 </h3>

#### Description: This was a fun ctf I participated in as an individual player. Thanks to the organizers for the awesome challenges
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b550193f-987a-48ca-a355-bf5a0948eeef)

<h3> Challenge Solved </h3>

## Misc
- Discord
- Way
- Go
- Minon Agbodo
- BUG|PWN
- php zlib

## Web
- Civilization
- Own Reality
- It shock you
- Cobalt Injection
- Africa
- Hebiossa Injection
- Cobalt Injection2
- Perfect Timing

## Forensics
- Thumb
- Find Me
- Africa Beauty
- Minon
- Base64
- Gift
- TorrentVerse

## PWN
- AM1
- youpi
- AXOVI
- 0xf

## Reverse Engineering
- SEYI
- Welcome
- babyrev
- checker
- Mazui

## Cryptography
- Back To Origin
- Blind
- Gooss

### Misc 6/7 :~

#### Discord
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ac8e231-b339-4e3a-a8d1-dc7f1ff504ef)

After joining the discord channel and viewing the `announcement` I saw the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/940d1887-ff3e-4e20-ac84-fe8a238df8ab)

```
Flag: battleCTF{WeLoveAfrica}
```

#### Way
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d94fc0b5-1d30-40c2-a13c-008eb815ad59)

After downloading the attached file checking the file type shows it is a zip file archive
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7772ffbf-77f1-44ab-a3c9-683c6f29f00a)

I tried to unzip it but I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1150a6fc-d214-46b5-8784-867a30b2c535)

With this I know that it will require a password if I try to unzip using `7z` 

So let us brute force the password

I converted it to a format john can understand using `zip2john`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e50380b7-2602-41d0-b61a-729d0372adb7)

The password is `samoanpride` 

Let us unzip it now
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/579712f5-75bf-4a95-b906-92bd86623a17)

It unzipped to form an image file

Checking the image shows the `BUG|PWN` logo
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2f45845b-ce17-4586-8cb7-c068d185a2e4)

Using strings showed me the password and from there I can filter it to get the last line in which the password is
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bd029b3b-2adb-4356-83ee-21ff6f2cedc9)

```
Flag: battleCTF{The_Best_Way_To_Learn}
```

### GO
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c7f019e1-3187-4ce6-b003-4357c5e2bb32)

It gave this string:

```
onggyrPGS{RaqGvzr_vf_terng}
```

I used [dcoder.fr](https://www.dcode.fr/cipher-identifier) to identify the type of cipher it is
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b35a9c43-b1ee-410d-8fed-d6440f69a292)

It says it is `ROTed` 

I then decoded it using [this](https://www.dcode.fr/rot-13-cipher) 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6f8d3b6c-4a99-4885-ab55-76a2f8d0dd66)

```
Flag: battleCTF{EndTime_is_great}
```
