---
title: Web Writeup @ CSEAN CTF 2026
date: 2026-05-27 03:00:00 +0000
categories: [CTF]
tags: [web]
math: true
mermaid: true
media_subpath: /assets/posts/2026-05-27-cseanctf-web
image:
  path: preview.png
---

## CSEAN CTF 2026

### Overview

CSEAN CTF has concluded with 9 web challenges released.

Here are my writeups as the author for some of them.

#### CNotes

- **Challenge Name** : CNotes
- **Description** :

```description
Online note-taking has always felt like too much hassle.

Creating accounts, remembering passwords… it gets tiring.

So here's something different: CNotes a platform with zero authentication and seamless security.

Just open it and start writing.

We've also rolled out a new feature: you can now report abuse, and an admin will review it.
```

- **author** : h4cky0u
- **solves** : 7/17

<h5 align="center">Source Code Analysis</h5>

The web application source code was provided.

Below is the file structure:

![one](cnotes_one.png)

From the `bot` directory, we can already infer that this is likely a client-side based challenge.

We begin by analyzing the `docker-compose.yml` file, as it reveals how the overall challenge infrastructure is set up.

```yml
version: "3"
services:
  webapp:
    build: ./src
    ports:
      - "3000:3000"
    restart: always
    environment:
      - JWT_SECRET_KEY='REDACTED'
      - BOT_URL=http://bot:9999/visit
  bot:
    build: ./bot
    restart: always
    environment:
      - JWT_SECRET_KEY='REDACTED'
      - DOMAIN=webapp
      - PORT=3000
      - FLAG=cseanctf26{fake_flag_for_testing}
```

The Docker setup consists of two services: 
- one hosting the main web application located in the `src` directory
- another responsible for running the bot, located in the `bot` directory.

It also setups some environment variable.

We'll begin by spinning up the container.

![docker_start_one](docker_start_one.png)

Now we analyze the main web application code.

Here's the `Dockerfile`

```dockerfile
FROM node:17.6

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN groupadd appgroup && useradd -g appgroup appuser 

COPY ./ ./

EXPOSE 3000

USER appuser

CMD node index.js
```

This simply setups a node container then creates a `appuser` user and runs the `index.js` script, from the compose file, the server is going to listen on port `3000` and that port is exposed to the main host on port `3000`.

It might be helpful to look through `package.json`

```js
{
  "dependencies": {
    "cookie-parser": "^1.4.6",
    "cross-fetch": "^3.1.5",
    "ejs": "^3.1.6",
    "express": "^4.17.3",
    "express-async-errors": "^3.1.1",
    "jsonwebtoken": "^8.5.1",
    "sqlite3": "^5.0.2"
  }
}
```

Although, there are vulnerabilities in some of the packages, but they're not needed to solve the challenge itself.

Here's the main page of the challenge when visited.

<figure>
  <img src="index.png" alt="statistics">
  <figcaption style="text-align:center;">
    Index page
  </figcaption>
</figure>


`index.js`

```js
const express = require('express')
const sqlite3 = require('sqlite3').verbose()
const jwt = require('jsonwebtoken')
const cookieParser = require('cookie-parser')
const crypto = require('crypto')
const fetch = require('cross-fetch')
require('express-async-errors')

const PORT = 3000
const JWT_SECRET = process.env.JWT_SECRET_KEY || 'REDACTED'

const app = express()

app.set('view engine', 'ejs')
app.use(express.json())
app.use(cookieParser())

app.use(function (req, res, next) {
    req.loggedUserId = undefined
    if (req.cookies.session) {
        try {
            const decoded = jwt.verify(req.cookies.session, JWT_SECRET);
            req.loggedUserId = decoded.userid
        } catch (err) {
            res.clearCookie('session')
            return res.redirect('/')
        }
    }
    next()
})

app.use(function (req, res, next) {
    if (req.loggedUserId === undefined) {
        req.loggedUserId = parseInt(Math.random() * 1000000000000) + 1
        const token = jwt.sign({ userid: req.loggedUserId }, JWT_SECRET, { expiresIn: '3h' });
        res.cookie('session', token)
    }
    next()
})

app.use(function (req, res, next) {
    const random = parseInt(Math.random() * 100000000000000000000000)
    res.locals.csp_nonce = crypto.createHash('md5').update(`${random}`).digest('base64')
    res.set('Content-Security-Policy', `script-src 'nonce-${res.locals.csp_nonce}';`)
    next()
})

const db = new sqlite3.Database(':memory:');
db.exec("CREATE TABLE notes (noteid INTEGER, userid INTEGER, content TEXT, PRIMARY KEY(noteid, userid))")

async function db_get(sql) {
    return new Promise((resolve, reject) => {
        db.get(sql, (e, r) => {
            if (e) {
                reject(e)
            }
            resolve(r)
        })
    })
}

app.get('/', async (req, res) => {
    res.render('index')
})

app.get('/notes', async (req, res) => {
    res.render('notes')
})

app.get('/add', async (req, res) => {
    res.render('addnote')
})

app.get('/abuse', async (req, res) => {
    res.render('abuse')
})

app.get('/api/note/:id', async (req, res) => {
    const noteid = parseInt(req.params.id)
    const note = await db_get(`SELECT * FROM notes WHERE userid = ${req.loggedUserId} AND noteid = ${noteid}`)
    if (note) {
        res.json(note)
    } else {
        res.status(404).json({ error: 'not found' })
    }
})

app.post('/api/note', async (req, res) => {
    const content = req.body.content
    const last_note_id = (await db_get(`SELECT MAX(noteid) AS last FROM notes WHERE userid = ${req.loggedUserId}`))['last'] ?? -1
    const noteid = last_note_id + 1
    const x = await db_get(`INSERT INTO notes (noteid, userid, content) VALUES (${noteid}, ${req.loggedUserId}, '${content}')`)
    res.json({ noteid })
})

app.post('/api/abuse', async (req, res) => {
    const link = req.body.link
    console.log(link)

    if (!link || typeof link !== 'string' || !link.startsWith('http'))
        return res.status(400).json({ msg: 'Invalid link' })

    try {
        const r = await fetch(process.env.BOT_URL, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'url': link })
        }).then(r => {
            if (r.status === 200) {
                res.json({ msg: 'Visited' })
            } else {
                res.status(r.status).json({ msg: 'Error' })
            }
        })
    } catch (error) {
        res.status(500).json({ msg: 'Error: ' + error })
    }
})

app.listen(PORT, () => {
    console.log(`App listening on port ${PORT}`)
})

setTimeout(() => {
    console.log("Restarting app");
    process.exit(0);
}, 5 * 60 * 1000);

```

