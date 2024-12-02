<h3> Conundrum 2 </h3>

Hi there, some months ago I was given some set of challenges made by `mug3njutsu` for a ctf he wrote challenges for but it got no solve
![image](https://github.com/user-attachments/assets/fa8fff24-d0ed-4eeb-8872-0e5d51771af0)

So I decided to tackle them and was able to solve 3/4 of the challenges for which i made a solution [here](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/writeup.md)

The last one i wasn't able to do it
![image](https://github.com/user-attachments/assets/4fa437ad-10f4-4fa1-8a08-0adb088bb05f)

At that time i wasn't so much familiar with various techniques so i thought it was a format string one shot sort of exploitation (maybe that's still possible im just not that good yet! 😅)

I still had the challenge file saved and while scrolling through challenges i should tackle today i came across it and decided to give it a shot
![image](https://github.com/user-attachments/assets/9ca2ec2f-51ab-44fc-bcd2-f722bb76d09b)

Now then let's start :)

The challenge came with its glibc file and linker, so the first thing I did was patch it to ensure the same libc would be used on my device as on the remote
![image](https://github.com/user-attachments/assets/830a5e52-5eb0-4b59-95ee-93970a7e6747)

```
pwninit --bin conundrum_v2 --libc libc.so.6 --ld ld-linux-x86-64.so.2 --no-template
```

Next thing is to get an idea as to what type of file we are working with and the protection enabled on it
![image](https://github.com/user-attachments/assets/570f7798-cc6b-48b7-9852-b1ebbb85cd9f)

We can see that it is a 64 bits executable which is dynamically linked and not stripped and from the protections enabled it's clear that only the stack canary is disblaed

Now i ran the binary to get an overview of what it does
![image](https://github.com/user-attachments/assets/9a53e7ee-9c3d-46bc-9525-584b49ec9b4b)

It seems to print some menu, receives our choice and based on the choice provided does some other stuffs

With that in mind i 
