import json
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / 'lessons'

def load_lesson(number):
    path = LESSONS_DIR / f'lesson{number}.json'
    with open(path, encoding='utf-8') as f:
        return json.load(f)