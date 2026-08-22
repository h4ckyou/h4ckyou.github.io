---
title: Roaster Secdojo
date: 2026-08-22 19:19:00 +0100
categories: [Machines]
tags: [Active Directory, Secdojo, Evasion]
math: true
mermaid: true
media_subpath: /assets/posts/2026-08-22-Roaster-Secdojo
image:
  path: preview.png
---

## Roaster

### Overview

This lab is a Windows environment designed to explore and exploit a range of Active Directory attack techniques, including Kerberos attacks, security evasion, privilege escalation, and delegation vulnerabilities, helping sharpen your skills in AD exploitation and offensive security.

![logo1](logo1.png)
![logo2](logo2.png)

We are given two Windows machines as part of the in-scope servers to compromise.

- 10.8.0.101 (WSRV)
- 10.8.0.100 (DC)

### WSRV

Here's the nmap scan of the `Portal` machine:

```bash
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-22 19:36 WAT
Nmap scan report for 10.8.0.101
Host is up (0.21s latency).

PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=WSRV.secdojo.local
| Not valid before: 2026-08-21T18:24:42
|_Not valid after:  2027-02-20T18:24:42
|_ssl-date: 2026-08-22T18:36:57+00:00; 0s from scanner time.
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: WSRV, NetBIOS user: <unknown>, NetBIOS MAC: 00:ff:42:d6:79:85 (unknown)
| smb2-time: 
|   date: 2026-08-22T18:36:51
|_  start_date: 2026-08-22T18:24:40
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.31 seconds
```

Here's the nmap scan of the `Roasted` machine:

