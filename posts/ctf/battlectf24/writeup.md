<h3> Battle CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/9d74fbd3-a76b-421c-8247-8630551c826d)

Hii 0x1337 here, this writeup contains the challenges I was able to solve in the Battle CTF 2024 prequalifiers event!

Hope you have fun reading.

Challenges:
- Rules (Misc)
- Invite Code (Misc)
- Do[ro x2] (Forensics)
- Sweet Game (Pwn)
- Universe (Pwn)
- NTCrack (Pwn)
- 0xterminal (Pwn)
- Hmmmm!... (Web)


**Rules**

Going over to the discord channel and checking the #announcement page gives the flag
![image](https://github.com/user-attachments/assets/8ec1e651-47c2-4989-972d-b314bb4801d1)

```
Flag: battleCTF{HereWeGo}
```

**Invite Code**

This challenge was actually released prior to the ctf beginning and you can find it on the discord here
![image](https://github.com/user-attachments/assets/1da6c398-493c-462b-933d-e2758158e7bb)

After decoding from hex it gives this
![image](https://github.com/user-attachments/assets/ab4af42a-ec7c-4093-b78f-cb8f9432e720)

```
UWNYZ1c5dzR3UWQvZWIudXR1b3kvLzpzcHR0aA=https://bugpwn.com/invite.ini
```

There are two things of interest there, one is a base64 encoded value and the other is the invite link path?

Spoiler alert:- The base64 value decodes to a Youtube link which is a rickroll :)

On checking the invite link i got this
![image](https://github.com/user-attachments/assets/64220696-88d8-4479-87c2-0bdd8fd2f6fd)
