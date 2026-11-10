# Cue-Smith

Cue-Smith teaches students to write better prompts for AI. Every lesson shows a weak prompt and a strong prompt for the same task, side by side, with one takeaway.

I built it because I kept re-prompting AI until I got something usable, and I wanted to understand why some prompts work and others don't.

Status: version 1, in progress. Five lessons so far.

## Screenshot

_Screenshot coming soon._

## What it does

- The home page lists every lesson in the `lessons/` folder
- Each lesson page compares a weak prompt with a strong one, with a takeaway and optional "Show more details"
- Quizzes and a "pick the better prompt" exercise on each lesson, with green/red feedback and "Try again"
- Progress tracking: mark lessons complete, see how many are done, and keep your best quiz score per lesson
- Dark and light mode, remembered as you move between pages

## Adding a lesson

Copy `lessons/lesson2.json`, change the `id` and the text, and save. The home page picks it up with no code changes.

## Run it yourself

You need Python 3.

```
git clone https://github.com/laksh-p-patil/Cue-Smith.git
cd Cue-Smith
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Then open http://localhost:8080 in your browser.

Optionally set `CUE_SMITH_SECRET` to your own random string before running. Without it, the app uses an insecure dev value and prints a warning.

## Built with

Python and NiceGUI. Lessons are JSON files, and the styling is custom CSS.

## Next

- More lessons
