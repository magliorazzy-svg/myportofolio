Name : Maglio Razzy Effendy

NPM : 2506553616

Class : PBP Kelas Internasional

## Project Description

This is a personal portfolio website built with Django, following the Model-View-
Template pattern. Every page extends a shared `templates/base.html`, which holds the
head, navigation, and footer, so each page template only has to define its own
`{% block content %}`. The Profile page carries the hero, Abilities, and Transmission
(contact) sections, while Case Files (my organisational and committee experience),
Achievements (my academic and non-academic awards, loaded with AJAX), and Projects are each a separate
page backed by their own Django model, view, and template. Projects is the one
section with full CRUD: new projects are added through a `ModelForm`, existing ones
can be edited or deleted from the Projects page, and the list itself is populated by
serialising the `Project` model to JSON and deserialising it back before rendering.
The layout is built with CSS Grid and Flexbox so that it adapts to both desktop and
mobile screens, and there are a few hover and keyframe animations to keep it from
feeling too static.

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

### Assignment 3

#### 1. ModelForm vs Manual HTML Forms, and Why CSRF Matters

Writing `<input>` elements by hand for every field means keeping the HTML in sync
with the model by hand too: if I add or rename a field on `Project`, I have to
remember to update the form markup and its validation to match. A `ModelForm` reads
the field definitions straight from `Meta.model`, so it generates the right input
type for each field (a text input for `CharField`, a textarea for `TextField`, a URL
input for `URLField`) and reuses the same validation the model already defines
(`max_length`, whether a field can be blank, whether a URL is actually a valid URL),
instead of me reimplementing that by hand. It also removes a step: `form.save()`
writes straight to the database, so there is no separate `Project.objects.create(...)`
call to keep in sync with whatever the form collected. The `{% csrf_token %}` tag is
necessary because Django rejects any POST request that does not carry a matching
token: without it, a different site could embed a hidden form pointed at my `/projects/
add/` endpoint and get a visitor's browser to submit it using their own session,
without my form ever being involved. The token proves the POST actually came from a
page my server rendered, not from somewhere else.

#### 2. JSON vs XML

I would pick JSON for this project, and for most modern web development in general.
A JSON array of projects is just key-value pairs and does not repeat the field name
in an opening and a closing tag the way XML does, so it is noticeably smaller for the
same data. It also maps directly onto the data structures Python and JavaScript
already use (dictionaries and lists on one side, objects and arrays on the other),
so there is no extra translation step, and both languages can parse it natively
(`json.loads` in Python, `JSON.parse` in JavaScript) without needing an XML parser or
a schema. XML still has real advantages in places that need strict document
structure, attributes, namespaces, or validation against a schema, which is why it
still shows up in older enterprise systems, but a small set of fields like `title`,
`description`, `tech_stack`, and two URLs does not need any of that.

#### 3. Serialization Flow and Why It Is Necessary

A `Project` object in memory is a Python object tied to Django's ORM: it has methods,
a connection back to the database, and is not something that can be written directly
onto an HTTP response, which only understands bytes and text. `get_projects_json`
calls `serializers.serialize("json", projects)`, which walks the queryset and turns
each model instance into a plain representation (model name, primary key, and a
dictionary of field values) and then encodes that as a JSON string. That string is
what actually gets sent in the `HttpResponse`. On the way back in, `show_projects`
calls `serializers.deserialize("json", ...)` on that same string, which parses the
JSON and reconstructs Python objects from it, and I pull the underlying model
instance out of each result with `.object` before handing the list to the template.
Serialization is necessary because HTTP has no concept of a Python or Django object:
it only carries text, so the object has to be converted into a portable, language
independent format on the way out, and converted back into something Python can work
with on the way back in.

### Assignment 5

1. Debouncing is a technique that delays running a function until a short period has
   passed without the triggering event happening again. In the Achievements page the
   search input listens to the `input` event, which fires on every keystroke. Instead of
   calling `fetchAchievements` immediately, the handler calls `clearTimeout` on the
   previous timer and starts a new `setTimeout` of 300 ms, so the request is only sent
   once the user has stopped typing. This matters for an AJAX search because every
   request goes to the server and hits the database: without debouncing, typing
   "Gold" would send four requests in a row, most of which are already outdated by the
   time they return. Debouncing cuts the number of requests, reduces server load, and
   avoids flickering results. I also use an `AbortController` so that if an older request
   is still in flight when a newer one starts, the older one is cancelled and cannot
   overwrite the newer results.

