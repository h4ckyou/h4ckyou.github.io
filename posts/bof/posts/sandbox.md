<h3> Sandbox </h3>

This was a binary I saw saved on my laptop I usually do that cause in CTFs I might not be able to solve lot of the pwn or other challenges so I usually save it randomly in my filesystem 

While I was less busy I saw it and said hmm let me give this a shot!

So here we are and I'll give you my solution used to solve it

First thing we'll check the file type and the protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7fddcda1-be63-4323-a703-3766620adc46)

Ok we're working with a x64 bit binary which is dynamically linked and not stripped 

From the result of checksec we can see that all protections are enabled 

I ran it to have an understanding of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/985dd096-c94f-4d85-b76b-7e4347408a03)

It just receives our input and prints it out back and that's done in a while loop
