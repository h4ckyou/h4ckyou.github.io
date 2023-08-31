Here's the writeup I put up on my team mate blog: @[writeup](https://github.com/vikialora/Writeups/blob/main/EcowasCTF/Prequal/writeup.md)

#### Fafame
![](https://hackmd.io/_uploads/By6u5Q5an.png)


Going over the url shows this
![](https://hackmd.io/_uploads/rJTcq75a3.png)

We have the option to register and login

So I will register since I don't have any credentials

After I registered I got this
![](https://hackmd.io/_uploads/Hya6cX5a3.png)
![](https://hackmd.io/_uploads/Hyj09m5T2.png)

From that we can see we would be able to write any html tag but javascript is disabled

When I clicked create `New` note I got this
![](https://hackmd.io/_uploads/SkA-sX9an.png)

I can inject any tag I want
![](https://hackmd.io/_uploads/HJ_XjXcT2.png)

After creating it I got this
![](https://hackmd.io/_uploads/rJh8i7q63.png)

Ok it actually allows any tag 

But it isn't executed

We can share the note to the admin
![](https://hackmd.io/_uploads/S1idi7963.png)

I tried to inject script tag to alert 'test'
![](https://hackmd.io/_uploads/r1kbh79T3.png)
![](https://hackmd.io/_uploads/rktLnX96h.png)

But it didn't work though the tag is there

The interesting thing to think is that why isn't that javascript executing?

Well if you take a look at debug console you will see this
![](https://hackmd.io/_uploads/Sy65379a3.png)

There's CSP which would prevent us from performing XSS

But actually the response gives the nonce
![](https://hackmd.io/_uploads/H1zlp79a3.png)

So because we have that we can bypass the CSP

Looking around the web app shows this function
![](https://hackmd.io/_uploads/ryKfTX5T2.png)

We can reset our password

Now this is interesting because we know that we can share our note to the admin user and we have XSS 

So this gives us an opportunity to escalate the XSS to CSRF
 
This is the request made when resetting a password
![](https://hackmd.io/_uploads/rkjspX963.png)
![](https://hackmd.io/_uploads/H1f5aX9T3.png)

We can now leverage this to change the admin password

Here's the exploit script

```js
<script nonce=2726c7f26c>

  const url = 'https://ctftogo-b6247a6b4d3c-markdown-1.chals.io/profile';
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'password=chained',
  });

</script>
```

I created a note with that content
![](https://hackmd.io/_uploads/BkTZCXqT3.png)

Then I shared it to admin
![](https://hackmd.io/_uploads/S1Cr0Xqan.png)

We can now login with `admin:chained`
![](https://hackmd.io/_uploads/r1JsAmca2.png)

And the flag is shown after login in

```
Flag: flag{look_at_me_im_the_admin_now} 
```
