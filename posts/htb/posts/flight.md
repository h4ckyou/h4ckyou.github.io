<h3> Flight HackTheBox </h3>

Difficulty = Hard

Nmap Scan:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c012e655-7e5c-4c31-8bf3-d31ab3d068d6)

We can see the domain name *flight.htb* I added it to my */etc/hosts* file

So there are lots of port but lets start enumerating

Checking smb doesn't allow anonymous listing of shares
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9296cc02-c57a-4eda-9c4a-b4541a8bd824)

Moving over to the web server on port 80 shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/432b7a5c-8c37-426f-bb93-f8540d78ca8f)

There's nothing really there

So lets fuzz for subdomains
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/129097e3-8909-4f06-90f0-5e255ca79ee2)

I'll update my */etc/hosts* file with the new sub domain

Checking it shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/73ecbdbf-a6f4-4915-bb3d-6d665b840d05)

When I clicked on the home button i get this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c2c901e0-2e9f-4b5b-84ed-e551893e52db)

Noticing the url we can see that it's including the file *home.html*

We can say that this is vulnerable to local file inclusion lets confirm it 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1c0a9997-6e39-48e1-be14-a0bfa3c115f0)

One way we can exploit this is by trying to perform ntlm hash theft 

Using responder i'll steal the ntlm hash
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6c41a537-551f-4fe6-aaa5-c3c21bcec541)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a55adb5c-80f3-49a1-b3fa-854601f3a899)

While on the web server I'll do this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/890cf68a-99be-4947-843f-862fa322773f)

Back on responder I got the hash for user *svc_apache*
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b99248b3-00e9-4a8a-bb67-67b1977a0eed)

I brute forced it using JTR 
