Name : Maglio Razzy Effendy

NPM : 2506553616

Class : PBP Kelas Internasional

## Project Description

This is a personal portfolio website built with plain HTML5 and CSS3 and served
through the Django development server. The page is divided into four sections:
Profile, Case Files (my organisational and committee experience), Abilities and
Interests, and Transmission (contact links). The layout is built with CSS Grid and
Flexbox so that it adapts to both desktop and mobile screens, and there are a few
hover and keyframe animations to keep it from feeling too static.

The visual theme is based on Stranger Things and its "Upside Down". The page sits on
a near black background with a warm, glowing red display serif for the headings
(Cinzel, used as a free stand in for the show's ITC Benguiat title font). On top of
that there is a fixed CRT scanline and vignette overlay, a divider styled after the
blinking Christmas lights on the Byers' wall, and a few slow moving spore particles
in the hero area. Teal is used sparingly as a secondary colour to give the palette
some contrast.

## How to Run Locally

```bash
python -m venv env
source env/bin/activate        # on Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Once the server is running, open http://127.0.0.1:8000/ in a browser.

## Answers to the Reflective Questions

### 1. Semantic HTML

I used the semantic elements `<header>`, `<nav>`, `<main>`, `<footer>`, and four
`<section>` blocks (`#profile`, `#experience`, `#skills`, and `#transmission`). The
name, NPM, and program details are marked up with `<dl>`, `<dt>`, and `<dd>` because
they are genuinely label and value pairs. Each experience entry in the Case Files
section is an `<article>`, since a single entry (role, organisation, year, and a
short description) still makes sense on its own if it were taken out of the page. I
did not use `<aside>` because the page has no sidebar or side content that sits apart
from the main text. Giving every section a matching `id` also let me build the in
page navigation, where each nav link jumps straight to its section, and it gives
assistive technology and search engines clearer landmarks than a page full of plain
`<div>` elements would.

### 2. Responsive Design

The part that took the most work was the hero section. On desktop it is a two column
grid, with my name and bio on one side and the photo on the other, and there is a
decorative square offset behind the photo. A phone screen is not wide enough for two
columns, and if I let the grid collapse in document order the photo ended up in an
awkward place. To deal with this I built the grid with `grid-template-areas`, which
meant I could redefine the stacking order (name, then photo, then details) inside a
`@media (max-width: 720px)` query without changing the HTML at all. When deciding
what to move and what to shrink, I put readability first: the text stays full width,
while the photo is given a smaller maximum width on mobile because it is mostly
decorative. For the Case Files grid I avoided a fixed breakpoint entirely by using
`repeat(auto-fit, minmax(280px, 1fr))`, so the number of columns changes on its own
as the screen gets narrower, and I used `clamp()` on the headings so they scale
smoothly instead of jumping between sizes. I also added a `prefers-reduced-motion`
query that turns off the glow pulse, the drifting particles, and the blinking lights
for anyone who has asked their system for less motion.

### 3. Limitations and Next Steps

At the moment the site is completely static. My bio, experience, and skills are
written directly into `index.html`, and although the project runs on Django,
`views.py` only renders the template and passes no data to it. In practice this means
every change requires editing HTML by hand, the only way to contact me is a `mailto:`
link, and nothing on the page can update without redeploying. For the next version I
would move the experience and skills entries into a Django model so that I can manage
them from the admin page instead of editing markup, and I would add a contact form
that actually stores or sends a message rather than opening the visitor's email
client.

## AI Usage Disclosure

I used two tools while working on this assignment: Gemini and Claude Code.

I used Gemini to understand parts of my own code that I was unsure about, in
particular how `grid-template-areas` worked in the hero section and how the
`auto-fit` and `minmax()` pattern behaved in the card grid. It also helped me with a
few CSS lines I was stuck on while moving content around between the desktop and
mobile layouts.

I used Claude Code to research the Stranger Things visual style (the ITC Benguiat
title font, the glowing red on black look, and motifs such as the Christmas lights
and the Upside Down) and to help apply that theme across `index.html` and
`style.css`, including the CRT overlay, the glow and flicker animations, the lights
divider, the particles, and the reworked card styling. I reviewed the result myself
and confirmed that the site still runs with `python manage.py runserver`.
