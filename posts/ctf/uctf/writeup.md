<h3> UCTF 2023 </h3>

I played this ctf with my friends

Here's the writeup of the challengs solved:

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

With this we can basically read local file off disk 
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/b6cb54c6-7e8a-4353-90e3-7ea3a536c427)

```r
curl -s -X POST "https://ecorpblog.uctf.ir/api/view.php" -H "Content-Type: application/json" -d '{"post":"file:///etc/passwd"}' | jq .post -r
```
