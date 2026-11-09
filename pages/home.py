from nicegui import app, ui
from loader import list_lessons


def home():
    lessons = list_lessons()
    completed = app.storage.user.setdefault('completed', [])
    done_count = sum(1 for lesson in lessons if lesson['id'] in completed)

    with ui.column().classes('w-full items-center q-pt-xl'):
        with ui.column().classes('slab items-center gap-1 fade-in'):
            ui.label('Cue-Smith').classes('title')
            ui.label('Learn to prompt AI, one lesson at a time.').classes('subtitle')
        ui.label(f'{done_count} of {len(lessons)} lessons complete').classes('subtitle q-mt-md fade-in-2')
        with ui.column().classes('q-mt-lg fade-in-2'):
            for lesson in lessons:
                with ui.link(target=f"/lesson/{lesson['id']}").classes('card-link'):
                    with ui.card().classes('panel').style('width: 480px; max-width: 90vw'):
                        check = ' ✓' if lesson['id'] in completed else ''
                        ui.label(f"Lesson {lesson['id']}{check}").classes('subtitle')
                        ui.label(lesson['title']).classes('card-title')
                        ui.label(lesson['summary'])
