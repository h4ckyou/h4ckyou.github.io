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

<figure>
  <img src="me@japan.jpg" alt="h4cky0u at Japan">
  <figcaption style="text-align:center;">
    Me at Japan 👀
  </figcaption>
</figure>


### International CyberSecurity Challenge Event

The ICC ran for a total of 4 days (Nov 11th - 14th):

<figure>
  <img src="streetbanner.jpg" alt="Team Poster">

  <figcaption style="text-align:center;">
    ICC Banner on the road of Chiba
  </figcaption>
</figure>

## Day 1 - Registration of teams & Opening Ceremony Orientation

We received our name tags, swags, stickers, and other goodies.

During the opening ceremony, the Japanese Minister of Cyber Security gave an opening remark:

<figure>
  <img src="minister.jpg" alt="Minister">

  <figcaption style="text-align:center;">
    Minister Giving Remarks
  </figcaption>
</figure>

Here's our team poster:

<figure>
  <img src="poster.jpg" alt="Team Poster">

  <figcaption style="text-align:center;">
    Team Poster
  </figcaption>
</figure>

My name tag:

<figure>
  <img src="nametag.jpg" alt="Nametag">

  <figcaption style="text-align:center;">
    My Name Tag
  </figcaption>
</figure>

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

<figure>
  <img src="scoreboard.png" alt="Jeopardy Scoreboard">
  <img src="pwnsolve.jpg" alt="Pwn Solves">

  <figcaption style="text-align:center;">
    Final Scoreboard & Challenges I Solved
  </figcaption>
</figure>


## Day 3 - Attack-Defense CTF

At first, the whole network setup was new and confusing, but after a while, things started to make sense.

Once again, I worked on the pwnable challenge (CGIPanic).

This challenge involved a lot of CGI pain, multiple bugs, but difficult to chain into a one stage exploit.

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

<figure>
  <img src="yudai.png" alt="ptr-yudai">
  <figcaption style="text-align:center;">
    The 🐐
  </figcaption>
</figure>

Unfortunately, we didn't place well in the Attack-Defense CTF, but this only motivates us to push harder and come back stronger next year, God willing.

After the CTF ended, we went for an After-Party

Here are some images I took

<figure>
  <img src="after_party.jpg" alt="party0">
  <img src="interesting.jpg" alt="party1">
  <img src="sweet.jpg" alt="party002">
  <img src="sweet2.jpg" alt="party022">
  <img src="food.jpg" alt="party222">
  <img src="whyme.jpg" alt="party3">
  <img src="smile.jpg" alt="party4">
  <img src="ohboy.jpg" alt="party5">
  <figcaption style="text-align:center;">
    After-Party Event
  </figcaption>
</figure>


## Day 4 - Sightseeing Program & Awards ceremony

In the morning, we gathered with other teams and went sightseeing.

Now I'm going to show a bit of pictures I took 😄

<figure>
  <img src="japanese_tea_garden.jpg" alt="Japanese Tea Garden 1">
  <img src="green_tea.jpg" alt="Japanese Tea Garden 2">
  <img src="history_talk.jpg" alt="Japanese Tea Garden 3">

  <figcaption style="text-align:center;">
    Various views from the Japanese Tea Garden
  </figcaption>
</figure>

<figure>
  <img src="japanese_tea_garden.jpg" alt="Japanese Tea Garden 1">
  <img src="green_tea.jpg" alt="Japanese Tea Garden 2">
  <img src="history_talk.jpg" alt="Japanese Tea Garden 3">

  <figcaption style="text-align:center;">
    Various views from the Japanese Garden - Mihama-en
  </figcaption>
</figure>

<figure>
  <img src="tour.jpg" alt="tour">
  <figcaption style="text-align:center;">
    Tour guide
  </figcaption>
</figure>

<figure>
  <img src="wow1.jpg" alt="Beautiful 1">
  <img src="wow2.jpg" alt="Beautiful 2">
  <img src="wow3.jpg" alt="Beautiful 3">
  <img src="wow4.jpg" alt="Beautiful 4">
  <img src="wow5.jpg" alt="Beautiful 5">
  <figcaption style="text-align:center;">
    Some beautiful scenery
  </figcaption>
</figure>

<figure>
  <img src="aziz.jpg" alt="aziz">
  <figcaption style="text-align:center;">
    Me with @aziz0x00, bruh where's he looking at 😭
  </figcaption>