Looking at it, there are not so many routes.

I'll go through the necessary code snippet needed.

It reads the `JWT_SECRET` from the environment variable defined in the docker compose file.

```js
const PORT = 3000
const JWT_SECRET = process.env.JWT_SECRET_KEY || 'REDACTED'
```

This is how the database is initialized. It uses an in-memory SQLite database, where a table named `notes` is created with three columns: `(noteid, userid, content)`.

```js
const db = new sqlite3.Database(':memory:');

db.exec(`
  CREATE TABLE notes (
    noteid INTEGER,
    userid INTEGER,
    content TEXT,
    PRIMARY KEY(noteid, userid)
`);
```

The application also defines a helper function for querying the database:

```js
async function db_get(sql) {
    return new Promise((resolve, reject) => {
        db.get(sql, (e, r) => {
            if (e) {
                reject(e);
            }
            resolve(r);
        });
    });
}
```

There are three middleware functions defined.

For every incoming request, these middleware are executed first. Only if all of them pass is the request considered valid and allowed to proceed.

The first middleware checks whether a `session` cookie is present. If it exists, it verifies the JWT contained in the cookie and extracts the `userid` from it. This value is then stored in `req.loggedUserId` for use in later handlers.

```js
app.use(function (req, res, next) {
    req.loggedUserId = undefined;

    if (req.cookies.session) {
        try {
            const decoded = jwt.verify(req.cookies.session, JWT_SECRET);
            req.loggedUserId = decoded.userid;
        } catch (err) {
            res.clearCookie('session');
            return res.redirect('/');
        }
    }

    next();
});
```

The second middleware is responsible for creating a valid JWT session token when a user does not already have one. If `req.loggedUserId` is not set, it generates a random user ID, signs it into a JWT, and assigns it to the `session` cookie.

```js
app.use(function (req, res, next) {
    if (req.loggedUserId === undefined) {
        req.loggedUserId = parseInt(Math.random() * 1000000000000) + 1;

        const token = jwt.sign(
            { userid: req.loggedUserId },
            JWT_SECRET,
            { expiresIn: '3h' }
        );

        res.cookie('session', token);
    }

    next();
});
```

The third middleware generates a Content Security Policy (CSP) for each request. It creates a random value, hashes it using MD5, encodes it in base64, and uses it as a nonce for inline scripts.

```js
app.use(function (req, res, next) {
    const random = parseInt(Math.random() * 100000000000000000000000);

    res.locals.csp_nonce = crypto
        .createHash('md5')
        .update(`${random}`)
        .digest('base64');

    res.set(
        'Content-Security-Policy',
        `script-src 'nonce-${res.locals.csp_nonce}';`
    );

    next();
});
```

There are 3 main features that we can make use of.

Here's an image of all:

<figure>
  <img src="create_note.png" alt="statistics">
  <figcaption style="text-align:center;">
    Create a note
  </figcaption>
</figure>

<figure>
  <img src="view_note.png" alt="statistics">
  <figcaption style="text-align:center;">
    View note
  </figcaption>
</figure>

<figure>
  <img src="report_note.png" alt="statistics">
  <figcaption style="text-align:center;">
    Report note
  </figcaption>
</figure>

`create_note`:

```js
app.post('/api/note', async (req, res) => {
    const content = req.body.content;

    const last_note_id = (
        await db_get(
            `SELECT MAX(noteid) AS last FROM notes WHERE userid = ${req.loggedUserId}`
        )
    )['last'] ?? -1;

    const noteid = last_note_id + 1;

    await db_get(
        `INSERT INTO notes (noteid, userid, content)
         VALUES (${noteid}, ${req.loggedUserId}, '${content}')`
    );

    res.json({ noteid });
});
```

When a note is created:
- The note content is taken from the HTTP POST body.
- The application queries the database to find the highest existing `noteid` for the current `userid`.
- It increments this value to generate a new `noteid`.
- Finally, it inserts the new note into the `notes` table and returns the created `noteid` as a response.

`view_note`:

```js
app.get('/api/note/:id', async (req, res) => {
    const noteid = parseInt(req.params.id);

    const note = await db_get(
        `SELECT * FROM notes 
         WHERE userid = ${req.loggedUserId} 
         AND noteid = ${noteid}`
    );

    if (note) {
        res.json(note);
    } else {
        res.status(404).json({ error: 'not found' });
    }
});
```

When a note is requested:
- The note ID is taken from the URL parameter and converted to an integer.
- The application queries the database for a matching record using both the current `userid` and the provided `noteid`.
- If a matching note is found, it is returned as a JSON response.
- Otherwise, the server responds with a `404` Not Found error.

`report_note`:

```js
app.post('/api/abuse', async (req, res) => {
    const link = req.body.link;
    console.log(link);

    if (!link || typeof link !== 'string' || !link.startsWith('http')) {
        return res.status(400).json({ msg: 'Invalid link' });
    }

    try {
        const r = await fetch(process.env.BOT_URL, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: link })
        }).then(r => {
            if (r.status === 200) {
                res.json({ msg: 'Visited' });
            } else {
                res.status(r.status).json({ msg: 'Error' });
            }
        });
    } catch (error) {
        res.status(500).json({ msg: 'Error: ' + error });
    }
});
```

When a note is reported as abusive:
- The link is extracted from the HTTP POST body.
- It validates that the input is a string and begins with http.
- If valid, the server forwards the link to the bot service via a POST request (`BOT_URL`) with the `URL` included in a JSON body.

Here is the template used when viewing a note:

```html
<%- include('header') -%>

    <div class="container col-lg-6 col-md-8">

        <div class="d-flex flex-row justify-content-between align-items-center pt-3 text-center">
            <div class="btn btn-light" id="prev">&#8592;</div>
            <span class="" id="number">0</span>
            <div class="btn btn-light" id="next">&#8594;</div>
        </div>

        <div class="row justify-content-center text-center pt-3">
            <div id="content"></div>
        </div>


    </div>
    <script nonce="<%= locals.csp_nonce %>">
        function loadNote() {
            const id = parseInt(location.hash.substring(1))
            console.log(id)

            if (!isNaN(id)) {

                fetch('/api/note/' + id,)
                    .then(r => r.json()
                        .then(j => {
                            console.log(j)
                            document.getElementById('number').innerText = id
                            const el = document.getElementById('content')
                            if (j.error !== undefined) {
                                el.innerHTML = j.error
                            } else {
                                el.innerHTML = j.content
                            }
                        })
                        .catch(e => alert(e))
                    ).catch(e => alert(e))
            }

        }

        window.onhashchange = loadNote

        if (location.hash === '') {
            location.hash = '0'
        } else {
            loadNote()
        }

        document.getElementById('next').addEventListener('click', () => {
            location.hash = parseInt(location.hash.substring(1)) + 1
        })

        document.getElementById('prev').addEventListener('click', () => {
            location.hash = parseInt(location.hash.substring(1)) - 1
        })

    </script>

    <%- include('footer') -%>
```

The important section is the javascript code.

```html
    <script nonce="<%= locals.csp_nonce %>">
        function loadNote() {
            const id = parseInt(location.hash.substring(1))
            console.log(id)

            if (!isNaN(id)) {

                fetch('/api/note/' + id,)
                    .then(r => r.json()
                        .then(j => {
                            console.log(j)
                            document.getElementById('number').innerText = id
                            const el = document.getElementById('content')
                            if (j.error !== undefined) {
                                el.innerHTML = j.error
                            } else {
                                el.innerHTML = j.content
                            }
                        })
                        .catch(e => alert(e))
                    ).catch(e => alert(e))
            }

        }

        window.onhashchange = loadNote

        if (location.hash === '') {
            location.hash = '0'
        } else {
            loadNote()
        }

        document.getElementById('next').addEventListener('click', () => {
            location.hash = parseInt(location.hash.substring(1)) + 1
        })

        document.getElementById('prev').addEventListener('click', () => {
            location.hash = parseInt(location.hash.substring(1)) - 1
        })

    </script>
```

When the page loads, the `<script>` tag is rendered, and it sets the `nonce` attribute using the value generated by the middleware which is stored in `res.locals.csp_nonce`. This allows inline JavaScript execution under the Content Security Policy.

You can read more about nonces here: https://content-security-policy.com/nonce/

The application defines a function called `loadNote`, which is triggered by a `window` event whenever the URL fragment (hash) changes.

This function extracts the `noteid` from the fragment. If the value is numeric, it fetches the corresponding note from the server.

If the request is successful, the response is parsed and the `DOM` is updated by injecting the note content into the element with the id `content`:

```js
document.getElementById('content').innerHTML = j.content;
```

