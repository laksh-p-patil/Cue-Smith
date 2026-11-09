from nicegui import app, ui
from loader import load_lesson, list_lessons

CSS = '''
:root {
    --bg: #f5f5f7;
    --panel: rgba(255, 255, 255, 0.7);
    --border: rgba(0, 0, 0, 0.06);
    --text: #1d1d1f;
    --muted: #6e6e73;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    --shadow-hover: 0 12px 32px rgba(0, 0, 0, 0.08);
}
body.body--dark {
    --bg: #121214;
    --panel: rgba(44, 44, 46, 0.6);
    --border: rgba(255, 255, 255, 0.1);
    --text: #f5f5f7;
    --muted: #a1a1a6;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    --shadow-hover: 0 12px 32px rgba(0, 0, 0, 0.6);
}
body {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: -apple-system, "SF Pro Display", "Helvetica Neue", sans-serif !important;
    transition: background 0.3s ease, color 0.3s ease;
}
.q-card.panel {
    background: var(--panel) !important;
    color: var(--text) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    box-shadow: var(--shadow);
    padding: 40px 48px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.q-card.panel:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-hover);
}
.title {
    font-family: "Fraunces", Georgia, serif;
    font-size: 40px;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text);
}
.card-title {
    font-family: "Fraunces", Georgia, serif;
    font-size: 24px;
    font-weight: 600;
    color: var(--text);
}
.subtitle {
    font-size: 17px;
    color: var(--muted);
}
.lesson-body {
    width: 100%;
    max-width: 880px;
    padding: 0 20px;
}
.section-title {
    font-family: "Fraunces", Georgia, serif;
    font-size: 26px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text);
    margin-top: 36px;
}
.body-text {
    font-size: 17px;
    line-height: 1.6;
    max-width: 720px;
    color: var(--text);
}
.part-name {
    font-weight: 600;
    color: var(--text);
}
.quote {
    font-style: italic;
    color: var(--muted);
}
.card-link {
    text-decoration: none;
    color: inherit;
}
.mode-toggle {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 10;
    color: var(--text) !important;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeUp 0.6s ease both; }
.fade-in-2 { animation: fadeUp 0.6s ease 0.15s both; }
'''


def setup_page():
    is_dark = app.storage.user.setdefault('dark_mode', True)
    bg, text = ('#121214', '#f5f5f7') if is_dark else ('#f5f5f7', '#1d1d1f')
    ui.add_head_html(f'''
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600&display=swap" rel="stylesheet">
    <style>
    body:not(.body--dark):not(.body--light) {{
        background: {bg} !important;
        color: {text} !important;
        transition: none !important;
    }}
    </style>
    ''')
    ui.add_css(CSS)
    dark = ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.button(icon='brightness_6', on_click=dark.toggle).props('flat round').classes('mode-toggle')


@ui.page('/')
def home_page():
    setup_page()
    with ui.column().classes('w-full items-center q-pt-xl'):
        ui.label('Cue-Smith').classes('title fade-in')
        ui.label('Learn to prompt AI, one lesson at a time.').classes('subtitle fade-in-2')
        with ui.column().classes('q-mt-lg fade-in-2'):
            for lesson in list_lessons():
                with ui.link(target=f"/lesson/{lesson['id']}").classes('card-link'):
                    with ui.card().classes('panel').style('width: 480px; max-width: 90vw'):
                        ui.label(f"Lesson {lesson['id']}").classes('subtitle')
                        ui.label(lesson['title']).classes('card-title')
                        ui.label(lesson['summary'])


@ui.page('/lesson/{number}')
def lesson_page(number: int):
    setup_page()
    try:
        lesson = load_lesson(number)
    except FileNotFoundError:
        with ui.column().classes('w-full items-center q-pt-xl'):
            ui.label('Lesson not found').classes('title')
            ui.link('Back to all lessons', '/').classes('subtitle card-link')
        return

    with ui.column().classes('w-full items-center q-pt-xl'):
        ui.link('← All lessons', '/').classes('subtitle card-link')
        ui.label(lesson['title']).classes('title fade-in')
        ui.label(lesson['summary']).classes('subtitle fade-in-2')

        with ui.column().classes('lesson-body items-start q-mt-lg fade-in-2'):
            if lesson.get('concept'):
                ui.label('The idea').classes('section-title')
                for paragraph in lesson['concept']:
                    ui.label(paragraph).classes('body-text')

            with ui.row().classes('w-full justify-center q-mt-lg'):
                with ui.card().classes('panel').style('max-width: 420px'):
                    ui.label('Weak prompt').classes('subtitle')
                    ui.label(lesson['bad_prompt'])
                with ui.card().classes('panel').style('max-width: 420px'):
                    ui.label('Strong prompt').classes('subtitle')
                    ui.label(lesson['good_prompt'])

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

            ui.label(lesson['takeaway']).classes('subtitle q-mt-lg')


ui.run(storage_secret='cue-smith-dev-secret')