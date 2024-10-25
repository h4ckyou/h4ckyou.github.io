<h3> Gonavision AfriHackBox </h3>

![image](https://github.com/user-attachments/assets/ff27ee41-d2d1-4088-aa7d-4301b8f5dfa0)

Hi, this is my first writeup for the AfriHackBox platform and i'll be showing you how I solved the Gonavision lab

So first things first we need to get the list of open ports on the host and my preferred choice of doing that is `rustscan & nmap (cause why not??)`
![image](https://github.com/user-attachments/assets/04daec19-5286-410c-9367-43b0b5d5d550)
![image](https://github.com/user-attachments/assets/54ba563d-4057-46b0-9af0-bb6e8c8cf7c2)

```r
- rustscan -a 10.0.1.5 -r 1-65535
- nmap -sCV -A 10.0.1.5 -p80
```

Going over to the web service running shows this
![image](https://github.com/user-attachments/assets/fb3cf5ad-3060-4b0a-8a5c-3e5f5c9aa5bd)

Trying some sqli as the username/password doesn't work so i moved on from messing with the login page

From this we can tell that this is an application created by `Nikhil Bhalerao` so the ideal thing is to probably search up "RedCock Farm" and see what comes up

But now, I didn't solve it that way and i'll show you how i did it

What I did next was to fuzz for files and specifically `php` because the application programming language is that 💀

Ok so we got various files

![image](https://github.com/user-attachments/assets/a7643970-f9da-4ca7-b722-871bdbf7d884)
![image](https://github.com/user-attachments/assets/f82ea3b7-1c1b-45f2-a5a4-a77fba8bb7d1)

The `register.php` looks interesting because if we can register a user then we can probably login and see other functions we can access

Another interesting thing to note is that, even though the other files return a status code of 302, which implies a redirect, their content length is absurdly large and we'll get to that soon

So first thing i did was to try register
![image](https://github.com/user-attachments/assets/c152a39b-8b3f-4412-99d7-787b2ab9ba72)
![image](https://github.com/user-attachments/assets/063c5283-8901-4344-b968-e5cf4e92ee40)

But after submitting the form i got this error, dang!
![image](https://github.com/user-attachments/assets/30037d8b-d2e2-484e-bbcd-a3bc01aa18fe)

This means we can't register a user (it seems!)

What next?

Well time to check out why those files which were supposed to do a "redirect" happens to have a large content length

If we try access it we will notice that it immediately redirects to the `/index.php` file



































