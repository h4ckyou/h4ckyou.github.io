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

We are given two windows machine as part of the in scope servers to hack

- 10.8.0.101 (WSRV)
- 10.8.0.100 (DC01)

### WSRV

Here's the nmap scan:

```
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

We can use `nxc` to add the FQDN and CN to the `/etc/hosts` file

```
mark@rwx:~/Desktop/Labs/Secdojo/Roaster$ nxc-hosts 10.8.0.101
SMB         10.8.0.101      445    WSRV             [*] Windows Server 2016 Datacenter 14393 x64 (name:WSRV) (domain:secdojo.local) (signing:True) (SMBv1:True)
[sudo] password for mark: 
mark@rwx:~/Desktop/Labs/Secdojo/Roaster$ tail -n1 /etc/hosts
10.8.0.101     WSRV.secdojo.local WSRV
mark@rwx:~/Desktop/Labs/Secdojo/Roaster$ 
```

From the output, we can determine that SMB signing is enabled, the machine is joined to the *secdojo.local* Active Directory domain, and its hostname is *WSRV*. We can also see that *SMBv1* is enabled on the target.

Attempting to view the available share fails using null authentication & anonymous user fails

![enum1](enum1.png)