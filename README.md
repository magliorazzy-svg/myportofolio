Name : Maglio Razzy Effendy

NPM : 2506553616

Class : PBP Kelas Internasional

## Project Description

This is a personal portfolio website built with Django, following the Model-View-
Template pattern. The Profile page carries the hero, Abilities, and Transmission
(contact) sections, while Case Files (my organisational and committee experience)
and Achievements (my academic and non-academic awards) are each a separate page
backed by their own Django model, view, and template. The layout is built with CSS
Grid and Flexbox so that it adapts to both desktop and mobile screens, and there are
a few hover and keyframe animations to keep it from feeling too static.

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

### Assignment 1

#### 1. Semantic HTML

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

#### 2. Responsive Design

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

#### 3. Limitations and Next Steps

At the time I first wrote this answer, the whole site was static: my bio,
experience, and skills were written directly into `index.html`, and `views.py` only
rendered the template without passing it any data. Since then, in Tutorial 02 and
Assignment 2, I moved the experience and achievement sections into their own Django
models (`Experience` and `Achievement`), each with its own view and template, so
those two sections are no longer hardcoded and new entries can be added without
touching any HTML. What is still static is the bio text on the Profile page, the
skill tags in the Abilities section, and the social links in Transmission, and the
only way to contact me is still a `mailto:` link rather than a form that actually
stores or sends a message. For the next iteration I would move the skills into a
model as well, following the same pattern as Experience and Achievement, and add a
working contact form.

### Assignment 2

#### 1. Request Flow

When a visitor opens `/achievements/`, the request first hits `portofolio/urls.py`,
the project level URL configuration, which forwards every path to `main.urls` through
`include("main.urls")`. Inside `main/urls.py`, the path `"achievements/"` is matched
to the view function `show_achievements`, registered under the name
`main:show_achievements` because of `app_name = "main"`. Django then calls
`show_achievements(request)` in `main/views.py`. That view queries the `Achievement`
model with `Achievement.objects.all()`, which asks the database for every row in the
achievement table and returns it as a queryset. The view puts that queryset into a
context dictionary under the key `achievement_list`, along with `name`, and passes
both to `render()`. Render loads `templates/achievements.html`, evaluates the
`{% for achievement in achievement_list %}` loop against the context, fills in every
`{{ achievement.field }}` placeholder, and returns the finished HTML as the response
the browser displays.

#### 2. Model vs Hardcoding

Storing data in a model instead of writing it directly into HTML separates the data
from the presentation. If I hardcode an achievement into `achievements.html`, adding
a new one, fixing a typo, or removing one that is no longer relevant means editing
markup by hand and risking breaking the surrounding HTML structure. With a model, the
same change is a single `Achievement.objects.create(...)` call or an edit through the
admin panel, and the template does not change at all, since it only knows how to loop
over whatever rows exist. This also means the data can eventually come from anywhere
else (a form, an API, an admin panel) without touching the template, and Django can
validate, query, or filter it instead of me manually keeping the HTML consistent every
time something changes.

#### 3. makemigrations vs migrate

`makemigrations` looks at the current state of the models in `main/models.py`,
compares it against the migration files Django already knows about, and writes a new
migration file describing the difference as a set of operations, for example "create
model Achievement" or "add field year to Achievement". It does not touch the database
at all, it only generates instructions. `migrate` is the command that actually applies
those instructions to the database, running whatever is needed to create or alter
tables so they match the migration files. A concrete example from this project: after
I added the `Achievement` class to `models.py`, running `makemigrations` produced
`main/migrations/0003_achievement.py` with the instructions to create the new table
and its columns, and only after I ran `migrate` did that table actually get created in
`db.sqlite3` so the app could start reading and writing `Achievement` rows.

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

For Tutorial 02 and Assignment 2, I used Claude Code as a tutor rather than to write
the feature for me. It walked me through what a Django model, view, and template each
do, using the existing `Experience` model as a worked example before I wrote the
`Achievement` model, view, template, URL, and tests myself. I made several mistakes
along the way that Claude Code helped me find and understand rather than fixing
directly: an invalid `import X import Y` line in `views.py`, a `year` field that I had
first written as `DateTimeField(auto_now_add=True)`, which would have silently
overwritten every achievement's year with the current date instead of the real year it
happened, a leftover `{% if experience.is_ongoing %}` block copied into
`achievements.html` that referenced a variable that did not exist there, a `class`
attribute I accidentally used to hold display text instead of an actual CSS class, and
a test method that was indented one level too deep, which meant it was never actually
being run. I fixed each of these myself and re-ran `python manage.py test main`
afterwards to confirm all nine tests passed before committing.
