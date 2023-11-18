<h3> Intigriti CTF 2023 </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8b17fe9f-67ac-4be7-8ad3-e96f14932f99)

Challenge Solved:

### Cryptography
-  Really Secure Apparently
-  Keyless

### Web
- CTFC

### Pwn
- Hidden
- Floor Mat Store

### Reversing
- FlagChecker


#### Cryptography

##### Really Secure Apparently
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f181b03b-f0d3-4cc6-8493-885cdf35c0a4)

From the challenge name we can tell this is RSA 

We are given `n, e and c` and our goal is to decrypt the value of `c` which would hold the flag

After downloading the attached ciphertext file I saw the content was as bytes but not long integer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/76b6219d-abe4-455a-a712-f6094cd58fad)

So I decided to convert it so that I would use DcodeFr to solve it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bf4ee23b-4998-41dc-8ae9-4eb8a1c4c040)

Now we have the values needed to decode the ciphertext:

```
n = 689061037339483636851744871564868379980061151991904073814057216873412583484720768694905841053416938972235588548525570270575285633894975913717130070544407480547826227398039831409929129742007101671851757453656032161443946817685708282221883187089692065998793742064551244403369599965441075497085384181772038720949
e = 98161001623245946455371459972270637048947096740867123960987426843075734419854169415217693040603943985614577854750928453684840929755254248201161248375350238628917413291201125030514500977409961838501076015838508082749034318410808298025858181711613372870289482890074072555265382600388541381732534018133370862587
c = 441001510077083440712098978980133930415086107290453312932779721137710693129669898774537962879522006041519477907847531444975796042514212299155087533072902229706427765901890350700252954929903001909850453303487994374982644931473474420223319182460327997419996588889034403777436157228265528747769729921745312710652
```

Using [link](https://www.dcode.fr/chiffre-rsa) I got the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/218f4606-5060-42e6-92ea-cf7f0c744ad8)

```
Flag: INTIGRITI{0r_n07_50_53cur3_m4yb3}
```

##### Keyless
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/fb3ac212-2408-4e63-aa14-b2dae187cd8b)

Downloading the attached file and unzipping it shows this python file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/37117060-02d9-4b06-b6c1-e9ba5d8a164b)

```python
def encrypt(message):
    encrypted_message = ""
    for char in message:
        a = (ord(char) * 2) + 10
        b = (a ^ 42) + 5
        c = (b * 3) - 7
        encrypted_char = c ^ 23
        encrypted_message += chr(encrypted_char)
    return encrypted_message

flag = "INTIGRITI{REDACTED}"
encrypted_flag = encrypt(flag)

with open("flag.txt.enc", "w") as file:
    file.write(encrypted_flag)
```

So basically this python file encrypts the flag and the output was written to `flag.txt.enc`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/c90681e2-9466-4bb1-b3bd-28a1b48f3271)

How can we decrypt it?

Well we just need to reverse the process and luckily nothing hard was done there

















