<h3> KnightCTF 2024 </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/028cfd1b-0727-4d3d-8b0f-f89a05bf2bb0)

During the weekend I and my team mates from `@error` participated in the ctf and we ended up 11th on the leaderboard
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a04f7e92-2c5a-4f04-a8ea-94e112506552)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/40c61e84-0ca1-4bcc-b723-2c9267e3a9d9)

With me playing as user `0x1337` I solved challenges from various categories like:
- Pwn
- Reverse Engineering
- Networking
- Web

I solved all challenges from the first 2 categories and I'll be dropping my solve scripts (currently too lazy to make a writeup)

To view my solve scripts checkout: [here](https://github.com/h4ckyou/h4ckyou.github.io/tree/main/posts/ctf/knightctf24)

I didn't drop solve script for the first & second rev because they can be solved without writing a script cause:
- REV1: The password expected is stored as a variable so we can just decode it and reverse the string (endianess)
- REV2: Uses `strcmp` on our input against the expected string

The catch in all the reverse challenges was that they were all `Statically Linked & Stripped`.....So figuring exactly the functions being used was the main thing for the second rev I suppose

Anyways that's all

GGs to my team mates!!
![certificate](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ba0dd700-d752-4722-b425-3f9f720f1d90)
