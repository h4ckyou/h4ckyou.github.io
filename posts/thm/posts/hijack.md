<h3> Hijack TryHackMe </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f4519c5a-bf39-44bd-989a-195f14153a0c)

Been long since I did a machine from TryHackMe but recently a friend of mine showed me this box so I decided to do it today

First thing first as always is enumeration

I started with an nmap scan and on doing so got me this available tcp ports open
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f87e8f09-67ae-40d2-b363-df0a3f251814)

Ok cool we have ftp, ssh, http and nfs open

Checking the mounts on nfs shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9cbe16a7-bd94-4af9-b594-cc3e375308df)

So anyone can mount the share on `/mnt/share`

I mounted it and saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c244adfe-248f-4ee3-9d4c-d0df276b74c1)

```
- mkdir mnt
- sudo mount -t nfs 10.10.38.234:/mnt/share mnt
```

Well we can't access the mounted share cause our user & group id isn't `1003` but `1001`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/096ae2e0-424f-4142-9298-836923711705)

To solve that I just changed the value from my `/etc/passwd` file (but u can actually create a dummy account and make the uid/gid 1003 then delete when done ...... as for me i'm too lazy to do that)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/32dc459d-a804-457e-b8c2-9f8af0fe0268)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f30871f0-fe8a-4822-bc7d-5ab6a1831519)

```
ftp creds :

ftpuser:W3stV1rg1n14M0un741nM4m4
```

Cool we have the ftp credentials now we can unmount the share and continue enumeration
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b28b3bc2-13e9-42e2-9192-4f32c31c5a22)

Let us check ftp shall we?
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a9598e72-db0f-4502-b673-de6a8cc40f6b)

That seems to be like a user directory and also two non default files are there (which are hidden) 

After transferring it to my host I checked it's content and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/26fd23bf-0b0c-4dce-a5d3-ab513dfbadf7)

```
➜  Hijack cat .from_admin.txt 
To all employees, this is "admin" speaking,
i came up with a safe list of passwords that you all can use on the site, these passwords don't appear on any wordlist i tested so far, so i encourage you to use them, even me i'm using one of those.

NOTE To rick : good job on limiting login attempts, it works like a charm, this will prevent any future brute forcing.
➜  Hijack
```

From this note we can tell there's a user called `admin` and he made a password list containing safe passwords. Also he says something to the user `rick` about rate limiting login attempts inorder to prevent future brute force attack

Cool so let's move to the webapp

One thing we can try here is to attempt brute force on ssh on user `admin / rick / root` with the password list but that won't work :P

Time to move to the webapp 
![giphy](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/09557d16-86b1-4eaf-834e-ec228f5613f5)

Going



![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cc9766c7-0691-4712-b222-8c1f12bf0e5b)