</figure>

<figure>
  <img src="vadel.jpg" alt="mvadel">
  <figcaption style="text-align:center;">
    Mvadel captured unaware
  </figcaption>
</figure>

<figure>
  <img src="narita.jpg" alt="narita">
  <img src="monster.jpg" alt="monster">
  <figcaption style="text-align:center;">
    On our way to Narita, so taking a drink..
  </figcaption>
</figure>

<figure>
  <img src="cars.jpg" alt="cars">
  <figcaption style="text-align:center;">
    Took a picture of some cars, I wonder who I took this for 🤔
  </figcaption>
</figure>

<figure>
  <img src="woah.jpg" alt="temple">
  <figcaption style="text-align:center;">
    A temple at Naritasan
  </figcaption>
</figure>

<figure>
  <img src="charles.jpg" alt="cars">
  <figcaption style="text-align:center;">
    Charles and I...
  </figcaption>
</figure>

<figure>
  <img src="aziz2.jpg" alt="aziz2">
  <figcaption style="text-align:center;">
    Okay! aziz redeemed himself
  </figcaption>
</figure>

<figure>
  <img src="daniel.jpg" alt="daniel">
  <figcaption style="text-align:center;">
    Why is Daniel full on black??? ~~(except his cap)~~
  </figcaption>
</figure>

<figure>
  <img src="kek.jpg" alt="me">
  <figcaption style="text-align:center;">
    Lovely background
  </figcaption>
</figure>

<figure>
  <img src="katana.jpg" alt="katana">
  <figcaption style="text-align:center;">
    Certified Hashira
  </figcaption>
</figure>

<figure>
  <img src="swags.jpg" alt="swags">
  <figcaption style="text-align:center;">
    I bought some souvenirs as well
  </figcaption>
</figure>

After this, we went for the award ceremony

Team Europe won both the Jeopardy and AD CTF, congratulations to team 🎉
![Europe](europe.jpg)

We were given a coin (kinda like a metal) as a token of appreciation for our participation:
<figure>
  <img src="coin.jpg" alt="coin">
  <figcaption style="text-align:center;">
    Here it is
  </figcaption>
</figure>

And finally we took a team photo!

<figure>
  <img src="teamphoto.jpg" alt="groupphoto">
  <figcaption style="text-align:center;">
    Good luck spotting me 😏
  </figcaption>
</figure>

After this we went for some networking dinner.

We waited till the event closed and after that, I, Charles and Daniel went to a supermarket to see if we could get an headphone (though sadly they were closed)

Final pictures at Japan!!!

<figure>
  <img src="icc_rocks.jpg" alt="single">
  <img src="noice.jpg" alt="double">
  <figcaption style="text-align:center;">
    ICC 2025 Recap
  </figcaption>
</figure>

## Departure 

My return flight back to Dakar was on the 10th Nov, so I had to stay at an Airbnb (thank you once again Serdab 🙏) since the hotel checkout was 8th Nov.

<figure>
  <img src="sakura.jpg" alt="sakura">
  <figcaption style="text-align:center;">
    Japan is really cold 🥶
  </figcaption>
</figure>

<figure>
  <img src="snack.jpg" alt="snack">
  <figcaption style="text-align:center;">
    Got some snack at the airport, it was delicious 😋
  </figcaption>
</figure>

<figure>
  <img src="game.jpg" alt="game">
  <figcaption style="text-align:center;">
    Got bored so I played angry bird on the plane, I kinda suck at it 😂 
  </figcaption>
</figure>

<figure>
  <img src="bye.jpg" alt="bye">
  <figcaption style="text-align:center;">
  My final flight from Ethiopia to Dakar 🥲
  </figcaption>
</figure>



## Conclusion

The International CyberSecurity Challenge was one of the best events I have ever attended.

Competing with top teams, connecting with talented people, and experiencing such a high-level competition motivated me to push my limits and keep learning.

The biggest lesson I learned:
- If you want to be the best, you need to face the best, learn from them, push yourself to their level, and eventually surpass them.

No one reaches the finals overnight, the competition draws from hundreds of players worldwide.

Being part of ICC not only inspired me to come back stronger next year with AFRICC, but also to focus on improving my skills and preparing even harder for future challenges.

See ya!