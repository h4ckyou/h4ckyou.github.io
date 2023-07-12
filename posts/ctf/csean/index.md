<h3> CSEAN CTF 2023 </h3>

### Description: This was a fun ctf I participated and it taught me new things >3

<h3> Challenge Solved: </h3>

## Forensics
-  Communication Is Key

## Malware Analysis
-  Two Way Street

## Misc
-  Welcome! Welcome!

## Pwn
-  ChatterBox

## Web
- Play By EAR 
- Enum Enum 
- FirstOfWAF  
- Handover
- Report Phish 
- Stupid Reset
- Handover 2


### Forensics 1/1:~

#### Communication Is Key
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5e2a7a4f-40a9-44c6-b0c2-48a00ebf1d39)

After downloading the attached file checking the file type shows that it is a windows executable
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38f3d7e1-a260-4a34-bcd6-713f82f383b4)

I normally would try decompile it in ghidra but I don't like decompilling .exe file in ghidra 

So instead what I did was to run it

Doing that I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0e868522-6cf0-45ed-9bbc-c025f7587896)

From the challenge name `communication` it is likely making some sort of requests 

So confirm that I opened wireshark then listened on all network interface
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5ddbf73a-26a9-4def-8b27-755ea49f2e1d)

Then I ran the binary again and got this 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b51361d1-2c72-4296-87f0-d789b6b1a25a)

There are http packets

I followed tcp stream and got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a7f6316-899c-4db6-8296-31b503929c35)

Also this binary is a python compiled binary

We can either confirm this by decompilling it or from the user agent we can see it's python2.8

Anyways since we got the flag what's the use of going through that

```
Flag: csean-ctf{CommunicationIsKey_NO_DOUBts!}
```

### Malware Analysis 1/1 :~

#### Two Way Street 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e14da56-e726-4b2e-a2e7-01b80b52c0a3)

I am not a Malware Person but luckily this wasn't tough

First thing I did was to check the file type
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/14bd9c92-644e-4f09-b48c-70ba48d3993d)

A windows executable

I uploaded it in [virus total](https://www.virustotal.com/gui/home/upload) 

And on checking the details I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e14ded4d-0318-4444-b78d-7dcba8b3e98b)

It's also a python compiled binary

Next thing is to convert it to a `.pyc` file then decompile the `.pyc` 

To convert it to a `.pyc` file I used [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor) 

Here's the resource that helped me out [hacktricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-methodology/specific-software-file-type-tricks/.pyc) 

