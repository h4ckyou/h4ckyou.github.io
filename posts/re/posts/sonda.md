<h3> Sonda </h3>

A fun reverse engineering challenge ;)

Let's get to it!

We are given a binary and checking the file type shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9c1e35f9-5975-41a7-936c-5487110b5854)

We're working with a 64bits binary which is dynamically linked and not stripped

I ran it to get an overview of what it does
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c5acd958-2bf9-4805-8241-d81045407860)

Seems it requires a magic number which i don't know

Let's get on with reversing it which in this case I used IDA
