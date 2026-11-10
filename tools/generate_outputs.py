"""Generate example outputs for each lesson's bad_prompt and good_prompt with Gemini.

Usage (from the project root, with GEMINI_API_KEY set in your environment):
    .venv/bin/python tools/generate_outputs.py            # fill in missing outputs
    .venv/bin/python tools/generate_outputs.py --force    # regenerate (overwrites existing outputs)

The API key is read only from the GEMINI_API_KEY environment variable.
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from google.genai import errors

MODEL = 'gemini-3.8-flash'
SKIP_LESSONS = {4}          # lesson 4's prompts are follow-ups with no earlier answer to follow up on
PAUSE_SECONDS = 5           # pause between API calls
RETRY_WAITS = (10, 20, 40, 80, 120)  # seconds to wait before each of the 5 retries
RETRYABLE_CODES = (429, 503)          # rate limited / model overloaded
LESSONS_DIR = Path(__file__).resolve().parent.parent / 'lessons'


def ask(client, prompt):
    """Send one prompt. Retry up to 5 times on 429/503; raise if it still fails."""
    for attempt in range(len(RETRY_WAITS) + 1):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            text = (response.text or '').strip()
            if not text:
                raise RuntimeError('Gemini returned an empty answer.')
            return text
        except errors.APIError as error:
            if error.code not in RETRYABLE_CODES or attempt == len(RETRY_WAITS):
                raise
            wait = RETRY_WAITS[attempt]
            print(f'  Temporary error ({error.code}). Waiting {wait}s, retry {attempt + 1} of {len(RETRY_WAITS)}...')
            time.sleep(wait)


def save(path, lesson):
    """Write the lesson file atomically so a failure can't leave it half-written."""
    temp = path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(lesson, indent=4, ensure_ascii=False), encoding='utf-8')
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--force', action='store_true',
                        help='regenerate lessons that already have outputs (overwrites them)')
    args = parser.parse_args()

    if not os.environ.get('GEMINI_API_KEY'):
        sys.exit('GEMINI_API_KEY is not set in your environment.')
    client = genai.Client()  # reads GEMINI_API_KEY from the environment

    first_call = True
    for path in sorted(LESSONS_DIR.glob('lesson*.json')):
        lesson = json.loads(path.read_text(encoding='utf-8'))
        name = path.name
        if lesson['id'] in SKIP_LESSONS:
            print(f'{name}: skipped (listed in SKIP_LESSONS)')
            continue
        has_outputs = 'bad_output' in lesson or 'good_output' in lesson
        if has_outputs and not args.force:
            print(f'{name}: skipped (already has outputs; use --force to regenerate)')
            continue
        if has_outputs:
            print(f'{name}: --force given, existing outputs will be replaced')

        try:
            outputs = {}
            for key in ('bad', 'good'):
                if not first_call:
                    time.sleep(PAUSE_SECONDS)
                first_call = False
                print(f'{name}: generating {key}_output with {MODEL}...')
                outputs[f'{key}_output'] = ask(client, lesson[f'{key}_prompt'])
        except Exception as error:
            sys.exit(f'{name}: stopped, nothing written for this lesson. {type(error).__name__}: {error}')

        lesson.update(outputs)
        lesson['model'] = MODEL
        lesson['generated_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
        save(path, lesson)
        print(f'{name}: saved')


if __name__ == '__main__':
    main()
