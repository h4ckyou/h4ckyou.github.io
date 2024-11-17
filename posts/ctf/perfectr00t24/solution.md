<h3> Perfectroot CTF 2024 </h3>

![image](https://github.com/user-attachments/assets/b55b9b6d-8b2c-429a-bd9f-b2542a787953)

Hey guys, 0x1337 here! Over the weekend I participated in this CTF with team `One Piece`

We ended up placing first so GGs to my team mates and every one
![image](https://github.com/user-attachments/assets/b15e30fe-d482-45c8-bd19-28aa3aad45a9)

I played as `ptr` btw
![image](https://github.com/user-attachments/assets/370d8198-f5fe-4c1a-ae6b-d950b1eff119)

I'm making this writeup because of the writeup contest lmao (i'm too tired to make it though)
![image](https://github.com/user-attachments/assets/6d9a5a42-50bc-4801-9c6c-94eae78b55a3)

Anyways I don't plan on making the solutions to all the challenges I solved but rather Pwn, Rev and Web
![image](https://github.com/user-attachments/assets/df755a22-23e7-4252-9e9e-b56a2228e82b)
![image](https://github.com/user-attachments/assets/cefac533-589c-4c64-b5de-707fc900547b)
![image](https://github.com/user-attachments/assets/6d01822d-971d-47d7-8673-fcbf0047cefc)

## Pwn
- Flow
- Nihil
- Daily Routine
- Heap Wars
- Heaps Don't Lie
- Sea Shells
- Arm and a Leg

## Rev
- Hackers Catch
- Re-Incarnation
- Hackers Catch 2
- Go Dark
- Box
- Pores

## Web
- Console-idation


### Pwn 7/8 :~

#### Flow
![image](https://github.com/user-attachments/assets/5fb6d5b0-074f-4859-bce8-c3a44eb5ddfb)

TD;LR -> Variable overwrite

I downloaded the attached file and checking the file type shows this
![image](https://github.com/user-attachments/assets/a919c171-5503-44fa-a3dd-903e5eea7334)

So we're working with a 64bits executable which is dynamically linked and not stripped

From the protections shown by `checksec` we can see just `PIE and NX` enabled

Moving on, I ran the binary to get an overview of what it does









