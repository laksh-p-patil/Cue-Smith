# Cue-Smith

Cue-Smith teaches students to write better prompts for AI. Every lesson shows a weak prompt and a strong prompt for the same task, side by side, with one takeaway.

I built it because I kept re-prompting AI until I got something usable, and I wanted to understand why some prompts work and others don't.

Status: version 1, in progress. Two lessons so far, text only.

## What it does

- The home page lists every lesson in the `lessons/` folder
- Each lesson page compares a weak prompt with a strong one
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
pip install nicegui
python3 main.py
```

Then open http://localhost:8080 in your browser.

## Built with

Python and NiceGUI. Lessons are JSON files, and the styling is custom CSS.

## Next

- Quiz questions after each lesson
- More lessons