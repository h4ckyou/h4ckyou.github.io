<h3> Fetch The Flag CTF </h3>

![image](https://github.com/user-attachments/assets/0e0fd28f-0748-4ce2-b415-f7b68321237f)

This is my writeup for some of the challenges i solved

I did solve all reverse engineering but i was really busy with school so hence my writeup coming late

### Challenge Solved (not based on difficulty)
- Crab Shell
- Letter To Nums
- Math For Me
- PShell
- It's Go Time


#### Crab Shell
Checking file type
![image](https://github.com/user-attachments/assets/0de1fe75-3fef-4e22-b5fd-ac0e4b3636ae)

Running strings we get this
![image](https://github.com/user-attachments/assets/f0f01a67-9069-41ad-bf93-45aaff58376c)

This is a rust compiled program, we can also confirm by grepping it
![image](https://github.com/user-attachments/assets/f7c1de05-7134-4cd7-a154-a81f64bca683)

Running it we get this
![image](https://github.com/user-attachments/assets/6b828840-480a-408e-953b-68ff32dc2423)

It asks for a 16 byte key and it does validate the input length

Loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/8e4ce70e-9222-4692-95f6-c15a60a7c57a)

I'm not so much familiar with rust reversing cause i don't know rust but i've looked at one or two decompilation before so i'm certain that the main program logic at `crabshell::main`

Decompiling it we have this
![image](https://github.com/user-attachments/assets/f3d9428e-7655-4535-b12d-ae24cbf19b6f)
![image](https://github.com/user-attachments/assets/cca302e1-cf63-4f6c-a1de-873b991204f7)











