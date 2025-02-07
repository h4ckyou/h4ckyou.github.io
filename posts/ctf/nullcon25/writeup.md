<h3> NullCon HackIM CTF Goa 2025! </h3>

![image](https://github.com/user-attachments/assets/2b329447-2314-45ac-b6d0-354a48adf30b)

Hi there, this is my writeup to the challenges I solved

I participated with team `QnQSec`
![image](https://github.com/user-attachments/assets/f6507fc0-8b88-4f31-bc95-77f3f0c20a2b)

### Pwn

#### Hateful
![image](https://github.com/user-attachments/assets/0c01849d-1be9-4300-8030-6a22899f3178)

We're given the libc and linker file as well as the binary, first thing i did was to patch it using `pwninit`
![image](https://github.com/user-attachments/assets/ea897b75-497d-42a0-8f0f-a69eabdf2a5f)

When we run it we either get to choose `yay or nay`

Checking the protections enabled on the binary shows this
![image](https://github.com/user-attachments/assets/6fd32695-12e9-4c1c-b507-2dc54bbc6e86)

Ok not much of a protection enabled here, loading it up in IDA here's the main function
![image](https://github.com/user-attachments/assets/28c564e4-95a7-4427-bf96-1a7425c8f446)

So if we choose `yay` the `send_message` function gets called
![image](https://github.com/user-attachments/assets/7a97c9ad-6668-422a-86b9-8caf98bd479f)

We see there are two bugs here which are a format string bug & a buffer overflow

The goal is simple, we first use the fsb to leak a libc address then we leverege the overflow to perform a ret2libc

In order to leak libc we can just leak pointers on the stack, but because pie is disabled i just decided to leak it by reading the value of the got of printf

Here's my exploit [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/nullcon25/Hateful/solve.py)
![image](https://github.com/user-attachments/assets/e353d2af-9a47-4321-bb58-d41f30cfd317)

Running it on the remote instance works
![image](https://github.com/user-attachments/assets/ecf1978d-f73d-4b7a-8047-9bf3f1468259)

```
Flag: ENO{W3_4R3_50RRY_TH4T_TH3_M3554G3_W45_N0T_53NT_T0_TH3_R1GHT_3M41L}$
```

Fun fact, during the competition the libc didn't work for me, so i had to leak the got of printf then used a libc [database](https://libc.rip/) to retrieve the right libc being used remotely

#### Hateful 2
![image](https://github.com/user-attachments/assets/d4def1c1-b27d-4006-baa8-302f903bed17)

Starting off i patched the binary
![image](https://github.com/user-attachments/assets/a30b10a4-cac6-4079-a6ed-24473dac87b5)

We can see that all protections are enabled

Running the binary shows this menu like option
![image](https://github.com/user-attachments/assets/d527d1c6-2db5-4387-92cd-e1c2f5f7957f)

We can assume this is probably going to be a heap exploitation

I loaded it up in IDA and here's the main function
![image](https://github.com/user-attachments/assets/34ec67ef-b066-4e54-a546-f5c6d433ee55)

The binary isn't striped so there's no need for reversing much here

I'll walkthrough the important details of what each function does

`about_us`:
![image](https://github.com/user-attachments/assets/b63ecdad-e040-430c-811b-f7ae344366ea)

- This function essentially leaks a stack address, so let's keep that in mind

`add_message`:
![image](https://github.com/user-attachments/assets/cd8bf061-2ff7-4d79-a219-2ce7ae8a3f31)

- We can only make up to 16 allocations
- We control the size of the memory to be allocated

`edit_message`:
![image](https://github.com/user-attachments/assets/105d9a65-b317-4ee8-ad52-7bfa13a70ee9)

- This is used to edit the content of the memory stored in the global allocations variable at the specified index

`view_message`:
![image](https://github.com/user-attachments/assets/b1fdb0aa-45d8-4734-a66f-bcfd72a0e862)

- Prints the content of the memory at the specified index of the allocations variable

`remove_message`:
![image](https://github.com/user-attachments/assets/a323ec54-e7d2-47e6-96f9-90a8c6daccc7)

- Used for memory deallocation
- It doesn't set the memory freed to null so a UAF is possible

Based on what we've gathered so far, this is just a standard heap exploitation and the vulnerability is a UAF

Which we will leverage that to get code execution

We are working with glibc 2.36
![image](https://github.com/user-attachments/assets/53d3d4c3-b67d-4272-8573-380679b1800a)

So that version has safe linking enabled and no hooks, but because we have a stack leak we can write over main return addres our ropchain








