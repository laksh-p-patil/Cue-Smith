from nicegui import app, ui
from loader import load_lesson, list_lessons
from pages.check import check_section


def lesson_page(number: int):
    try:
        lesson = load_lesson(number)
    except FileNotFoundError:
        with ui.column().classes('w-full items-center q-pt-xl'):
            ui.label('Lesson not found').classes('title')
            ui.link('Back to all lessons', '/').classes('subtitle card-link')
        return

    has_details = any(lesson.get(key) for key in ('concept', 'breakdown', 'mistakes', 'try_it'))

    with ui.column().classes('w-full items-center q-pt-xl'):
        ui.link('← All lessons', '/').classes('subtitle card-link')
        ui.label(lesson['title']).classes('title fade-in')
        ui.label(lesson['summary']).classes('subtitle fade-in-2')

        with ui.row().classes('w-full justify-center q-mt-lg fade-in-2'):
            with ui.card().classes('panel').style('max-width: 420px'):
                ui.label('Weak prompt').classes('subtitle')
                ui.label(lesson['bad_prompt'])
            with ui.card().classes('panel').style('max-width: 420px'):
                ui.label('Strong prompt').classes('subtitle')
                ui.label(lesson['good_prompt'])

        ui.label(lesson['takeaway']).classes('subtitle q-mt-md')

        check_section(number, lesson)

        if has_details:
            def toggle():
                details.set_visibility(not details.visible)
                toggle_button.set_text('Show less' if details.visible else 'Show more details')

            toggle_button = ui.button('Show more details', on_click=toggle, color=None) \
                .props('flat no-caps').classes('glass-btn q-mt-lg')

            with ui.column().classes('lesson-body items-start fade-in') as details:
                if lesson.get('concept'):
                    ui.label('The idea').classes('section-title')
                    for paragraph in lesson['concept']:
                        ui.label(paragraph).classes('body-text')

                if lesson.get('breakdown'):
                    ui.label('Why the strong prompt works').classes('section-title')
                    for item in lesson['breakdown']:
                        with ui.column().classes('q-mb-sm'):
                            ui.label(item['part']).classes('part-name')
                            ui.label(f"“{item['quote']}”").classes('quote')
                            ui.label(item['why']).classes('body-text')

                if lesson.get('mistakes'):
                    ui.label('Common mistakes').classes('section-title')
                    for mistake in lesson['mistakes']:
                        ui.label(f'• {mistake}').classes('body-text')

                if lesson.get('try_it'):
                    with ui.card().classes('panel w-full q-mt-lg'):
                        ui.label('Try it yourself').classes('card-title')
                        ui.label(lesson['try_it']).classes('body-text')
            details.set_visibility(False)

        completed = app.storage.user.setdefault('completed', [])

        def mark_complete():
            if number not in completed:
                completed.append(number)
            complete_button.set_text('Completed ✓')

        ids = [item['id'] for item in list_lessons()]
        later = [i for i in ids if i > number]
        next_id = later[0] if later else None

        with ui.row().classes('q-mt-xl gap-4 justify-center'):
            complete_button = ui.button(
                'Completed ✓' if number in completed else 'Mark as complete',
                on_click=mark_complete, color=None,
            ).props('flat no-caps').classes('glass-btn')
            if next_id is not None:
                ui.button('Next lesson', on_click=lambda: ui.navigate.to(f'/lesson/{next_id}'), color=None) \
                    .props('flat no-caps').classes('glass-btn')
