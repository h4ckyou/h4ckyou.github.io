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
- First I'll need to get the current captcha from the image so that I can send the first captcah request with it's value
- Using tesseract which is an OCR tool I can extract the text from the image
- Then do a while loop to repeat the process till the capcha check is completed

That sounds easy writing **that** but the script took me some good amount of time debugging 😂

Here's my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/uctf/web/Captcha1/solve.py) and I must admit it takes about 12minutes

But after running the script

And back on the web page I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0a7edada-b61b-4fab-b4c0-34b8d2c9a07c)

#### Captcha2 | the Missing Lake
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/219d75b7-644d-434b-92ac-186076d9e535)

No link is given but we can just guess the url since the first one was `https://captcha1.uctf.ir/` then the second should be `https://captcha2.uctf.ir/`

Going over the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1441d150-86d4-48a4-8a32-24d46cafb8f8)

This one is actually slight difficult than the first one because it deals with animal images and not text in an image

But we can do it manually since it's just 100 captchas

----- Will try solve it by automating -------

#### MongoDB NoSQL Injection
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b772a480-0009-4b97-8133-7299c55c2bf7)

From the challenge name we can tell we will be doing NoSQL Injection

Going over to the url shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3593ab49-4297-403d-86c0-9243e8442ff3)

We have a login page but since no credential was giving let us try bypass it using NoSQL Injection

I used burp to intercept the login request
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/15a311ff-124d-446b-89b0-3cb5ade06d90)

Failed login request just redirects to `/login`

Notice the header
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7b7848bf-df6e-4bc2-b54e-43909cf8e081)

It's running Express server which is like NodeJS and usually the database that runs on NodeJS is MongoDB

Also because of this we can pass the parameters in form of json
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/19231513-689d-45b3-8f74-fe503e1102e2)

We can see that on forwarding the request it works 

To check for NoSQL Injection I used the not equal `$ne` parameter 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b1d8f98f-ccd9-4d1d-8fd8-cdec64d86ea4)

```r
{"username":{"$ne":"uche"},"password":{"$ne":"uche"}}
```

What that does is to tell the MongoDB that the value of `username` is not equal to `uche` which is True because the database doesn't have any username as `uche` also the same applies to the password

With that the login will be successfull

By intercepting the login request and modifying it to that payload I was able to bypass the login page
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0dc5ac97-3fd6-458a-bfa6-27a9d4381b96)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/86bda8f4-1e90-4c28-8b25-c7b6ff6089f6)

In the home page we can search for a user

But when I tried searching for some names it didn't return any result

There's a `/users` endpoint but that gives this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e6fd12f6-87fc-4713-a03a-e506477237d5)

So we need to find a way to get the users

We can take advantage of the NoSQL injection to dump the users from the username column

The way to do it is by using regular expression

So basically this:

```r
{"username":{"$regex":"^"},"password":{"$ne":"uche"}}
```

That will return True and get us logged in because `^` is a wildcard which 
