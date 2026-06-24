---
title: Ecowas 2026 Recap
date: 2026-06-24 03:00:00 +0000
categories: [CTF]
tags: [onsite, events]
math: true
mermaid: true
media_subpath: /assets/posts/2026-06-24-Ecowas-Recap
image:
  path: preview.png
---

## ECOWAS Cybersecurity Hackathon 2026 - Accra, Ghana

In this blog post, I'll be sharing my personal experience as a participant and winner of the ECOWAS Cybersecurity Hackathon 2026.

### Overview

The Economic Community of West African States (ECOWAS) organizes an annual cybersecurity competition that attracts top cybersecurity teams from across West Africa. The participating teams compete in a series of challenges, with the highest-ranking teams advancing to the finals.

Representing Nigeria, my team, error, successfully qualified for the ECOWAS Cybersecurity Regional Finals. 

<figure>
  <img src="preview2.png" alt="team error">
  <figcaption style="text-align:center;">
    Representing Nigeria (error)
  </figcaption>
</figure>

The finals, held in Accra, Ghana, brought together the best cybersecurity teams from across West Africa to compete for the regional championship.

Twelve teams representing twelve countries qualified for the finals:

![teams](teams.jpg)

| Country            | Team                    |
| ------------------ | ----------------------- |
| 🇧🇯 Benin         | Escadron                |
| 🇨🇻 Cape Verde    | CyberSharks             |
| 🇨🇮 Côte d'Ivoire | Back2Root               |
| 🇬🇲 Gambia        | GamHunters              |
| 🇬🇭 Ghana         | CYCLONE                 |
| 🇬🇳 Guinea        | SilySec                 |
| 🇬🇼 Guinea-Bissau | Cyber_gw                |
| 🇱🇷 Liberia       | Lyberia Cybers Warriors |
| 🇳🇬 Nigeria       | error                   |
| 🇸🇳 Senegal       | Jambars                 |
| 🇸🇱 Sierra Leone  | Sudo-SL                 |
| 🇹🇬 Togo          | RedTeam-TG              |

Prior to the regional finals, a national qualification round was conducted to determine the team that would represent each country.

The qualification process consisted of three phases:

- Jeopardy
- King of the Hill (KoTH)
- Battleground

Our team, error, placed 1st nationally in all three phases, earning the opportunity to represent Nigeria at the ECOWAS Cybersecurity Regional Finals in Accra, Ghana.

### Sunday, June 7: Arrival in Accra

Our flight to Accra was on *Sunday, June 7*. Before that, I had travelled back home to *Lagos, Nigeria* since I was at school, on *Friday, June 5*.

At the airport, I met up with my teammates, *securedviki* and *proflamyt*.

![airport](IMG_4254.jpg)
![airport2](IMG_4258.jpg)
![plane1](IMG_4269.jpg)
<figure>
  <img src="plane2.jpg" alt="aiport">
  <figcaption style="text-align:center;">
    Me on my phone (as usual 😭)
  </figcaption>
</figure>

Our fourth teammate, *Theory*, was based in *Dakar, Senegal* at the time, so he travelled separately with the Senegalese team.

Upon arriving in Accra, a representative from the hotel was waiting to pick us up from the airport and take us to the venue.

<figure>
  <img src="plane3.jpg" alt="team error">
  <figcaption style="text-align:center;">
    Interestingly, we had the entire shuttle bus to ourselves, as none of the other teams had arrived yet.
  </figcaption>
</figure>

The check-in process was smooth, and each of us was assigned an individual room.

I also got some good view from the hotel room.

<figure>
  <img src="IMG_4286.jpg" alt="h4cky0u">
  <figcaption style="text-align:center;">
      👀
  </figcaption>
</figure>

![room1](IMG_4342.jpg)
![room2](IMG_4455.jpg)

About two hours later, *Theory*, my closest friend, finally arrived. The last time I had seen him was during my three-month internship in Dakar, Senegal, so it felt really good to reunite after all that time.

