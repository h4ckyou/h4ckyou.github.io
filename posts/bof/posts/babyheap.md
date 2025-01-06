<h3> Pwn Writeup </h3>

- BabyHeap (Dcquals 2019)
- File: [chall](https://github.com/guyinatuxedo/nightmare/tree/master/modules/29-tcache/dcquals19_babyheap)

Hi there, recently i've been trying to learn more on heap exploitation so i decided to make a writeup on how i was able to solve this challenge

## Recon

We are given a binary and it's libc
![image](https://github.com/user-attachments/assets/57f89f86-3dca-4480-aa0f-3d5944d3624e)

The first thing I always do is patch the binary to use the provided libc. This ensures that I am working with the correct version, which matches the one used on the remote instance.
![image](https://github.com/user-attachments/assets/8928dfa7-3b12-4f11-94ec-22d2c7a198d7)

```
cmd: pwninit --bin babyheap --libc libc.so.6 --no-template
```

Now time to start, first i'll check the type of file i'm working with then the protections enabled.
![image](https://github.com/user-attachments/assets/f6c615a4-5c93-4d5f-ba55-6d788f790af1)

As you can see from the image above, we are working with a 64 bits executable and it has all protections enabled (sheesh!).

We also need to know the libc version we're working with
![image](https://github.com/user-attachments/assets/69602119-9485-4907-8451-5383c8733a1d)

This is `glibc 2.29` 

Running it we get this four options which we can choose from
![image](https://github.com/user-attachments/assets/928c903a-a01f-4b3d-8154-bba8c28d7d5d)

Time to fire up IDA to reverse this

```
Note: the binary was stripped so i had already renamed variables, data types, function names
```
