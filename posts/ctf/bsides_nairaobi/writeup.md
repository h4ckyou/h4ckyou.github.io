<h3> Bsides Nairobi 2023 </h3>

### Pwn Challenge Writeup:
- Conundrum
- Simple

This challenges were made by @mug3njutsu and I really enjoyed solving it :)

### Conundrum

Attached file: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/bsides_nairaobi/Conundrum/conundrum.zip)

We are given a zip file which contained a binary, libc and ld file when decompressed

First thing I did was to patch the binary using [pwninit](https://github.com/io12/pwninit) so as to make sure the binary uses the same libc as the remote instance does 

Now I checked the file type and protections enabled on it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6838a330-70e3-4c2f-8127-6d179b3dbe66)

So we're working with a x64 binary which is dynamically linked and not stripped

And from the result gotten from running `checksec` we can see that all protections are enabled!
