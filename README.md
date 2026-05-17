# Fingal Valley RRA — Website

Static site for the **Fingal Valley Residents & Ratepayers Association** (Tasmania, AU).
Built with Hugo · Sveltia CMS · Web3Forms · Cloudflare Pages.

---

## Resuming work (daily workflow)

### 1. Open the project folder

The working copy lives at:
```
C:\Users\NinaTran\Downloads\FingalWeb
```

### 2. Start the dev server

Open **PowerShell** (or Windows Terminal), then run:

```powershell
docker-compose -f "C:\Users\NinaTran\Downloads\FingalWeb\docker-compose.yml" --project-directory "C:\Users\NinaTran\Downloads\FingalWeb" up
```

Or, if your terminal is already in the project folder:

```powershell
cd "C:\Users\NinaTran\Downloads\FingalWeb"
docker-compose up
```

The first run pulls the Hugo Docker image (~200 MB). Subsequent starts are instant.

### 3. Open the site

```
http://localhost:1313
```

The server watches for file changes every 500 ms and **hot-reloads the browser automatically** — just save a file and refresh.

### 4. Stop the server

Press `Ctrl + C` in the terminal. Or from another terminal:

```powershell
docker-compose -f "C:\Users\NinaTran\Downloads\FingalWeb\docker-compose.yml" --project-directory "C:\Users\NinaTran\Downloads\FingalWeb" down
```

---

## Editing content

| What to edit | File location |
|---|---|
| Home page text | `content/_index.md` |
| About page | `content/about.md` |
| Add a news post | Create a new `.md` file in `content/news/` |
| Add an event | Create a new `.md` file in `content/events/` |
| Add a document | Create a new `.md` file in `content/documents/` |
| Contact page intro | `content/contact.md` |
| Site title / menu | `config.toml` |
| Page layouts (HTML) | `themes/fingal-theme/layouts/` |
| Styles (CSS) | `themes/fingal-theme/static/css/style.css` |
| Images | `static/images/` |
| Downloadable files | `static/docs/` |

### News post front matter template

```yaml
---
title: "Your Post Title"
date: 2026-06-01
summary: "One or two sentences shown on the listing page."
author: "FVRRA Committee"
draft: false
---

Your content here in Markdown.
```

### Event front matter template

```yaml
---
title: "Event Name"
date: 2026-06-01          # publish date
eventDate: "2026-07-20T19:00:00"
eventTime: "7:00 PM"
eventLocation: "Fingal Valley Community Hall"
draft: false
---

Event details here.
```

---

## Project structure

```
FingalWeb/
├── config.toml                  ← site title, menu, Web3Forms key, hero image
├── content/
│   ├── _index.md                ← home page text
│   ├── about.md
│   ├── contact.md
│   ├── thank-you.md
│   ├── news/                    ← blog-style posts
│   ├── events/                  ← community events
│   └── documents/               ← downloadable resources
├── static/
│   ├── images/                  ← photos and logos served to the browser
│   ├── docs/                    ← downloadable .docx / .pdf files
│   └── admin/                   ← Sveltia CMS (config.yml + index.html)
└── themes/fingal-theme/
    ├── layouts/                 ← HTML page templates
    └── static/
        ├── css/style.css        ← all site styles
        └── js/nav.js            ← mobile hamburger menu
```

---

## Deploying to production (Cloudflare Pages)

Before first deploy, complete these one-time steps:

| Step | What to do |
|---|---|
| 1. GitHub repo | `git init` → `git add .` → `git commit` → push to GitHub |
| 2. Cloudflare Pages | Dashboard → Pages → New project → connect GitHub repo |
| 3. Build settings | Build command: `hugo` · Output dir: `public` · Env var: `HUGO_VERSION = 0.147.0` |
| 4. Update baseURL | Edit `config.toml` → set `baseURL` to your real `.pages.dev` URL → commit |
| 5. Web3Forms | Sign up at web3forms.com → copy access key → paste into `config.toml` `web3formsKey` |
| 6. Sveltia CMS OAuth | Create GitHub OAuth App (callback: `https://sveltia-cms-auth.pages.dev/callback`) → register with Sveltia proxy → update `static/admin/config.yml` `repo:` field |
| 7. CMS editor access | Add org admin as GitHub collaborator (Write access) → they log in at `yoursite.pages.dev/admin/` |

After setup, every `git push` triggers an automatic redeploy (~1 minute).

---

## Tech stack

| Tool | Purpose |
|---|---|
| [Hugo](https://gohugo.io) | Static site generator |
| [Sveltia CMS](https://github.com/sveltia/sveltia-cms) | Web-based content editor at `/admin/` |
| [Web3Forms](https://web3forms.com) | Contact & membership forms → email |
| [Cloudflare Pages](https://pages.cloudflare.com) | Free hosting + CDN |
| [Docker](https://docker.com) | Local development (no Hugo install needed) |