```bash
Nmap scan report for 10.8.0.100
Host is up, received user-set (0.19s latency).
Scanned at 2026-08-22 20:07:30 WAT for 117s

PORT     STATE SERVICE      REASON  VERSION
53/tcp   open  domain       syn-ack Simple DNS Plus
88/tcp   open  kerberos-sec syn-ack Microsoft Windows Kerberos (server time: 2026-08-22 19:07:36Z)
135/tcp  open  msrpc        syn-ack Microsoft Windows RPC
139/tcp  open  netbios-ssn  syn-ack Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds syn-ack Windows Server 2016 Datacenter 14393 microsoft-ds (workgroup: DC01)
464/tcp  open  kpasswd5?    syn-ack
593/tcp  open  ncacn_http   syn-ack Microsoft Windows RPC over HTTP 1.0
5985/tcp open  http         syn-ack Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
5986/tcp open  ssl/http     syn-ack Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_ssl-date: 2026-08-22T19:09:24+00:00; -1s from scanner time.
| tls-alpn: 
|   h2
|_  http/1.1
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
| ssl-cert: Subject: commonName=EC2AMAZ-0288PK6
| Subject Alternative Name: DNS:EC2AMAZ-0288PK6, DNS:EC2AMAZ-0288PK6
| Issuer: commonName=EC2AMAZ-0288PK6
| Public Key type: rsa
| Public Key bits: 4096
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2023-11-09T15:08:37
| Not valid after:  2026-11-08T15:08:37
| MD5:   2544:bb93:ad9f:f1c5:98ee:d3cd:5482:812f
| SHA-1: ad3d:51d5:b135:978a:4710:c396:1b95:5f0d:ee10:68c2
| -----BEGIN CERTIFICATE-----
| MIIFMTCCAxmgAwIBAgIQKyxpUeZvc69ENA6R00Gu9DANBgkqhkiG9w0BAQsFADAa
| MRgwFgYDVQQDDA9FQzJBTUFaLTAyODhQSzYwHhcNMjMxMTA5MTUwODM3WhcNMjYx
| MTA4MTUwODM3WjAaMRgwFgYDVQQDDA9FQzJBTUFaLTAyODhQSzYwggIiMA0GCSqG
| SIb3DQEBAQUAA4ICDwAwggIKAoICAQDG/3ejhrlCLfUtjtWcdTIZ/s7LbO+vwM/U
| q69xQMKfLAJk05O/Z6oakEDPl4+4vtGIsxaYGlbK54tP+GYnn2YNlkhl1povqd7X
| n0rVCLe5LNVZ39RuPo9WlEdKsu+tbwD/5F/2b56AA5G2pyu7AR8ZrhMrX60NwFZ+
| NXxI4wX2P6U3Ttlh593Ong+KmscQeXtseRKstN44AhpmfVSaBuQTvyypo+zXWhuM
| AgxE2I3sXd6S7n38rcXMtflvgTGI8UumyNaa7lpuGAW9FIjb5AJXnFmdxHZox5s3
| 329rN/mCjxWW6rjlCWa/ztLbqBiDOhD8LmjHXNl/kJL66wrAtL4tbPSYEDlQVozf
| G5F3X2Ii2PzI2P2dfQyPV6cW1YxXvbJc7z65D0VMIewzhIRfHf65XsDHBMdfbkop
| /ksbQ+D2Xl6nLo5bLvWtVCUar0Ad+jTU9sqa9ic78cx168jQM0Iu87kEAQp7O3PU
| jJf4Xd3kvHW8eFg0Vm2tQKVj8vF0V82BXKEu7Ovwtpmg1IkpgroCeoZjGlUbq3EI
| l+aVCcaLiASu/EombRIR6Joi5NqEIWSrxwKsZr2KOlRa1S7QC0F3cS9uRbtEPSdF
| NEjhqTNlGegF6/P2B9Jv2fAW5D776+DK6u4bDQg6+4j19m3RGpNMjMbHoI7pStWh
| 3/+6GsjneQIDAQABo3MwcTAOBgNVHQ8BAf8EBAMCBaAwEwYDVR0lBAwwCgYIKwYB
| BQUHAwEwKwYDVR0RBCQwIoIPRUMyQU1BWi0wMjg4UEs2gg9FQzJBTUFaLTAyODhQ
| SzYwHQYDVR0OBBYEFLO4D0KnHHF92ZSOOgs5nsGjXuN7MA0GCSqGSIb3DQEBCwUA
| A4ICAQChOeiNLYlQz0T6aoqgsbW1MqSdIG50bMlZ7Q3cnCofI19DBu7b272o7RlK
| U4n8yf8J8BArS9E95JeW142U+W48Ncz0TIllt7KhvH4Y7O8kgxGdoxY7DtfyqyVj
| wkQYhFFdzEFeTBwCAqb7HEHI8hWwchuZLKeObISDG3LMoxvoFfuWwC38x3wCjroz
| zvlUYHbTb6rROPLl99bBrk7Dg88yGw8U1axetFFUjCEkgO0iFzowLRS/fdXF38LY
| DbVlWAwJg4G+1frpmjufj9h3tDyyan+l9NfhUz8H4xm+8pGiJWlfO9JaR3H0qDef
| aFrv7/o8Bx+uvypDBaKXOI+im9nlB6cw47iG/Dc+WyRb7ChlFhVer1jZ4N4al3rT
| dGvUWDruv0YKF61uBfvY1xo2BFBtdPL38MBcK/4NklDhptJwcEuF77noxLxGiXS9
| bZq38gtJe1U9m0kf6J6ShZLtV7Q+Bjr65U9uWlmgBXD09l3Ozcl0Ene8f4H25C10
| QkhQ15luNNvnrJKB8utGfPdtbRDnrZRKzZSlInWg5dQHCORyp+w6Lp/Wj4VGGD9k
| e9mK/+7aXE9z/LXwLMo6jCG64pFU4JNlj0SZh3JtiXCvb5bvzXdqX8GiptgZCwp7
| Z3ihvq3Tb4LxTz/+Y5XK0+ZN+lUkDx68i7LVY6kG3Dc6ilfLsQ==
|_-----END CERTIFICATE-----
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2016 Datacenter 14393 (Windows Server 2016 Datacenter 6.3)
|   Computer name: DC
|   NetBIOS computer name: DC\x00
|   Domain name: secdojo.local
|   Forest name: secdojo.local
|   FQDN: DC.secdojo.local
|_  System time: 2026-08-22T19:08:30+00:00
|_clock-skew: mean: 0s, deviation: 4s, median: -1s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 38332/tcp): CLEAN (Couldn't connect)
|   Check 2 (port 50845/tcp): CLEAN (Couldn't connect)
|   Check 3 (port 43774/udp): CLEAN (Failed to receive data)
|   Check 4 (port 21252/udp): CLEAN (Timeout)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| smb2-time: 
|   date: 2026-08-22T19:08:25
|_  start_date: 2026-08-22T18:24:49
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| nbstat: NetBIOS name: DC, NetBIOS user: <unknown>, NetBIOS MAC: 00:ff:75:68:91:0b (unknown)
| Names:
|   DC01<00>             Flags: <group><active>
|   DC<00>               Flags: <unique><active>
|   DC01<1c>             Flags: <group><active>
|   DC<20>               Flags: <unique><active>
|   DC01<1b>             Flags: <unique><active>
| Statistics:
|   00:ff:75:68:91:0b:00:00:00:00:00:00:00:00:00:00:00
|   00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
|_  00:00:00:00:00:00:00:00:00:00:00:00:00:00
```

