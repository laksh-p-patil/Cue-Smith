from nicegui import app, ui
from loader import list_lessons


def home():
    lessons = list_lessons()
    completed = app.storage.user.setdefault('completed', [])
    quiz_best = app.storage.user.setdefault('quiz_best', {})
    done_count = sum(1 for lesson in lessons if lesson['id'] in completed)

    with ui.column().classes('w-full items-center q-pt-xl'):
        with ui.column().classes('slab items-center gap-1 fade-in'):
            ui.label('Cue-Smith').classes('title')
            ui.label('Learn to prompt AI, one lesson at a time.').classes('subtitle')
        ui.label(f'{done_count} of {len(lessons)} lessons complete').classes('subtitle q-mt-md fade-in-2')
        with ui.column().classes('home-grid q-mt-lg fade-in-2'):
            for lesson in lessons:
                with ui.link(target=f"/lesson/{lesson['id']}").classes('card-link'):
                    with ui.card().classes('panel'):
                        check = ' ✓' if lesson['id'] in completed else ''
                        ui.label(f"Lesson {lesson['id']}{check}").classes('subtitle')
                        ui.label(lesson['title']).classes('card-title')
                        if str(lesson['id']) in quiz_best and lesson.get('quiz'):
                            ui.label(f"Quiz {quiz_best[str(lesson['id'])]}/{len(lesson['quiz'])}").classes('subtitle')
                        ui.label(lesson['summary'])
