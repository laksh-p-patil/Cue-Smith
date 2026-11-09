import json
from pathlib import Path

LESSONS_DIR = Path(__file__).parent / 'lessons'

def load_lesson(number):
    path = LESSONS_DIR / f'lesson{number}.json'
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def list_lessons():
    lessons = []
    for path in LESSONS_DIR.glob('lesson*.json'):
        with open(path, encoding='utf-8') as f:
            lessons.append(json.load(f))
    return sorted(lessons, key=lambda lesson: lesson['id'])