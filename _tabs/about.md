---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

**-> Whoami?**
```c
typedef struct {
    const char *status;
    const char *passion;
    const char *skills[3];
    const char *discord;
} Pwner;

Pwner me = {
    .status = "Computer Science Student",
    .passion = "Cybersecurity Enthusiast & CTF Player",
    .skills = {"Pwn", "RE", "Offensive Security"},
    .discord = "@h4cky0u"
};


**-> About Me**

I enjoy breaking things and understanding how they work, wannabe hacker in progress.

When I'm not ~~pwning~~, I'm probably watching anime.

When I'm not watching anime, I'm probably not touching grass 😅

```c
for (;;) {
    Eat();
    Sleep();
    Pwn();
    Repeat();
}
```