2. `fetch()` is asynchronous: it returns a Promise immediately, and the actual HTTP
   response arrives later. The `await` keyword pauses the `async` function until that
   Promise settles, and then gives me the real value, so `const response = await
   fetch(url)` gives a `Response` object and `await response.json()` gives the parsed
   data, while the rest of the page keeps working because only that function is
   suspended. Without `await`, `response` would just be a pending Promise, so reading
   `response.ok` or calling `response.json()` on it would not work as intended: the code
   after the call would run before any data exists, `response.json()` would itself return
   another Promise instead of the list of achievements, and `forEach` over it would fail.
   Errors would also escape the `try/catch`, because a rejected Promise that is not
   awaited is not caught there.

3. Cross-Site Scripting (XSS) is an attack where an attacker gets their own JavaScript to
   run in other users' browsers, usually by saving malicious text such as
   `<img src="x" onerror="alert('XSS!')">` as a normal field value. When that value is
   later displayed as HTML, the browser treats it as real markup and executes the
   script, which can then read cookies, send requests as the victim, or change the page.
   Data displayed through a Django template is safer by default because the template
   engine auto-escapes `{{ variable }}`, turning `<` and `>` into `&lt;` and `&gt;` so
   they show up as plain text. Data displayed through AJAX loses that protection: the
   JSON is fetched as raw text and I build the cards in JavaScript, inserting values into
   template literals that are assigned to `innerHTML`. Django is no longer in the loop, so
   nothing escapes the text and the browser parses it as HTML. To fix this I wrap every
   value coming from the JSON with an `escapeHtml` function before it is placed into
   `innerHTML`, and on the server `AchievementForm` removes HTML tags with `strip_tags` in
   its `clean_title`, `clean_event`, and `clean_description` methods. Escaping at display
   time is the main defense and the server side cleaning is a second layer.

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

For Tutorial 03 and Assignment 3, I again used Claude Code as a tutor rather than to
write the feature for me: it explained what `{% extends %}`/`{% block %}` template
inheritance does before I refactored `index.html`, `experience.html`, and
`achievements.html` into `base.html`, what a `ModelForm` is before I wrote
`ProjectForm`, and what each of the create, JSON, and delete view functions was doing
before I wrote them myself. I made several mistakes along the way that I found and
fixed with its help rather than having it fix them directly: forgetting the `<title>`
block entirely when I first wrote `base.html`, a leftover `is_ongoing` property copied
onto the `Project` model that referenced a field the model does not have, a mismatch
between the template file name (`projects.html`) and the name the view rendered
(`project.html`), and an `<a>` edit link I nested inside the delete `<form>` instead of
next to it. For the Update feature specifically, I wrote `update_project`,
its URL, and the edit link myself, reusing the existing `projects_form.html` template
and `ProjectForm` with `instance=project` rather than building a separate form and
template for editing. I tested the full create, edit, delete, and search flow myself
in the browser, and re-ran `python manage.py test main` and `python manage.py check`
to confirm nothing regressed before committing.

For Tutorial 05 and Assignment 5, I used Claude Code mostly as a tutor. For Assignment
5 I applied the Tutorial 05 patterns (AJAX list, debounced search, modal form submitted
with fetch, toasts, XSS protection) to the Achievements section instead of Projects.
Claude Code explained the concepts and gave me the plan and the step order, and I wrote
the `starred_by` field and migration, `AchievementForm`, the three views
(`get_achievements_json`, `toggle_achievement_star`, `create_achievement_ajax`), the URLs,
and the modal component myself, which Claude Code reviewed and tested after each step.
Bugs it found in my work that I fixed: `starred_by` being returned instead of its
`.count()` in the JSON (a `TypeError`), `clean_tech_stack` copied from the Project form so
the `event` field was never sanitised, a wrong URL name in the modal that caused a
`NoReverseMatch`, a `fields` typo and a missing comma in the form, and Find and Replace
changes that pointed the achievements page at a non-existent `delete_achievement` URL
and at the Project star endpoint. Because of the deadline, I asked Claude Code to write
the final version of `templates/achievements.html` (cleaning up the Find and Replace
result), update `show_achievements`, and draft the answers above; I reviewed them
against the code. Claude Code also tested all four roles (visitor, regular user, editor,
superuser), the 400/403/201 responses, the star state, and an XSS payload both through
the form (rejected by the server) and inserted directly into the database (displayed as
plain text by `escapeHtml`). Limitations I noticed: the tutorial CSS used variables
(`--paper`, `--line`, `--accent`) that do not exist in my Stranger Things theme, so I
had to map them to my own variables, and a few of Claude Code's own test scripts gave
false alarms that I only trusted after checking the real output.
