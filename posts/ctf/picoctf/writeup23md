<h3> PICOCTF '23 </h3>

#### Description: This was a fun ctf i participated in with team 8h037. I really learnt a lot during this ctf thanks to the organizers for bringing such a good challenge
![image](https://user-images.githubusercontent.com/113513376/228130926-bc6f29e7-1276-47d0-9a00-f04321d01b82.png)

<h3> Challenge Solved </h3>

## General Skills
- Chrono
- Money-Ware
- Permissions
- Repetitions
- Useless
- Special
- Specialer

## Forensics
- HideMe
- PcapPoisioning
- Invisible Words

## Reverse Engineering
- Ready Gladiator 0
- Reverse
- Safe Opener 2
- Timer
- No Way Out
- Ready Gladiator 1
- Ready Gladiator 2

## WEB
- FindMe
- MatchTheRegex
- SOAP
- More SQLi
- Java Code Analysis

## Cryptography
- HideToSee
- ReadMyCert
- Rotation
- SRA

## Binary Exploitation
- BabyGame01
- Two-Sum
- BabyGame02
- Hijacking
- Tic-Tac
- VNE
- HorseTrack

### General Skills 8/8 :~

#### Chrono
![image](https://user-images.githubusercontent.com/113513376/226774724-2da29127-0d1c-46db-b704-61e5f2edc084.png)

We're given a ssh instance to connect to after loggin i looked back at the description and saw its referring to automating task on linux 
![image](https://user-images.githubusercontent.com/113513376/226775361-d0b4f42b-daf9-4341-bd4a-4486a5c60280.png)

And that means likely cron jobs

So i checked the cron jobs and got the flag
![image](https://user-images.githubusercontent.com/113513376/226775428-e6365e90-03e1-48b3-87fe-14bda5483aa4.png)

```
Flag: picoCTF{Sch3DUL7NG_T45K3_L1NUX_d83baed1}
```

#### Money-Ware
![image](https://user-images.githubusercontent.com/113513376/228133106-71cff255-6497-409e-9be8-59bf0d62018f.png)

We're given an address which looks like a btc address and we're asked to submit the malware name

So i just paste the address on google then saw this
![image](https://user-images.githubusercontent.com/113513376/228133217-54ab6dff-17a0-450d-b851-74738b819258.png)

The second link looks promising then i checked it [Link](https://www.cnbc.com/2017/06/28/ransomware-cyberattack-petya-bitcoin-payment.html)
![image](https://user-images.githubusercontent.com/113513376/228133283-0ab1e126-d01a-4652-bc7a-4873895d363a.png)

Below the news on the cyberattack shows a malware name
![image](https://user-images.githubusercontent.com/113513376/228133403-441edd7e-c1e5-48ba-973d-84170217ec17.png)

```
Flag: picoCTF{Petya}
```

#### Permissions
![image](https://user-images.githubusercontent.com/113513376/226775869-8adc022c-b6da-4796-b033-32f66b3532f7.png)

After connecting to the ssh instance i checked what the user can run as root `sudo -l`
![image](https://user-images.githubusercontent.com/113513376/226776108-f730984c-11e1-4afa-936a-b7625653efc3.png)

So the user can run `/usr/bin/vi` as root

Checking [gtfobins](https://gtfobins.github.io/gtfobins/vi/#sudo) I got a shell escape command 
![image](https://user-images.githubusercontent.com/113513376/226776338-a4d0b355-eeb4-4d49-872c-7bee9824a2d5.png)

```
Flag: picoCTF{uS1ng_v1m_3dit0r_ad091ce1}
```

#### Repetitions
![image](https://user-images.githubusercontent.com/113513376/226776787-e19f128f-8336-4939-8dbb-e3cc858a5168.png)

After downloading the enc_flag and checking its content i see that its base64 encoded
![image](https://user-images.githubusercontent.com/113513376/226776959-597fda93-492f-4cc1-b18d-de677826261e.png)

I tried decoding it but i get another base64 encoded value
![image](https://user-images.githubusercontent.com/113513376/226777033-f7446716-a37e-4867-9247-8012926873de.png)

From the challenge name `repetition` its likely this has been encoded multiple times 

So I wrote a script to decode it until it isn't a base64 encoded value again [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/web/repetition.py)

Running it I got the flag
![image](https://user-images.githubusercontent.com/113513376/226778310-ca4955f7-a22d-4196-b1e7-44ba2f5ca099.png)

```
Flag: picoCTF{base64_n3st3d_dic0d!n8_d0wnl04d3d_4557ec3e}
```

#### Rule 2023
![image](https://user-images.githubusercontent.com/113513376/226778508-8f53f3c2-a96d-4223-92dd-acaaea3e96d9.png)

Checking the link provided doesn't show the flag
![image](https://user-images.githubusercontent.com/113513376/226778573-cb2b0be9-2069-407f-9f7d-cb9036255a7e.png)

But after checking source code and using `CTRL +F` I got the flag
![image](https://user-images.githubusercontent.com/113513376/226778655-0a37b9ed-18a6-43ed-8639-04418493b987.png)

```
Flag: picoCTF{h34rd_und3r5700d_4ck_cba1c711}
```

#### Useless
![image](https://user-images.githubusercontent.com/113513376/226778798-ddbe6cce-bd0f-4cb6-a46c-43c73fc494bd.png)

After connecting to the ssh instance i saw a file in the current directory of the user
![image](https://user-images.githubusercontent.com/113513376/226778921-715be6d3-b300-490f-bc88-6d1424421b9e.png)

And its a shell script 

From the challenge tag `man` I ran `man` command on the script and I got the flag
![image](https://user-images.githubusercontent.com/113513376/226779090-8a1c2a3f-c722-4703-b709-704c4334dd81.png)

```
Flag: picoCTF{us3l3ss_ch4ll3ng3_3xpl0it3d_7065}
```

#### Special
![image](https://user-images.githubusercontent.com/113513376/226779323-fc8c9283-c566-419b-99d9-322e44abfbee.png)

After connecting to the ssh server I get this weird shell
![image](https://user-images.githubusercontent.com/113513376/226779437-d7481695-8898-4c7f-813e-b482750bd846.png)

So it capitalize the 0th index of our input making us not able to run commands

What I did next was to find any special character value that won't be affected from the capitaliation of the 0th index of our input
![image](https://user-images.githubusercontent.com/113513376/226779885-11726bf6-bd01-4998-972a-db9075bc946e.png)

I did play around to get the value and `__|` worked well for me

Now we can just pass in any command we want to run 

From that I got the flag
![image](https://user-images.githubusercontent.com/113513376/226780057-93ba7140-09fe-42ca-93b0-91b7100d4928.png)

```
Flag: picoCTF{5p311ch3ck_15_7h3_w0r57_b741d1b1}
```

#### Specialer
![image](https://user-images.githubusercontent.com/113513376/226780263-30692113-af20-4210-a8d7-f56fae67c218.png)

Just like `Special Chall` after loggin I got into a weird shell that doesn't have much command
![image](https://user-images.githubusercontent.com/113513376/226780466-bb5980bf-597c-47df-9d0a-e23eef5b69be.png)

After trying some command I got that `echo` works 
![image](https://user-images.githubusercontent.com/113513376/226780589-80735891-7cde-4943-bde3-3367771ce81e.png)

And we can access enumerate files using echo + a wildcard (`*`)

I checked the files in the user's current working directory
![image](https://user-images.githubusercontent.com/113513376/226781072-3df55197-b3dc-467a-a943-ddb625acf92d.png)

Now we can use `echo` and get the content of a file to the standard output `stdout`

```
Command: echo $(</etc/passwd)
```

Trying that I got the flag
![image](https://user-images.githubusercontent.com/113513376/226781340-e35bbad6-82ef-4564-83ab-7e735733d1e1.png)

```
Flag: picoCTF{y0u_d0n7_4ppr3c1473_wh47_w3r3_d01ng_h3r3_c42168d9}
```

### Forensics 3/6 :~

#### Hideme
![image](https://user-images.githubusercontent.com/113513376/226781641-a9951b36-19c0-4103-8ea4-aef8cf817aa8.png)

First thing first I checked the file type after downloading the file given
![image](https://user-images.githubusercontent.com/113513376/226781764-e1bb25d0-fcc2-4aa2-8bc9-be7d97827aef.png)

It's a PNG file (image file) 

On viewing it just shows the picoctf logo
![image](https://user-images.githubusercontent.com/113513376/226782001-e9aeb48e-fecd-43bc-bb6c-63f8dcc645c5.png)

Now i check its metadata
![image](https://user-images.githubusercontent.com/113513376/226781868-5ec7ff65-fb32-447c-82c7-b88a8c46362d.png)

Running `zsteg` on it shows that there's a ZIP file embedded in it
![image](https://user-images.githubusercontent.com/113513376/226782101-5693c614-4b9a-4073-98cf-90a9befd0eb5.png)

So i'll use `binwalk` to extract it
![image](https://user-images.githubusercontent.com/113513376/226782188-72f886e2-f998-45ed-b239-25d7e84b3d86.png)

From there I got the flag

```
Flag: picoCTF{Hiddinng_An_imag3_within_@n_ima9e_85e04ab8}
```

#### PcapPoisoning
![image](https://user-images.githubusercontent.com/113513376/226782430-a25534cf-826a-47a1-b589-6b9abf9cfbf0.png)

After downloading the file attached I checked its file type which happens to be a pcap file
![image](https://user-images.githubusercontent.com/113513376/226782531-9de1359e-a0b3-4b21-a3b7-dcb2749daea5.png)

Then I tried low hanging fruits by running strings on it and got the flag
![image](https://user-images.githubusercontent.com/113513376/226782634-9c77e7ca-704e-47b6-b45f-ba4f63cc3635.png)

```
Flag: picoCTF{P64P_4N4L7S1S_SU55355FUL_4d72dfcc}
```

#### Invisible Words
![image](https://user-images.githubusercontent.com/113513376/226783355-d637c2e2-8fc1-449c-a192-b3e8b02f2065.png)

After downloading the attached file I checked its file type and its happens to be a bmp file
![image](https://user-images.githubusercontent.com/113513376/226783526-eb7f95bc-b950-49b2-b64f-f53f9da86b9e.png)

I checked the metadata of the file but I got nothing from it
![image](https://user-images.githubusercontent.com/113513376/226791222-1631a0c5-3f44-4d96-b880-ef5fd343c8ee.png)

I also ran various tools to check the file but I got nothing

Then after i checked the hex dump I noticed this
![image](https://user-images.githubusercontent.com/113513376/226783896-0d8bd721-4979-4530-ba79-ef4e0eb48d2e.png)

That is the file header for a zip file. You can check it out here [Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures)

So now the idea is that we can extract the values from that spot below 

But first I need to get what length it is from the zip file, and I used python for it
![image](https://user-images.githubusercontent.com/113513376/226784264-f74f7474-6cb1-4a41-9682-bb96216cefec.png)

So that means the zip file should start from offset `140` 

I wrote a script to extract the content of the zip file starting from index 140

Here's the script [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/forensics/invisiblewords.py)

After I run it, it dumps the zip file content
![image](https://user-images.githubusercontent.com/113513376/226786280-3ebec4b8-10ac-4d15-af68-63efb134ddbf.png)

Then I used `binwalk` to extract it's content
![image](https://user-images.githubusercontent.com/113513376/226786388-319f6cb9-fc96-484e-b4d9-6df8ca9c60b4.png)

From that I got the flag

```
Flag: picoCTF{w0rd_d4wg_y0u_f0und_5h3113ys_m4573rp13c3_5eadc23e}
```

### Reverse Engineering 7/9 :~

#### Reverse
![image](https://user-images.githubusercontent.com/113513376/226787298-3f870961-16ba-4be7-8d2b-34a0062b05f9.png)

After downloading the binary I checked what file it is
![image](https://user-images.githubusercontent.com/113513376/226787424-d48ebeb7-0cef-4607-bdf5-e8f5a30fff7c.png)

And its a x64 binary which is not stripped

So i'll run it to know what it does
![image](https://user-images.githubusercontent.com/113513376/226787535-652b7e31-e7ab-409a-8408-eb4957648d67.png)

Its asking for a password to unlock the file

Since I don't currently know it I ran `strings` to check for low hanging fruits

And from there I got the flag
![image](https://user-images.githubusercontent.com/113513376/226787715-b4b3a9e4-52a1-4a04-948b-e70aab5e08eb.png)

```
Flag: picoCTF{3lf_r3v3r5ing_succe55ful_d55531cd}
```

#### Safe Opener
![image](https://user-images.githubusercontent.com/113513376/226787855-d5749b1b-03d5-4393-94ac-ba34e11fcf82.png)

After downloading the file and checking its file type i got it to be a java compiled binary
![image](https://user-images.githubusercontent.com/113513376/226788013-a95569d2-e83e-4eea-b888-adf33bf05be6.png)

So I used an online [decompiler](http://www.javadecompilers.com/) to decompile the .class file to a readable format

After decompiling the binary I got the flag
![image](https://user-images.githubusercontent.com/113513376/226788376-78ee2258-8f7f-46f7-8c7b-2470dbda5bfb.png)
![image](https://user-images.githubusercontent.com/113513376/226788407-e685fd5a-ff78-4eff-b83a-8d2b0ce69121.png)
![image](https://user-images.githubusercontent.com/113513376/226788439-a08da371-af5c-4a95-b454-81e1878abab9.png)

```
Flag: picoCTF{SAf3_0p3n3rr_y0u_solv3d_it_b427942b}
```

#### Timer
![image](https://user-images.githubusercontent.com/113513376/226788726-7033f4e1-ca45-473a-852c-491795d90a6b.png)

After downloading the file given and checking its file type it turns out to be an apk file
![image](https://user-images.githubusercontent.com/113513376/226788883-eb63c81d-597e-49f9-b8ad-717aa2984d51.png)

So here's I did. First I unzip the content of the apk file then use dex2jar to convert the class file to a jar file which later i then use jd-gui to view the decompiled code
![image](https://user-images.githubusercontent.com/113513376/226789326-daf3693d-795b-430e-a3b6-9dd488a2404b.png)
![image](https://user-images.githubusercontent.com/113513376/226789516-8bb1f010-4a86-4eff-83cf-009254fda70e.png)

```
Flag: picoCTF{t1m3r_r3v3rs3d_succ355fully_17496}
```

#### Ready Gladiator 0
![image](https://user-images.githubusercontent.com/113513376/228129746-51381ebc-fe46-40fa-8907-371fecfd61e2.png)

After checking the attached file given i couldn't get what it does 

But i just connected to the netcat instance and got the flag
![image](https://user-images.githubusercontent.com/113513376/228130089-d8e9a1b1-a9ce-4e29-a969-36f5b75886f8.png)

```
Flag: picoCTF{h3r0_t0_z3r0_4m1r1gh7_a7bf8a57}
```

#### Ready Gladiator 1/2
![image](https://user-images.githubusercontent.com/113513376/226789810-abe5a448-fa22-4ea9-b737-d101543d5980.png)

This one I didn't even download the file but I searched for what CoreWars means then I saw this resources 
[CoreWar](http://moscova.inria.fr/~doligez/corewar/?fbclid=IwAR30dNfoG6Jg3TMocKKW2HxbmMHA-c509YIQkPuxtWi3v5BGtXkZ0eMhuuA)
[Payload](http://moscova.inria.fr/~doligez/corewar/rc/frenzyv6.txt)

And when I used the payload on the remote server it worked for both Gladiator 1 & 2

Running it for Gladiator 1 works
![image](https://user-images.githubusercontent.com/113513376/226790260-542b84f1-de63-4e6c-8536-bc71c5e7a7fb.png)
![image](https://user-images.githubusercontent.com/113513376/226790284-f9f1f310-d1b8-423c-a526-b34cd2525863.png)

```
Flag: picoCTF{1mp_1n_7h3_cr055h41r5_dba6f40d}
```

Running it for Gladiator 2 works 
![image](https://user-images.githubusercontent.com/113513376/226790409-7b443ee9-bf5a-4071-bab5-78260d9afb22.png)
![image](https://user-images.githubusercontent.com/113513376/226790454-27c215cb-2b28-450d-b522-5b1f0a1140cc.png)
![image](https://user-images.githubusercontent.com/113513376/226790547-d1421ab6-9e60-48a6-b393-7cc16c5c4662.png)

```
Flag: picoCTF{d3m0n_3xpung3r_106bc275}
```

#### No Way Out 
![image](https://user-images.githubusercontent.com/113513376/229038952-ff7284cb-8ee4-457f-8c15-4b627802c174.png)

We're given the files to download and i downloaded the type for windows

After downloading and checking it out, it shows the unity files for a windows game
![image](https://user-images.githubusercontent.com/113513376/229034711-04b2eaf6-506e-4308-93fb-cfe59362ba07.png)

When i treid playing the game initially, i noticed the player is like limited to crossing the boundry
![image](https://user-images.githubusercontent.com/113513376/229035071-1ac87aed-9ae0-47d1-944c-5c910db33f7a.png)

So after checking online for how to reverse unity file binary i got that you can edit the dll file for the game

And the particular .dll file we're looking for should contain the program logic

It was located here 
![image](https://user-images.githubusercontent.com/113513376/229035617-b84b7dff-0198-4191-b7e7-ca9631dce7db.png)

Using dnSPY, I can manipulate it

After searching around i then moveDirection variable and edited it to a constant value
![image](https://user-images.githubusercontent.com/113513376/229038669-7446d99f-b57e-4f57-b420-5184923ba38d.png)

Then on running the game again i got the flag after moving over the wall
![image](https://zeredy879.github.io/img/picoCTF2023/nowayout1.png)

```
Flag: picoCTF{WELCOME_TO_UNITY!!}
```

### WEB 5/7 :~

#### findme
![image](https://user-images.githubusercontent.com/113513376/226196980-2dc3639f-3416-4c2a-9ff4-c59aef2935ff.png)

We're given a remote instance to connect to which is a web server and its has a login form
![image](https://user-images.githubusercontent.com/113513376/226234296-933cbff0-a814-4806-b271-1df6b21edca7.png)

Since the description says we should login as `test:test1` lets try it
![image](https://user-images.githubusercontent.com/113513376/226234345-7aba1bbf-e0a1-4cfd-bd6d-891e1faa4463.png)
![image](https://user-images.githubusercontent.com/113513376/226234401-b183a10e-64ed-4869-9104-6a3192ea61ec.png)

While i was login in i noticed the url had some base64 values before it gets redirected to home page

So i'll login again but this time use burp to intercept the request
![image](https://user-images.githubusercontent.com/113513376/226234642-992c1394-fcdc-4fcc-8ae5-21c4d2be6dae.png)
![image](https://user-images.githubusercontent.com/113513376/226234711-433c8e3a-ae77-4a4f-9764-770381c653bc.png)

From here:

```
Right Click --> Do Intercept --> Response To Request
```

I got the first portion of the flag `picoCTF{proxies_al`
![image](https://user-images.githubusercontent.com/113513376/226235258-d7c6b8e7-d690-4ffa-83ba-e518f7c38a00.png)

After forwarding the request i get the second portion
![image](https://user-images.githubusercontent.com/113513376/226235383-24dbe6ec-40e2-4626-8ff6-f78ea3c749ab.png)

```
Flag: picoCTF{proxies_all_the_way_df44c94c}
``` 

#### MatchTheRegex
![image](https://user-images.githubusercontent.com/113513376/226236038-e623244f-76a6-4519-aadf-257bbd192feb.png)

Same as always we're given a remote instace which is a web server

Checking it out shows that it requires giving some text
![image](https://user-images.githubusercontent.com/113513376/226236178-fe11354d-9531-42cf-a316-2a4389e502c4.png)

Since i don't know the particular input to give it i checked the source code
![image](https://user-images.githubusercontent.com/113513376/226236255-a356eb4b-5121-4b7f-80c8-6004bbdc4a4b.png)

From the js portion of the script i saw the commented part of it 

```
		// ^p.....F!?
```

And its a regular expression which means:

```
1. "^p": Matches the start of a line or string, followed by the letter "p".
2. ".....": Matches any five characters except newline.
3. "F!?": Matches the letter "F" followed by an optional exclamation mark.
```

So the best value to be given is `picoCTF` 
![image](https://user-images.githubusercontent.com/113513376/226236705-e4643bd4-1960-4269-bf0b-8b55f8a5bea9.png)

After submitting it I got the flag
![image](https://user-images.githubusercontent.com/113513376/226236763-effd2655-d3b4-4960-be8b-83cdc2f23259.png)

Other form of value can be used like `pythonF, plololF` as long as it matches the regrex

```
Flag: picoCTF{succ3ssfully_matchtheregex_08c310c6}
```

#### SOAP
![image](https://user-images.githubusercontent.com/113513376/226237031-90e2bb58-5d52-40f1-a169-92025545fd3d.png)

Checking the instance given shows this
![image](https://user-images.githubusercontent.com/113513376/226237140-5a742f55-8db8-4c9a-b6f5-ce2da90ddb4e.png)

Clicking on `details` and intercepting the request shows that the data which it's trying to fetch is gotten using the xml format style
![image](https://user-images.githubusercontent.com/113513376/226237292-b3a77ab3-141d-4db9-981a-06d19ee8233a.png)

So since its this we can perform XXE

After checking [HackTricks](https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity) I made the payload to read the `/etc/passwd` file

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
<!ELEMENT data ANY>
<!ENTITY file SYSTEM "file:///etc/passwd">
]>
<data>
    <ID>&file;</ID>
</data>
```

On submitting that I got the flag
![image](https://user-images.githubusercontent.com/113513376/226237740-3c7b556f-6b87-4510-a74b-b9333ccf3f34.png)

```
Flag: picoCTF{XML_3xtern@l_3nt1t1ty_e5f02dbf}
```

#### More SQLi
![image](https://user-images.githubusercontent.com/113513376/226237913-bbe98b86-9897-4bd8-a3c3-fa43a3db0be8.png)

Checking the web server instance given shows this login page
![image](https://user-images.githubusercontent.com/113513376/226238001-5e21f53e-4277-4a8f-86bf-bc73b8255f81.png)

From the challenge title which is `SQLi` i'll try using sql injection to bypass the login page

```
Username: ' or 1=1 --
Password: ' or 1=1 --
```

Trying that works
![image](https://user-images.githubusercontent.com/113513376/226238142-1ea000a6-f98e-4bd8-9863-bc945b62d6c7.png)

There's another search functionality in the web app

So i'll search for something then intercept the request with burp
![image](https://user-images.githubusercontent.com/113513376/226238278-3ee33cdc-d8b1-4942-8455-60537cf3470a.png)

Then i will save the request in a file 
![image](https://user-images.githubusercontent.com/113513376/226238696-f125d72f-054f-47df-be34-90bcb75505e6.png)

With this i can use `sqlmap`
![image](https://user-images.githubusercontent.com/113513376/226238857-95a69707-23ad-4283-96be-9cef44b9c4c9.png)

Then I dump the whole table to see if any thing is of interest there 
![image](https://user-images.githubusercontent.com/113513376/226239183-9be7000a-89aa-41bc-bb45-2ef75238774c.png)
![image](https://user-images.githubusercontent.com/113513376/226239219-399755f0-5d37-4094-a5e8-06a027c69f77.png)

```
Flag: picoCTF{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_783cc6bd} 
```

#### Java Code Analysis!?!
![image](https://user-images.githubusercontent.com/113513376/226239434-16913e35-bdc2-4972-8529-1ee72cdd8075.png)

The web server source code is given

After checking it this is what i found interesting
![image](https://user-images.githubusercontent.com/113513376/226240120-d3ee6b98-ee73-4759-892d-cb7a53aa4ae1.png)
![image](https://user-images.githubusercontent.com/113513376/226240396-4179df0e-0cd3-47c7-bc36-f8b59ac08b22.png)
![image](https://user-images.githubusercontent.com/113513376/226487093-4c897912-5653-4995-b8b6-cf4be3eaf75c.png)

So the key is the secret key for the jwt which is `1234`

I'll connect to the web server and login using the cred `user:user`
![image](https://user-images.githubusercontent.com/113513376/226488083-d7c29d3a-60f7-4417-8aec-b57350707396.png)
![image](https://user-images.githubusercontent.com/113513376/226488141-71bd993c-9118-4abb-a46b-15b417f1ff5e.png)

If you try to click the flag image file it won't allow access cause the user isn't admin
![image](https://user-images.githubusercontent.com/113513376/226489195-db199e06-4f26-4ed3-92e3-189eef637949.png)

After i checked for the cookies i couldn't find any JWT token 
![image](https://user-images.githubusercontent.com/113513376/226488228-cb5beaee-a18b-4836-9faf-b812bab7738a.png)

So i decided to login again but this time pass the request through my burp proxy
![image](https://user-images.githubusercontent.com/113513376/226488487-4b8701e3-c0c0-490d-b88b-8a2efddb737c.png)
![image](https://user-images.githubusercontent.com/113513376/226488541-b35b171a-7ed2-4058-90ac-02c3a1c5cf1b.png)

Cool so it generated a token for me and from checking [jwt.io](https://jwt.io) i got its algorithm to be HS256
![image](https://user-images.githubusercontent.com/113513376/226488790-31e7606b-3499-4941-a5f5-773450fe4417.png)

Here's the jwt decoded value:

```
{
  "role": "Free",
  "iss": "bookshelf",
  "exp": 1679960313,
  "iat": 1679355513,
  "userId": 1,
  "email": "user"
}
```

Since we know the sign key to be `1234` that means that we can generate another token 

I made a script to generate the token for me 

After running it i got the new token
![image](https://user-images.githubusercontent.com/113513376/226492467-7f89beb7-eebf-4c3c-8c5a-63c93e310ad0.png)

So i then logged in again but this time intercept the request and replace the token to the newly generated own
![image](https://user-images.githubusercontent.com/113513376/226492548-5714f4db-10aa-4418-9063-3fd0a434cb45.png)
![image](https://user-images.githubusercontent.com/113513376/226492624-396a7fcb-b100-45bb-8782-269726c80ed0.png)

```
Intercept Request --> Response To Request
```

Now i will replace this with the new token generated
![image](https://user-images.githubusercontent.com/113513376/226492724-c1ebaea4-995f-411c-b88c-8dc1b745ba84.png)

After forwarding the request i get logged in as admin
![image](https://user-images.githubusercontent.com/113513376/226492769-03e06262-dd97-4c59-81b1-0f355aa6c4a3.png)
![image](https://user-images.githubusercontent.com/113513376/226493100-3a84d037-6e9e-4576-a016-45fc11de1fc2.png)
![image](https://user-images.githubusercontent.com/113513376/226493137-6e2459cb-eeee-4ab5-86d3-e95150e7e94b.png)

From here we can just get the flag 
![image](https://user-images.githubusercontent.com/113513376/226773157-1bdf8d2a-0f2c-4ae6-b569-15c59785a94a.png)

Here's my automated script to get the flag xD [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/web/java_solve.py)
![image](https://user-images.githubusercontent.com/113513376/226773435-89f793ce-3949-4c75-8ba2-ee5b17f694b3.png)
![image](https://user-images.githubusercontent.com/113513376/226773481-1c19bbd5-a006-49a7-a460-7a0e1c877e25.png)

### Cryptography 4/7:~

#### HideToSee
![image](https://user-images.githubusercontent.com/113513376/226864503-f4e97699-4e3b-4b89-9259-85e6873cc67c.png)

After downloading the file attached and checking its file type shows its an image file
![image](https://user-images.githubusercontent.com/113513376/226914695-1bf6ff04-61f9-4e45-8214-5defbe931b7c.png)

It content is referring to atbash cipher and it contains the way of decoding atbash cipher

But no encrypted text is given. So now i checked if there's any data hidden in the jpg file
![image](https://user-images.githubusercontent.com/113513376/226865665-6395f3f5-603d-41f0-92c0-446cc03c9cfd.png)

Now on viewing the encrypted data it gives this
![image](https://user-images.githubusercontent.com/113513376/226865814-54d8fd0a-063d-470d-8554-2263b3d880dc.png)

```
Cipher Text: krxlXGU{zgyzhs_xizxp_1u84w779}
```

We can use that table in the image already given or an online tool [Dcodefr](https://www.dcode.fr/chiffre-atbash) to decode it
![image](https://user-images.githubusercontent.com/113513376/226866925-36d6d120-9e6f-4497-bc4d-2be8f8e5cd43.png)
![image](https://user-images.githubusercontent.com/113513376/226867110-edfddb9a-7d67-4751-a1bd-b138fcfeaa11.png)

```
Flag: picoCTF{atbash_crack_1f84d779}
```

#### ReadMyCert
![image](https://user-images.githubusercontent.com/113513376/226868432-adc07c99-bc19-4884-92ce-0289680c2336.png)

After downloading the file attached i checked its file type and its a `PEM certificate request` file
![image](https://user-images.githubusercontent.com/113513376/226868656-54be6957-f6d1-4cee-813b-21210fb5ae8d.png)

So if we view it what we will see is just the certificate file
![image](https://user-images.githubusercontent.com/113513376/226869747-9633bc8e-9fb2-4e7b-ba6a-2fca2437f02c.png)

Next thing i did was to search `how to decode .csr file with openssl` 

And i got this [Resource](https://lindevs.com/decode-certificate-signing-request-csr-using-openssl)

I put it in a bash script
![image](https://user-images.githubusercontent.com/113513376/226869217-dc1a0558-554c-467a-a889-c1ea4d514525.png)

And after running it i got the flag
![image](https://user-images.githubusercontent.com/113513376/226870277-eadc6687-04fa-43e1-a18a-d3bfafa59f0c.png)

```
Flag: picoCTF{read_mycert_a7163be8}
```

#### Rotation
![image](https://user-images.githubusercontent.com/113513376/226871454-3f13176d-6acd-475b-82b8-f73157f9ddc7.png)

We're given the encrypted file
![image](https://user-images.githubusercontent.com/113513376/226872606-0018604a-0738-4c9c-8157-c1c79272a489.png)

So i used [DcodeFR](https://www.dcode.fr/cipher-identifier) to identify the cipher type and used it also for decoding it
![image](https://user-images.githubusercontent.com/113513376/226871808-3fdf069b-2240-4e5a-b8d2-bcc3bdc11e5b.png)

Its likely a rot cipher so i used [Decoder](https://www.dcode.fr/rot-cipher) to decode it
![image](https://user-images.githubusercontent.com/113513376/226872120-2302a90e-cfa4-4d25-ab16-27f88ad89365.png)

```
Flag: picoCTF{r0tat1on_d3crypt3d_25d7c61b}
```

#### SRA
![image](https://user-images.githubusercontent.com/113513376/226874186-85577e8d-2872-47cb-a05b-481c3f298f9f.png)

We're given the remote file being used

Here's its content
![image](https://user-images.githubusercontent.com/113513376/226874614-afe47f55-4d0d-44c5-9049-459c3f7973fc.png)

And this is what's happening

```
1. It creates 16 random values which are either ascii or digits
2. After that it generates random prime numbers with 128 bits in two variables
3. It then multiplies those two variable which is stored in a new variable
4. 65537 is stored in variable sloth
5. The multiplicative inverse of sloth and (gluttony - 1) * (greed - 1) is done and stored in variable envy
6. It converts the value of pride to a long integer then does the modular exponential of pride where the public exponent is sloth and the modulus is lust
```

Overall this is a process of encrypting a message using RSA

So if we run the prorgam it will generate the private key (d) and its ciphertext(c)

Then it asks for our input and check if its equal to the value stored in pride. If the check is meet we get the flag else it prints out Hubris!

But now that we know both the private key and the ciphertext we can calculate:

```
1. kphi from ed-1
2. Then go to factordb and take every prime factor which will be put in a list
3. From there we can use any for loop with product from itertools to calculate the multplication of some factors and check the result of this multiplication which will be called n
4. Then we check if isPrime(n+1) and if (n+1).bit_lenght() = 128. If the check is meet we can save (n+1) in a list
5. With this we will get a list of all possible primes that could construct N
6. We can then make two for loops where i and j are the iterate with the list and calcualte N=i*j; if long_to_bytes(pow(c,d,N)).isprintable(): print(ong_to_bytes(pow(c,d,N)))
```

Thats the way I solve it

So I wrote a script for it [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/crypto/sra.py)

Running it gives the flag

```
➜  sage solve.py
[-] Opening connection to saturn.picoctf.net on port 51615: Connected
anger = 10874849782922899596926546059091484448219162477034704964483223843381834331753
envy = 6079395884215855559684171323910149420899924737311416787335412267518949259009
vainglory?
picoCTF{7h053_51n5_4r3_n0_m0r3_3858bd66}
➜  sra 
```

```
Flag: picoCTF{7h053_51n5_4r3_n0_m0r3_3858bd66}
```

### Binary Exploitation 7/7 :~

#### BabyGame01 
![image](https://user-images.githubusercontent.com/113513376/226915406-7b091a70-4eba-4433-9b95-6fdc0739cac7.png)

I checked what file type it is and the protections enabled on the binary
![image](https://user-images.githubusercontent.com/113513376/226915845-174be1da-0e88-4f12-b129-c9466cdac690.png)

Its a x86 binary which is dynamically linked and not stripped, the protections enabled on the binary are Canary and NX (No Execute)

Next i'll run it to get an idea of what it does
![image](https://user-images.githubusercontent.com/113513376/226916252-ca68d82a-5d2c-45cb-bfff-d30dba3b21d9.png)

Looks like some sort of game

Using ghidra i decompiled the binary

Here's the main function
![image](https://user-images.githubusercontent.com/113513376/226916410-85a2f069-9b06-4262-be4f-ca5802680ecf.png)

This is the part am interested about

```
    } while (local_aac != 0x1d);
  } while (local_aa8 != 0x59);
  puts("You win!");
  if (local_aa4 != '\0') {
    puts("flage");
    win();
    fflush(stdout);
```

If `local_aac == 0x1d and local_aa8 == 0x59` it will print out you win then another check is done that checks if the value of `local_aa4` is not equal to a null terminator it will call the win() function which will give the flag
![image](https://user-images.githubusercontent.com/113513376/226917164-f7c2faf1-fd97-400d-a7fa-028f111ae3ad.png)

To trigger this condition we must firstly win the game and the local variable local_aa4 must be non-zero to get the flag.

So the way to move the player of the game is by using `w,a,s,d` and other good functions are `p,l`
![image](https://user-images.githubusercontent.com/113513376/226917544-4c346935-cdf8-4746-9362-b7c80f79be89.png)

And here's what each does:

```
1. w --> moves the player up
2. a --> moves the player left
3. s --> moves the player right
4. d --> moves the player down
5. l --> change the player structure
6. p --> auto solve the game
```

And what I noticed while i tried it is that when the player goes out of bound you get a seg fault
![image](https://user-images.githubusercontent.com/113513376/226919417-38196385-f3bd-4c7d-aad6-5e6a74693175.png)

The reason is cause the program tried accessing a memory address that isn't valid
![image](https://user-images.githubusercontent.com/113513376/226919764-d948ee0d-b697-4614-b9c9-decd9a556810.png)

Looking at the stack layout 
![image](https://user-images.githubusercontent.com/113513376/226920424-df297ecd-f47f-418c-98d1-25a866d5abff.png)

```
  | local_aac        | [$EBP - 0xAAC]               player_x_pos (or row in map)
  | local_aa8        | [$EBP - 0xAA8]               player_x_pos (or column in map)
  | local_aa4        | [$EBP - 0xAA4]  char         flag_win_condition (!= 0)
  | local_aa0        | [$EBP - 0xAA0]  char[2700]   map_buf  
```

The offset between the player_x_pos and `local_aa4` is `0x4`

```
➜  game01 python3
Python 3.11.1 (main, Dec 31 2022, 10:23:59) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> hex(int(0xaa8)-int(0xaa4))
'0x4'
>>> 0x4
4
>>>
```

This also tells us our initial starting position is always  { X, Y } = { 4, 4 } 

Now the idea is that if we can reach that particular position `0x59 = 89` and also go out of bound we can overwrite the value of `local_aa4` by adding extra 4 bytes since thats the required offset needed to overwrite `local_aa4`

The function init_player() takes the address of local_aac and writes three words, array indexing flowing into subsequent parameters of main() 

```
local_aac[0] = 4                    = player_y_pos (or row in map)
local_aac[1] = 4   ---> local_aa8   = player_x_pos (or column in map)
local_aac[2] = 0   ---> local_aa4   = flag_win_condition (!= 0)
```

init_map() function confirms the purpose and ordering of the player position coordinates, as detailed above. It also exposes the exit position which is the game win condition, that is the player must reach { 29, 89 } = { 0x1d, 0x59 

And the decompilation of the move_player function is

```
if (param_2 == 'w') {
  *param_1 = *param_1 + -1;
}
else if (param_2 == 's') {
  *param_1 = *param_1 + 1;
}
else if (param_2 == 'a') {
  param_1[1] = param_1[1] + -1;
}
else if (param_2 == 'd') {
  param_1[1] = param_1[1] + 1;
}
*(undefined *)(*param_1 * 0x5a + param_3 + param_1[1]) = player_tile;
```

But if we substitute with our variable names and making the code a little easier to read :

```
*map_buf[(player_y_pos * 0x5a) + player_x_pos)] = player_title
```

What we can notice there is that:

```
1. There is no bounds checking on position increment/decrement operations
2. These new player position values form the index of an array dereference
```

This is the vulnerable part of the code because we control the player position values and hence can control the dereferenced array entry (and hence address) and the character that gets written there, forming a write-what-where primitive.

So our aim here will be to underflow the `map_buf` array and write a non-zero value to the `local_aa4` our `  if (local_aa4 != '\0') {` condition , which was initialised to zero by init_player()

This means an effective position of { 0, -4 } will write the player_title character to the LSB of local_aa4

Now to solve this we need to move player position from { 4, 4 } to { 0, -4 }, this underflows the map_buf[] and writes the player's position character over local_aa4 (satisfying the non-zero flag win condition)

```
Payload: aaaawwwwaaaap
```

So what that does is to:

```
1. Move left 4 times
2. Go up 4 times
3. Go out of bound with 4 bytes 
4. Auto win the game
```

Doing that gets me the flag locally
![image](https://user-images.githubusercontent.com/113513376/226922980-59ab86d8-7b47-467b-b2fb-c8676e4f2f1c.png)

So I did the same remotely
![image](https://user-images.githubusercontent.com/113513376/226923379-0064a59d-8eef-4ff1-9691-9fbb1667537e.png)

Here's the auto solve script [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/pwn/babygame01.py)

Running it gives the flag 
![image](https://user-images.githubusercontent.com/113513376/226925087-45390d09-827b-4c2c-a125-8af55a6b85b4.png)

```
Flag:  picoCTF{gamer_m0d3_enabled_3aa88304}
```

#### TwoSum
![image](https://user-images.githubusercontent.com/113513376/226925764-70d8c6f7-f7e8-4992-b5aa-bdabacc474f8.png)

The source code is given
![image](https://user-images.githubusercontent.com/113513376/226926370-501f3391-ce34-46b8-8f2b-bfe0faf5cd64.png)
![image](https://user-images.githubusercontent.com/113513376/226926425-71eaf022-35f1-4449-962f-465395ea03b5.png)

Here's what it does:

```
1. Creates a function called addIntOvf and it requires 3 parameters which are result, a & b
2. What the function does is to sum up int a and int b and store them in result 
3. It then checks if the value of a and b is greater than 0 and the value of result is less than 0 
4. It then returns error
5. Also an if check is done that checks if the value of a and b is less than 0 and the result is greater than 0 
6. If its that case it returns error 
7. Else it exits
```

For the main function here's what it does:

```
1. It prints out n1 > n1 + n2 or n2 > n1 + n2 
2. Then it prints What two positive numbers can make this possible:
3. It receives our input which are two numbers stored in &num1 and &num2
4. A variable sum is created which takes the sum of num1 and num2
5. Then it calls the addIntOvf function which takes in the sum, &num1, &num2 as parameters and check if it returns true 
6. If that returns true it prints out No overflow
7. Else if addIntOvf returns false it prints out You have an integer overflow
8. After that it then checks if the value of &num1 and &num2 are greater than 0 (non negative number)
9. If the check is meet it prints out the flag
```

Looking at the code what the program expects is two positive numbers that when sumed up gives a negative number

Is that possible? 

Yes!!! And its called an integer overflow

So basically performing integer overflow means going above the maximum value of the signed integer, and the result usually becomes a negative number

Here's the resource [Resource](https://www.acunetix.com/blog/web-security-zone/what-is-integer-overflow/)

This are two integers that when added result in an integer overflow

```
Num1: 2147483647
Num2: 1
```

Giving that as the num to the binary gives an integer overflow and then the flag (locally)
![image](https://user-images.githubusercontent.com/113513376/226935108-8a2282b9-23cd-4e4d-bb44-51fb67a34f73.png)

Trying that on the remote server works also
![image](https://user-images.githubusercontent.com/113513376/226935561-6ba12a02-fbc1-4fe3-baef-552059294a26.png)

Here's the solve script [Solve](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/pwn/twosum.py)

Running it gives the flag
![image](https://user-images.githubusercontent.com/113513376/226936803-392c0482-2ee3-483c-8dce-82f98c48b260.png)

```
Flag: picoCTF{Tw0_Sum_Integer_Bu773R_0v3rfl0w_e06700c0}
```

#### BabyGame02
![image](https://user-images.githubusercontent.com/113513376/228136576-46e9f3e7-b31a-4a72-9e4e-1487ebd4abea.png)

After downloading the binary i checked its file type and the protection enabled
![image](https://user-images.githubusercontent.com/113513376/228230535-3f41858c-b209-4717-a130-d040c7395920.png)

Cool the only protection enabled is No-Execute

Running the binary shows the same output as the previous one
![image](https://user-images.githubusercontent.com/113513376/228230715-974a5711-f7d0-46ce-ac11-7e26955b3a52.png)

So i decompiled it using ghidra and now here's the difference between the it and the first binary
![image](https://user-images.githubusercontent.com/113513376/228232659-1f8b7a49-333f-4f19-a8f9-94a18dabd2ca.png)

After the user wins it doesn't print any flag or calls the win function
![image](https://user-images.githubusercontent.com/113513376/228233461-b950f39b-ffb2-4dfa-a834-041fedf4608f.png)

Since its the same function as the previous binary, i won't share ss of the whole decompiled code

Visualising the stack frame of main() from the disassembly to show placement and relative offsets of local variables and other elemts on the stack. I've augmented the variables with their purpose obtained from analysis of functions (main(), init_player() and move_player()) 

```
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined main(undefined1 param_1)
             undefined         AL:1           <RETURN>
             undefined1        Stack[0x4]:1   param_1                                 XREF[1]:     08049674(*)  
             undefined4        Stack[0x0]:4   local_res0                              XREF[1]:     0804967b(R)  
             undefined1        Stack[-0x10]:1 local_10                                XREF[1]:     08049753(*)  
             undefined1        Stack[-0x11]:1 local_11                                XREF[2]:     080496eb(W), 
                                                                                                   080496ee(R)  
             undefined1        Stack[-0xa9d   local_a9d                               XREF[4]:     080496aa(*), 
                                                                                                   080496c3(*), 
                                                                                                   080496f5(*), 
                                                                                                   08049716(*)  
             undefined4        Stack[-0xaa4   local_aa4                               XREF[1]:     08049730(R)  
             undefined4        Stack[-0xaa8   local_aa8                               XREF[6]:     08049694(*), 
                                                                                                   080496a3(*), 
                                                                                                   080496bc(*), 
                                                                                                   080496fd(*), 
                                                                                                   0804970f(*), 
                                                                                                   08049725(R)  
                             main                                            XREF[5]:     Entry Point(*), 
                                                                                          _start:08049110(*), 
                                                                                          _start:08049116(*), 0804a0e8, 
                                                                                          0804a2a8(*)  
        08049674 8d 4c 24 04     LEA        ECX=>param_1,[ESP + 0x4]
```
move_player(player_y_pos, input_ch, map_buf) contains the same exploitable line of code that forming a write-what-where primative. We control the player X and Y position and hence the address to write to, aswell as the byte to write through the ability to change the player_title

So the vulnerable part of the code is 

```
map_buf[(player_y_pos * 0x5a) + player_x_pos)] = player_title
```

This time we must overwrite a return address on the stack with the addres of the win() function to gives the flag instead of overwriting a local variable of main().

The behaviour of move_player() is slightly different in babygame02, in that before moving the player it writes to the previous player position (before move), clearing it with '.' (0x2e) character before updating and writing the new player position. This means cycling this exploit to write multiple bytes is not possible as it corrupts the previous byte written with the clear. Therefore we need to find a location where only one write operation is required to divert the flow of execution to the win() function address.

After playing with the binary i noticed is that at address `0x080495b6`. The value at $esp will be the return pointer
![image](https://user-images.githubusercontent.com/113513376/228238735-6c7d14a6-1e7a-4d90-916c-47634c48cc72.png)
![image](https://user-images.githubusercontent.com/113513376/228238884-05af7f82-eb17-4403-962c-708095f37158.png)
![image](https://user-images.githubusercontent.com/113513376/228238965-5effc700-5c91-43d8-ae67-5319b6bb595c.png)

What we can see there is

```
*EIP  0x80495b6  →  <solve_round+47> add esp, 0x10     ← $esp
It's showing that the player_move was called from the solve_round function. So our input 'p', we won't need to use the p command for game02
```

Now here's what happen when i move around the map and check the stack memory address

After setting a new breakpoint at `0x8049548 = <move_player+212>: ret`
![image](https://user-images.githubusercontent.com/113513376/228240131-69cbb6f4-79a1-4865-bad1-269331671493.png)
![image](https://user-images.githubusercontent.com/113513376/228240177-73436646-954e-44a9-a076-0977f6afbc8d.png)
![image](https://user-images.githubusercontent.com/113513376/228240269-42dc2a4d-d235-4fa4-8979-3bfc48713203.png)
![image](https://user-images.githubusercontent.com/113513376/228240403-236e33e9-2962-417e-9e5f-ae1b7e50f8fe.png)
![image](https://user-images.githubusercontent.com/113513376/228240474-cff397e2-a41a-431d-b59c-ca34d93ae77c.png)

Now that `@` is the player, and we're moving it around in stack memory

And this is what happens when we go out of bound, the program will crash and its so cause the instruction pointer will try to access an invalid memory address

Now when we move round the memory it's pointers on the stack that we're modifying. Now the questions is... can we modify something useful to control the execution of the program so that we can get it to print the flag?

The goal is to make the eip call the win() function

But the problem is even tho we can overwrite the `@` structure it only just overwrites the last byte of an address of the stack

We need something similar to the win() function address and after setting a breakpoint at `*solve_round+47` 
![image](https://user-images.githubusercontent.com/113513376/228244236-f395302c-67aa-4457-9d78-f2f679a6d0b5.png)
![image](https://user-images.githubusercontent.com/113513376/228244295-fff395eb-281b-4c45-a3ff-7c42d9e6e655.png)
![image](https://user-images.githubusercontent.com/113513376/228244365-b3610f3a-41fd-4404-9ed2-e6bb6dfc20cd.png)

Then checking the stack, i got an address of the stack that looks very similar to the win() function
![image](https://user-images.githubusercontent.com/113513376/228244859-0de6a39f-1b8f-4983-93fc-a4c36823ef00.png)

We can see the similarity between the stack address `0x08049709` and the win function address `0x0804975d`

Only one byte that makes it not the same as the win function address

Now next thing is that since while we move round the map and out of bound, the player character is also moving round the stack therefore overwriting bytes on the stack which makes the program crashes, the idea is that that particular memory on the stack can be overwritten to the win function address. 

And for this to occur the character needed to overwrite it is `]` which will later turn to `5d` in hex

```
➜  game02 python
Python 3.11.1 (main, Dec 31 2022, 10:23:59) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> a=']'
>>> b=ord(a)
>>> hex(b)
'0x5d'
>>> 
```

And we know that the `l` function changes the player character to anything specified. So that means we can change our player character to `]`

So basically, when we jump up and down, we jump in the memory. Cause 2d arrays in memory become 1d with offsets and since we know the width of the map
to be 89, we know that we jump 89 bytes every time we move up and down.

We can control where this `0x5d` ends up as this `]` which is now the player so try and find the position on the map that is 89 bytes offset from that address that is close to the win function which is the stack address we got earlier.

So i just made a script to move round the map but out of bound i.e `w`

Here's my local fuzz script [Fuzz_Local](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/pwn/local_fuzz.py)

Running it locally gets me the offset
![image](https://user-images.githubusercontent.com/113513376/228273738-5f2e1210-1d00-425f-9bc1-e8a453e401a7.png)

Then i can get local flag 
![image](https://user-images.githubusercontent.com/113513376/228273977-179f8680-56be-4548-ba50-23a206d86368.png)

```
python2 -c "print 'l]' + 'wwww' + 'd'*47 + 'wp'"  | ./game
```

But trying it remotely doesn't work
![image](https://user-images.githubusercontent.com/113513376/228274268-c2332215-11de-4288-8cb7-e6186a3b5605.png)

So its likely the stack offset i think

Then a made a brute script and auto solve script for the remote own 

Here's the [Exploit](https://github.com/markuched13/markuched13.github.io/blob/main/solvescript/pico23/pwn/babygame02.py)

Running it works and i got the flag
![image](https://user-images.githubusercontent.com/113513376/228274867-410d2327-8341-41ae-ab09-0ed50c9ccf08.png)
![image](https://user-images.githubusercontent.com/113513376/228274963-aec298ed-4d8f-4a9b-889e-846d847e6b63.png)

```
Flag: picoCTF{gamer_jump1ng_4r0unD_498dff8d}
```

#### Hijacking
![image](https://user-images.githubusercontent.com/113513376/226937384-38c96e95-b535-473d-ae00-6da9b6fa8847.png)

After i connected to the ssh remote instance i saw this file called .server.py
![image](https://user-images.githubusercontent.com/113513376/226937728-135c2e94-49bc-4c27-a780-8f48e1b8eb52.png)

Since its own by root and the aim of this chall is to get root so i decided to take a look at it
![image](https://user-images.githubusercontent.com/113513376/226938017-febf1ad2-e778-41dc-b725-724ae9373f8b.png)

What the script does is to attempt to gather information by pinging picoctf.org

But we don't have any write access over this file
![image](https://user-images.githubusercontent.com/113513376/226938411-9159806a-e1b7-4cf4-9086-03018a5bb868.png)

So now what we can do is a python library hijack

Since those libraries i.e base64, os, socket are imported in the file we can attempted to hijack and add malicious content to those library files so that when its is being called when the .server.py is executed our malicious command will also be executed

But first we need to have write access over any of the library files

And base64.py seems ok to be abused
![image](https://user-images.githubusercontent.com/113513376/226939600-0e922e6a-b4ed-479e-a0fd-b7a1a6ce627c.png)

So now we can add in any thing we want inside the base64.py file then after we run .server.py it will be executed

I added a command to make `/bin/bash` an suid binary
![image](https://user-images.githubusercontent.com/113513376/226940622-f35e3189-5bb5-4fb3-89c1-f7869d9ebad9.png)

Now checking `sudo -l` shows we can run the .server.py as root
![image](https://user-images.githubusercontent.com/113513376/226940794-9661a7dc-142d-4b1d-a2b4-582221b8b1a2.png)

And that is ok cause we are trying to change the permission of a binary to suid

From here we can run the script 
![image](https://user-images.githubusercontent.com/113513376/226941042-cf5540ac-10fe-4f71-bbf4-4aaadbf26feb.png)

We can see now that `/bin/bash` permission is now that of an suid binary

Root should be easy from here 👻
![image](https://user-images.githubusercontent.com/113513376/226941381-c9c74ef8-8dbf-4af9-a98b-f9731df1deef.png)

```
Flag: picoCTF{pYth0nn_libraryH!j@CK!n9_0083cb0b}
```

### TicTac
![image](https://user-images.githubusercontent.com/113513376/227712172-db0a783c-c411-4789-9c87-27942b86bb9b.png)

After connecting to the ssh instance i got this two files
![image](https://user-images.githubusercontent.com/113513376/227712243-afa0175e-572e-422f-8cfa-dd07f82c714e.png)

Looking at the source code and the binary perm, it shows the binary is a suid binary
![image](https://user-images.githubusercontent.com/113513376/227712354-31185a04-5023-4be3-9454-188fa93ab31b.png)

And the source code for the txtreader binary is:

```
1. A C++ program 
2. The program checks if the user has provided exactly one command line argument (the filename to be read). If not, it displays a usage message and exits with an error code of 1
3. The program opens the file using an input file stream (std::ifstream).
4. The program uses the stat() system call to retrieve the file's status information, which includes the owner's user ID. If stat() returns an error (-1), the program displays an error message and exits with an error code of 1.
5. The program compares the owner's user ID to the ID of the current user (obtained using getuid()). If they don't match, the program displays an error message and exits with an error code of 1.
6. The program reads the contents of the file line by line using std::getline() and outputs each line to the console using std::cout.
7. If the file cannot be opened, the program displays an error message and exits with an error code of 1.
8. If everything goes well, the program exits with a success code of 0.
```

Overall, this program reads a file and outputs its contents to the console, but only if the user has permission to read the file (i.e., if they are the owner)

At this point what we would love to read is the flag.txt file
![image](https://user-images.githubusercontent.com/113513376/227712530-172eff47-a15e-47b2-bc68-63e285c5fe2a.png)

But the problem now is the file is only own by root 

So since the program reads files owned by the user, we won't be able to read the flag.txt

Thats what its normally supposed to do but here's the vulnerability 

From the task description it says `toc-tou` which means `Race Condition`
![image](https://user-images.githubusercontent.com/113513376/227712718-f07515f6-e722-4d81-9901-c66c8653ad91.png)

After reading some of the articles i found a way to exploit this

And its using symlink

Here's the exploitation phase:
![image](https://user-images.githubusercontent.com/113513376/227713039-11953029-e348-4d26-adea-117557e57696.png)

```
touch fake_flag
while true; do ln -sf flag.txt link; ln -sf fake_flag link; done &
while true; do ./txtreader link 2>/dev/null; done > val &
cat val
```

From that we can get the flag

```
Flag: picoCTF{ToctoU_!s_3a5y_5748402c}
```

### VNE
![image](https://user-images.githubusercontent.com/113513376/228078907-de95b7af-c532-471c-a863-3be22c42441c.png)

After i connected to the ssh instance i saw a binary there and ran it

But i got this
![image](https://user-images.githubusercontent.com/113513376/228079106-f1d7648f-9e56-4081-a959-36cb29d6946c.png)

So it reqires the `SECRET_DIR` environment to be set

It can be easily set like this
![image](https://user-images.githubusercontent.com/113513376/228079316-b956a43a-563a-4d16-a8a3-cc30f0062664.png)

So from the output we can tell that the binary does directory listing on the path specified 

Now what we can try here is command injection in the environment variable

Doing that works
![image](https://user-images.githubusercontent.com/113513376/228079603-fcf66dd3-cfd2-4470-be09-4bf2cb0ef893.png)

```
Flag: picoCTF{Power_t0_man!pul4t3_3nv_fc3ff2c9}
```

Thats all 👻

<h3> Teammate Writeup </h3>
	
## Forensics
- Who Is It
- Find And Open
- MSB
- Unforgotten Bits

## Cryptography
- PowerAnalysis: Warmup
- PowerAnalysis: Part 1
- PowerAnalysis: Part 2

## Reverse Engineering
- Virtual Machine 0
- Virtual Machine 1

Here's the link to the writeup [Link](https://kism37.github.io/posts/picoCTF2023/writeups.html)