![theory](IMG_4284.jpg)

Later in the evening, we went out to grab something at the nearest KFC.

<figure>
  <img src="camphoto_1804928587.jpg" alt="kfc">
  <figcaption style="text-align:center;">
      I was starving but viki (my team cap) got us food 🥹 
  </figcaption>
</figure>

### Monday, June 8: Briefing

Monday morning began with the official competition briefing, conducted by the organizers and Mrs. Folake Olagunju, Director of Digital Economy and Post at the ECOWAS Commission.

During the session, we were introduced to the competition format, schedule, and start times. We also received a piece of news that took some time to process: the scoreboard would remain hidden throughout the entire competition. Unlike most CTF events, we would have no way of knowing our standing relative to the other teams until the competition ended.

We were also informed that a separate women's cybersecurity competition would take place later that evening.

The competition consisted of six phases:

| Order | Phase |
|:-----:|-------|
| 1 | Jeopardy (Round 1) |
| 2 | King of the Hill (Double Session, 4 Teams per Hill) |
| 3 | Code Review |
| 4 | Red vs Blue (Double Session) |
| 5 | Battleground (Double Session) |
| 6 | Jeopardy (Final Round) |

Based on our experience during the qualification rounds, we already had a strong suspicion about which phase would be the most decisive. King of the Hill had consistently created the largest point differences between teams, and we expected it to play a major role in determining the final standings.

### Tuesday, June 9: Opening Ceremony

Tuesday morning started with a short opening ceremony before the competition officially began.

Each country was called to the stage with a song from their region playing in the background, and every team was expected to dance their way onto the stage as part of the introduction.

Needless to say, some teams handled this better than others 😭.

#### Phase 1: Jeopardy

The first phase of the competition was a large-scale Jeopardy round.

Many of the challenges were straightforward enough that a capable LLM could solve them with minimal human intervention. I suspect the organizers anticipated this. First bloods were appearing across the scoreboard at a pace I had never seen in a traditional CTF. 

Every team had clearly come prepared, and some had obviously invested significant effort into developing and refining their AI-assisted workflows before arriving in Accra.

At that point, choosing not to use the same tools as everyone else was hardly an option. Refusing to adapt would have meant falling behind on principle. 

The competition quickly became as much a race between AI workflows as it was a test of technical skill.

The Jeopardy round stretched well beyond the opening day. We were still solving challenges late into Tuesday night and continued working through Wednesday morning.

#### Phase 2: King of the Hill

King of the Hill (KOTH) began at 9:00 a.m. on Wednesday. Going into the round, we already knew this was likely where the competition would be won or lost.

For those unfamiliar with KOTH, the objective is simple: gain access to a shared target machine, escalate privileges to root, and then patch the vulnerability you used so that other teams cannot exploit the same path.

To prove ownership of the machine, teams must write their team name to **/root/team.txt**. The first team to claim a hill receives a bonus, and additional points are awarded for every scoring tick that your team's name remains in the file. To keep things competitive, the machine is reset every hour, forcing teams to repeat the process and fight for control all over again.

Unlike Jeopardy, where teams solve challenges independently, KOTH is a direct contest between competitors. Every point you gain comes at someone else's expense.

![koth](koth.png)

For the first KOTH session, we were matched against **CYCLONE (Ghana), Jambars (Senegal), and Sudo-SL (Sierra Leone)**.

Once the round began, we quickly gained access to the target machine, escalated privileges, and successfully patched the vulnerability before any of the other teams could take control.

As a result, we secured the maximum possible score of **1000** points, a feat matched by only one other team, **SilySec (Guinea)**.

After securing the machine, we automated the process. We developed scripts that would automatically exploit the target, gain control, and apply our patches whenever the machine was reset. 

Since each hill was reset every hour, having a reliable automation pipeline significantly reduced the time required to reclaim ownership and allowed us to focus on improving our defenses and preparing for subsequent rounds.

