---
title: My Journey To ICC
date: 2025-11-25 21:38:05 +0000
categories: [CTF]
tags: [onsite, events]
math: true
mermaid: true
media_subpath: /assets/posts/2025-11-25-ICC-Recap
image:
  path: preview.png
---

## International Cybersecurity Challenge (ICC) - Tokyo Japan

In this blog post, I'll be sharing my personal experience as a first time participant of the International Cybersecurity Challenge (ICC) during it's fourth (4th) edition representing the Africa Regional Cybersecurity Committee (AFRICC) competing against the top qualified players from 8 regions covering the whole globe.

This was also my first international onsite CTF.

### International CyberSecurity Challenge (ICC) Overview

![ICC](ICC.png)

The International Cybersecurity Challenge is a cybersecurity competition created and organised by a global consortium including Europe (European Union Agency for Cybersecurity (ENISA) ), Asia (Code Blue, Div0, BoB, Bitscore), USA (Katzcy), Canada (Cyber*Sci), Oceania (The University of Queensland ), Africa (Namibia University of Science and Technology ), and Latin America (ICC Latino America).

The participants, all aged 26 or younger, compete in eight teams that have advanced through representatives.
The competition features both Jeopardy and Attack-and-Defense challenges.

### History

The International CyberSecurity Challenge (ICC) has witnessed its’ first edition in 2021 where the event was held Athens, Greece between 14 and 17 June where team Europe claimed the first place, team Asia second and team USA third.

The second edition was held in San Diego, California between 1 and 4 August where team Europe once again claimed the win back-to-back, team Oceania coming up second and team Asia settling for third place.

And the third edition was held in Santiago, Chile from 28th October to 1st November where team Europe had a back-to-back-to-back win streak, as where the second and third ranks were claimed by team Asia and team Oceania.

## AFRICC team

![AFRICC](AFRICC.jpeg)

African Region to Cybersecurity Competition (AFRICC) was established in 2021 to develop original african talent in order to create a team that will represent the continent in the International Cyber Security Challenge.

The AFRICC team was pretty diversified this year gathering players from 10+ african countries (Tunisia, Morocco, Namibia, Uganda, Nigeria, South Africa, Zimbabwe, etc.).

This was unfortunately our first appearance onsite for the ICC finals, since the team has 17 members which makes getting sponsorship a bit challenging.

## AFRICC qualification

In order for players to be eligible to participate in the ICC, they have to through qualifier rounds within their continent. An example of this is the Europe CyberSecurity Challenge that facilitates the qualification process for team Europe.

However, since Africa did not really have a qualification competition, the choosing on players was based off on some other criterias:

- Players performance throughout the year.
- Willingness to participate and represent team AFRICC in the ICC. (passion)
- Individual skill.
- Specialties when it comes to Security and CTF categories.
- Team play and being a good and positive team player.
- Multiple particiations in CTFs throughout the year which will help in allowing the player to gain more knowledge.

### The Beginning 

When I was first told to prepare my visa documents, everything felt really rushed. I had to travel to Dakar from Nigeria in just a few days, so there wasn’t enough time to process the visa back in Nigeria.

Thankfully, the coaches didn’t give up, they helped me make it work.

I finally managed to process my visa at the Embassy of Japan in Dakar, Senegal.

I really want to give a big shoutout to Pius and Sidiya (z0r), they helped me so much. 

I also sincerely appreciate Serdab for the sponsorship.

### Atmosphere of Overseas Participation

The International CyberSecurity Challenge (ICC) was held in Tokyo, Japan, specifically at the [New Otani Makuhari Hotel](https://www.newotani.co.jp/en/makuhari/), which was an incredible venue.

It was my very first time traveling to Japan or anywhere in Asia, for that matter. The journey was long, as I had to travel all the way from Dakar, Senegal.

Nevertheless, the trip wasn’t as exhausting as I expected, and I found myself excited for what was ahead.


### International CyberSecurity Challenge Event

The ICC ran for a total of 4 days (Nov 11th - 14th):

![Banner][streetbanner.jpg]

## Day 1 - Registration of teams & Opening Ceremony Orientation

We received our name tags, swags, stickers, and other goodies.

During the opening ceremony, the Japanese Minister of Cyber Security gave an opening remark:

![Minister][minister.jpg]

Here's our team poster:

![AFRICC POSTER][poster.jpg]

My name tag:

![h4cky0u][nametag.jpg]

After the ceremony the organizers opened both the Jeopardy and the Attack-Defense networks for testing purposes by the players. It was a pretty good decision since there were some minor network issues that were resolved later.

Off to day 2!

## Day 2 - Jeopardy CTF

A Jeopardy-Style Capture the Flag (CTF) competition is a cybersecurity challenge that provides players with standalone challenges that are not linked and that revolves around the following categories:
- Web Exploitation
- Reverse Engineering
- Binary Exploitation
- Digital Forensics and Incident Response
- Cryptography
- Cloud
- FullPwn (pentesting)
- Hardware Hacking
- Blockchain/Web3
- AI/LLM Hacking

The CTF span across 9 hours and almost 6 categories. It was pretty intense as the coordination that had to be done was crazy since we were 15 players on the team, hard and numerous challenges, scoreboard pressure, etc.

I'm pleased we placed 7th in the Jeopardy CTF. I focused on the pwnable challenges and solved 3 out of 6. I was mostly the only one working on them, so the pressure was real.

One of the challenges I solved ended with only 3 solves total, and I was the 3rd solver, which honestly made me proud.

![Scoreboard][scoreboard.png]
![Pwn Solves][pwnsolve.jpg]

## Day 3 - Attack-Defense CTF

At first, the whole network setup was new and confusing, but after a while, things started to make sense.

Once again, I worked on the pwnable challenge (CGIPanic).

These challenges involved a lot of CGI pain, multiple bugs, but difficult to chain into a one stage exploit.

I managed to get working exploits for two different CGI services.

Later, I spent a lot of time reversing another CGI binary (a C++ game-like application), but I couldn’t figure the bug before time ran out.

The second pwnable (**Umacorn**) was a custom x64 OS and emulator built on a completely different CPU architecture.

It was built by the GOAT @**ptr-yudai** who spent a **WHOLE YEAR** developing the challenge. The challenge intentionally had vulnerabilities such as:

- negative fd allowed
- rng seed can be any address
- file password address can point to disk cache (eg comparing password to itself)
- *fwrite* allowed arb write to kernel memory
- no *memzero* for freed pages -> realloc to get flag
- *pagealloc* error -> return value is assumed to be valid address nontheless (get physical page 0)
- table UAF
- *fopen* name could be *flag1*
- kernel memory was rw initially
- write syscall can read arb memory
- most password compares could be timeable
- *strcpy* in *fopen*
- kernel uses *movs* instruction but doesn’t call *cld* so you could call *std* in userland and cause stack overflow in kernel

It was absolutely insane.

![ptr-yudai][yudai.png]

Unfortunately, we didn't place well in the Attack-Defense CTF, but this only motivates us to push harder and come back stronger next year, God willing.

## Day 4 - Sightseeing Program & Awards ceremony

In the morning, we gathered with other teams and went sightseeing.

Now I'm going to show lots of pictures I took 😄

![Japanese Tea Garden][japanese_tea_garden.jpg]