We can use `nxc` to resolve the target hostnames and add their FQDNs and hostnames to `/etc/hosts`.

![enum6](enum6.png)

From the output, we can determine that 
- SMB signing is enabled
- the machine `WSRV` is joined to the `secdojo.local` Active Directory domain
- *SMBv1* is enabled on the target

Attempts to enumerate the available SMB shares fail with both null authentication and anonymous authentication.

![enum1](enum1.png)

At this point, there isn't much we can do without valid credentials. 

However, with port *80* open, we can enumerate the web service and see if it exposes any useful information or potential attack vectors.

![enum2](enum2.png)

It shows just the default IIS web page.

Fuzzing with *ffuf* gives */dev*
![enum5](enum5.png)
![enum3](enum3.png)

The web page contains mostly static content so nothing much can be done here, but it does give us potential user names

![enum4](enum4.png)

```
- Boris Johnson
- Kate Winslet
- Adam Crew
- Cody Gardner
```

Using [username-anarchy](https://github.com/urbanadventurer/username-anarchy), we can generate a wordlist containing potential usernames based on the provided user list.

```bash
mark@rwx:~/Desktop/Tools/username-anarchy$ ./username-anarchy -i potential > /home/mark/Desktop/Labs/Secdojo/Roaster/potential_users.txt
mark@rwx:~/Desktop/Tools/username-anarchy$ wc -l /home/mark/Desktop/Labs/Secdojo/Roaster/potential_users.txt
56 /home/mark/Desktop/Labs/Secdojo/Roaster/potential_users.txt
mark@rwx:~/Desktop/Tools/username-anarchy$ 
```

To validate the generated usernames against the domain controller, I used `kerbrute`.

![enum7](enum7.png)

We have 3 confirmed valid users:
- boris.johnson
- kate.winslet
- cody.gardner

The next step is to check whether any of these accounts are vulnerable to *AS-REP Roasting*. This Kerberos attack is possible when the *Do not require Kerberos preauthentication* option is enabled on a user account.

![enum8](enum8.png)

```
$krb5asrep$23$cody.gardner@SECDOJO.LOCAL:d7deb849577f0d9093856c23d5a96885$8d5ccbfd680df1a3ca313c4ae08e484f74485c67d675c50c68576a5ff02c193fbade0b356f64a9824d90fa978a02c7f3b1aecdcdfd3130314e07b9786504d62cc6f7ace91309c104e73906531ec4c00f126f67004ba86677d124f4c2ae2ae1cbee261090590039195e59d89dc307e510ae0801cb1ebbe4b5ea5b1605f049f8e91d2b3f692c17f81b982b03dd1520d8f0bd81cdedc6ce0be203e56a0aac10953c4836af0a3d472cdf572deff78877d453e90a00065668aeb2df3bb3bc0eb3a8c5cc52517050c37b80d62e773981ebcf4596ab0dc81bdfb022a0b19573fa3353ce9a2b761f496f069ffec4a7f9b280
```

Cracking the hash with `John the Ripper` using the `rockyou.txt` wordlist was successful!

![enum9](enum9.png)

We can now confirm that the recovered credentials are valid.

![enum10](enum10.png)

Testing the credentials against various services on the `WSRV` machine shows that we have `RDP` access.

![enum11](enum11.png)