#### Phase 3: Code Review

The next phase was Code Review, and honestly, it was a welcome change of pace. After the AI-driven rush of the Jeopardy round, it was refreshing to have a challenge that required teams to sit down and actually read code.

The format was straightforward. An administrator would project a piece of C or web application code on a screen, and each team had to:
- Identify the vulnerability
- Explain how it should be patched

Although it was never formally presented this way, the challenges naturally fell into two categories: web and pwn. 

Fortunately for us, those were areas where our team was particularly strong. We had strong pwners and web players in the team, making this round feel much closer to our comfort zone. The "manual side of things".

Several teams took their turns before us. The vulnerabilities covered a wide range of common security issues, including SQL injection, Cross-site Scripting (XSS), Buffer Overflow, Integer Overflows, Prototype Pollution and a number of others.

When our turn came, we were presented with a challenge similar in spirit to the illustrative example below:

```php
<?php

class Logger
{
    public $filename;
    public $data;

    public function __destruct()
    {
        file_put_contents($this->filename, $this->data);
    }
}

$data = $_POST['data'];
$obj = unserialize($data);
```

Again, just an example. Can you spot the vulnerability, name it, and explain how to patch it? If yes, then you've got a pretty good idea of what the Code Review round was testing. The whole phase was about recognizing insecure code patterns quickly and accurately.

#### Phase 4: Red vs Blue

The next phase was Red vs Blue, a format that forces teams to attack and defend at the same time.

Each team is given a vulnerable machine. The objective is to exploit your opponent's system to retrieve their flag while simultaneously securing your own infrastructure against incoming attacks. Success requires balancing offensive and defensive efforts under significant time pressure.

For our match, we were paired against *SilySec* (Guinea).

The round started well for us. We were the first team to successfully compromise the opposing machine and capture their flag, earning the coveted first blood bonus.

However, the victory was not entirely one-sided. Before we could fully secure and patch our system, *SilySec* managed to gain access to our machine and retrieve our flag as well.

#### Phase 5: Battleground

Much like King of the Hill, teams were required to compromise a target machine. However, instead of maintaining control over the system, the objective was simply to retrieve and submit the user and root flags as quickly as possible. Speed was everything.

For this round, we were paired against CyberSharks (Cape Verde).

We managed to capture the user flag first. However, CyberSharks were faster when it came to privilege escalation and secured the root flag before we could.

By this stage of the competition, we still had no idea where we stood overall because the scoreboard remained hidden. However, after the Code Review phase, the organizers had briefly given us a glimpse of the rankings. 

Based on what we saw and our performances in the subsequent rounds, we suspected that we were somewhere in the top three, although there was no way to be certain.

#### Final Jeopardy

The final phase of the competition was another Jeopardy round, but this time the scoring worked differently.

Unlike the opening Jeopardy session, this round did not have its own standalone ranking. Instead, every point earned was added directly to each team's cumulative competition score. At that stage, leaderboard position was irrelevant the only thing that mattered was maximizing points.

Our goal was this: solve as many challenges as possible, collect every flag we could, and keep pushing until the very end.

Regardless, we stayed focused on the competition itself. We kept solving, submitting, and chasing every available point right up until the timer finally reached 00:00:00:00.

#### Results Ceremony

When the timer finally hit zero, nobody celebrated.

To be honest, there wasn't even much relief. We were exhausted from days of competition, still had no idea where we stood, and could do nothing but wait for the results.

The awards ceremony felt longer than any of the competition rounds. Team after team was called to the stage. Certificates were handed out, photos were taken, and the suspense only grew. Even at that point, we still had no idea whether we had done enough.

Then came the moment that changed everything.

The host announced that the three remaining teams should stand up and move to the back of the room.

We stood.

That was the moment it finally sank in: we had made the podium. Out of every team that had qualified from across West Africa, we were in the final three.

For the first time since the competition began, we knew that all the preparation, the qualification rounds, the late nights, and the pressure had been worth it.

