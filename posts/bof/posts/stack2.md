<h3> AD World Challenges </h3>

- Name: Stack2
- Source: [chall](https://adworld.xctf.org.cn/media/file/task/3fb1a42837be485aae7d85d11fbc457b)
  
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/81c32a17-233b-412d-acf0-db0748e6e314)

**File Checks**

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2ccf4116-0ba9-44eb-9e2a-a0750b72403f)

So we are working with a x86 executable which is dynamically linked and not stripped

And the protections enabled are: Canary & NX

Running the binary to get an overview of what it does shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3ca880da-0072-4aec-90d3-2ededf7d4947)

Basically this binary provides us with a calculator like structure where we can perform about 4 operations on
- Show numbers
- Add number
- Change number
- Get average

Now that we know that I decided to decompile the binary inorder to reverse it and find the vulnerability

**Reversing**
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ac90000d-e2fa-4a06-a0bc-4f3530816523)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/722cf5e6-ce1c-4ff0-ad11-c66d86961015)

I will look through what each function does and explain 🙂

First it will receive the number of integers we want to store in the array with it's value











